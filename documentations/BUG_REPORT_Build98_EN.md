# Bug Report — BookingScraper Pro v6.0.0 Build 98

**Date:** 2026-05-04  
**Build:** 98 (previous: 97)  
**Platform:** Windows 11 / Python 3.14 / PostgreSQL 14+  
**Schema:** schema_v77_complete.sql (no changes in this build)  
**Source:** Technical Audit Report Build 97 + Master Code Modification Prompt v1.0  

---

## Summary of Changes

| ID | Priority | Type | File(s) Modified | Status |
|----|----------|------|-----------------|--------|
| BUG-SVC-002-FIX | 🟠 HIGH | Bug Fix | `api_payload_builder.py` | ✅ Fixed |
| BUG-EXTRACT-IT-001-FIX | 🟠 HIGH | Performance Fix | `scraper.py` | ✅ Fixed |
| GAP-EXPORT-001-FIX | 🟡 MEDIUM | Missing Feature | `api_export_system.py` | ✅ Fixed |
| GAP-CONFIG-001 | 🟡 MEDIUM | Version Sync | `config.py`, `__init__.py` | ✅ Verified (both = 98) |

**Schema changes:** None.  
**ORM changes:** None.  
**API contract changes:** None.  

---

## BUG-SVC-002-FIX — Room-Level Amenities Mixed into `services[]`

### Classification
**Priority:** 🟠 HIGH  
**Type:** Data contamination (API payload corruption)  
**Module:** `app/api_payload_builder.py`

### Root Cause

When the `_extract_all_services()` extractor falls back to DOM strategies (1, 1.5, or 2) instead of the primary Apollo/GraphQL JSON strategy, Booking.com's room-amenity section (`groupId=15`) is included alongside hotel-level facilities. This produces items such as:

- `"Papel higiénico"` / `"Toilet paper"` (room amenity)
- `"Baño privado"` / `"Private bathroom"` (room amenity)
- `"TV de pantalla plana"` / `"Flat-screen TV"` (room amenity)
- `"Ducha"` / `"Shower"` (room amenity)

…appearing inside the `services[]` field of the API payload alongside genuine hotel-level facilities like `"WiFi gratis"`, `"Parking"`, `"Bar"`.

**Confirmed in:** `pruebas/_table__hotels_all_services__.csv` — rows 11–16 (ES, `service_category = "Comodidades"`) contain clear room-level items.

The Apollo JSON strategy (Strategy 0) always returns correctly categorized hotel-level facilities only. The DOM fallback path does not discriminate between hotel and room facility groups.

### Fix Applied

**File:** `app/api_payload_builder.py`

1. Added `_ROOM_LEVEL_CATEGORIES` frozenset containing the localized heading names for Booking.com's `groupId=15` (Room Amenities) in all scraping languages:

```python
_ROOM_LEVEL_CATEGORIES: frozenset = frozenset({
    "room amenities",    # EN
    "comodidades",       # ES / PT
    "zimmerausstattung", # DE
    "dotazioni camera",  # IT
})
```

2. Modified `_load_services()` to filter out rows whose `service_category` (lowercased) matches this set before building the `services[]` payload. Filtered rows are counted and logged at DEBUG level.

**Why French is excluded from the filter:**  
The French `groupId=15` label is `"Équipements"`, which collides with the hotel-level facilities label `"Équipements"` used in `_CATEGORY_LABELS["hotel_services"]["fr"]`. Filtering `"équipements"` in FR would silently drop legitimate hotel facilities. This is documented as **GAP-SVC-002-FR** (deferred).

### Verification Steps

1. Trigger a scrape on any URL for all 6 languages.
2. Check `pruebas/_table__hotels_all_services__.csv` — confirm rows with `service_category IN ('Comodidades', 'Zimmerausstattung', 'Room Amenities', 'Dotazioni camera')` are NOT present in `services[]`.
3. Call `GET /hotels/url/{url_id}/api-payload` — confirm `data.services.es` does not contain `"Papel higiénico"`, `"Ducha"`, `"Baño privado"` or similar room-only items.
4. Confirm `data.services.en` still contains hotel-level items like `"Free WiFi"`, `"Parking"`, `"Bar"`.

### Pre/Post Behavior

| Field | Before Build 98 | After Build 98 |
|-------|----------------|----------------|
| `services.es` | Contains "Papel higiénico", "Baño privado", "TV de pantalla plana" | Only hotel-level services |
| `services.de` | Contains "Eigenes Badezimmer", "Flachbildfernseher" | Only hotel-level services |
| `services.en` | May contain "Toilet paper", "Shower", "Flat-screen TV" | Only hotel-level services |

---

## BUG-EXTRACT-IT-001-FIX — Italian (& All Languages) Sequential Wait Latency

### Classification
**Priority:** 🟠 HIGH  
**Type:** Performance fix  
**Module:** `app/scraper.py`

### Root Cause

In `_fetch_with_selenium()`, the code waited for the hotel page to load by iterating 4 CSS selectors **sequentially**, each with its own `WebDriverWait(driver, content_wait_s)`:

```python
# Old code (Build 97)
for selector in hotel_selectors:  # 4 selectors
    try:
        WebDriverWait(driver, content_wait_s).until(...)  # 10 s each
        loaded = True
        break
    except TimeoutException:
        continue
```

**Worst case:** if the first 3 selectors timeout and only the 4th matches (as on Italian, German, and French pages using `h1.pp-header__title`), the effective wait is `3 × 10 s = 30 s` **before** the real content is found — plus the actual load time.

**Observed impact:** Italian scrapes: 15–75 s average, with outliers >120 s.

Build 64 (`BUG-PERF-001-FIX`) reduced `content_wait_s` from 30 s to 10 s, cutting worst case from 120 s to 40 s, but did not eliminate the sequential multiplication.

### Fix Applied

**File:** `app/scraper.py`

Replaced the sequential `for` loop with a single `WebDriverWait` using **`EC.any_of()`**, which evaluates all selectors in parallel and resolves as soon as the first one appears:

```python
# New code (Build 98)
WebDriverWait(driver, content_wait_s).until(
    EC.any_of(
        *[
            EC.presence_of_element_located((By.CSS_SELECTOR, sel))
            for sel in hotel_selectors
        ]
    )
)
loaded = True
```

`EC.any_of()` is available since Selenium 4.0. The project requirement is `selenium >= 4.27.0` — no version risk.

**Improvement:**

| Scenario | Build 97 | Build 98 |
|----------|---------|---------|
| Best case (1st selector matches) | 0 s wait | 0 s wait |
| Worst case (4th selector matches) | 30 s extra wait | 0 s extra wait |
| Worst case (no selector matches) | 40 s (4×10) | 10 s (1×10) |

**Expected reduction:** Italian scrapes from 15–75 s → ~10–25 s (75% reduction in wait overhead).

### Verification Steps

1. Trigger a scrape on any URL with `lang="it"`.
2. Check Celery worker logs — Italian scrape duration should drop from 15–75 s range toward 10–25 s.
3. Check for regression: `loaded` variable must still be correctly set to `False` on `TimeoutException`.

---

## GAP-EXPORT-001-FIX — No HTTP 429 Rate Limit Recovery in API Export

### Classification
**Priority:** 🟡 MEDIUM  
**Type:** Missing error handling  
**Module:** `app/api_export_system.py`

### Root Cause

`_send_hotel()` treated HTTP 429 (Too Many Requests) identically to any other non-OK status code — it applied the standard exponential backoff (`retry_delay * 2^attempt`, default: 2 s, 4 s, 8 s) and immediately retried. This is insufficient:

- API servers responding with 429 typically require 30–120 s before accepting new requests.
- The standard backoff (≤8 s for 3 attempts) always hit the rate limit again on retry.
- The `Retry-After` response header (standard RFC 6585) was ignored entirely.

**Impact:** When exporting batches of multiple hotels, the system would flood the API on rate-limited attempts, fail all retries, and silently return the last HTTP status code.

### Fix Applied

**File:** `app/api_export_system.py`

1. **Added `email.utils.parsedate_to_datetime`** import for RFC 2822 HTTP-date parsing.
2. **Added two new `APIConfig` fields** (backwards-compatible, with defaults):
   - `rate_limit_wait_s: float = 60.0` — minimum wait when HTTP 429 is received
   - `max_retry_after_s: float = 300.0` — maximum acceptable Retry-After; if exceeded, abort retries for this hotel
3. **Added explicit 429 branch** in `_send_hotel()` retry loop:
   - Reads `Retry-After` header (both numeric seconds and HTTP-date formats)
   - Applies `max(Retry-After, rate_limit_wait_s)` as the effective wait
   - If the required wait exceeds `max_retry_after_s`, logs an error and aborts (avoids blocking the export queue indefinitely)
   - After sleeping, `continue`s to the next retry attempt (skips the standard backoff sleep)

**Logic flow for HTTP 429:**

```
resp.status_code == 429
  → read Retry-After header (numeric or HTTP-date)
  → effective_wait = max(Retry-After, rate_limit_wait_s)
  → if effective_wait > max_retry_after_s → log error, return 429 (abort)
  → else → sleep(effective_wait) → continue to next attempt
```

**Configuration (APIConfig.to_dict / from_dict):** both serialization methods updated — existing config files without these fields will use default values (backwards-compatible).

### Verification Steps

1. Configure a test API endpoint that returns HTTP 429 with `Retry-After: 30`.
2. Trigger an export — log should show: `"GAP-EXPORT-001-FIX: API 429 hotel_id=... rate limited. Esperando 60 s"` (60 s because max(30, 60) = 60).
3. Trigger with `Retry-After: 400` — log should show: `"Retry-After=400 supera max_retry_after_s=300"` and abort.
4. Normal non-429 errors should continue using standard exponential backoff unchanged.

---

## GAP-CONFIG-001 — Build Version Consistency

### Classification
**Priority:** 🟡 MEDIUM (Observation)  
**Type:** Housekeeping  

### Status

Both `config.py` (`BUILD_VERSION: int = Field(default=98)`) and `app/__init__.py` (`BUILD_VERSION = 98`) are now synchronized at **Build 98**. Verified by grepping both files.

---

## Pre-Output Validation Checklist

| # | Check | Status |
|---|-------|--------|
| 1 | Schema changes reflected in ORM models | ✅ N/A — no schema changes |
| 2 | New extractors called from `extract_all()` | ✅ N/A — no new extractors |
| 3 | New persistence functions called from `_persist_hotel_data()` | ✅ N/A — no new upserts |
| 4 | New payload builder methods called from `build_payload()` | ✅ N/A — filter added to existing method |
| 5 | API payload still generates all mandatory fields | ✅ Confirmed — filter only removes room-level rows |
| 6 | No `session.commit()` added to `scraper_service.py` | ✅ `scraper_service.py` not modified |
| 7 | Config fields have defaults and referenced safely | ✅ `rate_limit_wait_s` and `max_retry_after_s` have explicit defaults |
| 8 | Schema validation query returns correct table count | ✅ N/A — schema unchanged |
| 9 | No CloudScraper or HTTP fallback code introduced | ✅ Confirmed — Selenium-only policy maintained |
| 10 | All modified files preserve original names | ✅ Confirmed |

---

## Files Delivered

| File | Changes | Build |
|------|---------|-------|
| `app/api_payload_builder.py` | `_ROOM_LEVEL_CATEGORIES` + filter in `_load_services()` | 98 |
| `app/scraper.py` | Sequential `WebDriverWait` loop → `EC.any_of()` | 98 |
| `app/api_export_system.py` | HTTP 429 detection + `Retry-After` handling + new `APIConfig` fields | 98 |
| `app/config.py` | `BUILD_VERSION` default → 98 | 98 |
| `app/__init__.py` | `BUILD_VERSION` → 98 | 98 |

---

## Deferred Items (Not Modified in Build 98)

| ID | Description | Reason Deferred |
|----|-------------|----------------|
| GAP-SVC-002-FR | French `"Équipements"` (groupId=15) ambiguity | Label collision with hotel-level FR — requires extractor-level fix |
| GAP-VALIDATION-001 | Automated selector health monitoring | New module — outside Build 98 scope |
| GAP-ROOM-001 | Room photo extraction + SVG occupancy fallback | Complex DOM change — separate build |
| GAP-REVIEW-PAGE-001 | Individual review pagination | Enhancement — separate build |
| GAP-METRICS-001 | `completeness_ratio` per field per language | Enhancement — separate build |

---

*Build 98 — BookingScraper Pro v6.0.0*  
*Generated: 2026-05-04*
