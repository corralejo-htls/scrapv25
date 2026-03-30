# CHANGELOG — BookingScraper Pro v6.0.0 Build 62
## Release Date: 2026-03-30

---

## Summary

Build 62 fixes a **new critical bug (BUG-LANG-002)** discovered in Build 61 production
logs, plus improves the BUG-LANG-001 fix from Build 61.

---

## Bug Fixes

### 🔴 BUG-LANG-002 (NEW — Critical)
**Selenium Language Mismatch: `requested=de got=es`**

- **Root cause:** Booking.com `bkng_lang` session cookies set during an earlier
  language request persist in the Selenium driver and override the `?lang=XX` URL
  parameter, causing all subsequent languages to be served in the cookie-locked
  language (typically `es` when VPN=Spain is used first).
- **Fix A — Cookie reset + Accept-Language header (scraper.py):**
  Added `_set_language_headers(driver, lang)` method called before every
  `driver.get()`. Uses CDP to inject the correct `Accept-Language` header and
  calls `delete_all_cookies()` to remove `bkng_lang` before each page load.
- **Fix B — Browser restart after VPN rotation (scraper.py + scraper_service.py):**
  Added `reset_browser()` method called after every forced VPN rotation. Quits
  and nullifies the driver instance so the next request spawns a completely clean
  Brave/Chrome profile with no cached DNS, TLS sessions, or cookies.
- **Config:** Added `SELENIUM_RESET_LANG_ON_EACH_REQUEST`, `SELENIUM_RESTART_AFTER_VPN_ROTATE`,
  `SELENIUM_LANG_VERIFY_TIMEOUT_S` fields.

### 🟡 BUG-LANG-001 (IMPROVEMENT — Build 61 partial fix)
**Missing Languages — VPN rotation threshold too high**

- **Problem:** Build 61 required 2 consecutive failures before forcing VPN rotation,
  wasting one language slot per block event.
- **Fix:** Added `ip_known_blocked` flag in `_process_url()`. After the **first**
  language failure, the flag is set to `True`. The next language iteration rotates
  VPN immediately **before** attempting, eliminating the wasted slot.
- **Config:** `MAX_CONSECUTIVE_LANG_FAILURES` changed from `2` to `1`.

---

## Files Modified

| File                                              | Type     | Bug          |
|---------------------------------------------------|----------|--------------|
| `app/scraper.py`                                  | Modified | BUG-LANG-002 |
| `app/scraper_service.py`                          | Modified | BUG-LANG-001 + 002 |
| `app/config.py`                                   | Modified | BUG-LANG-001 + 002 |
| `env.example`                                     | Modified | BUG-LANG-001 + 002 |
| `documentations/BUG-LANG-002_Technical_Analysis_EN.md` | New | — |
| `documentations/BUG-LANG-002_Analisis_Tecnico_ES.md`   | New | — |
| `documentations/Bug_query-SQL.md`                 | New      | — |

---

## Expected Outcomes

| Metric                            | Build 61   | Build 62   |
|-----------------------------------|------------|------------|
| Languages per URL (target: 6/6)   | 3–6 / 6    | 6 / 6      |
| Selenium language mismatch rate   | ~15–20%    | ~0%        |
| VPN rotations before 2nd failure  | No         | Yes        |
| Browser restart after VPN rotate  | No         | Yes        |

---

## How to Apply Build 62

1. Update `app/scraper.py`:
   - Add `LANG_TO_ACCEPT_LANGUAGE` dict and `_BOOKING_LANG_COOKIE` constant.
   - Add `_set_language_headers()` method to `SeleniumScraperEngine`.
   - Add `reset_browser()` method to `SeleniumScraperEngine`.
   - Call `self._set_language_headers(driver, lang)` inside `_fetch_with_selenium()`
     **immediately before every `driver.get(url)`** call.

2. Update `app/scraper_service.py`:
   - In `_process_url()`, add `ip_known_blocked: bool = False`.
   - Modify VPN rotation condition to check `ip_known_blocked`.
   - After `vpn_rotated = True`, call `self._selenium_engine.reset_browser()`.
   - Set `ip_known_blocked = True` on failure, `False` on success.

3. Update `app/config.py`:
   - Change `MAX_CONSECUTIVE_LANG_FAILURES` default from `2` to `1`.
   - Add `SELENIUM_RESET_LANG_ON_EACH_REQUEST`, `SELENIUM_RESTART_AFTER_VPN_ROTATE`,
     `SELENIUM_LANG_VERIFY_TIMEOUT_S` fields.

4. Copy `env.example` to `.env` (or merge new fields into existing `.env`):
   ```
   MAX_CONSECUTIVE_LANG_FAILURES=1
   SELENIUM_RESET_LANG_ON_EACH_REQUEST=true
   SELENIUM_RESTART_AFTER_VPN_ROTATE=true
   SELENIUM_LANG_VERIFY_TIMEOUT_S=5.0
   ```

5. Run acceptance test (Query Q9 in `Bug_query-SQL.md`) after first batch.

---

*BookingScraper Pro v6.0.0 Build 62 — 2026-03-30*
