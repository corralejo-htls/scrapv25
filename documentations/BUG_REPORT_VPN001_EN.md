date report: 02 de abril del 2026

# Bug Report — BUG-VPN-001

| Field | Value |
|---|---|
| **ID** | BUG-VPN-001 |
| **Title** | VPN does not rotate every 50 s between languages; error-triggered rotation blocked by `should_rotate()` guard |
| **Severity** | 🔴 Critical — data loss (5 of 6 languages silently skipped per URL) |
| **Build detected** | Build 67 |
| **Build fixed** | Build 68 |
| **Files changed** | `app/scraper_service.py`, `app/config.py`, `env.example` |
| **Date** | 2026-04-02 |

---

## 1. Observed Behaviour

Second batch session. URLs `24f87116` and `25b89627` scraped only `lang=en`.
Languages `es`, `de`, `it`, `fr`, `pt` were **never attempted**.
Both URLs remained `url_queue.status = 'pending'` with empty `languages_completed`.

| URL (abbrev.) | Scraped | Missing |
|---|---|---|
| `24f87116-84c3-41fa-ac10-d358c83682ba` | en | es de it fr pt |
| `25b89627-d476-4e2a-a53c-56e7751b656c` | en | es de it fr pt |

SQL verification:

```sql
SELECT url_id, COUNT(DISTINCT language) AS langs
FROM hotels
GROUP BY url_id
HAVING COUNT(DISTINCT language) < 6;
-- Returns: both affected URLs with langs = 1
```

---

## 2. Evidence from Production Logs

```
[01:03:43] VPN-PROACTIVE: rotation successful — new IP secured (batch 2 start)
[01:03:49] NordVPNManager initialised | VPN_ROTATION_INTERVAL=50
[01:03:49] VPN: original IP = 185.111.157.78
[01:03:49] VPN: home country detected = IT
[01:03:50] VPN disconnected.
[01:03:55] VPN: connecting to Sweden (SE)...
[01:04:13] VPN connected to Sweden — IP: 79.116.133.126     ← _last_rotation set here
[01:04:29] SSL handshake failed; net_error -100              ← tunnel already unstable
[01:04:51] SSL handshake failed; net_error -100
[01:05:10] URL 25b89627 lang=en: SUCCESS                    ← t=+57s since last rotation
[01:05:10] inter-language delay 11.6s before .../es         ← should_rotate() True here
                                                               but never called
[01:05:20] URL 24f87116 lang=en: SUCCESS                    ← t=+67s since last rotation
[01:05:20] inter-language delay 13.0s before .../es
           *** LOG ENDS — no es/de/it/fr/pt ever logged ***
```

`VPN_ROTATION_INTERVAL = 50 s`. At `01:05:10`, elapsed time since last rotation = **57 s** → `should_rotate()` returned `True`. But `_process_url()` never called it between languages. The tunnel collapsed during the inter-language delay and no recovery was triggered.

---

## 3. Root Cause Analysis

### Primary cause — `should_rotate()` not checked between languages

**Location:** `scraper_service.py` → `_process_url()` language loop (lines 226–325, Build 67).

The loop iterated languages without ever consulting `should_rotate()`. The only time-based check was at `dispatch_batch()` (batch start), which uses a fresh `NordVPNManager` instance with `_last_rotation = 0` — so it always fires at the very beginning of the batch. Once the batch is running, no further time-based check exists between languages.

```python
# BUILD 67 — MISSING: no time-based rotation between languages
for i, lang in enumerate(languages):
    if i > 0:
        time.sleep(base_delay + jitter)   # delay only — no VPN check
    ok = self._scrape_language(url_obj, lang)
```

With `en` taking ~57 s (scrape + image download), `VPN_ROTATION_INTERVAL = 50` s expired before `es` started, but no rotation occurred.

### Secondary cause — Error-triggered rotation blocked by `should_rotate()`

**Location:** `scraper_service.py` → `_scrape_language()` lines 344–360, Build 67.

```python
# BUILD 67 — BUG: guard prevents rotation when interval hasn't elapsed
if html is None and getattr(cfg, "VPN_ENABLED", False):
    if self._vpn.should_rotate():            # ← WRONG: blocks rotation after
        rotated = self._vpn.rotate()         #   a recent batch-start rotation
```

The batch-start rotation set `_last_rotation = time.monotonic()`. When `es` failed (< 50 s later), `should_rotate()` returned `False` → rotation was skipped → browser retried through a dead VPN tunnel → all retries exhausted → `es` marked failed → same pattern for `de`, `it`, `fr`, `pt`.

### Causal chain

```
01:04:13  VPN connects to Sweden (_last_rotation = T0)
          Tunnel already unstable (SSL net_error -100 immediately)
01:05:10  en: SUCCESS (57 s elapsed = T0 + 57 s)
          should_rotate() → True (57 s ≥ 50 s)
          _process_url() loop does NOT call should_rotate() → no rotation
01:05:10  inter-language delay 11.6 s
          VPN tunnel drops completely during delay
01:05:22  es: fetch attempted through dead tunnel
          html = None
          _scrape_language(): should_rotate() → False (< 50 s since T0+57s=T1)
          Error-triggered rotation SKIPPED
          Selenium retries through dead tunnel
          All MAX_LANG_RETRIES exhausted
          es → FAILED (same pattern repeats for de, it, fr, pt)
          url_queue.status never written → URL stays "pending"
```

---

## 4. Fix Applied — Build 68

### Fix A — Time-based rotation per language (`_process_url`)

Added `should_rotate()` check **before every language** in the iteration loop:

```python
# BUILD 68 — FIX A: _process_url() — time-based rotation per language
vpn_rotated: bool = False
if getattr(cfg, "VPN_ENABLED", False) and self._vpn.should_rotate():
    _elapsed = time.monotonic() - self._vpn._last_rotation
    logger.info(
        "BUG-VPN-001-FIX: VPN_ROTATION_INTERVAL elapsed "
        "(%.0fs >= %ds) before %s/%s — rotating",
        _elapsed, getattr(cfg, "VPN_ROTATION_INTERVAL", 50), url_id, lang,
    )
    if self._vpn.rotate(force=False):
        consecutive_failures = 0
        ip_known_blocked = False
        vpn_rotated = True
```

The existing `should_rotate_now` failure-triggered block is then guarded with `not vpn_rotated` to prevent double rotation in the same language iteration.

The existing `vpn_rotated` → `reset_browser()` block (BUG-LANG-002-FIX) handles browser restart for both time-based and failure-triggered rotations — no duplication.

### Fix B — Error-triggered rotation on every failure (`_scrape_language`)

Removed the `should_rotate()` guard. Any `html is None` result immediately triggers `rotate(force=True)`:

```python
# BUILD 68 — FIX B: _scrape_language() — rotate on every fetch failure
# Previously:  if html is None and VPN_ENABLED and self._vpn.should_rotate():
# Now:         if html is None and VPN_ENABLED:  (no interval gate)
if html is None and getattr(cfg, "VPN_ENABLED", False):
    logger.warning(
        "BUG-VPN-001-FIX: fetch failed for %s/%s — "
        "error-triggered VPN rotation (force=True)", url_id, lang,
    )
    rotated = self._vpn.rotate(force=True)   # force=True bypasses interval
```

`force=True` is already implemented in `NordVPNManager.rotate()` (Build 61, BUG-LANG-001-FIX) and bypasses the `VPN_ROTATION_INTERVAL` check inside the lock.

### config.py — BUILD_VERSION bumped

```python
BUILD_VERSION: int = Field(default=68, ...)   # was 67
```

### env.example — VPN_ROTATION_INTERVAL comment updated

```ini
# Rotar IP cada 50 segundos para evitar bloqueos.
# BUILD 68 — BUG-VPN-001-FIX: comprobado antes de CADA idioma (no solo en
# batch start). Adicionalmente, cualquier error de fetch dispara rotación
# inmediata con force=True independientemente del tiempo transcurrido.
VPN_ROTATION_INTERVAL=50
```

---

## 5. Expected Log After Fix

```
[01:05:10] inter-language delay 11.6s before 25b89627/es
[01:05:22] BUG-VPN-001-FIX: VPN_ROTATION_INTERVAL elapsed (69s >= 50s)
           before 25b89627/es — rotating
[01:05:22] VPN: rotating (current=SE)...
[01:05:27] VPN: connecting to Germany (DE)...
[01:05:42] VPN connected to Germany — IP: 185.X.X.X
[01:05:42] BUG-LANG-002-FIX: Restarting Selenium browser after VPN rotation.
[01:05:42] BUG-LANG-002-FIX: Browser reset complete — next request will spawn a fresh driver.
[01:05:52] URL 25b89627 lang=es: SUCCESS

OR (if fetch still fails before rotation is checked):

[01:05:22] BUG-VPN-001-FIX: fetch failed for 25b89627/es — error-triggered VPN rotation (force=True)
[01:05:22] VPN: rotating (current=SE)...
[01:05:42] VPN connected to Germany — IP: 185.X.X.X
[01:05:42] BUG-VPN-001-FIX: VPN rotated (error-triggered) — retrying 25b89627/es with Selenium.
[01:05:52] URL 25b89627 lang=es: SUCCESS
           ...
[01:07:30] URL 25b89627: COMPLETE (6/6) langs=['en','es','de','it','fr','pt']
```

---

## 6. Verification Queries

```sql
-- All URLs must have 6 languages after a complete batch:
SELECT url_id, COUNT(DISTINCT language) AS lang_count
FROM hotels
GROUP BY url_id
HAVING COUNT(DISTINCT language) < 6;
-- Expected after fix: 0 rows

-- No URLs stuck in pending with partial data:
SELECT uq.id, uq.status, COUNT(DISTINCT h.language) AS langs_scraped
FROM url_queue uq
LEFT JOIN hotels h ON h.url_id = uq.id
WHERE uq.status = 'pending'
GROUP BY uq.id, uq.status
HAVING COUNT(DISTINCT h.language) > 0;
-- Expected after fix: 0 rows

-- Confirm rotation log messages appear:
SELECT event_type, language, scraped_at
FROM scraping_logs
WHERE error_message ILIKE '%BUG-VPN-001%'
ORDER BY scraped_at DESC LIMIT 20;
```

---

## 7. Regression Risk

| Area | Risk | Mitigation |
|---|---|---|
| Double rotation (time + failure) | Mitigated | `not vpn_rotated` guard prevents both checks firing on same language |
| Excessive rotations on slow networks | Low | `force=False` for time-based (interval still applies); `force=True` only on confirmed failure |
| Browser reset race condition | None | Existing `vpn_rotated` → `reset_browser()` block handles both rotation paths |
| `_last_rotation` access | None | `NordVPNManager._last_rotation` is a standard instance float; no lock needed for read |

---

*BookingScraper Pro — Build 67 → Build 68 — 2026-04-02*
