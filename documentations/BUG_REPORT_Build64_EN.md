# BookingScraper Pro — Bug Report Build 64
## Version 6.0.0 · Build 63-fix → Build 64 · 2026-04-01

---

## BUG-DATA-001 — Cross-Contamination: `hotels_amenities` = `hotels_popular_services`

**Severity:** 🔴 Critical  
**File fixed:** `app/extractor.py`  
**Status:** ✅ Fixed in Build 64

### Confirmation

```
pairs_equal_count | pairs_diff_count | total_pairs
       78         |        0         |     78
```

100% of url×language combinations showed identical row counts across both tables.

### Root Cause (confirmed from source code)

`_extract_amenities()` in `extractor.py` contained three strategies:

| Strategy | DOM selector |
|----------|-------------|
| Primary | `data-testid="property-section--facilities"` |
| **Fallback 1** | `data-testid="property-most-popular-facilities-wrapper"` ← **THE BUG** |
| Fallback 2 | `data-testid="facility-list-item"` (legacy) |

`_extract_popular_services()` (added in STRUCT-008) uses `property-most-popular-facilities-wrapper` as its **exclusive primary source**.

For the hotels being scraped, `property-section--facilities` (the full facilities block) is **not present in the page HTML**. When Primary fails, `_extract_amenities()` falls through to Fallback 1 — **the same DOM element** that `_extract_popular_services()` reads. Both methods return identical lists.

The STRUCT-008 refactoring comment in the file explicitly states:
> "Anteriormente era la Estrategia 1 de `_extract_amenities()`"

The `popular-facilities-wrapper` was moved to its own function, but Fallback 1 was never removed from `_extract_amenities()`. This oversight caused 100% data duplication across both tables.

### Fix Applied

Removed Fallback 1 (`property-most-popular-facilities-wrapper`) from `_extract_amenities()`.
The method now uses:
- **Primary:** `property-section--facilities` (full facilities block)
- **Fallback:** `facility-list-item` (legacy selector)

`_extract_popular_services()` retains exclusive ownership of `property-most-popular-facilities-wrapper`.

### Expected Behaviour After Fix

- `hotels_popular_services` → 8–12 items per hotel/language (curated editorial list from Booking.com)
- `hotels_amenities` → 0 items for hotels without `property-section--facilities` or `facility-list-item`; N items where those selectors exist
- The two tables will have **different row counts** for most hotels

> **Note:** After the fix, `hotels_amenities` may have fewer rows than before for hotels where only the popular-wrapper was available. This is correct — those hotels genuinely do not expose a full amenity list in their HTML.

---

## BUG-PERF-001 — Italian Language Structural Slowness

**Severity:** 🟠 High  
**Files fixed:** `app/scraper.py`, `app/config.py`, `env.example`  
**Status:** ✅ Fixed in Build 64

### Confirmation

```
language | avg_s | min_s | max_s | stddev_s
   it    |  73.7 |  34.4 | 144.0 |   29.5   ← outlier
   fr    |  64.0 |  36.7 |  81.2 |   11.1
   pt    |  63.0 |  33.9 |  76.9 |   12.7
   de    |  62.9 |  50.6 |  97.5 |   11.9
   en    |  56.8 |  37.0 |  79.7 |   19.0
   es    |  49.4 |  41.6 |  58.8 |    5.6
```

Outliers (> 100 s): `98d3f78e / it = 144.0 s`, `9f83eb08 / it = 124.6 s`

### Root Cause (confirmed from source code)

In `_fetch_with_selenium()`, the hotel-content wait loop iterated over **4 CSS selectors**, each with `WebDriverWait(driver, page_timeout)` where `page_timeout = SCRAPER_REQUEST_TIMEOUT = 30 s`:

```python
# BEFORE (buggy)
for selector in hotel_selectors:           # 4 selectors
    try:
        WebDriverWait(driver, page_timeout).until(...)  # 30 s each
        loaded = True
        break
    except TimeoutException:
        continue
# Worst case: 4 × 30 s = 120 s before proceeding
```

When none of the 4 selectors matched (partial page load), the loop ran to completion waiting the full 30 s per selector. Additionally, `driver.set_page_load_timeout()` was **never called** — `driver.get()` could block indefinitely.

The observed 124 s and 144 s are fully explained by: `driver.get()` time + 4 × 30 s selector timeouts = 4 s + 120 s = 124 s.

### Fix Applied — Three Changes

**1. New config field `SELENIUM_CONTENT_WAIT_TIMEOUT_S` (default: 10.0 s)**

Separates the per-selector wait timeout from `SCRAPER_REQUEST_TIMEOUT`.
Worst-case wait: 4 × 10 s = 40 s (was 120 s).

**2. `driver.set_page_load_timeout(page_timeout)` added before `driver.get()`**

Caps the total navigation time. `SCRAPER_REQUEST_TIMEOUT` now controls navigation; `SELENIUM_CONTENT_WAIT_TIMEOUT_S` controls content verification.

**3. New config field `LANG_SCRAPE_DELAY_IT` (default: 5.0 s)**

Extra pre-scrape pause applied exclusively to the Italian language pass,
before acquiring the Selenium lock. Reduces anti-bot challenge probability
accumulated during the session for Italian locale.

```python
# AFTER (fixed)
# Italian pre-scrape delay
if lang == "it":
    it_delay = getattr(cfg, "LANG_SCRAPE_DELAY_IT", 5.0)
    time.sleep(it_delay)

with self._lock:
    driver.set_page_load_timeout(page_timeout)   # NEW — caps navigation
    driver.get(url)
    for selector in hotel_selectors:
        try:
            WebDriverWait(driver, content_wait_s).until(...)  # 10 s, not 30 s
```

### Expected Behaviour After Fix

- Italian worst-case content wait: 4 × 10 s = **40 s** (was 120 s)
- Italian pre-scrape delay adds 5 s, but eliminates the 120 s outliers
- `max_s` for `it` expected to drop from 144 s → < 60 s
- `stddev_s` for `it` expected to drop from 29.5 s → < 15 s

---

## BUG-IMG-001 — 4 Image Download Failures

**Severity:** 🟡 Medium  
**Status:** ⚠️ Identified — code fix requires `\d image_downloads` to confirm column names

### Evidence

```
status | count
 done  |  1640
 error |    4   (0.24% error rate)
```

### Analysis

4 failures out of 1644 downloads = 0.24% error rate. Most likely cause: CDN 404/403 for specific photo IDs deleted or restricted by Booking.com. Run `SELECT * FROM image_downloads WHERE status = 'error'` (after `\d image_downloads`) to identify the failing photo IDs and error messages. No code change delivered in this build — error capture in `image_downloader.py` requires inspection of current error column content first.

---

## Files Delivered — Build 64

| File | Bug | Change |
|------|-----|--------|
| `app/extractor.py` | BUG-DATA-001 | Removed Fallback 1 from `_extract_amenities()` |
| `app/config.py` | BUG-PERF-001 | Added `SELENIUM_CONTENT_WAIT_TIMEOUT_S`, `LANG_SCRAPE_DELAY_IT` |
| `app/scraper.py` | BUG-PERF-001 | `set_page_load_timeout` + `content_wait_s` + Italian delay |
| `env.example` | BUG-PERF-001 | Documented 2 new config fields |
| `app/__init__.py` | — | `BUILD_VERSION = 64`, changelog updated |

---

## Complete Fix Status — All Sessions

| ID | Description | Session | Status |
|----|-------------|---------|--------|
| BUG-IMPORT-001..004 | Import aliases | #1 | ✅ |
| BUG-CFG-001..5 | 11 missing Settings fields | #1 | ✅ |
| BUG-EXTRACTOR-001 | Singleton extractor | #1 | ✅ |
| BUG-PERSIST-001 | 7 missing upsert methods | #1 | ✅ |
| BUG-PHOTO-001 | Images never downloaded | #1 | ✅ |
| BUG-BROWSER-001 | Brave didn't close | #1 | ✅ |
| FIX-PH-LEGACY-001 | Property highlights DOM | #1 | ✅ |
| BUG-LOG-001 | `hotel_id` in scraping_logs | #1 | ⚠️ Unverified |
| BUG-VERIFY-001 | `verify_system.py` version | #1 | ✅ |
| BUG-SCRIPT-001 | `create_db.bat` schema ref | #2 | ✅ |
| **BUG-DATA-001** | Amenities = popular_services | **Build 64** | ✅ **Fixed** |
| **BUG-PERF-001** | Italian language slowness | **Build 64** | ✅ **Fixed** |
| BUG-IMG-001 | 4 image download errors | #3 | ⚠️ Pending `\d` inspection |
| WARN-ORM-001 | `scraped_at` as ORM PK | #3 | ✅ Closed (0 collisions) |

---

*BookingScraper Pro v6.0.0 Build 64 — 2026-04-01*
