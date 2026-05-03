# COMPREHENSIVE AUDIT REPORT: BookingScraper Pro + API Export
## Combined System Review — Build 95 / Schema v77
**Date:** 2026-05-02  
**Architecture:** Scraper (Windows 11) + API Export (Linux) — Separate Applications, Unified Workflow  
**Scope:** `app/*.py`, `schema_v77_complete.sql`, `documentations/*.md`, `pruebas/*.csv`, `_API_.md`

---

## 1. Executive Summary — Combined System Architecture

This report audits the **combined BookingScraper Pro system**, which consists of **two separate applications** working in sequence:

### Application 1: BookingScraper Pro (Windows 11)
| Component | Purpose | Platform |
|-----------|---------|----------|
| `scraper.py` | Scrapes Booking.com via Selenium (Brave/Chrome) + NordVPN rotation | Windows 11 |
| `extractor.py` | Parses HTML using BeautifulSoup + JSON-LD fallback | Windows 11 |
| `scraper_service.py` | Orchestrates batch scraping, language iteration, retry logic | Windows 11 |
| `database.py` | SQLAlchemy + PostgreSQL connection pooling | Windows 11 |
| `tasks.py` | Celery background tasks for scheduled scraping | Windows 11 |
| `config.py` | Pydantic Settings for all scraper configuration | Windows 11 |

**Output:** Populates 14+ PostgreSQL tables with hotel data, images stored in `BookingScraper/data/images/`.

### Application 2: API Export (Linux)
| Component | Purpose | Platform |
|-----------|---------|----------|
| `api_payload_builder.py` | Reads 14 DB tables, constructs `_API_.md` JSON payloads | Linux |
| `api_export_system.py` | Sends HTTP `PATCH` requests to external API endpoint | Linux |
| `models.py` | SQLAlchemy models for DB read access | Linux |

**Output:** Sends hotel data to external API endpoint (`https://web.com/api/en/.../update/:hotel_id.json`).

### Critical Constraint
> **Database is ALWAYS deleted at startup.** SQL file re-executed to generate fresh database. No migrations. No data preservation.

This means the scraper must complete its run before the API export can begin. There is no incremental scraping or data retention between runs.

---

## 2. Data Flow — End to End

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          WINDOWS 11 — SCRAPER APP                           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │   Booking    │───►│   Brave/     │───►│  extractor   │───►│ PostgreSQL│ │
│  │   .com       │    │   Selenium   │    │  (BS4/JSON)  │    │   DB      │ │
│  └──────────────┘    └──────────────┘    └──────────────┘    └────┬─────┘ │
│         ▲                    │                                     │       │
│         │                    │ NordVPN rotation                    │       │
│         │                    └─────────────────────────────────────┘       │
│         │                                                                  │
│         │                    Images saved to:                              │
│         │                    BookingScraper/data/images/                     │
│         │                                                                  │
└─────────┼──────────────────────────────────────────────────────────────────┘
          │
          │  Database dump / direct connection / file export
          │  (data transfer mechanism between Windows and Linux)
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            LINUX — API EXPORT APP                           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │  PostgreSQL  │───►│   ApiPayload │───►│   APIExporter│───►│ External  │ │
│  │     DB       │    │   Builder    │    │   (requests) │    │   API     │ │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────┘ │
│         ▲                                                                  │
│         │                    Reads image metadata from image_downloads      │
│         │                    (actual files may be on shared storage)        │
│         │                                                                  │
└─────────┼──────────────────────────────────────────────────────────────────┘
          │
          │  No Brave, No ChromeDriver, No NordVPN, No Selenium
          │  Pure Python + SQLAlchemy + requests
          ▼
```

---

## 3. Scraper Application Review (Windows 11)

### 3.1 Core Files

| File | Purpose | Status |
|------|---------|--------|
| `app/config.py` | Pydantic Settings — centralized config | ✅ Functional |
| `app/database.py` | SQLAlchemy engine, session management | ✅ Functional |
| `app/scraper.py` | Selenium engine (Brave/Chrome) | ⚠️ Selenium-only since Build 63 |
| `app/extractor.py` | HTML parsing via BeautifulSoup | ⚠️ Fragile selectors |
| `app/scraper_service.py` | Batch dispatch, language iteration | ✅ Functional |
| `app/tasks.py` | Celery background tasks | ✅ Functional |
| `app/models.py` | SQLAlchemy ORM models (17+ tables) | ✅ Complete |
| `schema_v77_complete.sql` | Database schema (single source of truth) | ✅ Current |

### 3.2 Extraction Reliability Assessment

| Data Category | Primary Selector | Fallback | Risk Level |
|---------------|------------------|----------|------------|
| Hotel name | `h2#hp_hotel_name` | `.hp__hotel-title h2`, JSON-LD | Medium |
| Address | `span[data-node_tt_id="property_address"]` | JSON-LD | Medium |
| Star rating | `span[data-testid="rating-stars"]` | Class parsing | High |
| Review score | `div[data-testid="review-score-component"]` | Legacy classes | Medium |
| Facilities | `div.important_facility` | Multiple legacy classes | **High** |
| Room types | `a.hprt-roomtype-link` | `div.hprt-roomtype-block` | **High** |
| Nearby places | `div.hp_location_block__section` | `div.hp-nearby-pois-list__item` | **High** |
| Reviews | `div.review_item_user_profile` | `span.bui-avatar-block__title` | Medium |

**Critical Finding:** The extractor relies heavily on legacy Booking.com CSS classes (`hprt-*`, `hp__*`, `bui-*`). Booking.com's modern DOM uses `data-testid` attributes which are more stable. The extractor lacks modern `data-testid` fallbacks for facilities and room types, leading to empty arrays in the API payload when legacy DOM is absent.

### 3.3 Database Schema (Schema v77)

**Core Tables:**
- `hotels` — Primary hotel metadata per language
- `url_queue` — URL tracking, status, language completion
- `image_downloads` — Image download tracking with `status` field
- `scraping_logs` — Partitioned logging table

**Satellite Tables (14 total):**
- `hotels_description`, `hotels_all_services`, `hotels_policies`
- `hotels_fine_print`, `hotels_legal`, `hotels_guest_reviews`
- `hotels_individual_reviews`, `hotels_room_types`, `hotels_nearby_places`
- `hotels_faqs`, `hotels_seo`, `hotels_extra_info`
- `hotels_popular_services`, `hotels_property_highlights`

**Key Constraints:**
- `hotels` has `UNIQUE(url_id, language)`
- All tables use `UUID` primary keys with `gen_random_uuid()`
- `hotels` references `url_queue(id)` via `url_id`
- Satellite tables reference `hotels(id)` via `hotel_id`

---

## 4. API Export Application Review (Linux)

### 4.1 What the API Export App Does

- ✅ Connects to PostgreSQL database (populated by Windows scraper)
- ✅ Reads 14 satellite tables via SQLAlchemy
- ✅ Transforms DB rows into `_API_.md` JSON payloads
- ✅ Filters fields and languages per `ExportTemplate`
- ✅ Validates payload completeness (structural checks)
- ✅ Sends `PATCH` requests via the `requests` library
- ✅ Exports to JSON files for inspection
- ✅ Reads image metadata from `image_downloads` table

### 4.2 What the API Export App Does NOT Do

- ❌ Scrape Booking.com
- ❌ Launch any browser (Brave, Chrome, etc.)
- ❌ Use NordVPN or any VPN
- ❌ Run Selenium or CloudScraper
- ❌ Download images (reads already-downloaded image metadata)
- ❌ Execute HTML parsing or CSS selector logic

### 4.3 API Export Process (7 Phases)

#### Phase 1: Export Selection (`ExportSelection`)
- `from_file(path)` — Loads UUIDs from JSON/text/CSV
- `from_db_all_pending(db)` — Selects URLs with `status='done'`
- **Gap:** Does not verify all `ENABLED_LANGUAGES` were scraped per URL

#### Phase 2: Template Resolution (`TemplateManager`)
- `default` — 15 fields, `en` only
- `full` — All 22 fields, all 6 languages
- `minimal` — 3 mandatory fields, `en` only

#### Phase 3: Payload Construction (`ApiPayloadBuilder`)
- Builds payload from 14 satellite tables
- **Bug:** `roomsQuantity` and `rating` emit `0` instead of `null` when DB value is `NULL`
- **Bug:** `toConsider` ignores `legal_details` when `legal_info` is present
- **Bug:** Unmapped review categories are silently dropped
- **Bug:** Address construction prioritizes `city_name` over `address_city`

#### Phase 4: Field Filtering (`_filter_payload()`)
- Filters multilingual fields to template languages
- **Gap:** Does not verify `en` data actually exists in DB

#### Phase 5: Validation (`_validate()`)
- Checks structural presence only
- **Gap:** No semantic validation (empty strings, invalid coordinates, missing images)

#### Phase 6: HTTP Transport (`_send()`)
- Sends `PATCH` to `{base_url}/en/{api_key}/update/{hotel_id}.json`
- **Issues:** No idempotency key, no connection pooling, no proxy/SSL config, no jitter

#### Phase 7: Batch Orchestration (`export_batch()`)
- Sequential processing, no checkpointing, no rate limiting

---

## 5. Data Completeness — DB vs. API Requirements

### 5.1 Field Mapping: Database → API Payload

| API Field | DB Table(s) | DB Column(s) | Builder Logic | Status |
|-----------|-------------|--------------|---------------|--------|
| `name.{lang}` | `hotels` | `hotel_name` | Direct per language | ✅ |
| `rating` | `hotels` | `star_rating` | `or 0` | ⚠️ Should be `null` |
| `address.{lang}` | `hotels` | Multiple address columns | `_build_address()` | ✅ |
| `geoPosition` | `hotels` | `latitude`, `longitude` | Direct | ✅ |
| `services.{lang}` | `hotels_all_services` | `service`, `service_category` | Grouped by category | ✅ |
| `conditions.{lang}` | `hotels_policies` | `policy_name`, `policy_details` | Array of objects | ✅ |
| `toConsider.{lang}` | `hotels_fine_print` + `hotels_legal` | `fp`, `legal_info`, `legal_details` | Concatenated | ⚠️ `legal_details` ignored if `legal_info` exists |
| `images` | `image_downloads` | `url` (status='done') | Prioritized by resolution | ⚠️ Empty if download failed |
| `scoreReview` | `hotels` | `review_score` | Direct | ✅ |
| `scoreReviewBasedOn` | `hotels` | `review_count` | Direct | ✅ |
| `roomsQuantity` | `hotels` | `rooms_quantity` | `or 0` | ⚠️ Should be `null` |
| `accommodationType` | `hotels` | `atnm_en` or `accommodation_type` | `or "Hotel"` | ✅ |
| `priceRange` | `hotels` | `price_range` | Direct | ✅ |
| `extraInfo` | `hotels_extra_info` | `extra_info` | Direct | ✅ |
| `longDescription.{lang}` | `hotels_description` | `description` | Direct | ✅ |
| `reviews.{lang}` | `hotels_individual_reviews` | Multiple columns | Structured array | ✅ |
| `categoryScoreReview.{lang}` | `hotels_guest_reviews` | `reviews_categories`, `reviews_score` | Mapped via key map | ⚠️ Unmapped categories dropped |
| `rooms.{lang}` | `hotels_room_types` | Multiple columns | Structured array | ⚠️ Often sparse |
| `nearbyPlaces.{lang}` | `hotels_nearby_places` | `place_name`, `distance`, `category_code` | Structured array | ⚠️ Often sparse |
| `guestValues.{lang}` | `hotels_faqs` | `ask`, `answer` | Structured array | ✅ |
| `seoDescription.{lang}` | `hotels_seo` | `seo_description` | Direct | ✅ |
| `keywords.{lang}` | `hotels_seo` | `keywords` | Direct | ✅ |

### 5.2 Data Quality Issues

1. **`bookingId` Null Rate:** Frequently `null` in `hotels_individual_reviews` — prevents deduplication
2. **`negative_comment` Literals:** Stores `"None"`, `"Nada"`, `"No"` instead of `null`
3. **`distance` Unit Inconsistency:** Raw text from Booking.com (`"0.1 miles"` vs `"0.3 kms"`)
4. **`facilities` Empty Arrays:** `hotels_room_types.facilities` often contains `[]`
5. **Image File Sync:** `image_downloads` says `done` but files may not exist in `data/images/`

---

## 6. Critical Bugs Summary

### Scraper (Windows 11)
| # | Bug | Location | Severity |
|---|-----|----------|----------|
| S1 | Legacy CSS selectors lack `data-testid` fallbacks | `extractor.py` | High |
| S2 | Room type extraction (`hprt-*` classes) may fail on modern Booking.com DOM | `extractor.py` | High |
| S3 | Nearby places extraction depends on lazy-loaded "Location" tab | `extractor.py` | High |
| S4 | Facilities extraction uses deprecated class names | `extractor.py` | High |

### API Export (Linux)
| # | Bug | Location | Severity |
|---|-----|----------|----------|
| A1 | `roomsQuantity` emits `0` for `NULL` values | `api_payload_builder.py` | Medium |
| A2 | `rating` emits `0` for unrated properties | `api_payload_builder.py` | Medium |
| A3 | `toConsider` ignores `legal_details` when `legal_info` exists | `api_payload_builder.py` | Medium |
| A4 | Unmapped review categories silently dropped | `api_payload_builder.py` | Medium |
| A5 | Address uses `city_name` (marketing label) over `address_city` (structured data) | `api_payload_builder.py` | Low |
| A6 | No idempotency key on API requests | `api_export_system.py` | Medium |
| A7 | No connection pooling (`requests` per hotel) | `api_export_system.py` | Low-Medium |
| A8 | `_validate()` only checks structure, not semantics | `api_export_system.py` | Medium |
| A9 | `from_db_all_pending()` ignores language completeness | `api_export_system.py` | Medium |
| A10 | No rate limiting or checkpointing in batch export | `api_export_system.py` | Low |

---

## 7. Recommendations

### For Scraper (Windows 11)
1. **Modernize selectors:** Add `data-testid` attributes as primary selectors, keep legacy classes as fallback
2. **Add room type `data-testid`:** `data-testid="room-type-card"`, `data-testid="room-type-title"`
3. **Add facilities `data-testid`:** `data-testid="facility-group"`, `data-testid="facility-item"`
4. **Handle lazy-loaded nearby places:** Trigger Selenium click on "Location" tab if section not present

### For API Export (Linux)
5. **Fix `roomsQuantity`/`rating` null semantics:** Emit `null` instead of `0` when DB value is `NULL`
6. **Fix `toConsider` concatenation:** Include both `legal_info` and `legal_details` when present
7. **Add fallback category:** `hotel_other` for unmapped review categories
8. **Prioritize `address_city`** over `city_name` in address construction
9. **Add idempotency key** to API requests
10. **Use `requests.Session()`** for connection pooling
11. **Add semantic validation:** Empty names, invalid coordinates, missing images
12. **Add language completeness check** before export
13. **Add proxy/SSL config** options to `APIConfig`

### For Combined System
14. **Data transfer mechanism:** Define how data moves from Windows scraper DB to Linux API export (DB dump, replication, or shared storage)
15. **Image file access:** Ensure Linux API export can access image files (shared storage or separate sync)
16. **Orchestration:** Coordinate scraper completion with API export start (Celery chain or scheduler)

---

## 8. Appendix — Complete Payload Example

```json
{
  "data": {
    "name": {
      "en": "Villa Dvor",
      "es": "Villa Cerro verde"
    },
    "rating": 0,
    "address": {
      "en": "Boro Sain 20, 6000 Ohrid, North Macedonia",
      "es": "Boro Sain 20, 6000 Ohrid, Macedonia del Norte"
    },
    "geoPosition": {
      "latitude": 41.113532,
      "longitude": 20.794691
    },
    "services": {
      "en": [{"Internet": ["WiFi is available..."]}, {"Outdoors": [...]}],
      "es": [{"Internet": ["WiFi disponible..."]}, {"Exteriores": [...]}]
    },
    "conditions": {
      "en": [{"condition": "Check-in", "detail": "From 3:00 PM..."}],
      "es": [{"condition": "Entrada", "detail": "Desde las 3:00 PM..."}]
    },
    "toConsider": {
      "en": "Guests are required to show a photo ID...",
      "es": "Los huéspedes deben mostrar un documento..."
    },
    "images": [
      "https://cf.bstatic.com/xdata/images/hotel/max1280x900/146556730.jpg"
    ],
    "scoreReview": 9.2,
    "scoreReviewBasedOn": null,
    "roomsQuantity": 0,
    "accommodationType": "Hotel",
    "priceRange": null,
    "extraInfo": null,
    "longDescription": {
      "en": "Essential Facilities: Villa Dvor in Ohrid offers...",
      "es": "Servicios esenciales: Villa Dvor en Ohrid ofrece..."
    },
    "reviews": {
      "en": [{"name": "Shelly", "score": 10, "title": "Amazing...", "comments": {"negative": "None", "positive": "The location..."}, "country": "United States", "bookingId": null}]
    },
    "categoryScoreReview": {
      "en": {
        "hotel_services": {"category": "Facilities", "score": 9.1},
        "hotel_clean": {"category": "Cleanliness", "score": 9.3},
        "hotel_comfort": {"category": "Comfort", "score": 9.2},
        "hotel_value": {"category": "Value for money", "score": 9.3},
        "hotel_location": {"category": "Location", "score": 9.4},
        "total": {"category": "Total", "score": 9.2},
        "hotel_wifi": {"category": "Free Wifi", "score": 9.3}
      }
    },
    "rooms": {
      "en": [{"name": "Double Room with Garden View", "adults": 2, "children": 1, "description": "...", "images": [...], "info": null, "facilities": []}]
    },
    "nearbyPlaces": {
      "en": [{"name": "St. Andrew's Church", "distance": "0.1 miles", "category": 1}]
    },
    "guestValues": {
      "en": [{"topic": "Hello. Do your rates include...", "topicComments": "Our rates include..."}]
    },
    "seoDescription": {
      "en": "Just a 9-minute walk from Church of St. John...",
      "es": "La Villa Dvor ofrece alojamiento con jardín..."
    },
    "keywords": {
      "en": "Villa Dvor, Ohrid, North Macedonia, Hotel, Hotels",
      "es": "Villa Cerro Verde, Ohrid, Macedonia del Norte, Hotel, Hoteles"
    }
  },
  "args": {
    "seoFormatKey": "",
    "onlyTitle": true,
    "regenerateSeo": true,
    "append": false,
    "cache": true,
    "locales": ["en", "es"]
  }
}
```
