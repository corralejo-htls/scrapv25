# TECHNICAL AUDIT REPORT - UPDATED (ENGLISH)
## BookingScraper Pro vs API Requirements
### Schema v77 - Updated Source of Truth

**Date:** 2026-04-06 09:58  
**System Version:** Build 76 (Patch 2026-04-04)  
**Schema Source of Truth:** `schema_v77_complete.sql` ⚠️ **UPDATED**  
**Reference URL:** https://www.booking.com/hotel/mk/villa-dvor.html  
**URL Queue ID:** `144bcbaf-1872-41e1-9f6e-e45bc0c672cf`

---

## 1. EXECUTIVE SUMMARY

### Overall Status: 🔴 CRITICAL - System Non-Operational

The system presents catastrophic failures preventing any data extraction. All URLs (14 URLs) failed across all 6 languages with a recurring database error.

### Critical Version Discrepancy Detected

| Element | Documented Version | Actual Version | Status |
|---------|-------------------|--------------|--------|
| SQL Schema | `schema_v76_complete.sql` | `schema_v77_complete.sql` | 🟠 **MISMATCH** |
| Documentation | Build 76 | Build 76 with v77 schema | 🟠 **INCONSISTENT** |
| Python Code | References v76 | v77 compatible? | ❓ **TO VERIFY** |

### Primary Error
```
psycopg.errors.UndefinedColumn: column hotels.accommodation_type does not exist
```

**Hypothesis:** Python code (Build 76) was updated to reference v77 fields, but the `schema_v77_complete.sql` file executed at startup **does not contain** the `accommodation_type` column, or there is a mismatch between the physical schema and ORM models.

---

## 2. API COMPLIANCE ANALYSIS vs EXTRACTED DATA

| API Field | Booking.com Source | DB Table (v77) | Status | Notes |
|-----------|-------------------|----------------|--------|-------|
| `name` (multilang) | `<h1>`, JSON-LD | `hotels.hotel_name` | 🔴 NOT EXTRACTING | Prior error |
| `rating` | JSON-LD `ratingValue` | `hotels.review_score` | 🔴 NOT EXTRACTING | Prior error |
| `address` (multilang) | JSON-LD `address.*` | `hotels.*_address` | 🔴 NOT EXTRACTING | Prior error |
| `geoPosition` | JSON-LD `geo.*` | `hotels.latitude/longitude` | 🔴 NOT EXTRACTING | Prior error |
| `services` (multilang) | `data-testid="property-most-popular-facilities-wrapper"` | `hotels_popular_services` | 🔴 NOT EXTRACTING | Prior error |
| `conditions` (multilang) | `data-testid="property-section--policies"` | `hotels_policies` | 🔴 NOT EXTRACTING | Prior error |
| `toConsider` (multilang) | `data-testid="fine-print-block"` | `hotels_fine_print` | 🔴 NOT EXTRACTING | Prior error |
| `images` | `data-testid="property-image"` | `image_data` | 🔴 NOT EXTRACTING | Not executed |
| `scoreReview` | JSON-LD `ratingValue` | `hotels.review_score` | 🔴 NOT EXTRACTING | Prior error |
| `scoreReviewBasedOn` | JSON-LD `reviewCount` | `hotels.review_count` | 🔴 NOT EXTRACTING | Prior error |
| `roomsQuantity` | JSON-LD `numberOfRooms` | `hotels.rooms_quantity` | 🔴 NOT EXTRACTING | Prior error |
| `accommodationType` | JSON-LD `@type` | `hotels.accommodation_type` | 🔴 **DOES NOT EXIST IN v77** | **BUG CONFIRMED** |
| `priceRange` | `data-testid="price-and-discounted-price"` | `hotels.price_range` | 🔴 NOT EXTRACTING | Prior error |
| `extraInfo` (multilang) | `data-testid="property-important-info"` | `hotels_extra_info` | 🔴 NOT EXTRACTING | Prior error |
| `longDescription` (multilang) | JSON-LD `description` | `hotels_description` | 🔴 NOT EXTRACTING | Prior error |
| `reviews` (multilang) | `data-testid="review-card"` | `hotels_individual_reviews` | 🔴 NOT EXTRACTING | Prior error |
| `categoryScoreReview` (multilang) | `data-testid="review-subscore"` | `hotels_guest_reviews` | 🔴 NOT EXTRACTING | Prior error |
| `rooms` (multilang) | `data-testid="room-block"` | `hotels_room_types` | 🔴 NOT EXTRACTING | Prior error |
| `nearbyPlaces` (multilang) | `data-testid="location-highlight"` | `hotels_nearby_places` | 🔴 NOT EXTRACTING | Prior error |
| `guestValues` (multilang) | `data-testid="faq-*"` | `hotels_faqs` | 🔴 NOT EXTRACTING | Prior error |
| `seoDescription` (multilang) | `<meta name="description">` | `hotels_seo` | 🔴 NOT EXTRACTING | Prior error |
| `keywords` (multilang) | `<meta name="keywords">` | `hotels_seo` | 🔴 NOT EXTRACTING | Prior error |

---

## 3. SCHEMA v77 vs MODELS ANALYSIS

### 3.1 Expected New Tables/Fields in v77

| Structure | Type | Description | DB Status |
|-----------|------|-------------|-----------|
| `hotels.accommodation_type` | `VARCHAR(64)` | Accommodation type (Hotel, Apartment, etc.) | 🔴 **DOES NOT EXIST** |
| `hotels.rooms_quantity` | `SMALLINT` | Number of rooms | ❓ Verify |
| `hotels.price_range` | `VARCHAR(64)` | Visible price range | ❓ Verify |
| `hotels_extra_info` | Table | "Good to know" / important info | ❓ Verify |
| `hotels_nearby_places` | Table | Nearby places with distance | ❓ Verify |
| `hotels_room_types` | Table | Normalized room types | ❓ Verify |
| `hotels_seo` | Table | Meta description and keywords | ❓ Verify |
| `hotels_individual_reviews` | Table | Individual reviews with comments | ❓ Verify |

### 3.2 Required Verification Query

```sql
-- Verify columns in hotels table
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'hotels' 
ORDER BY ordinal_position;

-- Verify existing tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'hotels_%'
ORDER BY table_name;
```

---

## 4. CRITICAL ERRORS IDENTIFIED (v77)

### BUG-SCHEMA-v77-001: Missing `accommodation_type` Column

**Severity:** 🔴 CRITICAL

**Description:** Despite `schema_v77_complete.sql` being the source of truth, the `accommodation_type` column does not exist in the `hotels` table created at startup.

**Possible Causes:**
1. The `schema_v77_complete.sql` file was not correctly updated
2. A different file is being executed
3. Cache from previous schema (v76) exists
4. Python code references fields not yet in SQL schema

**Required Validation:**
```bash
# Verify schema_v77_complete.sql content
grep -n "accommodation_type" schema_v77_complete.sql
```

### BUG-VERSION-001: Documentation vs Schema Mismatch

**Severity:** 🟠 HIGH

Official documentation (Guide_Documentation_BookingScraper_EN.md) references:
- Build 76 Patch 2026-04-04
- `schema_v76_complete.sql` as source of truth

**Observed reality:**
- Executed schema: `schema_v77_complete.sql`
- No confirmation of v77 vs v76 changes

---

## 5. HTML SELECTORS AND EXTRACTION

### 5.1 Primary Selectors (v77 Compatible)

| Field | Primary Selector | Fallback | Python Extraction |
|-------|------------------|----------|-------------------|
| `hotel_name` | JSON-LD `@graph.name` | `//h1` | `_extract_name()` |
| `accommodation_type` | JSON-LD `@type` | N/A | `_extract_accommodation_type()` |
| `review_score` | JSON-LD `aggregateRating.ratingValue` | `data-testid="review-score"` | `_extract_review_score()` |
| `review_count` | JSON-LD `aggregateRating.reviewCount` | N/A | `_extract_review_count()` |
| `latitude` | JSON-LD `geo.latitude` | N/A | `_extract_latitude()` |
| `longitude` | JSON-LD `geo.longitude` | N/A | `_extract_longitude()` |
| `address_city` | JSON-LD `address.addressRegion` | N/A | `_extract_city()` |
| `popular_services` | `data-testid="property-most-popular-facilities-wrapper"` | N/A | `_extract_popular_services()` |
| `all_services` | `data-testid="property-section--services"` | N/A | `_extract_all_services()` |
| `policies` | `data-testid="property-section--policies"` | N/A | `_extract_policies()` |
| `fine_print` | `data-testid="fine-print-block"` | N/A | `_extract_fine_print()` |
| `faqs` | `data-testid="faq-question"` / `data-testid="faq-answer"` | N/A | `_extract_faqs()` |
| `guest_reviews` | `data-testid="review-subscore"` | N/A | `_extract_guest_reviews()` |
| `individual_reviews` | `data-testid="review-card"` | N/A | `_extract_individual_reviews()` |
| `room_types` | `data-testid="room-block"` | `room-type-title`, `room-description`, `room-facilities` | `_extract_room_types()` |
| `price_range` | `data-testid="price-and-discounted-price"` | N/A | `_extract_price_range()` |
| `rooms_quantity` | JSON-LD `numberOfRooms` | count `room-block` | `_extract_rooms_quantity()` |
| `extra_info` | `data-testid="property-important-info"` | N/A | `_extract_extra_info()` |
| `nearby_places` | `data-testid="location-highlight"` | N/A | `_extract_nearby_places()` |
| `seo_description` | `<meta name="description">` | N/A | `_extract_seo()` |
| `keywords` | `<meta name="keywords">` | N/A | `_extract_seo()` |

### 5.2 Python Extraction Code (v77)

```python
# app/extractor.py - HotelExtractor v77
class HotelExtractor:
    def extract_all(self, html: str, language: str) -> dict:
        """Extracts 24 fields for API v77"""
        jsonld = self._get_jsonld(html)
        soup = BeautifulSoup(html, 'html.parser')

        return {
            # Core hotel data
            'hotel_name': self._extract_name(jsonld, soup),
            'accommodation_type': self._extract_accommodation_type(jsonld),  # v77
            'review_score': self._extract_review_score(jsonld),
            'review_count': self._extract_review_count(jsonld),
            'latitude': self._extract_latitude(jsonld),
            'longitude': self._extract_longitude(jsonld),
            'address_city': self._extract_city(jsonld),
            'street_address': self._extract_street(jsonld),
            'address_locality': self._extract_locality(jsonld),
            'address_country': self._extract_country(jsonld),
            'postal_code': self._extract_postal(jsonld),

            # Extended data (v77)
            'price_range': self._extract_price_range(soup),
            'rooms_quantity': self._extract_rooms_quantity(jsonld, soup),
            'room_types': self._extract_room_types(soup),  # v77 with adults/children/images/info

            # Services and policies
            'popular_services': self._extract_popular_services(soup),
            'all_services': self._extract_all_services(soup),
            'policies': self._extract_policies(soup),
            'fine_print': self._extract_fine_print(soup),
            'faqs': self._extract_faqs(soup),
            'extra_info': self._extract_extra_info(soup),  # v77

            # Reviews
            'guest_reviews': self._extract_guest_reviews(soup),  # Category scores
            'individual_reviews': self._extract_individual_reviews(soup),  # v77 - Text reviews

            # Location
            'nearby_places': self._extract_nearby_places(soup),  # v77

            # SEO
            'seo': self._extract_seo(soup),  # v77
        }
```

---

## 6. SQLALCHEMY MODELS vs SCHEMA v77

### 6.1 Hotel Model (v77 Expected)

```python
# app/models.py - Hotel class v77
class Hotel(Base):
    __tablename__ = 'hotels'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    url_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('url_queue.id'))
    url: Mapped[str] = mapped_column(String(2048))
    language: Mapped[str] = mapped_column(String(10))

    # Core fields
    hotel_name: Mapped[Optional[str]] = mapped_column(String(512))
    hotel_id_booking: Mapped[Optional[str]] = mapped_column(String(64))
    address_city: Mapped[Optional[str]] = mapped_column(Text)
    latitude: Mapped[Optional[float]] = mapped_column(DOUBLE_PRECISION)
    longitude: Mapped[Optional[float]] = mapped_column(DOUBLE_PRECISION)
    star_rating: Mapped[Optional[float]] = mapped_column(DOUBLE_PRECISION)
    review_score: Mapped[Optional[float]] = mapped_column(DOUBLE_PRECISION)
    review_count: Mapped[Optional[int]] = mapped_column(Integer)

    # v77 New fields
    price_range: Mapped[Optional[str]] = mapped_column(String(64))  # STRUCT-019
    rooms_quantity: Mapped[Optional[int]] = mapped_column(SMALLINT)  # STRUCT-020
    accommodation_type: Mapped[Optional[str]] = mapped_column(String(64))  # GAP-EXTRACT-001
    room_types: Mapped[Optional[dict]] = mapped_column(JSONB)

    # Address components
    street_address: Mapped[Optional[str]] = mapped_column(String(512))
    address_locality: Mapped[Optional[str]] = mapped_column(String(256))
    address_country: Mapped[Optional[str]] = mapped_column(String(128))
    postal_code: Mapped[Optional[str]] = mapped_column(String(20))

    # Metadata
    raw_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    scrape_engine: Mapped[str] = mapped_column(String(32), default='selenium')
    version_id: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), onupdate=func.now())
```

### 6.2 Required SQL Schema v77

```sql
-- schema_v77_complete.sql - hotels table
CREATE TABLE hotels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url_id UUID REFERENCES url_queue(id),
    url VARCHAR(2048) NOT NULL,
    language VARCHAR(10) NOT NULL,

    -- Core data
    hotel_name VARCHAR(512),
    hotel_id_booking VARCHAR(64),
    address_city TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    star_rating DOUBLE PRECISION,
    review_score DOUBLE PRECISION,
    review_count INTEGER,
    main_image_url VARCHAR(2048),
    short_description TEXT,
    rating_value DOUBLE PRECISION,
    best_rating DOUBLE PRECISION,

    -- Address components
    street_address VARCHAR(512),
    address_locality VARCHAR(256),
    address_country VARCHAR(128),
    postal_code VARCHAR(20),

    -- v77 Extended fields
    price_range VARCHAR(64),           -- STRUCT-019
    rooms_quantity SMALLINT,           -- STRUCT-020
    accommodation_type VARCHAR(64),    -- GAP-EXTRACT-001 (v77)
    room_types JSONB,

    -- Metadata
    raw_data JSONB,
    scrape_duration_s DOUBLE PRECISION,
    scrape_engine VARCHAR(32) DEFAULT 'selenium',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    version_id INTEGER DEFAULT 0,

    CONSTRAINT uq_hotel_url_language UNIQUE (url_id, language)
);

-- v77 New tables
CREATE TABLE hotels_extra_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url_id UUID REFERENCES url_queue(id),
    hotel_id UUID REFERENCES hotels(id),
    language VARCHAR(10) NOT NULL,
    extra_info_content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE hotels_nearby_places (
    id BIGSERIAL PRIMARY KEY,
    url_id UUID REFERENCES url_queue(id),
    hotel_id UUID REFERENCES hotels(id),
    language VARCHAR(10) NOT NULL,
    place_name VARCHAR(256),
    distance VARCHAR(64),
    category VARCHAR(128),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE hotels_room_types (
    id BIGSERIAL PRIMARY KEY,
    url_id UUID REFERENCES url_queue(id),
    hotel_id UUID REFERENCES hotels(id),
    language VARCHAR(10) NOT NULL,
    room_name VARCHAR(256),
    description TEXT,
    facilities JSONB,
    adults SMALLINT,        -- v77
    children SMALLINT,      -- v77
    images JSONB,           -- v77
    info TEXT,              -- v77
    UNIQUE(url_id, language, room_name)
);

CREATE TABLE hotels_seo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url_id UUID REFERENCES url_queue(id),
    hotel_id UUID REFERENCES hotels(id),
    language VARCHAR(10) NOT NULL,
    seo_description TEXT,
    keywords TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE hotels_individual_reviews (
    id BIGSERIAL PRIMARY KEY,
    url_id UUID REFERENCES url_queue(id),
    hotel_id UUID REFERENCES hotels(id),
    language VARCHAR(10) NOT NULL,
    reviewer_name VARCHAR(128),
    score NUMERIC(4,1),
    title TEXT,
    positive_comment TEXT,
    negative_comment TEXT,
    reviewer_country VARCHAR(128),
    booking_id VARCHAR(64),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 7. v77 TABLE STATUS (pruebas/*.csv)

| Table | Expected Rows (13 URLs × 6 lang) | Actual Rows | v77 Status |
|-------|---------------------------------|-------------|------------|
| `hotels` | 78 | 0 | 🔴 EMPTY - Column error |
| `hotels_description` | 78 | 0 | 🔴 EMPTY |
| `hotels_policies` | Variable | 0 | 🔴 EMPTY |
| `hotels_legal` | 78 | 0 | 🔴 EMPTY |
| `hotels_popular_services` | Variable | 0 | 🔴 EMPTY |
| `hotels_fine_print` | 78 | 0 | 🔴 EMPTY |
| `hotels_all_services` | Variable | 0 | 🔴 EMPTY |
| `hotels_faqs` | Variable | 0 | 🔴 EMPTY |
| `hotels_guest_reviews` | Variable | 0 | 🔴 EMPTY |
| `hotels_property_highlights` | Variable | 0 | 🔴 EMPTY |
| `hotels_extra_info` | 78 | 0 | 🔴 EMPTY - NEW v77 |
| `hotels_nearby_places` | Variable | 0 | 🔴 EMPTY - NEW v77 |
| `hotels_room_types` | Variable | 0 | 🔴 EMPTY - NEW v77 |
| `hotels_seo` | 78 | 0 | 🔴 EMPTY - NEW v77 |
| `hotels_individual_reviews` | Variable | 0 | 🔴 EMPTY - NEW v77 |
| `image_data` | Variable | 0 | 🔴 EMPTY |
| `image_downloads` | Variable | 0 | 🔴 EMPTY |
| `url_language_status` | 84 | 84 | 🟢 EXISTS (errors only) |
| `url_queue` | 14 | 14 | 🟢 EXISTS |

---

## 8. API vs EXTRACTION GAPS (v77)

### 8.1 API Fields with Direct v77 Mapping ✅

| API Field | v77 DB Structure | Compatibility |
|-----------|------------------|---------------|
| `name` | `hotels.hotel_name` | ✅ Direct |
| `rating` | `hotels.review_score` | ✅ Direct |
| `address` | `hotels.*_address` | ✅ Direct |
| `geoPosition` | `hotels.latitude/longitude` | ✅ Direct |
| `scoreReview` | `hotels.review_score` | ✅ Direct |
| `scoreReviewBasedOn` | `hotels.review_count` | ✅ Direct |
| `roomsQuantity` | `hotels.rooms_quantity` | ✅ Direct |
| `accommodationType` | `hotels.accommodation_type` | 🔴 **MISSING COLUMN** |
| `priceRange` | `hotels.price_range` | ✅ Direct |
| `longDescription` | `hotels_description.description` | ✅ Direct |
| `conditions` | `hotels_policies` + structure | ✅ Mappable |
| `toConsider` | `hotels_fine_print` | ✅ Direct |
| `guestValues` | `hotels_faqs` | ✅ Mappable |
| `categoryScoreReview` | `hotels_guest_reviews` | ✅ Mappable |
| `reviews` | `hotels_individual_reviews` | ✅ Compatible |
| `rooms` | `hotels_room_types` | ✅ Compatible (with adults/children/images) |
| `nearbyPlaces` | `hotels_nearby_places` | ⚠️ Requires numeric category mapping |
| `seoDescription` | `hotels_seo.seo_description` | ✅ Direct |
| `keywords` | `hotels_seo.keywords` | ✅ Direct |

### 8.2 Specific v77 Gaps

| API Field | Issue | Required Solution |
|-----------|-------|-------------------|
| `services` | API: categorized structure `{Internet: [...], Outdoors: [...]}` | Add `hotels_services_categorized` table or process in API layer |
| `nearbyPlaces.category` | API: `1` (numeric), DB: text | Category mapping or add `category_code` field |
| `images` | Only downloads on EN pass | Verify cross-language availability |

---

## 9. PRIORITY RECOMMENDATIONS v77

### Priority P0 (Blocking - System Down)

| # | Issue | Action | File |
|---|-------|--------|------|
| 1 | **Verify schema_v77_complete.sql** | Confirm it contains `accommodation_type` | `schema_v77_complete.sql` |
| 2 | **Compare v76 vs v77** | Identify real schema differences | Diff v76/v77 |
| 3 | **Synchronize models.py with v77** | Ensure ORM reflects physical schema | `app/models.py` |
| 4 | **Recreate DB** | Execute clean v77 schema at startup | PostgreSQL |
| 5 | **Validate persistence** | Run 1 test URL post-fix | System |

### Priority P1 (High - Functionality)

| # | Issue | Action |
|---|-------|--------|
| 6 | Validate `_upsert_hotel_individual_reviews()` | Confirm in `_persist_hotel_data()` |
| 7 | Validate `_upsert_hotel_room_types()` | Confirm adults/children/images/info |
| 8 | Validate `_upsert_hotel_seo()` | Confirm seo_description/keywords |
| 9 | Validate `_upsert_hotel_nearby_places()` | Confirm place_name/distance/category |
| 10 | Validate `_upsert_hotel_extra_info()` | Confirm extra_info_content |

### Priority P2 (Medium - API Optimization)

| # | Issue | Action |
|---|-------|--------|
| 11 | Design service category mapping | `services` structured vs flat |
| 12 | Normalize `nearbyPlaces.category` | Numeric vs text field |
| 13 | Validate `bookingId` extraction | Individual reviews |
| 14 | Update documentation | Guide_Documentation_Build_77.md |

---

## 10. CONCLUSION v77

### Current Status: 🔴 CRITICAL - Schema Mismatch

**BookingScraper Pro** is inoperable due to a **desynchronization between Python code (referencing v77 schema) and the executed SQL file**.

### Root Cause Identified

```
Python Code:    References accommodation_type (v77)
Executed Schema: ??? (possibly incomplete v76 or corrupt v77)
Result:         Column does not exist → Total failure
```

### Immediate Action Required

1. **Physically verify** `schema_v77_complete.sql` content
2. **Compare** with `schema_v76_complete.sql` (structural diff)
3. **Confirm** file on disk matches expected version
4. **Fix** if necessary (add missing column)
5. **Restart** application (DB auto-recreates at startup)

### Post-Recovery

Once restored, validate complete extraction of **22 API fields** mapped to **8 v77 tables** (existing + 5 new).

---

## 11. APPENDICES

### A. Complete API Payload Structure
See file `_API_.md` - Villa Dvor reference example.

### B. SQL Error Logs
See file `_Bug_Query-SQL.md` - Complete v77 error traces.

### C. v77 Persistence Sequence

```python
# _persist_hotel_data() v77 - Complete sequence
def _persist_hotel_data(self, session, url_id, language, data):
    self._upsert_hotel(session, url_id, language, data)  # 🔴 Fails here
    self._upsert_hotel_description(session, url_id, language, data)
    self._upsert_hotel_policies(session, url_id, language, data)
    self._upsert_hotel_legal(session, url_id, language, data)
    self._upsert_hotel_popular_services(session, url_id, language, data)
    self._upsert_hotel_fine_print(session, url_id, language, data)
    self._upsert_hotel_all_services(session, url_id, language, data)
    self._upsert_hotel_faqs(session, url_id, language, data)
    self._upsert_hotel_guest_reviews(session, url_id, language, data)
    self._upsert_hotel_property_highlights(session, url_id, language, data)
    self._upsert_hotel_extra_info(session, url_id, language, data)        # v77
    self._upsert_hotel_nearby_places(session, url_id, language, data)      # v77
    self._upsert_hotel_room_types(session, url_id, language, data)        # v77
    self._upsert_hotel_seo(session, url_id, language, data)                # v77
    self._upsert_hotel_individual_reviews(session, url_id, language, data) # v77
    session.commit()
```

### D. v77 Verification Checklist

- [ ] `schema_v77_complete.sql` exists and is readable
- [ ] Column `hotels.accommodation_type` defined in schema
- [ ] Table `hotels_extra_info` defined
- [ ] Table `hotels_nearby_places` defined
- [ ] Table `hotels_room_types` with adults/children/images/info columns
- [ ] Table `hotels_seo` defined
- [ ] Table `hotels_individual_reviews` defined
- [ ] `app/models.py` synchronized with schema
- [ ] `app/scraper_service.py` calls all _upsert_
- [ ] `app/extractor.py` extracts all v77 fields
- [ ] Successful test with 1 URL × 6 languages

---

*Report updated: 2026-04-06 09:58*
*Schema source of truth: schema_v77_complete.sql*
