# SCRAPV25 — BookingScraper Pro
State-Aware Multilingual Scraping System (Strategy E)
---
**Repository:** https://github.com/corralejo-htls/scrapv25  
**Version:** v6.0.0 Build 116+  
**Core Concept:** Data Integrity First  
**Platform:** Windows 11 / Python + Celery + Memurai (Redis) + PostgreSQL + Selenium 
**Architecture Style:** Hybrid (Service + Script-based + Automation Layer)
**Readme:** https://raw.githubusercontent.com/corralejo-htls/scrapv25/main/documentations/readme.md
**Schema Source of Truth:** https://github.com/corralejo-htls/scrapv25/blob/main/schema_v77_complete.sql
**repository file listings:** https://github.com/corralejo-htls/scrapv25/blob/main/documentations/_path-file.csv
**File listings in Windows:** https://github.com/corralejo-htls/scrapv25/blob/main/pruebas/_arbol_.csv
**Python code (repository)** https://github.com/corralejo-htls/scrapv25/tree/main/app
**File tree (repository):**  https://raw.githubusercontent.com/corralejo-htls/scrapv25/main/documentations/_path-file.md
**Schema Source of Truth raw:** https://raw.githubusercontent.com/corralejo-htls/scrapv25/main/schema_v77_complete.sql
---

## Overview
SCRAPV25 (BookingScraper Pro) v6.0.0 Build 116+ is a distributed, state-aware multilingual scraping system for Booking.com hotel data. It operates on Windows 11 using Python, Selenium, PostgreSQL, Celery, and Memurai (Redis).

---

## 1. Python Core (`app/*.py`)

| File | Role |
|------|------|
| `scraper_service.py` | Strategy E engine. URL processing, language iteration (EN/ES/DE/IT), state management, and decision logic. |
| `extractor.py` | DOM parsing layer. Extracts hotel data from Booking.com HTML. Primary strategies: DOM-based (1, 1.5, 2), fallback Apollo JSON. |
| `scraper.py` | Selenium browser automation. ChromeDriver/Brave integration. Page navigation and raw HTML capture. |
| `main.py` | API server. Exposes `GET /hotels/{id}` serving denormalized data from `v_hotels_full`. |
| `models.py` | SQLAlchemy ORM. Maps 22 database tables. |
| `database.py` | PostgreSQL connection layer. Session management and pooling. |
| `config.py` | System configuration. Environment variables, constants, feature flags. |
| `language_config.py` | Multilingual setup. Language codes, labels, and mappings. |
| `celery_app.py` | Distributed task queue. Celery + Memurai/Redis configuration. |
| `tasks.py` | Celery background task definitions. |
| `completeness_service.py` | Strategy E validation. Checks 4/4 language completeness per URL. |
| `api_export_system.py` | Data export logic to external API. |
| `api_payload_builder.py` | Constructs API payload from database records per `_API_.md` specification. |
| `export_ui.py` | Export user interface for interactive selection and preview. |
| `image_downloader.py` | Image download pipeline. Async fetching of thumb/large/highres variants. |
| `image_classifier.py` | Image classification. Sets `gallery_visible`, `source`, `subcategory`, `gallery_order`. |
| `vpn_manager_windows.py` | Windows VPN integration. IP rotation and connection diagnostics. |
| `vpn_manager.py` | VPN abstraction layer. |
| `alembic_env.py` | Alembic database migration environment. |
| `__init__.py` | Package initialization. |

---

## 2. Database Schema (`schema_v77_complete.sql`)

The schema is the source of truth. The database is recreated from this file on every system startup.

### 2.1 Tables (22 total)

| Table | Purpose |
|-------|---------|
| `url_queue` | URL queue with status, priority, retry count, and Strategy-E language tracking. |
| `hotels` | Main hotel data per language. Includes `city_name`, `dest_ufi`, `atnm_en`, `dest_id`, `region_name`, `district_name`. |
| `hotels_description` | Long description text per language. |
| `hotels_policies` | Policies per hotel/language. One row per policy name. |
| `hotels_legal` | Legal info per language. Includes `has_legal_content` boolean. |
| `hotels_popular_services` | Popular services (editorial selection). Canonical source since Build 65. |
| `url_language_status` | Per-URL per-language scraping status tracking. |
| `scraping_logs` | Partitioned by month (RANGE 2025–2028). 5 indexes added in Build 117. FK enforced via trigger. |
| `image_downloads` | Image download tracking with status, local path, and file size. |
| `image_data` | Photo metadata: `id_photo`, dimensions, alt text, `gallery_visible`, `source`, `subcategory`, `gallery_order`. |
| `system_metrics` | System health snapshots: CPU, memory, active workers, pool status. |
| `hotels_fine_print` | Fine print HTML per language. Sanitized. |
| `hotels_all_services` | All services per hotel/language. Includes `service_category` column. |
| `hotels_faqs` | FAQs per language. `ask` and `answer` columns. |
| `hotels_guest_reviews` | Guest review category scores per language. |
| `hotels_property_highlights` | Property highlights with `highlight_category` and `highlight_detail` structure. |
| `hotels_extra_info` | "Good to know" / important info block per language. |
| `hotels_nearby_places` | Nearby places with `category_code` for API mapping. |
| `hotels_room_types` | Normalized room types. Includes `adults`, `children`, `images`, `info`. |
| `hotels_seo` | SEO meta tags: `seo_description` and `keywords` per language. |
| `hotels_individual_reviews` | Individual guest review texts: reviewer name, score, title, positive/negative comments. |

### 2.2 Views

| View | Purpose |
|------|---------|
| `v_hotels_full` | Denormalized hotel with all satellite data. JSONB aggregates for highlights, services, policies, reviews, nearby places, room types. |
| `v_scraping_summary` | Scraping completeness summary per URL: languages done, languages error, max attempts. |
| `v_api_export_images` | One row per gallery photo with best available URL (highres > large > thumb). Uses `DISTINCT ON` deduplication. |

### 2.3 Triggers & Functions

- `fn_set_updated_at()` — Auto-updates `updated_at` timestamp on row modification.
- `trg_scraping_logs_fk_check` — FK validation trigger for the partitioned `scraping_logs` table.

---

## 3. Data Extraction Files (`pruebas/*.csv`)

| File | Content |
|------|---------|
| `_arbol_.csv` | Windows file tree index of the repository. |
| `_Calidad__fichas_hotel_.csv` | Hotel data quality audit results. |
| `_Calidad__images1.csv` | Image quality audit batch 1. |
| `_Calidad__images2.csv` | Image quality audit batch 2. |

---

## 4. HTML Parsing Snapshots (`pruebas/*.html`)

Raw HTML snapshots captured during extraction for audit and selector verification.

| File | Hotel | Location |
|------|-------|----------|
| `HTML_1001_Villa-Dvor_Ohrid.html` | Villa Dvor | Ohrid, North Macedonia |
| `HTML_76033__Hotel-Topazz.html` | Hotel Topazz | Austria |
| `HTML_76224__Radisson-Hotel-Graz.html` | Radisson Hotel Graz | Austria |
| `HTML_76569__Hotel-Aquamarin.html` | Hotel Aquamarin | Austria |
| `HTML_76972__haus-mobene-garni.html` | Haus Mobene Garni | Austria |
| `HTML_77149__trofana-royal.html` | Trofana Royal | Austria |
| `HTML_77414__Arlberg.html` | Arlberg | Austria |
| `HTML_77736__bruecklwirt.html` | Bruecklwirt | Austria |
| `HTML_78465_wild-&-bolz-eMotel.html` | wild & bolz eMotel | Austria |

---

## 5. Image Evidence Files (`pruebas/*.png`)

Visual evidence captured during extraction.

---

## 6. Data Export Guide (`documentations/_API_.md`)

The `_API_.md` file defines the contract for exporting scraped hotel data to the external API.

### 6.1 Endpoint
```
PATCH https://web.com/api/en/543-clave-api/update/:hotel_id.json
Content-Type: application/json
```

### 6.2 Payload Structure

| Field | Type | Notes |
|-------|------|-------|
| `name` | Object | Multilingual. `en` must be listed first. |
| `rating` | Number | Overall numeric rating. |
| `address` | Object | Multilingual full address. |
| `geoPosition` | Object | `latitude`, `longitude`. |
| `services` | Array | Multilingual categorized services. |
| `conditions` | Array | Multilingual check-in/out policies. |
| `toConsider` | String | Multilingual fine print. Use `\n` for newlines. |
| `images` | Array | Array of image URLs (max1280x900). |
| `scoreReview` | Number | Overall review score (e.g., 9.2). |
| `scoreReviewBasedOn` | Null/Number | Review count basis. |
| `roomsQuantity` | Number | Number of room types. |
| `accommodationType` | String | Hotel, Apartment, Villa, etc. |
| `priceRange` | String/Null | Price range or null. |
| `extraInfo` | String/Null | Additional info. |
| `longDescription` | Object | Multilingual structured description. |
| `reviews` | Array | Multilingual individual reviews. |
| `categoryScoreReview` | Object | Multilingual category scores (Facilities, Cleanliness, Comfort, Value, Location, WiFi, Total). |
| `rooms` | Array | Multilingual room types with `adults`, `children`, `images`, `facilities`, `info`. |
| `nearbyPlaces` | Array | Multilingual nearby places with `category` code (1=airport, 2=restaurant, 3=beach, 4=transport, 5=nature, 6=attraction). |
| `guestValues` | Array | Multilingual Q&A values. |
| `seoDescription` | Object | Multilingual SEO meta description. |
| `keywords` | Object | Multilingual SEO keywords. |

### 6.3 Rules
- **English first**: In any multi-language payload, `en` translations must precede other languages.
- **All fields optional**: Omit any field that should not be updated.
- **Newlines**: Use `\n` (not HTML `<br>`) for line breaks in text fields.
- **Args**: `args.locales` is required; other `args` fields are optional.

---

## 7. Supporting Components

### 7.1 Windows Automation (`.bat`)
- **Server**: `start_server.bat`, `stop_server.bat`, `restart_all.bat`
- **Celery**: `start_celery.bat`, `start_celery_beat.bat`, `stop_celery.bat`
- **Database**: `backup_db.bat`, `create_db.bat`, `export_data.bat`
- **Maintenance**: `cleanup_logs.bat`, `limpiar_cache.bat`, `verify_system.bat`, `verify_memurai.bat`, `show_status.bat`, `diagnostico_vpn.bat`
- **Startup**: `iniciar.bat` (initializes system, recreates DB), `inicio_rapido.bat`

### 7.2 Utility Scripts (`scripts/*.py`)
- `retry_incomplete.py` — Partial retry for failed languages (Strategy E).
- `load_urls.py` — Loads URLs from CSV into `url_queue`.
- `export_data.py` — Executes data export.
- `verify_system.py` — System health checks.
- `create_tables.py` — Table creation helper.
- `gen_memurai_conf.py` — Memurai/Redis config generator.
- `create_project_structure.py` — Project scaffolding.

### 7.3 Test Suite (`tests/*.py`)
- `test_extractor.py`
- `test_models.py`
- `test_scraper.py`
- `test_strategy_e.py`
- `test_completeness.py`
- `test_config.py`

### 7.4 Root Configuration
- `config.ini` — Main application configuration.
- `env.example` — Environment variable template.
- `languages.json` — Language definitions and mappings.
- `requirements.txt` — Production dependencies.
- `requirements-optional.txt` — Optional dependencies.
- `alembic.ini` — Alembic configuration.
- `memurai.conf` — Memurai (Redis for Windows) configuration.
- `schema_v77_complete.sql` — Source of truth SQL schema.
- `windows_service.py` — Windows service wrapper.
- `install_chromedriver_helper.py` — ChromeDriver installation helper.

---

## 8. Architecture Summary

```
URL Queue (DB)
    ↓
app/scraper_service.py  (Strategy E)
    ↓
Language Processing Engine
    ↓
ChromeDriver (Selenium)
    ↓
Booking.com Extraction Layer (extractor.py)
    ↓
Database Storage (PostgreSQL)
    ↓
Strategy E Validation Layer
    ↓
Retry System (scripts/retry_incomplete.py)
    ↓
API Export (api_payload_builder.py → _API_.md contract)
```

---

*Generated from repository state as of Build 117+.*


---

## 9. HTML Tag Analysis for Data Extraction

This chapter documents the HTML tag patterns, selectors, and data sources identified in the `pruebas/*.html` snapshot files. The analysis is derived from the extraction logic in `app/extractor.py` and the schema comments in `schema_v77_complete.sql`.

### 9.1 Data Sources in Booking.com HTML

The HTML snapshots contain multiple embedded data layers:

| Layer | Format | Location in HTML | Usage |
|-------|--------|------------------|-------|
| JSON-LD | `application/ld+json` | `<script type="application/ld+json">` | Hotel name, address, geo, rating, review count, accommodation type, room types |
| booking.env | JavaScript object | `<script>` tag with `booking.env = {...}` | City name (`b_city_name`), UFI (`b_ufi`), accommodation type (`atnm_en`), destination ID (`context_dest_id`) |
| Apollo State | JSON | `window.__APOLLO_STATE__` | Fallback data for services, reviews, rooms |
| hotelPhotos | JSON | `hotelPhotos = {...}` | Image metadata, gallery order, photo dimensions |
| DOM Selectors | HTML elements | Various `data-testid` and class selectors | Primary extraction source for all visible content |

### 9.2 DOM Selectors by Data Category

#### 9.2.1 Hotel Core Data (`hotels` table)

| Field | Selector / Source | Tag Pattern |
|-------|-------------------|-------------|
| `hotel_name` | JSON-LD `name` | `<script type="application/ld+json">` |
| `address_city` | JSON-LD `address.addressRegion` or breadcrumb DOM | `<script type="application/ld+json">` / breadcrumb `<nav>` items |
| `city_name` | `booking.env` `b_city_name` or breadcrumb | `<script>` with `booking.env` / breadcrumb items[1] |
| `dest_ufi` | `booking.env` `b_ufi` | `<script>` with `booking.env` |
| `dest_id` | `booking.env` `context_dest_id` | `<script>` with `booking.env` |
| `region_name` | Breadcrumb items[3] (when non-generic) | `<nav>` / `<ol>` / `<li>` breadcrumb structure |
| `district_name` | Breadcrumb items[5] (when n==7 and non-generic) | `<nav>` / `<ol>` / `<li>` breadcrumb structure |
| `atnm_en` | `booking.env` `atnm_en` (no `b_` prefix) | `<script>` with `booking.env` |
| `latitude` | JSON-LD `geo.latitude` | `<script type="application/ld+json">` |
| `longitude` | JSON-LD `geo.longitude` | `<script type="application/ld+json">` |
| `star_rating` | JSON-LD `starRating` / 2 | `<script type="application/ld+json">` |
| `review_score` | JSON-LD `aggregateRating.ratingValue` | `<script type="application/ld+json">` |
| `review_count` | JSON-LD `aggregateRating.reviewCount` | `<script type="application/ld+json">` |
| `accommodation_type` | JSON-LD `@type` (e.g., Hotel, Apartment, Villa) | `<script type="application/ld+json">` |
| `price_range` | Availability section DOM | Room block pricing elements |
| `rooms_quantity` | JSON-LD `numberOfRooms` or count of room blocks | `<script type="application/ld+json">` / room-block count |
| `main_image_url` | JSON-LD `image` | `<script type="application/ld+json">` |
| `street_address` | JSON-LD `address.streetAddress` | `<script type="application/ld+json">` |
| `address_locality` | JSON-LD `address.addressLocality` | `<script type="application/ld+json">` |
| `address_country` | JSON-LD `address.addressCountry` | `<script type="application/ld+json">` |
| `postal_code` | JSON-LD `address.postalCode` | `<script type="application/ld+json">` |

#### 9.2.2 Description (`hotels_description`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `description` | Long description block | `<div>` with class containing `description` or `property-description` |

#### 9.2.3 Policies (`hotels_policies`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `policy_name` | `data-testid="property-section--policies"` | `<div data-testid="property-section--policies">` → `<h2>` or `<h3>` heading |
| `policy_details` | Same section → text content | `<div>` / `<p>` / `<span>` within the policies block |

#### 9.2.4 Legal Information (`hotels_legal`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `legal` | Legal block title | `<h2>` / `<h3>` with legal-related text (multilingual: "Información legal", "Legal information", etc.) |
| `legal_info` | Introductory text | `<p>` / `<div>` following the legal heading |
| `legal_details` | Extended details | `<p>` / `<div>` within the legal section |
| `has_legal_content` | Presence flag | Set to `TRUE` if the legal block is found with content; `FALSE` if the section is absent (common in BR/UY markets) |

#### 9.2.5 Popular Services (`hotels_popular_services`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `popular_service` | `property-most-popular-facilities-wrapper` | `<div>` / `<span>` with class `popular-facility` or similar within the "Most popular facilities" wrapper |

#### 9.2.6 Fine Print (`hotels_fine_print`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `fp` | Fine print block | `<div>` with `data-testid` or class matching `property-section--fine-print` or similar. HTML is sanitized: `<br>` preserved, SVG/img and attributes removed. |

#### 9.2.7 All Services (`hotels_all_services`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `service` | Facility group items | `<li>` / `<span>` within `facility-group` blocks. Each `<li>` contains one service text. |
| `service_category` | Facility group heading | `<h3>` / `<div>` heading of the `facility-group` block (e.g., "Internet", "Parking", "Pool") |

**Extraction Strategy (v4.5 / Build 103+):**
- Phase 1 ("Great for your stay") was **eliminated**.
- Only Phase 2 (facility-group DOM) is used.
- `_FACILITY_GROUP_MAP` and `_SERVICE_CATEGORY_RULES` removed.
- `service_category` is taken verbatim from the DOM heading.

#### 9.2.8 FAQs (`hotels_faqs`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `ask` | FAQ accordion question | `<div>` / `<button>` with `data-testid` matching FAQ question pattern |
| `answer` | FAQ accordion answer (v56+) | `<div>` / `<p>` revealed when accordion is expanded. May require interaction or pre-rendered DOM. |

#### 9.2.9 Guest Reviews (`hotels_guest_reviews`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `reviews_categories` | Review category name | `<span>` / `<div>` within review score block (e.g., "Limpieza", "Confort", "Ubicación") |
| `reviews_score` | Review category score | `<span>` / `<div>` with numeric score (e.g., "9.3", "8.8") |

#### 9.2.10 Property Highlights (`hotels_property_highlights`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `highlight_category` | Highlight group name | `<h3>` / `<div>` heading (e.g., "Ideal para tu estancia") |
| `highlight_detail` | Individual highlight item | `<li>` / `<span>` / `<div>` within the group (e.g., "Baño privado", "Parking") |

**Structure:** One row per `(category, detail)` pair per hotel/language.

#### 9.2.11 Extra Info (`hotels_extra_info`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `extra_info` | `data-testid="property-important-info"` | `<div data-testid="property-important-info">` — the "Good to know" / "Información importante" block, distinct from Fine Print. |

#### 9.2.12 Nearby Places (`hotels_nearby_places`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `place_name` | Location highlight name | `<span>` / `<div>` within `location-highlight` block |
| `distance` | Distance text | `<span>` with distance (e.g., "2.1 km", "500 m") |
| `category` | Icon category text | Derived from icon class or `data-testid` (e.g., "airport", "restaurant", "beach") |
| `category_code` | Mapped numeric code | `1=airport 2=restaurant 3=beach 4=transport 5=nature 6=attraction` (BUILD-82-FIX) |

#### 9.2.13 Room Types (`hotels_room_types`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `room_name` | Room block title | `<h3>` / `<div>` / `<span>` within room block |
| `description` | Room description | `<p>` / `<div>` within room block |
| `facilities` | Room facilities list | `<li>` / `<span>` within room block (stored as JSONB array) |
| `adults` | Max adults (SVG icon) | Extracted from occupancy icon SVG in availability table. `NULL` if table not loaded. |
| `children` | Max children (SVG icon) | Extracted from occupancy icon SVG in availability table. `NULL` if table not loaded. |
| `images` | Room image URLs | `<img>` `src` within room block (stored as JSONB array) |
| `info` | Additional room info | `<div>` / `<span>` with supplementary room information |

#### 9.2.14 SEO (`hotels_seo`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `seo_description` | Meta description | `<meta name="description" content="...">` or `<meta property="og:description" content="...">` |
| `keywords` | Meta keywords | `<meta name="keywords" content="...">` |

#### 9.2.15 Individual Reviews (`hotels_individual_reviews`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `reviewer_name` | Guest name | `<span>` / `<div>` within review item |
| `score` | Individual score (0-10) | `<span>` / `<div>` with numeric score |
| `title` | Review title | `<h4>` / `<span>` / `<div>` review headline |
| `positive_comment` | "Liked" text | `<div>` / `<p>` with positive comment |
| `negative_comment` | "Disliked" text | `<div>` / `<p>` with negative comment |
| `reviewer_country` | Guest country | `<span>` / `<div>` with country flag or text |
| `booking_id` | Internal Booking.com review ID | Extracted from DOM attribute or URL if available |

**Note:** As of Build 78, the extractor implementation for individual reviews is pending. The table exists in the schema for model/schema consistency, but the extraction function (`_extract_individual_reviews()`) and persister (`_upsert_hotel_individual_reviews()`) are not yet implemented. The data source would be the reviews modal (`/reviews/hotel/...`) or the "Read all reviews" modal.

#### 9.2.16 Image Data (`image_data` + `image_downloads`)

| Field | Selector | Tag Pattern |
|-------|----------|-------------|
| `id_photo` | `hotelPhotos` JS array | `<script>` with `hotelPhotos = [{"id_photo": "49312038", ...}]` |
| `orientation` | Calculated from width/height | `landscape` / `portrait` / `square` |
| `photo_width` | `hotelPhotos` JS | `hotelPhotos[i].photo_width` |
| `photo_height` | `hotelPhotos` JS | `hotelPhotos[i].photo_height` |
| `alt` | `hotelPhotos` JS or DOM `alt` | `hotelPhotos[i].alt` or `<img alt="...">` |
| `gallery_visible` | Gallery modal detection | `TRUE` if photo appears in the public gallery modal; `FALSE` if only in the JS super-set |
| `source` | Capture origin | `gallery_modal` \| `js_array` \| `dom_scan` \| `unknown` |
| `subcategory` | Photo classification | `gallery` \| `room` \| `facility` \| `exterior` \| `thumbnail` \| `review_photo` \| `unknown` |
| `gallery_order` | Modal display order | Integer position in gallery modal (`NULL` if not in gallery) |
| `url` (downloads) | `hotelPhotos` URL variants | `thumb_url` (max200), `large_url` (max1024x768), `highres_url` (max1280x900) |

### 9.3 HTML File Inventory (`pruebas/*.html`)

| File | Hotel ID | Hotel Name | Location | Size | Purpose |
|------|----------|------------|----------|------|---------|
| `HTML_1001_Villa-Dvor_Ohrid.html` | 1001 | Villa Dvor | Ohrid, North Macedonia | ~1.4 MB | Full-page snapshot for service extraction testing |
| `HTML_76033__Hotel-Topazz.html` | 76033 | Hotel Topazz | Austria | ~29 KB | Compact snapshot for policy/legal extraction testing |
| `HTML_76224__Radisson-Hotel-Graz.html` | 76224 | Radisson Hotel Graz | Austria | ~1.4 MB | Full-page snapshot for room type extraction |
| `HTML_76569__Hotel-Aquamarin.html` | 76569 | Hotel Aquamarin | Austria | ~28 KB | Compact snapshot for amenity extraction testing |
| `HTML_76972__haus-mobene-garni.html` | 76972 | Haus Mobene Garni | Austria | ~63 KB | Mid-size snapshot for service category testing |
| `HTML_77149__trofana-royal.html` | 77149 | Trofana Royal | Austria | ~1.4 MB | Full-page snapshot for highlight extraction |
| `HTML_77414__Arlberg.html` | 77414 | Arlberg | Austria | ~1.6 MB | Full-page snapshot for nearby places extraction |
| `HTML_77736__bruecklwirt.html` | 77736 | Bruecklwirt | Austria | ~1.4 MB | Full-page snapshot for review extraction |
| `HTML_78465_wild-&-bolz-eMotel.html` | 78465 | wild & bolz eMotel | Austria | ~1.2 MB | Full-page snapshot for image gallery extraction |

### 9.4 Recommended New Extraction Opportunities

Based on the HTML structure analysis, the following data points are present in the DOM but not yet fully extracted or utilized:

| Data Point | DOM Source | Target Table | Priority |
|------------|------------|--------------|----------|
| **Sustainability / Eco certifications** | `data-testid="property-section--sustainability"` or similar green badge blocks | New table or `hotels` column | Medium |
| **Accessibility features detailed** | Within `facility-group` under "Accessibility" heading | `hotels_all_services` (already captured) | Low (already in all_services) |
| **Property surroundings / neighborhood** | Beyond `location-highlight` — descriptive text blocks | `hotels_description` or new table | Low |
| **Cancellation policy details** | Within `property-section--policies` → specific cancellation subsection | `hotels_policies` (already captured) | Low |
| **Host / property manager info** | `data-testid="host-profile"` or similar | New table `hotels_host` | Low |
| **Check-in instructions** | Within `property-important-info` or policies | `hotels_extra_info` / `hotels_policies` | Low |
| **Property labels / badges** | "Genius", "Travel Sustainable", etc. badge DOM elements | New column in `hotels` | Medium |
| **Payment methods accepted** | `data-testid="payment-methods"` or similar | New table `hotels_payment_methods` | Low |
| **Breakfast details** | Within `facility-group` "Food & Drink" or separate breakfast block | `hotels_all_services` (already captured) | Low |
| **Spa & wellness details** | Within `facility-group` "Spa & Wellness" or separate block | `hotels_all_services` (already captured) | Low |

### 9.5 Extraction Strategy Notes

1. **Primary vs. Fallback**: The current system uses DOM selectors as primary (strategies 1, 1.5, 2) and Apollo JSON as fallback (strategy 3). Any new extraction should follow this hierarchy.
2. **Multilingual Consistency**: All selectors must work across EN, ES, DE, and IT. Text-based selectors (e.g., heading content) should use multilingual matching or structural position.
3. **Dynamic Content**: Some blocks (FAQ answers, review modal, availability table) require JavaScript execution or modal interaction. The HTML snapshots in `pruebas/` capture the post-execution DOM state.
4. **Sanitization**: HTML fragments stored in the database (`hotels_fine_print`, `hotels_property_highlights` historically) are sanitized: SVG and `<img>` removed, attributes stripped, `<br>` preserved.
5. **JSON-LD Reliability**: The `application/ld+json` script is the most stable source for core metadata (name, address, geo, rating). It should remain the primary source for these fields.
6. **booking.env Reliability**: The `booking.env` JavaScript object provides city metadata (`b_city_name`, `b_ufi`, `atnm_en`, `context_dest_id`) but requires regex parsing from inline `<script>` tags. Fallback to breadcrumb DOM if missing.

