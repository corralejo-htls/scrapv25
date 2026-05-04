# CHANGELOG — BookingScraper Pro v6.0.0 Build 63
## Release Date: 2026-03-30

---

## Summary

Build 63 eliminates CloudScraperEngine entirely. The evidence from production
logs (2026-03-29/30) is unambiguous: 78+ CloudScraper attempts produced 0
successes. Every CloudScraper request returned a Cloudflare challenge page
(3962 bytes). Keeping this code actively degrades the system by wasting
retries and reinforcing IP blocks before Selenium can attempt.

---

## Changes

### ❌ REMOVED: CloudScraperEngine (scraper.py)

**Removed ~250 lines** constituting the entire `CloudScraperEngine` class,
including:
- `_fetch_with_cloudscraper()` method
- `scrape()` method (CloudScraper version)
- All `cloudscraper` session management code
- `Block detected` / `CloudScraper retry N/3` log logic

**Removed import:** `import cloudscraper`

### ❌ REMOVED: CloudScraper from requirements.txt

```diff
- cloudscraper>=1.2.71,<1.3.0
```

### ✅ MODIFIED: scraper_service.py — _scrape_language()

**Before (dual-engine):**
```python
html = self._cloud_engine.scrape(lang_url, retries=self._cfg.MAX_LANG_RETRIES)
if html is None:
    logger.info("CloudScraper failed for %s/%s — trying Selenium.", ...)
    html = self._selenium_engine.scrape(lang_url, lang)
if html is None and self._cfg.VPN_ENABLED:
    if self._vpn.should_rotate():
        rotated = self._vpn.rotate()
        if rotated:
            html = self._cloud_engine.scrape(lang_url, retries=1)
            if html is None:
                html = self._selenium_engine.scrape(lang_url, lang)
```

**After (Selenium only):**
```python
# Build 63: Selenium is the sole engine
html = self._selenium_engine.scrape(lang_url, lang)
if html is None and self._cfg.VPN_ENABLED:
    if self._vpn.should_rotate():
        rotated = self._vpn.rotate()
        if rotated:
            self._selenium_engine.reset_browser()  # BUG-LANG-002
            html = self._selenium_engine.scrape(lang_url, lang)
```

### ✅ MODIFIED: scraper_service.py — __init__()

```diff
- self._cloud_engine = CloudScraperEngine()
  self._selenium_engine = SeleniumEngine()
```

### ✅ MODIFIED: config.py — field descriptions updated

`MAX_LANG_RETRIES` and `SCRAPER_RETRY_DELAY` descriptions updated to reflect
their new purpose as Selenium retry parameters (previously CloudScraper).
Defaults unchanged.

---

## Files Modified

| File | Change | Lines Δ |
|---|---|---|
| `app/scraper.py` | CloudScraperEngine removed | −250 |
| `app/scraper_service.py` | Dual-engine → Selenium-only | −15 |
| `app/config.py` | Descriptions updated | 0 |
| `requirements.txt` | cloudscraper removed | −1 |
| `env.example` | CloudScraper comments removed | −5 |

**Net reduction: ~270 lines of dead code eliminated.**

---

## Why Selenium Is Now Safe as the Sole Engine

| Concern | Status |
|---|---|
| Selenium is slower than HTTP | ✅ Acceptable — CloudScraper took same time (always blocked) |
| Higher resource usage | ✅ HEADLESS_BROWSER=true for production |
| No HTTP-level fallback | ✅ VPN rotation provides IP diversity |
| Single point of failure | ✅ Retry logic (MAX_LANG_RETRIES=3) still applies |

---

## Expected Improvement in Metrics

| Metric | Build 62 | Build 63 |
|---|---|---|
| CloudScraper wasted requests per URL | 18+ | **0** |
| Time per language (when blocked) | ~90s (Cloud×3 + Selenium) | **~60s (Selenium only)** |
| Log noise (Block detected, retry N/3) | High | **None** |
| IP reinforcement from failed requests | Yes | **No** |

---

## How to Apply Build 63

1. Replace `app/scraper.py` → complete file
2. Replace `app/scraper_service.py` → complete file
3. Replace `app/config.py` → complete file
4. Replace `requirements.txt` → complete file
5. Replace `env.example` → complete file (or merge into `.env`)
6. Uninstall the now-unused package:
   ```
   pip uninstall cloudscraper -y
   ```
7. Verify no other module imports `cloudscraper` directly:
   ```
   grep -r "cloudscraper" app/
   # Expected: no output
   ```
8. Restart Celery worker and confirm in logs:
   - No more `"CloudScraper failed"` messages
   - No more `"Block detected attempt N/3"` messages
   - `"Selenium: Brave started"` appears at first request

---

*BookingScraper Pro v6.0.0 Build 63 — 2026-03-30*
