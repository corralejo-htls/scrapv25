# BUG REPORT — Build 76 · API Gap Analysis
## BookingScraper Pro v6.0.0 — External API Payload Compliance

**Report Date:** 2026-04-04
**Build:** 76
**Classification:** Internal Technical Documentation
**Severity Distribution:** 2 Critical · 2 High · 3 Medium
**Auditor:** Architectural Review (Claude / Anthropic)

---

## TABLE OF CONTENTS

1. [BUG-PERSIST-002 — CRITICAL: 4 v76 Upsert Methods Never Called](#bug-persist-002)
2. [BUG-MAIN-001 — HIGH: GET /hotel/{id} Missing All v76 Fields](#bug-main-001)
3. [GAP-API-001 — CRITICAL: No API Payload Builder Exists](#gap-api-001)
4. [GAP-SCHEMA-001 — HIGH: hotels_guest_reviews Semantic Mismatch](#gap-schema-001)
5. [GAP-SCHEMA-002 — MEDIUM: hotels_room_types Missing API-Required Columns](#gap-schema-002)
6. [GAP-EXTRACT-001 — MEDIUM: accommodation_type Not Extracted or Stored](#gap-extract-001)
7. [GAP-SCHEMA-003 — MEDIUM: hotels_nearby_places.category Type Mismatch vs API](#gap-schema-003)
8. [Summary Table](#summary-table)
9. [Fix Roadmap](#fix-roadmap)

---

## BUG-PERSIST-002 {#bug-persist-002}

| Field        | Value |
|---|---|
| **ID**       | BUG-PERSIST-002 |
| **Severity** | 🔴 CRITICAL |
| **Files**    | `app/scraper_service.py` |
| **Scope**    | Data persistence layer |
| **Pattern**  | Same root cause as BUG-PERSIST-001 (Build 63) |

### Description

Four upsert methods introduced in Build 76 for the new v76 tables are **defined** in `ScraperService` but are **never invoked** from `_persist_hotel_data()`. This is an exact repeat of BUG-PERSIST-001, where 7 upsert methods went uncalled for multiple builds.

As a consequence, the four new tables are **always empty** despite data being correctly extracted by `HotelExtractor.extract_all()`.

### Affected Tables

| New Table (v76) | Upsert Method | Status |
|---|---|---|
| `hotels_extra_info` | `_upsert_hotel_extra_info()` | ❌ Never called |
| `hotels_nearby_places` | `_upsert_hotel_nearby_places()` | ❌ Never called |
| `hotels_room_types` | `_upsert_hotel_room_types()` | ❌ Never called |
| `hotels_seo` | `_upsert_hotel_seo()` | ❌ Never called |

### Evidence

```python
# scraper_service.py — _persist_hotel_data() — lines 530–546
# Current state — INCOMPLETE:
with get_db() as session:
    hotel = self._upsert_hotel(session, url_obj, lang, data, duration_ms)
    hotel_id = str(hotel.id)
    self._upsert_hotel_description(session, url_obj, hotel, lang, data)
    self._upsert_hotel_policies(session, url_obj, hotel, lang, data)
    self._upsert_hotel_legal(session, url_obj, hotel, lang, data)
    self._upsert_hotel_popular_services(session, url_obj, hotel, lang, data)
    self._upsert_hotel_fine_print(session, url_obj, hotel, lang, data)
    self._upsert_hotel_all_services(session, url_obj, hotel, lang, data)
    self._upsert_hotel_faqs(session, url_obj, hotel, lang, data)
    self._upsert_hotel_guest_reviews(session, url_obj, hotel, lang, data)
    self._upsert_hotel_property_highlights(session, url_obj, hotel, lang, data)
    session.commit()
    # ❌ MISSING — 4 calls for STRUCT-021/022/023/024:
    # self._upsert_hotel_extra_info(session, url_obj, hotel, lang, data)
    # self._upsert_hotel_nearby_places(session, url_obj, hotel, lang, data)
    # self._upsert_hotel_room_types(session, url_obj, hotel, lang, data)
    # self._upsert_hotel_seo(session, url_obj, hotel, lang, data)
```

### Fix

Add the four missing calls **before** `session.commit()`, after `_upsert_hotel_property_highlights`:

```python
# scraper_service.py — _persist_hotel_data()
self._upsert_hotel_property_highlights(session, url_obj, hotel, lang, data)
# ✅ ADD: STRUCT-021/022/023/024 (v76)
self._upsert_hotel_extra_info(session, url_obj, hotel, lang, data)
self._upsert_hotel_nearby_places(session, url_obj, hotel, lang, data)
self._upsert_hotel_room_types(session, url_obj, hotel, lang, data)
self._upsert_hotel_seo(session, url_obj, hotel, lang, data)
session.commit()
```

### Impact

- `hotels_extra_info`: `extraInfo` field missing from API payload
- `hotels_nearby_places`: `nearbyPlaces` field missing from API payload
- `hotels_room_types`: normalized rooms table always empty (JSONB fallback in `hotels.room_types` still populated)
- `hotels_seo`: `seoDescription` and `keywords` fields missing from API payload

---

## BUG-MAIN-001 {#bug-main-001}

| Field        | Value |
|---|---|
| **ID**       | BUG-MAIN-001 |
| **Severity** | 🟠 HIGH |
| **Files**    | `app/main.py` |
| **Scope**    | REST API response layer |

### Description

`main.py` only imports the original model classes and the `GET /hotel/{id}` endpoint response does not expose any of the fields added in v76. The four new tables and the two new columns on `hotels` (`price_range`, `rooms_quantity`) are completely invisible to API consumers.

### Evidence

```python
# main.py — line 59-62: model imports
from app.models import (
    Base, Hotel, HotelDescription, HotelLegal,
    HotelPolicy, HotelPopularService, ScrapingLog, URLLanguageStatus, URLQueue,
)
# ❌ NOT IMPORTED: HotelExtraInfo, HotelNearbyPlace, HotelRoomType, HotelSEO
```

The `get_hotel()` endpoint response dict (lines 919–972) does not include:
- `price_range` (hotels column, STRUCT-019)
- `rooms_quantity` (hotels column, STRUCT-020)
- `extra_info` (hotels_extra_info, STRUCT-021)
- `nearby_places` (hotels_nearby_places, STRUCT-022)
- `room_types` (hotels_room_types, STRUCT-023)
- `seo` (hotels_seo, STRUCT-024)

### Fix

1. Add imports in `main.py`:

```python
from app.models import (
    Base, Hotel, HotelDescription, HotelExtraInfo, HotelLegal,
    HotelNearbyPlace, HotelPolicy, HotelPopularService, HotelRoomType,
    HotelSEO, ScrapingLog, URLLanguageStatus, URLQueue,
)
```

2. Add queries and fields to `get_hotel()` response:

```python
# Query new v76 tables
extra_info_row = session.query(HotelExtraInfo).filter_by(hotel_id=hid, language=row.language).first()
nearby_rows    = session.query(HotelNearbyPlace).filter_by(hotel_id=hid, language=row.language).all()
room_rows      = session.query(HotelRoomType).filter_by(hotel_id=hid, language=row.language).all()
seo_row        = session.query(HotelSEO).filter_by(hotel_id=hid, language=row.language).first()

# Add to response dict:
"price_range":    row.price_range,
"rooms_quantity": row.rooms_quantity,
"extra_info":     extra_info_row.extra_info if extra_info_row else None,
"nearby_places":  [{"place_name": p.place_name, "distance": p.distance, "category": p.category} for p in nearby_rows],
"room_types":     [{"room_name": r.room_name, "description": r.description, "facilities": r.facilities} for r in room_rows],
"seo":            {"seo_description": seo_row.seo_description, "keywords": seo_row.keywords} if seo_row else None,
```

---

## GAP-API-001 {#gap-api-001}

| Field        | Value |
|---|---|
| **ID**       | GAP-API-001 |
| **Severity** | 🔴 CRITICAL |
| **Files**    | `app/main.py` (missing endpoint) |
| **Scope**    | API payload generation for external system |

### Description

**No code exists anywhere in the application** that constructs the payload format specified in `_API_.md`. The `_API_.md` document defines the exact JSON structure required by the external destination API, but there is no service, endpoint, or transformer that maps the scraped data to that format.

The following `_API_.md` fields have **no mapping** to any existing code path:

| `_API_.md` Field | Status | Notes |
|---|---|---|
| `data.geoPosition` | ⚠️ PARTIAL | `latitude`/`longitude` exist in DB — not mapped to output object |
| `data.services` | ❌ MISSING | Requires nested `{category: [items]}` from `hotels_all_services` flat rows |
| `data.conditions` | ⚠️ PARTIAL | `hotels_policies` has `policy_name`/`policy_details` — different key names |
| `data.toConsider` | ❌ MISSING | `hotels_fine_print` + `hotels_legal` — no concatenation logic |
| `data.categoryScoreReview` | ❌ MISSING | `hotels_guest_reviews` stores category scores but not in nested keyed format |
| `data.reviews` | ❌ MISSING | No table for individual guest reviews (name/title/positive/negative/country) |
| `data.nearbyPlaces` | ❌ MISSING | Table exists but data not persisted (BUG-PERSIST-002) |
| `data.guestValues` | ⚠️ PARTIAL | `hotels_faqs` has question/answer — key names differ |
| `data.seoDescription` | ❌ MISSING | Table exists but data not persisted (BUG-PERSIST-002) |
| `data.keywords` | ❌ MISSING | Table exists but data not persisted (BUG-PERSIST-002) |
| `data.accommodationType` | ❌ MISSING | Not extracted anywhere (see GAP-EXTRACT-001) |
| `data.images` | ⚠️ PARTIAL | `image_data` table exists — no URL list builder |
| `args.*` | ❌ MISSING | `seoFormatKey`, `onlyTitle`, `regenerateSeo`, `append`, `cache`, `locales` — no source |

### Fix

Create a new endpoint `GET /hotels/{id}/api-payload` (or equivalent export service) that:

1. Aggregates data from all relevant tables per hotel
2. Transforms field names and structures to match `_API_.md` format exactly
3. Groups data by language and constructs the multilingual nested objects
4. Builds the `args` section from configuration

This is a **new feature**, not a bug fix to an existing method.

---

## GAP-SCHEMA-001 {#gap-schema-001}

| Field        | Value |
|---|---|
| **ID**       | GAP-SCHEMA-001 |
| **Severity** | 🟠 HIGH |
| **Files**    | `schema_v76_complete.sql`, `app/extractor.py`, `app/scraper_service.py` |
| **Scope**    | Schema design — semantic mismatch |

### Description

`hotels_guest_reviews` stores **category rating scores** (e.g. Cleanliness: 9.3, Comfort: 9.2), not individual guest reviews. The `_API_.md` payload requires two completely different structures:

**`categoryScoreReview`** — what the DB stores (category scores):
```json
{
  "hotel_services": {"category": "Facilities", "score": 9.1},
  "hotel_clean":    {"category": "Cleanliness", "score": 9.3}
}
```

**`reviews`** — what the DB does NOT store (individual guest reviews):
```json
[{
  "name": "Shelly",
  "score": 10,
  "title": "Amazing. I enjoyed my stay",
  "comments": {"negative": "None", "positive": "The location..."},
  "country": "United States",
  "bookingId": null
}]
```

The schema `REJECTED` comment on line 23 (`hotels_category_scores → DUPLICADO de hotels_guest_reviews`) is **incorrect**: `hotels_guest_reviews` only stores category scores, not the keyed format (`hotel_services`, `hotel_clean`, etc.) needed for `categoryScoreReview`. Additionally, **individual text reviews are not captured at all**.

### Fix

Two separate actions required:

1. **`categoryScoreReview`**: Map the keyed format (`hotel_services`, `hotel_clean`, `hotel_comfort`, `hotel_value`, `hotel_location`, `hotel_wifi`, `total`) from `hotels_guest_reviews` via a lookup/normalization step in the payload builder.

2. **`reviews` (individual)**: Add a new table `hotels_individual_reviews` to `schema_v77_complete.sql`:

```sql
CREATE TABLE IF NOT EXISTS hotels_individual_reviews (
    id           BIGSERIAL     NOT NULL,
    hotel_id     UUID          NOT NULL,
    url_id       UUID          NOT NULL,
    language     VARCHAR(10)   NOT NULL,
    reviewer_name VARCHAR(128) NULL,
    score        NUMERIC(4,1)  NULL,
    title        TEXT          NULL,
    positive_comment TEXT      NULL,
    negative_comment TEXT      NULL,
    reviewer_country VARCHAR(128) NULL,
    booking_id   VARCHAR(64)   NULL,
    created_at   TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_hir PRIMARY KEY (id),
    CONSTRAINT fk_hir_hotel FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
);
```

And implement `_extract_individual_reviews()` in `extractor.py` targeting Booking.com review cards.

---

## GAP-SCHEMA-002 {#gap-schema-002}

| Field        | Value |
|---|---|
| **ID**       | GAP-SCHEMA-002 |
| **Severity** | 🟡 MEDIUM |
| **Files**    | `schema_v76_complete.sql`, `app/extractor.py` |
| **Scope**    | Schema incompleteness — rooms |

### Description

`hotels_room_types` (STRUCT-023, v76) is missing three columns required by the `_API_.md` `rooms[]` structure:

| API Field | DB Column | Status |
|---|---|---|
| `name` | `room_name` | ✅ Present (different key name) |
| `description` | `description` | ✅ Present |
| `facilities` | `facilities` (JSONB) | ✅ Present |
| `adults` | — | ❌ Missing |
| `children` | — | ❌ Missing |
| `images` | — | ❌ Missing |
| `info` | — | ❌ Missing (nullable in API) |

The extractor's `_extract_room_types()` explicitly avoids capturing `adults`/`children` (see docstring: "Selenium with `window.stop()` may cut SVG loading → omitted to avoid incorrect counts (always 0)"). This is a reasonable technical constraint but it must be documented as a known gap.

Room images are fully absent from both extraction logic and schema.

### Fix

1. Add columns to `schema_v77_complete.sql`:

```sql
-- In hotels_room_types:
adults    SMALLINT NULL,
children  SMALLINT NULL,
images    JSONB    NULL DEFAULT '[]'::jsonb,
info      TEXT     NULL
```

2. Attempt extraction of `adults`/`children` from `data-testid="occupancy-max-guests"` / `data-testid="occupancy-max-children"` — with a fallback to `NULL` if SVG-dependent counts are unreliable.

3. Extract room image URLs from `img[data-testid="room-photo"]` within each `room-block`.

---

## GAP-EXTRACT-001 {#gap-extract-001}

| Field        | Value |
|---|---|
| **ID**       | GAP-EXTRACT-001 |
| **Severity** | 🟡 MEDIUM |
| **Files**    | `app/extractor.py`, `schema_v76_complete.sql` |
| **Scope**    | Data extraction gap |

### Description

`accommodationType` (API field) is **not extracted** from the page and **no column exists** in any schema table to store it.

The JSON-LD block contains `"@type": "Hotel"` or `"LodgingBusiness"` on every Booking.com page. The extractor already parses JSON-LD (`_extract_json_ld()`) and even validates the `@type` field (line 502), but discards the value.

### Evidence

```python
# extractor.py — line 502
if item.get("@type") not in ("Hotel", "LodgingBusiness", "Accommodation"):
    continue
# The @type value is validated but never captured or returned
```

### Fix

1. Add column to `hotels` table in `schema_v77_complete.sql`:

```sql
accommodation_type  VARCHAR(64) NULL,
-- e.g. 'Hotel', 'Apartment', 'GuestHouse', 'Villa'
```

2. In `extractor.py` — `extract_all()`, add:

```python
"accommodation_type": self._extract_accommodation_type(),
```

3. Add method:

```python
def _extract_accommodation_type(self) -> Optional[str]:
    jsonld = self._get_jsonld()
    return jsonld.get("@type") or None
```

4. In `_upsert_hotel()` in `scraper_service.py`, add:

```python
"accommodation_type": data.get("accommodation_type"),
```

---

## GAP-SCHEMA-003 {#gap-schema-003}

| Field        | Value |
|---|---|
| **ID**       | GAP-SCHEMA-003 |
| **Severity** | 🟡 MEDIUM |
| **Files**    | `schema_v76_complete.sql`, `app/extractor.py` |
| **Scope**    | Type mismatch — nearbyPlaces.category |

### Description

`hotels_nearby_places.category` is defined as `VARCHAR(128)` in the schema (storing descriptive strings like `"airport"`, `"restaurant"`, `"beach"`). However, the `_API_.md` payload uses `category` as an **INTEGER** (`"category": 1`), representing an icon/type code.

Neither the schema type nor the extraction logic matches the API contract. The extractor (`_extract_nearby_places()`) captures the Booking.com icon category as a text string.

### Fix

**Option A** (minimal, recommended given DB-delete-on-start constraint): Keep `VARCHAR(128)` in DB, add a translation map in the payload builder:

```python
NEARBY_CATEGORY_MAP = {
    "airport": 1, "train_station": 2, "restaurant": 3,
    "beach": 4, "monument": 5, "shopping": 6,
    # ... extend as Booking.com categories are discovered
}
```

**Option B** (schema change): Change column to `SMALLINT` in `schema_v77_complete.sql` and update extractor to return integer codes directly.

---

## Summary Table {#summary-table}

| ID | Severity | File(s) | Root Cause | Impact on API |
|---|---|---|---|---|
| BUG-PERSIST-002 | 🔴 CRITICAL | `scraper_service.py` | 4 upsert calls missing from `_persist_hotel_data()` | 4 tables always empty: `extra_info`, `nearby_places`, `room_types`, `seo` |
| GAP-API-001 | 🔴 CRITICAL | `main.py` | No payload transformer for external API format | Entire `_API_.md` format unimplemented |
| GAP-SCHEMA-001 | 🟠 HIGH | `schema_v76_complete.sql`, `extractor.py` | Semantic mismatch: category scores ≠ individual reviews | `categoryScoreReview` malformed; `reviews[]` absent |
| BUG-MAIN-001 | 🟠 HIGH | `main.py` | Missing imports and response fields for v76 | All v76 fields invisible to API consumers |
| GAP-SCHEMA-002 | 🟡 MEDIUM | `schema_v76_complete.sql`, `extractor.py` | `hotels_room_types` missing `adults`/`children`/`images` | `rooms[]` incomplete in API payload |
| GAP-EXTRACT-001 | 🟡 MEDIUM | `extractor.py`, `schema_v76_complete.sql` | `accommodation_type` never extracted | `accommodationType` always null |
| GAP-SCHEMA-003 | 🟡 MEDIUM | `schema_v76_complete.sql`, `extractor.py` | `category` VARCHAR vs API INTEGER | `nearbyPlaces[].category` type mismatch |

---

## Fix Roadmap {#fix-roadmap}

### Phase 1 — Immediate (Build 77) — No schema changes needed

| Action | File | Effort |
|---|---|---|
| Add 4 missing upsert calls in `_persist_hotel_data()` | `scraper_service.py` | < 1h |
| Add v76 imports and response fields to `get_hotel()` | `main.py` | < 2h |

### Phase 2 — Schema Update (schema_v77_complete.sql)

| Action | Schema Change | Effort |
|---|---|---|
| Add `accommodation_type` column to `hotels` | `hotels.accommodation_type VARCHAR(64)` | < 1h |
| Add `adults`, `children`, `images`, `info` to `hotels_room_types` | 4 columns | < 1h |
| Create `hotels_individual_reviews` table | New table | < 2h |

### Phase 3 — New Feature (API Payload Builder)

| Action | File | Effort |
|---|---|---|
| Create `GET /hotels/{id}/api-payload` endpoint | `main.py` | 1–2 days |
| Implement field transformers for all `_API_.md` fields | New service | 1–2 days |
| Extract `accommodation_type` in extractor | `extractor.py` | < 1h |
| Extract individual guest reviews | `extractor.py` | 2–4h |
| Extract room `adults`/`children`/`images` | `extractor.py` | 2–4h |

---

## Document Information

| Property | Value |
|---|---|
| **Report** | BUG_REPORT_Build76_API_Gaps_EN.md |
| **Build** | 76 |
| **Schema** | schema_v76_complete.sql |
| **Date** | 2026-04-04 |
| **Status** | Final |

*End of Report*
