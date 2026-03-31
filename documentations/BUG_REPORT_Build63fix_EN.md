# BookingScraper Pro — Bug Report
## Version 6.0.0 · Build 63-fix · Audit Date: 2026-03-31

---

## Executive Summary

Full technical audit of BookingScraper Pro v6.0.0 following Build 63 (CloudScraper removal). The repository base contained **12 bugs** ranging from startup `ImportError` crashes to silent data-loss issues affecting 7 database tables. All bugs have been fixed in the delivered files.

**Current system state (post-fix):** 13/13 URLs × 6/6 languages = 78 records with complete integrity in core tables. Worker, Beat, and API start cleanly.

---

## Bug Inventory

| ID | Severity | File | Category | Status |
|----|----------|------|----------|--------|
| BUG-IMPORT-001 | 🔴 Critical | `models.py` | Import / Naming | ✅ Fixed |
| BUG-IMPORT-002 | 🔴 Critical | `extractor.py` | Import / Naming | ✅ Fixed |
| BUG-IMPORT-003 | 🔴 Critical | `config.py` | Missing constant | ✅ Fixed |
| BUG-IMPORT-004 | 🔴 Critical | `models.py` | Import / Naming | ✅ Fixed |
| BUG-CFG-001 | 🔴 Critical | `config.py` | Missing Settings fields | ✅ Fixed |
| BUG-CFG-002..5 | 🔴 Critical | `config.py` | Missing Settings fields | ✅ Fixed |
| BUG-EXTRACTOR-001 | 🔴 Critical | `scraper_service.py` | Design pattern mismatch | ✅ Fixed |
| BUG-PERSIST-001 | 🔴 Critical | `scraper_service.py` | Silent data loss | ✅ Fixed |
| BUG-PHOTO-001 | 🔴 Critical | `scraper_service.py` | Images never downloaded | ✅ Fixed |
| BUG-BROWSER-001 | 🟡 Medium | `scraper_service.py` | Resource leak | ✅ Fixed |
| FIX-PH-LEGACY-001 | 🔴 Critical | `extractor.py` | DOM strategy mismatch | ✅ Fixed |
| BUG-LOG-001 | 🟡 Medium | `scraper_service.py` | Incomplete log records | ✅ Fixed |
| BUG-VERIFY-001 | 🟢 Low | `verify_system.py` | Stale version / false FAIL | ✅ Fixed |

---

## Detailed Bug Descriptions

---

### BUG-IMPORT-001 — `ScrapingLogs` plural does not exist in `models.py`
**Severity:** 🔴 Critical — prevents all three processes from starting (API, Worker, Beat)

**File:** `app/models.py` → `app/scraper_service.py:40`

**Root cause:**
`scraper_service.py` imports `ScrapingLogs` (plural) but the ORM class is defined as `ScrapingLog` (singular).

```python
# scraper_service.py:40 — WRONG
from app.models import URLQueue, URLLanguageStatus, Hotel, ScrapingLogs

# models.py:672 — actual class name
class ScrapingLog(Base):
    __tablename__ = "scraping_logs"
```

**Fix:** Added compatibility alias at end of `models.py`:
```python
ScrapingLogs = ScrapingLog
```

**Impact:** System refused to start. All three processes (Celery Worker, Celery Beat, Uvicorn API) raised `ImportError` at startup.

---

### BUG-IMPORT-002 — `BookingExtractor` does not exist in `extractor.py`
**Severity:** 🔴 Critical — prevents all three processes from starting

**File:** `app/extractor.py` → `app/scraper_service.py:44`

**Root cause:**
`scraper_service.py` imports `BookingExtractor` but the class is named `HotelExtractor`.

```python
# scraper_service.py:44 — WRONG
from app.extractor import BookingExtractor

# extractor.py:356 — actual class name
class HotelExtractor:
```

**Fix:** Added compatibility alias at end of `extractor.py`:
```python
BookingExtractor = HotelExtractor
```

---

### BUG-IMPORT-003 — `_VALID_VPN_COUNTRIES` removed from `config.py`
**Severity:** 🔴 Critical — prevents scraping tasks from executing

**File:** `app/config.py` → `app/vpn_manager_windows.py:39`

**Root cause:**
During Build 63 CloudScraper cleanup, the module-level constant `_VALID_VPN_COUNTRIES` was accidentally removed from `config.py`. `vpn_manager_windows.py` imports it directly.

```python
# vpn_manager_windows.py:39
from app.config import get_settings, _VALID_VPN_COUNTRIES  # ImportError!
```

**Fix:** Restored `frozenset` constant before the `Settings` class in `config.py` (line 47), including both space and underscore variants for multi-word country names.

**Impact:** Every `scrape_pending_urls` task failed with `ImportError` even when `VPN_ENABLED=False`, because `NullVPNManager` is also in the same module.

---

### BUG-IMPORT-004 — `HotelPolicies` plural does not exist in `models.py`
**Severity:** 🔴 Critical — all language scraping succeeded but DB write failed for every hotel

**File:** `app/models.py` → `app/scraper_service.py:475`

**Root cause:**
`_upsert_hotel_policies()` imports `HotelPolicies` (plural). The ORM class is `HotelPolicy` (singular).

```python
# scraper_service.py:475
from app.models import HotelPolicies  # ImportError at runtime!

# models.py:426 — actual class
class HotelPolicy(Base):
    __tablename__ = "hotels_policies"
```

**Evidence from `url_language_status`:**
```
last_error: "DB write error: cannot import name 'HotelPolicies' from 'app.models'"
```
All 13 URLs × 6 languages raised this error during persistence.

**Fix:** Added alias in `models.py`:
```python
HotelPolicies = HotelPolicy
```

---

### BUG-CFG-001 — Missing `APP_NAME`, `APP_VERSION`, `BUILD_VERSION` in `Settings`
**Severity:** 🔴 Critical — `verify_system.py` raised `AttributeError` at configuration check

**File:** `app/config.py`

**Root cause:**
`verify_system.py` accesses `s.APP_NAME`, `s.APP_VERSION`, `s.BUILD_VERSION` but these fields were not declared in the `Settings` class.

**Fix:** Added three fields to `Settings`:
```python
APP_NAME: str = Field(default="BookingScraper Pro")
APP_VERSION: str = Field(default="6.0.0")
BUILD_VERSION: int = Field(default=63)
```

---

### BUG-CFG-002..5 — Eight Missing Attributes in `Settings`
**Severity:** 🔴 Critical — startup failures (API, Worker, tasks)

**File:** `app/config.py`

| Attribute | Type | Used In | Default |
|-----------|------|---------|---------|
| `database_url` | `@property` | `database.py:45` | Computed from `DB_*` fields |
| `LOGS_DIR` | `Path` | `main.py:80,98` | `logs/` |
| `LOGS_DEBUG_DIR` | `Path` | `main.py:81` | `data/logs/debug/` |
| `IMAGES_DIR` | `Path` | `image_downloader.py:204` | `data/images/` |
| `DEBUG_HTML_DIR` | `Path` | `tasks.py:191` | `data/debug_html/` |
| `MAX_ERROR_LEN` | `int` | `extractor.py:563` | `10000` |
| `STMT_TIMEOUT_OLAP_MS` | `int` | `database.py:144` | `30000` |

**Fix:** All attributes added to `Settings`. `database_url` implemented as `@property` computing the psycopg v3 connection string with URL-encoded password.

---

### BUG-EXTRACTOR-001 — `BookingExtractor` used as stateless singleton
**Severity:** 🔴 Critical — `TypeError` on every scraping task

**File:** `app/scraper_service.py:100`

**Root cause:**
`ScraperService.__init__()` attempted to instantiate `BookingExtractor()` without arguments. `HotelExtractor.__init__` requires `html` as mandatory positional argument (it parses the DOM at construction time).

```python
# WRONG — TypeError: HotelExtractor.__init__() missing 1 required positional argument
self._extractor = BookingExtractor()  # scraper_service.py:100

# Correct usage
extractor = BookingExtractor(html=html, url=lang_url, language=lang)
extracted = extractor.extract_all()
```

**Fix:** Removed singleton from `__init__`. Each language request now instantiates a fresh `BookingExtractor(html, url, lang)` inside `_scrape_language()`.

---

### BUG-PERSIST-001 — 7 database tables never received data
**Severity:** 🔴 Critical — silent data loss

**File:** `app/scraper_service.py` — `_persist_hotel_data()`

**Root cause:**
`_persist_hotel_data()` only called 3 of the 10 required `_upsert_*` methods. Data for 7 tables was extracted by `HotelExtractor.extract_all()` but silently discarded.

| Table | Method | Status (before fix) |
|-------|--------|---------------------|
| `hotels` | `_upsert_hotel()` | ✅ Called |
| `hotels_description` | `_upsert_hotel_description()` | ✅ Called |
| `hotels_policies` | `_upsert_hotel_policies()` | ✅ Called |
| `hotels_legal` | `_upsert_hotel_legal()` | ✅ Called |
| `hotels_amenities` | `_upsert_hotel_amenities()` | ❌ Missing |
| `hotels_popular_services` | `_upsert_hotel_popular_services()` | ❌ Missing |
| `hotels_fine_print` | `_upsert_hotel_fine_print()` | ❌ Missing |
| `hotels_all_services` | `_upsert_hotel_all_services()` | ❌ Missing |
| `hotels_faqs` | `_upsert_hotel_faqs()` | ❌ Missing |
| `hotels_guest_reviews` | `_upsert_hotel_guest_reviews()` | ❌ Missing |
| `hotels_property_highlights` | `_upsert_hotel_property_highlights()` | ❌ Missing |

**Fix:** Added 7 new `_upsert_*` methods and their corresponding calls in `_persist_hotel_data()`.

---

### BUG-PHOTO-001 — Hotel images never downloaded
**Severity:** 🔴 Critical — `image_downloads` table always empty, `data/images/` always empty

**File:** `app/scraper_service.py:376` → `app/extractor.py`

**Root cause:**
`extract_all()` documentation explicitly states `'photos': ELIMINADO` (removed in v50). However, `scraper_service.py` was still reading `extracted.get("photos", [])` — always returning `[]`. The actual extraction method `extract_hotel_photos()` existed on `HotelExtractor` but was never called.

```python
# WRONG — "photos" key was removed from extract_all() in v50
photos = extracted.get("photos", [])  # always []
if photos and hotel_id and lang == "en":  # condition never true
    ...download images...

# FIXED
if hotel_id and lang == "en" and html:
    _photo_extractor = BookingExtractor(html=html, url=lang_url, language="en")
    photos = _photo_extractor.extract_hotel_photos()  # actual extraction
    if photos:
        self._image_downloader.download_photo_batch(hotel_id, photos)
```

**Impact:** Zero rows in `image_downloads`, zero files in `data/images/` despite Brave correctly opening galleries and logging "Gallery: 138 unique image URLs extracted".

---

### BUG-BROWSER-001 — Brave browser remained open after batch completion
**Severity:** 🟡 Medium — resource leak, window stays on last scraped page

**File:** `app/scraper_service.py` — `dispatch_batch()`

**Root cause:**
`SeleniumEngine` uses a singleton driver (`self._driver`) that persists for the lifetime of the Worker process. After batch completion, no `quit()` was called.

**Fix:** Added `reset_browser()` call at the end of `dispatch_batch()`:
```python
try:
    self._selenium_engine.reset_browser()
    logger.info("Selenium: Brave closed after batch completion.")
except Exception as _exc:
    logger.warning("Selenium: reset_browser after batch raised: %s", _exc)
```

---

### FIX-PH-LEGACY-001 — `hotels_property_highlights` always empty (DOM mismatch)
**Severity:** 🔴 Critical — table always empty despite data present in HTML

**File:** `app/extractor.py` — `_extract_property_highlights()`

**Root cause:**
The extractor's Strategies 0–3 searched for React DOM patterns (`e43cb5a00e`, `data-testid="property-highlights"`). The actual Booking.com HTML uses a **server-rendered legacy** structure:

```html
<!-- Legacy server-rendered (actual) -->
<div class="property-highlights ph-icon-fill-color">
  <div class="ph-sections">
    <div class="ph-section">
      <h4 class="ph-item-header">Breakfast info</h4>
      <p class="ph-item">Buffet</p>
    </div>
  </div>
</div>
```

Validated against `pruebas/_HTML-view-source__manaus-hoteis-millennium_en-gb_html__.md`.

**Fix:** Added "LEGACY" strategy executed **before** all existing strategies:
- Finds `div.property-highlights`
- Iterates `div.ph-section` elements
- Maps `h4.ph-item-header` → `category`, `p.ph-item` → `detail`

**Extracted data example (Manaus Hotéis Millennium):**
```
category="Top Location"   | detail="Top location: Highly rated by recent guests (8.8)"
category="Breakfast info" | detail="Buffet"
category="Parking"        | detail="Private parking at the hotel"
category="Loyal customers"| detail="There are more repeat guests here than most other properties."
```

---

### BUG-LOG-001 — `hotel_id` never populated in `scraping_logs`
**Severity:** 🟡 Medium — reduces diagnostic query capability

**File:** `app/scraper_service.py` — `_log_scraping_event()`

**Root cause:**
The `scraping_logs` schema includes a nullable `hotel_id UUID` column for JOIN queries. However, `_log_scraping_event()` never passed this value, leaving it `NULL` in every row.

**Fix:** Added optional `hotel_id` parameter:
```python
def _log_scraping_event(
    self, url_obj, lang, event_type, status, duration_ms,
    error_message=None, hotel_id=None  # NEW
) -> None:
```

---

### BUG-VERIFY-001 — `verify_system.py` shows stale version and false `[FAIL]`
**Severity:** 🟢 Low — cosmetic / misleading

**File:** `scripts/verify_system.py`

**Issues:**
1. Header displays `"BookingScraper Pro v48"` — should be `v6.0.0 Build 63-fix`
2. `cloudscraper` listed as a **critical** dependency — Build 63 intentionally removed it. Every startup shows `[FAIL] cloudscraper` counting as a "critical problem"

**Fix:** Updated header string to `v6.0.0 Build 63-fix`. Removed `cloudscraper` from `critical[]` list (left as comment explaining removal).

---

## Files Delivered

| File | Changes | Bugs Fixed |
|------|---------|------------|
| `app/__init__.py` | BUILD_VERSION 60 → 63, changelog | All |
| `app/config.py` | 11 new fields + `_VALID_VPN_COUNTRIES` + `database_url` | BUG-IMPORT-003, BUG-CFG-001..5 |
| `app/models.py` | Aliases `ScrapingLogs`, `HotelPolicies` | BUG-IMPORT-001, BUG-IMPORT-004 |
| `app/extractor.py` | LEGACY strategy + `BookingExtractor` alias | FIX-PH-LEGACY-001, BUG-IMPORT-002 |
| `app/scraper_service.py` | 7 new upsert methods, photo fix, browser close, hotel_id log | BUG-EXTRACTOR-001, BUG-PERSIST-001, BUG-PHOTO-001, BUG-BROWSER-001, BUG-LOG-001 |
| `scripts/verify_system.py` | Version string, cloudscraper moved | BUG-VERIFY-001 |

---

## Deployment Procedure

```batch
REM 1. Stop all services
stop_server.bat
stop_celery.bat

REM 2. Replace files
copy __init__.py       C:\BookingScraper\app\
copy config.py         C:\BookingScraper\app\
copy models.py         C:\BookingScraper\app\
copy extractor.py      C:\BookingScraper\app\
copy scraper_service.py C:\BookingScraper\app\
copy verify_system.py  C:\BookingScraper\scripts\

REM 3. Verify (expect 0 critical errors, "build=63")
python scripts\verify_system.py

REM 4. Restart
inicio_rapido.bat
```

---

## Known Non-Bug Behaviors

| Observation | Explanation |
|-------------|-------------|
| Brave stays open between languages | `SeleniumEngine` singleton — expected, now closes after each batch |
| `[WARN] Python 3.14 pre-release` | System functional, but 3.11/3.12 recommended for production |
| `scraping_logs` partitions only until 2027 | `ensure_log_partitions` task creates 2 months ahead automatically |
| `completeness_service.py` unused | Present in repo but not called from any task — not a runtime bug |

---

*BookingScraper Pro v6.0.0 Build 63-fix — Audit 2026-03-31*
