# BUG-LANG-001 — Bug Report (English)
## Missing Languages on Multi-Language Scraping

| Field | Value |
|-------|-------|
| **Bug ID** | BUG-LANG-001 |
| **Build** | BookingScraper Pro v6.0.0 Build 61 |
| **Severity** | HIGH |
| **Status** | ✅ FIXED |
| **Fix Date** | 2026-03-29 |
| **Affected URL** | `3420c869-fd48-4f79-9557-5e185e9e580f` |
| **Failure Rate** | 83% (5 of 6 languages failed) |

---

## 1. Symptom

SQL query evidence shows that URL `3420c869-fd48-4f79-9557-5e185e9e580f`
produced only **1 row** in `hotels` (language `es`), while 12 other URLs
correctly produced 6 rows each.

```sql
SELECT url_id, COUNT(url_id) FROM hotels GROUP BY url_id ORDER BY url_id;
-- Result: "3420c869-..."; "1"   ← only 'es', 5 languages missing
```

`url_language_status` confirms the failure pattern:

| Language | Status | Error |
|----------|--------|-------|
| en | ❌ error | All scraping engines failed |
| es | ✅ done | — |
| de | ❌ error | All scraping engines failed |
| it | ❌ error | All scraping engines failed |
| fr | ❌ error | All scraping engines failed |
| pt | ❌ error | All scraping engines failed |

---

## 2. Root Cause Analysis

### C1 — No inter-language delay (`scraper_service.py`)

The language loop in `_process_url()` fired all 6 language requests in
**immediate succession** with zero delay between them:

```python
# BEFORE (build 60) — NO delay
for lang in languages:
    ok = self._scrape_language(url_obj, lang)
```

Six HTTP requests to `booking.com` within seconds is a bot signature.
Booking.com's Cloudflare layer detects the pattern and blocks the IP,
returning a **~3,962-byte challenge page** instead of the real hotel page
(which is 150,000–500,000 bytes).

### C2 — VPN rotates only on timer, not on failure (`scraper_service.py` + `vpn_manager_windows.py`)

```python
# BEFORE (build 60) — interval-only check
if html is None and self._cfg.VPN_ENABLED:
    if self._vpn.should_rotate():   # ← True only if 50s have elapsed
        self._vpn.rotate()
```

After `es` succeeded (~05:02), the IP was flagged by Booking.com.
`de` failed at 05:16 — **14 minutes later** — but `should_rotate()` still
returned `False` because `VPN_ROTATION_INTERVAL=50s` had already been used
for the `es` rotation, and the lock prevented another rotation.
No new IP was obtained; `it`, `fr`, `pt` all failed on the same blocked IP.

### C3 — Short HTML wastes retries (`scraper.py`)

When the engine received the 3,962-byte Cloudflare page it did:

```python
# BEFORE (build 60)
if html_len < 5000:
    logger.warning("Short HTML (%d bytes)...", html_len)
    time.sleep(random.uniform(8, 15))
    continue  # ← retry with the SAME blocked IP/session
```

This consumed all `MAX_LANG_RETRIES=3` attempts with the same blocked
session, wasting ~30–45 seconds per language without any chance of success.

---

## 3. Timeline Analysis (URL: 3420c869...)

| Language | Timestamp | Status | Gap | Notes |
|----------|-----------|--------|-----|-------|
| en | 05:00:03 | ❌ FAILED | — | IP already flagged |
| es | 05:02:41 | ✅ OK | +2m 38s | VPN rotated during gap |
| de | 05:16:59 | ❌ FAILED | +14m 18s | Same blocked IP, no rotation |
| it | 05:30:40 | ❌ FAILED | +13m 41s | Same blocked IP |
| fr | 05:43:13 | ❌ FAILED | +12m 33s | Same blocked IP |
| pt | 05:55:37 | ❌ FAILED | +12m 24s | Same blocked IP |

---

## 4. Applied Fixes (Build 61)

### FIX-LANG-001-A — Inter-language delay (`scraper_service.py`)

```python
# AFTER (build 61) — delay before each language except the first
if i > 0:
    base_delay  = self._cfg.LANG_SCRAPE_DELAY   # default: 10.0s
    jitter      = random.uniform(0.0, self._cfg.LANG_SCRAPE_JITTER)  # 0–5s
    total_delay = base_delay + jitter
    time.sleep(total_delay)
```

- **Base delay:** 10 seconds — mimics human page reading time
- **Jitter:** 0–5 seconds random — prevents predictable request patterns
- **Per-URL overhead:** ~50–75 seconds total (acceptable)
- **Configurable:** `LANG_SCRAPE_DELAY` / `LANG_SCRAPE_JITTER` in `.env`

### FIX-LANG-001-B — Forced VPN rotation on consecutive failures (`scraper_service.py`)

```python
# AFTER (build 61) — forced rotation when consecutive failures reach threshold
if consecutive_failures >= max_consec_failures and self._cfg.VPN_ENABLED:
    rotated = self._vpn.rotate(force=True)   # bypasses interval timer
    if rotated:
        consecutive_failures = 0
```

- Resets `consecutive_failures` counter on each success
- After `MAX_CONSECUTIVE_LANG_FAILURES` (default: 2) failures in a row,
  calls `vpn.rotate(force=True)` which **bypasses** `VPN_ROTATION_INTERVAL`
- `NullVPNManager.rotate()` signature updated for consistency

### FIX-LANG-001-C — Short HTML fast-fail (`scraper.py`)

```python
# AFTER (build 61) — return None immediately on block page
if html_len < cfg.SHORT_HTML_THRESHOLD:
    logger.warning("BUG-LANG-001-FIX: Short HTML (%d bytes) — block page, skipping retries", html_len)
    _save_debug_html(html, url, f"short_html_a{attempt}")
    with self._lock:
        self._blocked_count += 1
    return None   # ← immediate exit, no wasted retries
```

Applied to both `CloudScraperEngine.scrape()` and `SeleniumEngine.scrape()`.
Saves the blocked page HTML to `debug/` for audit trail.

---

## 5. New Configuration Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `LANG_SCRAPE_DELAY` | `10.0` | 0–120s | Base delay between languages |
| `LANG_SCRAPE_JITTER` | `5.0` | 0–30s | Max random jitter added to base |
| `MAX_CONSECUTIVE_LANG_FAILURES` | `2` | 1–6 | Failures before forced VPN rotation |
| `SHORT_HTML_THRESHOLD` | `5000` | 1000–20000 bytes | Min size for valid page |

---

## 6. Files Modified

| File | Change |
|------|--------|
| `app/config.py` | 4 new `Field` definitions + updated header (build 61) |
| `app/scraper_service.py` | Language loop: inter-language delay + consecutive failure VPN trigger |
| `app/scraper.py` | `return None` on short HTML in both `CloudScraperEngine` and `SeleniumEngine` |
| `app/vpn_manager_windows.py` | `rotate(force=False)` parameter in `NordVPNManager` + `NullVPNManager` |
| `env.example` | 4 new documented parameters, header updated to build 61 |

---

## 7. Expected Impact

| Metric | Before Fix | After Fix |
|--------|-----------|-----------|
| Language success rate | ~17% (1/6) | ~95%+ |
| Wasted retries on blocked IPs | 3× per language | 0 (immediate return) |
| VPN rotation on consecutive failures | Never | After 2 failures |
| Per-URL overhead | ~0s (all fail fast) | +50–75s (acceptable) |

---

## 8. Verification Query

```sql
-- After running build 61, confirm all 6 languages per URL:
SELECT url_id, COUNT(DISTINCT language) AS lang_count
FROM hotels
GROUP BY url_id
HAVING COUNT(DISTINCT language) < 6
ORDER BY lang_count ASC;
-- Expected result: 0 rows (all URLs have 6 languages)
```

---

*Report generated: 2026-03-29 | BookingScraper Pro v6.0.0 Build 61*
