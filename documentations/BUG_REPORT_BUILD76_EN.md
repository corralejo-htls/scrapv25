# Bug Report — BookingScraper Pro v6.0.0 (Build 76)
**Date:** 2026-04-04
**Origin:** Audit document `00_TABLA_RESUMEN_RAPIDA.md`
**Status:** RESOLVED — 6 STRUCTs implemented, 2 rejected

---

## Audit Proposals: Accept / Reject Decision Table

| Proposal | Decision | Reason |
|---|---|---|
| `priceRange` → `hotels` (ALTER) | ✅ IMPLEMENT | New column, genuinely absent |
| `roomsQuantity` → `hotels` (ALTER) | ✅ IMPLEMENT | New column, genuinely absent |
| `extraInfo` → `hotels_extra_info` (NEW) | ✅ IMPLEMENT | Different block from fine_print |
| `categoryScoreReview` → `hotels_category_scores` | ❌ REJECT | Exact duplicate of `hotels_guest_reviews` (same selector, same fields) |
| `rooms` → `hotels_room_types` (NEW TABLE) | ✅ IMPLEMENT | Normalizes existing JSONB column |
| `nearbyPlaces` → `hotels_nearby_places` (NEW) | ✅ IMPLEMENT | Genuinely absent |
| `guestValues` → `hotels_guest_qa` | ❌ REJECT | Exact duplicate of `hotels_faqs` (same selectors `faq-question`/`faq-answer`) |
| `seoDescription` + `keywords` → `hotels_seo` | ✅ IMPLEMENT | Genuinely absent |

---

## Rejected Proposals — Technical Justification

### ❌ `hotels_category_scores`
The audit proposes `data-testid="review-subscore"` as the extractor selector for a new `hotels_category_scores` table with fields `hotel_clean`, `hotel_comfort`, `hotel_location`, etc.

**Reality:** `hotels_guest_reviews` (STRUCT-016, v53) already extracts from `data-testid="review-subscore"` and persists `reviews_categories` + `reviews_score` — one row per category per hotel/language. Creating `hotels_category_scores` would be a verbatim duplicate with only a name change.

### ❌ `hotels_guest_qa`
The audit proposes `data-testid="faq-question"` / `data-testid="faq-answer"` as selectors for a new `hotels_guest_qa` table with fields `topic` and `topicComments`.

**Reality:** `hotels_faqs` (STRUCT-015, v53, BUG-FAQ-ANSWERS v56) already extracts from the same selectors and stores `ask` + `answer` per hotel/language. Functionally identical data.

---

## STRUCT-019 — `hotels.price_range` (ALTER)

**File:** `schema_v76_complete.sql`, `models.py`, `extractor.py`, `scraper_service.py`

New column `price_range VARCHAR(64) NULL` added to `hotels` table.

**⚠ Architectural limitation:** Booking.com only renders prices when the URL contains date parameters (`?checkin=YYYY-MM-DD&checkout=YYYY-MM-DD`). On static hotel pages scraped without dates, this field will be `NULL`. Value reflects the displayed price for the first available room, not a price range catalogue.

**Extraction strategies:**
1. `data-testid="price-and-discounted-price"` — React primary
2. `data-testid="availability-rate-information"` → first `<span>`
3. BUI class fallbacks (`bui-price-display__value`, `prco-valign-middle-helper`)

---

## STRUCT-020 — `hotels.rooms_quantity` (ALTER)

**File:** `schema_v76_complete.sql`, `models.py`, `extractor.py`, `scraper_service.py`

New column `rooms_quantity SMALLINT NULL` added to `hotels` table.

**⚠ Semantic note:** This field counts the number of **room type blocks** visible in the DOM (`data-testid="room-block"`), not the total physical room count of the hotel. When JSON-LD `numberOfRooms` is present it is preferred as it represents the actual room inventory.

**Extraction strategies (priority order):**
1. JSON-LD `numberOfRooms` (most accurate)
2. `len(soup.find_all(data-testid="room-block"))`
3. Last `<option>` value in `select[name="nr_rooms"]`

---

## STRUCT-021 — `hotels_extra_info` (NEW TABLE)

**File:** `schema_v76_complete.sql`, `models.py`, `extractor.py`, `scraper_service.py`

New table storing the "Good to know" / "Important information" block from Booking.com.

**Distinction from `hotels_fine_print`:** Fine Print is the "Fine Print" / "Letra pequeña" section (STRUCT-013). Extra info is `data-testid="property-important-info"` — a separate block that appears higher on the page with practical operational information.

**Schema:** `id UUID PK`, `hotel_id`, `url_id`, `language`, `extra_info TEXT`, 1 row per hotel/language. UNIQUE on `(url_id, language)`.

**Extraction strategies:**
1. `data-testid="property-important-info"`
2. `data-testid="house-rules"`
3. `id="hotelPoliciesInc"` (legacy)
4. `class~="hp--important_info"` (legacy)

---

## STRUCT-022 — `hotels_nearby_places` (NEW TABLE)

**File:** `schema_v76_complete.sql`, `models.py`, `extractor.py`, `scraper_service.py`

New table storing nearby points of interest as shown in Booking.com's location section.

**Schema:** `id BIGSERIAL PK`, `hotel_id`, `url_id`, `language`, `place_name VARCHAR(256)`, `distance VARCHAR(64)`, `category VARCHAR(128)`. UNIQUE on `(hotel_id, language, place_name)`. GIN index not needed (no full-text search on place names).

**DOM extraction:**
- Container: `data-testid="location-highlight"` (one per POI)
- Name: `<h3>` text
- Distance: `<span>` with `class~="distance"` or regex `\d+[.,]?\d*\s*(km|m|mi|min)`
- Category: `<svg data-testid="icon-*">` → strips `icon-` prefix

---

## STRUCT-023 — `hotels_room_types` (NEW NORMALIZED TABLE)

**File:** `schema_v76_complete.sql`, `models.py`, `scraper_service.py`

New normalized table complementing the existing `hotels.room_types JSONB` column.

**Why both?** The JSONB column enables fast full-document reads. The normalized table enables SQL queries (`WHERE room_name LIKE '%Suite%'`, `WHERE facilities @> '["WiFi"]'::jsonb`). GIN index on `facilities` JSONB column supports containment queries.

**Schema:** `id BIGSERIAL PK`, `hotel_id`, `url_id`, `language`, `room_name VARCHAR(256)`, `description TEXT`, `facilities JSONB`. UNIQUE on `(hotel_id, language, room_name)`.

**Data source:** `data.get("room_types")` — already extracted by `_extract_room_types()` (STRUCT-018, Build 75). No new extractor method needed; only a new persistence target.

---

## STRUCT-024 — `hotels_seo` (NEW TABLE)

**File:** `schema_v76_complete.sql`, `models.py`, `extractor.py`, `scraper_service.py`

New table storing SEO meta tags from the `<head>` of each Booking.com hotel page.

**Schema:** `id UUID PK`, `hotel_id`, `url_id`, `language`, `seo_description TEXT`, `keywords TEXT`. 1 row per hotel/language. UNIQUE on `(url_id, language)`. Row is skipped if both fields are empty.

**Extraction:**
- `seo_description`: `<meta name="description">` → fallback `<meta property="og:description">`
- `keywords`: `<meta name="keywords">` → fallback `<meta property="og:keywords">`

---

## Complete Change Matrix

| Component | STRUCT-019 | STRUCT-020 | STRUCT-021 | STRUCT-022 | STRUCT-023 | STRUCT-024 |
|---|---|---|---|---|---|---|
| `schema_v76_complete.sql` | ALTER hotels | ALTER hotels | NEW TABLE | NEW TABLE | NEW TABLE | NEW TABLE |
| `models.py` | Hotel field | Hotel field | HotelExtraInfo | HotelNearbyPlace | HotelRoomType | HotelSEO |
| `extractor.py` | `_extract_price_range()` | `_extract_rooms_quantity()` | `_extract_extra_info()` | `_extract_nearby_places()` | *(existing)* | `_extract_seo()` |
| `scraper_service.py` | `_upsert_hotel()` field | `_upsert_hotel()` field | `_upsert_hotel_extra_info()` | `_upsert_hotel_nearby_places()` | `_upsert_hotel_room_types()` | `_upsert_hotel_seo()` |

---

## Validation

| Check | Result |
|---|---|
| `ast.parse(extractor.py)` | PASS |
| `ast.parse(models.py)` | PASS |
| `ast.parse(scraper_service.py)` | PASS |
| `ast.parse(scraper.py)` | PASS |
| `price_range` in all 4 components | ✓ |
| `rooms_quantity` in all 4 components | ✓ |
| `hotels_extra_info` in all 4 components | ✓ |
| `hotels_nearby_places` in all 4 components | ✓ |
| `hotels_room_types` in schema + models + service | ✓ |
| `hotels_seo` in all 4 components | ✓ |
| `hotels_category_scores` absent in all files | ✓ REJECTED |
| `hotels_guest_qa` absent in all Python files | ✓ REJECTED |
| Total tables: 16 → 21 (schema_v76) | ✓ |
