# BookingScraper Pro — System Documentation
## Version 6.0.0 · Build 76 · Patch 2026-04-04

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Repository Structure](#2-repository-structure)
3. [Application Architecture](#3-application-architecture)
4. [Workflow Description](#4-workflow-description)
5. [Functions and Procedures](#5-functions-and-procedures)
6. [Database Structure](#6-database-structure)
7. [Configuration](#7-configuration)
8. [Build History & Bug Fixes](#8-build-history--bug-fixes)

---

## 1. System Overview

**BookingScraper Pro** is a Python-based web scraping system designed to extract structured hotel data from Booking.com across multiple languages. The system uses Selenium with Brave Browser as its sole scraping engine, NordVPN for IP rotation, Celery/Redis for task queuing, and PostgreSQL for persistence.

### Key Characteristics

| Attribute | Value |
|-----------|-------|
| **Application Name** | BookingScraper Pro |
| **Version** | 6.0.0 |
| **Build** | 76 (patch 2026-04-04) |
| **Platform** | Windows 11 (primary) |
| **Language** | Python 3.x |
| **Database** | PostgreSQL 14+ |
| **Task Queue** | Celery with Redis/Memurai |
| **Scraping Engine** | Selenium + Brave Browser (**sole engine** — CloudScraper eliminated Build 63) |
| **Schema Source of Truth** | `schema_v76_complete.sql` |
| **DB Strategy** | Always dropped and recreated at startup — no migrations ever |

### Core Capabilities

- **Multi-language Scraping**: 6 languages per hotel (en, es, de, fr, it, pt). English always first.
- **Strategy-E Partial Retry**: Tracks per-language completion independently — failed languages retry without repeating successful ones.
- **VPN Integration**: NordVPN rotation on time interval and consecutive failure threshold.
- **Image Download**: Hotel images downloaded on the English pass only (language-independent).
- **Structured Extraction**: JSON-LD primary source; DOM/BeautifulSoup fallbacks per field.
- **Comprehensive Logging**: Partitioned `scraping_logs` table (monthly partitions, 2025–2027).
- **Auto-Scheduling**: Celery Beat triggers scraping every 30 seconds.
- **Observability**: `system_metrics` snapshots, structured JSON logs, audit log endpoint.

### Scale Reference

| Dimension | Value |
|-----------|-------|
| URLs tracked | 13 |
| Languages per URL | 6 |
| Total hotel rows (full run) | 78 |
| Schema tables | 22 (v76 patch) |
| Scraping log partitions | 36 (2025–2027) |

---

## 2. Repository Structure

```
scrapv25/
├── app/                            # Core application package
│   ├── __init__.py                 # Version constants, package init
│   ├── celery_app.py               # Celery application factory
│   ├── completeness_service.py     # Data completeness verification
│   ├── config.py                   # Pydantic Settings — all configuration
│   ├── database.py                 # SQLAlchemy engine, pool, session manager
│   ├── extractor.py                # HotelExtractor — all DOM/JSON-LD extraction
│   ├── image_downloader.py         # Parallel hotel image download
│   ├── main.py                     # FastAPI app + REST endpoints
│   ├── models.py                   # SQLAlchemy ORM models (singular class names)
│   ├── scraper.py                  # SeleniumScraperEngine (sole engine)
│   ├── scraper_service.py          # ScraperService — orchestration, persistence
│   ├── tasks.py                    # Celery background tasks
│   ├── vpn_manager.py              # VPN interface (stub/Linux)
│   └── vpn_manager_windows.py      # NordVPN Windows implementation
├── documentations/                 # Bug reports, changelogs, guides
├── pruebas/                        # CSV table exports + HTML samples
│   ├── _table__*.csv               # Live database table snapshots
│   └── _HTML-view-source__*.md     # Raw Booking.com HTML for selector validation
├── scripts/                        # Utility scripts (load_urls, export, verify)
├── tests/                          # Unit and integration tests
├── schema_v76_complete.sql         # ⚠ SINGLE SOURCE OF TRUTH for all schema
├── env.example                     # Canonical config reference — all parameters
├── requirements.txt                # Python dependencies
├── requirements-optional.txt       # Optional dependencies
└── *.bat                           # Windows 11 operational scripts
```

### Key File Roles

| File | Role |
|------|------|
| `schema_v76_complete.sql` | **Single source of truth** — recreated on every startup |
| `env.example` | Canonical reference for all config parameters |
| `app/extractor.py` | All data extraction logic — `HotelExtractor.extract_all()` |
| `app/scraper_service.py` | `_persist_hotel_data()` — writes all tables |
| `app/models.py` | ORM definitions — must always mirror `schema_v76_complete.sql` |

---

## 3. Application Architecture

### 3.1 Module Overview

#### `config.py`
Centralized configuration via Pydantic `Settings`. Single instance (`get_settings()`). Sources: `.env` file + environment variables. Covers database, scraper, VPN, language, browser, logging, and debug parameters. `env.example` is the canonical reference — all new parameters must be documented there first.

#### `database.py`
SQLAlchemy engine with connection pooling. Key components:
- `get_db()`: context manager, auto-commits and closes session
- `get_serializable_db()`: SERIALIZABLE isolation for DDL
- `get_pool_status()`: pool health metrics
- Pool size: `DB_POOL_SIZE` (default 10) + `DB_MAX_OVERFLOW` (default 5)

**Windows 11 constraint**: `max_connections ≤ 100` (Desktop Heap limitation). Antivirus must exclude the PostgreSQL data directory.

#### `models.py`
SQLAlchemy ORM models using `DeclarativeBase` + `Mapped[]` typed columns. **Class naming convention: singular** (`Hotel`, not `Hotels`). All class names must match the table definitions in `schema_v76_complete.sql`. Compatibility aliases defined at the bottom of the file for import names that differ from class names (`ScrapingLogs = ScrapingLog`, `HotelPolicies = HotelPolicy`).

**Current models (Build 76 patch):**

| ORM Class | Table | Notes |
|-----------|-------|-------|
| `URLQueue` | `url_queue` | Strategy-E fields |
| `Hotel` | `hotels` | Core data + price_range + rooms_quantity + **accommodation_type** |
| `HotelDescription` | `hotels_description` | Long description |
| `HotelPolicy` | `hotels_policies` | Check-in/out, pets, etc. |
| `HotelLegal` | `hotels_legal` | `has_legal_content` flag |
| `HotelPopularService` | `hotels_popular_services` | Curated services subset |
| `URLLanguageStatus` | `url_language_status` | Per-language scraping state |
| `ScrapingLog` | `scraping_logs` | Partitioned by month |
| `ImageDownload` | `image_downloads` | Download tracking |
| `ImageData` | `image_data` | Photo metadata |
| `SystemMetric` | `system_metrics` | Health snapshots |
| `HotelFinePrint` | `hotels_fine_print` | Fine print HTML |
| `HotelAllService` | `hotels_all_services` | All services flat list |
| `HotelFAQ` | `hotels_faqs` | FAQ question + answer |
| `HotelGuestReview` | `hotels_guest_reviews` | Category scores (Cleanliness: 9.3) |
| `HotelPropertyHighlight` | `hotels_property_highlights` | Highlight category + detail |
| `HotelExtraInfo` | `hotels_extra_info` | "Good to know" block |
| `HotelNearbyPlace` | `hotels_nearby_places` | POI name + distance + category |
| `HotelRoomType` | `hotels_room_types` | Normalized room types + **adults/children/images/info** |
| `HotelSEO` | `hotels_seo` | Meta description + keywords |
| `HotelIndividualReview` | `hotels_individual_reviews` | **NEW** — individual guest reviews with positive/negative text |

#### `scraper.py`
`SeleniumScraperEngine` is the **sole scraping engine**. `CloudScraperEngine` was eliminated in Build 63 after confirmed 0% success rate. Key behaviors:
- Brave browser via Selenium WebDriver
- `set_page_load_timeout()` configured before every `driver.get()`
- CDP header injection (`_set_language_headers()`) for language isolation
- `delete_all_cookies()` before each language page load (BUG-LANG-002 fix)
- `SHORT_HTML_THRESHOLD` (default 5000 chars) — immediate abort if challenge page detected

#### `extractor.py`
`HotelExtractor` — receives raw HTML + language code. Single public method: `extract_all()` returns a `dict` with all fields. JSON-LD parsed once via `_get_jsonld()` and reused across all sub-methods.

**Current extraction methods (Build 76 patch):**

| Method | Output Key | Destination Table |
|--------|-----------|-------------------|
| `_extract_name()` | `hotel_name` | `hotels` |
| `_extract_description()` | `description` | `hotels_description` |
| `_extract_review_score()` | `review_score` | `hotels` |
| `_extract_review_count()` | `review_count` | `hotels` |
| `_extract_star_rating()` | `star_rating` | `hotels` |
| `_extract_city()` | `address_city` | `hotels` |
| `_extract_latitude/longitude()` | `latitude`, `longitude` | `hotels` |
| `_extract_popular_services()` | `popular_services` | `hotels_popular_services` |
| `_extract_policies()` | `policies` | `hotels_policies` |
| `_extract_legal()` | `legal` | `hotels_legal` |
| `_extract_hotel_id()` | `hotel_id_booking` | `hotels` |
| `_extract_fine_print()` | `fine_print` | `hotels_fine_print` |
| `_extract_all_services()` | `all_services` | `hotels_all_services` |
| `_extract_faqs()` | `faqs` | `hotels_faqs` |
| `_extract_guest_reviews()` | `guest_reviews` | `hotels_guest_reviews` |
| `_extract_property_highlights()` | `property_highlights` | `hotels_property_highlights` |
| `_extract_room_types()` | `room_types` | `hotels.room_types` (JSONB) + `hotels_room_types` |
| `_extract_price_range()` | `price_range` | `hotels.price_range` |
| `_extract_rooms_quantity()` | `rooms_quantity` | `hotels.rooms_quantity` |
| `_extract_extra_info()` | `extra_info` | `hotels_extra_info` |
| `_extract_nearby_places()` | `nearby_places` | `hotels_nearby_places` |
| `_extract_seo()` | `seo` | `hotels_seo` |
| `_extract_accommodation_type()` | `accommodation_type` | `hotels.accommodation_type` |
| `_extract_individual_reviews()` | `individual_reviews` | `hotels_individual_reviews` |

`extract_hotel_photos()` is called separately — English pass only.  
Alias: `BookingExtractor = HotelExtractor` (compatibility).

#### `scraper_service.py`
`ScraperService` — top-level orchestrator. Key flow: `dispatch_batch()` → `_process_single_url()` → `_process_language()` → `_persist_hotel_data()`.

`_persist_hotel_data()` calls **all** upsert methods in order. **Current call sequence (Build 76 patch — BUG-PERSIST-002 fixed):**

```python
_upsert_hotel()
_upsert_hotel_description()
_upsert_hotel_policies()
_upsert_hotel_legal()
_upsert_hotel_popular_services()
_upsert_hotel_fine_print()
_upsert_hotel_all_services()
_upsert_hotel_faqs()
_upsert_hotel_guest_reviews()
_upsert_hotel_property_highlights()
_upsert_hotel_extra_info()          # STRUCT-021 — was missing until patch
_upsert_hotel_nearby_places()       # STRUCT-022 — was missing until patch
_upsert_hotel_room_types()          # STRUCT-023 — was missing until patch
_upsert_hotel_seo()                 # STRUCT-024 — was missing until patch
_upsert_hotel_individual_reviews()  # STRUCT-025 — new in patch
session.commit()
```

VPN rotation: `vpn_manager_windows.py` — rotates on time interval (`VPN_ROTATION_INTERVAL`) and on consecutive language failures (`MAX_CONSECUTIVE_LANG_FAILURES`). Forces browser reset after rotation.

#### `image_downloader.py`
`ImageDownloader` — downloads hotel images in parallel (ThreadPoolExecutor, max 3 workers). Called after the English-language scrape only. Persists to `image_data` and `image_downloads`. Images stored at `data/images/{hotel_id}/`.

#### `tasks.py`
Celery background tasks (broker: Redis/Memurai):

| Task | Schedule | Description |
|------|----------|-------------|
| `scrape_pending_urls` | Every 30s | Main scraping dispatch |
| `ensure_log_partitions` | Daily 02:00 | Creates next month's partition |
| `purge_old_debug_html` | Daily 03:00 | Removes stale HTML debug files |
| `collect_system_metrics` | Every 5min | Snapshots pool + queue stats |
| `reset_stale_processing_urls` | Every 10min | Resets URLs stuck in `processing` >60min |

#### `main.py`
FastAPI REST API. Key endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | System health check |
| `GET` | `/hotel/{id}` | Full hotel data (all v76 fields) |
| `GET` | `/hotels` | List hotels with filters |
| `POST` | `/urls/load` | Load URLs into queue |
| `POST` | `/scrape/force` | Trigger immediate scrape |
| `GET` | `/logs/audit` | Download audit log (CSV/JSON) |
| `GET` | `/status` | Queue and scraper status |
| `GET` | `/metrics` | System metrics |

`GET /hotel/{id}` response includes all v76 fields: `accommodation_type`, `price_range`, `rooms_quantity`, `extra_info`, `nearby_places`, `room_types`, `seo`, `individual_reviews` (BUG-MAIN-001 fixed in patch).

---

## 4. Workflow Description

### 4.1 Phase 1: Startup & Initialization

1. **Database Recreation**
   - `schema_v76_complete.sql` executed — drops and recreates entire DB
   - All 22 tables + views + triggers created fresh
   - No migration logic exists or is needed

2. **Configuration Loading**
   - `config.py` loads `.env` file via Pydantic Settings
   - Validates required parameters (`DB_USER`, `DB_PASSWORD`)
   - Creates `logs/`, `data/`, `backups/` directories

3. **Service Startup**
   - FastAPI + Uvicorn starts on configured port
   - Celery workers attach to Redis/Memurai broker
   - Celery Beat scheduler activates periodic tasks

### 4.2 Phase 2: URL Loading

URLs loaded via `POST /urls/load` or `scripts/load_urls.py` from `urls_cargas_.csv`:

```
Column 0: external_ref (numeric ID)
Column 1: base_url     (Booking.com hotel URL)
Column 2: external_url (optional alternate URL)
```

Each URL inserted into `url_queue` with `status='pending'`, `priority=5`.

### 4.3 Phase 3: Batch Dispatch (Strategy-E)

1. `scrape_pending_urls` Celery task fires every 30 seconds
2. `ScraperService.dispatch_batch()` selects `pending` URLs ordered by priority
3. Per URL: iterates 6 languages → English always first
4. `url_language_status` tracks per-language state independently
5. On partial failure: URL set to `incomplete`, failed languages tracked in `languages_failed`
6. Retry runs only the failed languages (Strategy-E partial retry)

### 4.4 Phase 4: Web Scraping (Selenium only)

**Engine: `SeleniumScraperEngine`** (Brave browser)

```
For each URL + language:
  1. delete_all_cookies()                  # Language isolation (BUG-LANG-002)
  2. set_page_load_timeout()               # SELENIUM_CONTENT_WAIT_TIMEOUT_S
  3. _set_language_headers() via CDP       # Inject Accept-Language header
  4. driver.get(language_url)
  5. Check HTML length < SHORT_HTML_THRESHOLD → abort (challenge page)
  6. Wait for content via WebDriverWait    # Reduced timeout: SELENIUM_CONTENT_WAIT_TIMEOUT_S
  7. LANG_SCRAPE_DELAY / LANG_SCRAPE_DELAY_IT (Italian: extra 5s)
  8. Extract via HotelExtractor.extract_all()
  9. _persist_hotel_data()
```

**VPN Rotation triggers:**
- Time elapsed > `VPN_ROTATION_INTERVAL` seconds
- Consecutive language failures ≥ `MAX_CONSECUTIVE_LANG_FAILURES`
- Forces `reset_browser()` after rotation

**Image download** (English pass only):
- `extract_hotel_photos()` → `ImageDownloader.download_photo_batch()`
- Parallel download: 3 workers max

### 4.5 Phase 5: Data Extraction

`HotelExtractor.extract_all()` returns a single `dict` with all 24 output keys. JSON-LD block parsed once and shared across all sub-methods. Extraction strategy per field: JSON-LD primary → DOM testid selectors → class/id fallbacks → regex last resort.

**Fields extracted and their primary selectors:**

| Field | Primary Source |
|-------|---------------|
| `hotel_name` | JSON-LD `@graph.name` / `//h1` |
| `review_score` | JSON-LD `aggregateRating.ratingValue` |
| `latitude/longitude` | JSON-LD `geo.latitude/longitude` |
| `address_*` | JSON-LD `address.*` |
| `accommodation_type` | JSON-LD `@type` |
| `popular_services` | `data-testid="property-most-popular-facilities-wrapper"` |
| `policies` | `data-testid="property-section--policies"` |
| `fine_print` | `data-testid="fine-print-block"` |
| `all_services` | `data-testid="property-section--services"` |
| `faqs` | `data-testid="faq-question"` / `data-testid="faq-answer"` |
| `guest_reviews` (category scores) | `data-testid="review-subscore"` |
| `individual_reviews` | `data-testid="review-card"` |
| `room_types` | `data-testid="room-block"` → `room-type-title`, `room-description`, `room-facilities` |
| `price_range` | `data-testid="price-and-discounted-price"` |
| `rooms_quantity` | JSON-LD `numberOfRooms` / count of `room-block` |
| `extra_info` | `data-testid="property-important-info"` |
| `nearby_places` | `data-testid="location-highlight"` |
| `seo_description` | `<meta name="description">` |
| `keywords` | `<meta name="keywords">` |

### 4.6 Phase 6: Persistence

`_persist_hotel_data()` calls 15 upsert methods in sequence, then `session.commit()`. All operations are idempotent (insert-or-update). No row is ever hard-deleted during a scraping cycle.

Image downloads persist to `image_data` (metadata) and `image_downloads` (status tracking).

### 4.7 Phase 7: Status Update

After all languages for a URL are processed:
- `url_queue.status`: `done` (all success) / `error` (all failed) / `incomplete` (partial)
- `url_queue.languages_completed`: comma-separated successful codes
- `url_queue.languages_failed`: comma-separated failed codes
- `url_language_status`: one row per URL+language with `attempts` counter
- `scraping_logs`: one row per scraping event (success or failure)

### 4.8 Phase 8: Error Handling

| Layer | Mechanism |
|-------|-----------|
| Challenge page detection | `len(html) < SHORT_HTML_THRESHOLD` → immediate None return |
| Language retry | `MAX_LANG_RETRIES` (default 3) per language per URL |
| URL retry | `MAX_RETRIES` (default 3) per URL overall |
| Stale recovery | Celery task resets URLs stuck in `processing` >60min |
| VPN failure | Rotation on consecutive failures; browser reset after VPN switch |
| Persistence error | Logged to `scraping_logs`; URL marked `error`; exception not propagated |

---

## 5. Functions and Procedures

### 5.1 Core Functions by Module

#### `config.py`

| Function | Description |
|----------|-------------|
| `get_settings()` | Returns Settings singleton |
| `reset_settings()` | Forces re-instantiation (test use) |

#### `database.py`

| Function | Description |
|----------|-------------|
| `get_db()` | Context manager — session with auto-commit/close |
| `get_serializable_db()` | SERIALIZABLE isolation for DDL |
| `get_pool_status()` | Pool health dict (size, checked-in, overflow) |
| `init_db()` | Creates all tables via ORM metadata |

#### `scraper.py`

| Function | Description |
|----------|-------------|
| `SeleniumScraperEngine.fetch()` | Main fetch — returns HTML string or None |
| `SeleniumScraperEngine._fetch_with_selenium()` | Brave browser fetch with CDP headers |
| `SeleniumScraperEngine.reset_browser()` | Destroys and recreates WebDriver instance |
| `SeleniumScraperEngine._set_language_headers()` | CDP network header injection |
| `BaseScraper._save_debug_html()` | Saves HTML to disk (DEBUG_HTML_SAVE) |

#### `extractor.py`

| Function | Description |
|----------|-------------|
| `HotelExtractor.extract_all()` | Returns full data dict (24 keys) |
| `HotelExtractor.extract_hotel_photos()` | Photo metadata extraction (EN only) |
| `HotelExtractor._get_jsonld()` | Parses and caches JSON-LD block |
| `HotelExtractor._extract_accommodation_type()` | JSON-LD `@type` extraction |
| `HotelExtractor._extract_individual_reviews()` | Individual guest reviews |
| `HotelExtractor._extract_room_types()` | Room blocks with name/description/facilities |
| `HotelExtractor._extract_nearby_places()` | POI list with distance/category |
| `HotelExtractor._extract_seo()` | `<meta>` description and keywords |
| `HotelExtractor._extract_extra_info()` | "Good to know" block |
| `HotelExtractor._extract_guest_reviews()` | Category score rows |
| `extract_hotel_photos_from_html()` | Module-level photo extractor |

#### `scraper_service.py`

| Function | Description |
|----------|-------------|
| `ScraperService.dispatch_batch()` | Fetches pending URLs, runs language loop |
| `ScraperService._process_single_url()` | Full URL processing + image download |
| `ScraperService._process_language()` | Single language fetch + persist |
| `ScraperService._persist_hotel_data()` | Calls all 15 upsert methods |
| `ScraperService._upsert_hotel()` | Core hotel row insert/update |
| `ScraperService._upsert_hotel_individual_reviews()` | Individual review rows |
| `ScraperService._upsert_hotel_room_types()` | Normalized room rows (with adults/children/images) |
| `ScraperService._upsert_hotel_seo()` | SEO meta row |
| `ScraperService._upsert_hotel_extra_info()` | Extra info row |
| `ScraperService._upsert_hotel_nearby_places()` | POI rows |
| `ScraperService._upsert_lang_status()` | URL language status update |
| `ScraperService._log_scraping_event()` | Writes to scraping_logs |

#### `image_downloader.py`

| Function | Description |
|----------|-------------|
| `ImageDownloader.download_photo_batch()` | Downloads list of photo dicts |
| `ImageDownloader._download_one()` | Single image download + file write |
| `ImageDownloader._upsert_image_data()` | Persists photo metadata |

#### `tasks.py`

| Task | Schedule | Description |
|------|----------|-------------|
| `scrape_pending_urls` | 30s | Main dispatch |
| `ensure_log_partitions` | Daily 02:00 | Creates partitions for next 2 months |
| `purge_old_debug_html` | Daily 03:00 | Cleans HTML debug files |
| `collect_system_metrics` | 5min | Pool + queue snapshot |
| `reset_stale_processing_urls` | 10min | Resets stuck URLs |

### 5.2 Call Graph

```
Celery Beat (30s)
    └── scrape_pending_urls()
        └── ScraperService.dispatch_batch()
            └── _process_single_url() [per URL]
                ├── _process_language() [×6 languages]
                │   ├── SeleniumScraperEngine.fetch()
                │   │   ├── delete_all_cookies()
                │   │   ├── _set_language_headers() [CDP]
                │   │   └── driver.get(url)
                │   ├── HotelExtractor.extract_all() [24 keys]
                │   └── _persist_hotel_data()
                │       ├── _upsert_hotel()            [hotels]
                │       ├── _upsert_hotel_description()
                │       ├── _upsert_hotel_policies()
                │       ├── _upsert_hotel_legal()
                │       ├── _upsert_hotel_popular_services()
                │       ├── _upsert_hotel_fine_print()
                │       ├── _upsert_hotel_all_services()
                │       ├── _upsert_hotel_faqs()
                │       ├── _upsert_hotel_guest_reviews()
                │       ├── _upsert_hotel_property_highlights()
                │       ├── _upsert_hotel_extra_info()
                │       ├── _upsert_hotel_nearby_places()
                │       ├── _upsert_hotel_room_types()
                │       ├── _upsert_hotel_seo()
                │       └── _upsert_hotel_individual_reviews()
                └── [EN only] ImageDownloader.download_photo_batch()
```

---

## 6. Database Structure

### 6.1 Critical Constraints

> ⚠ **The database is always dropped and recreated at startup.**
> `schema_v76_complete.sql` is the single source of truth for all tables, indexes, constraints, views, triggers, and column definitions. **No migrations. No ALTER TABLE statements. No data preservation between runs.**

Column names used in `models.py`, `scraper_service.py`, and `extractor.py` must always be verified against `schema_v76_complete.sql` — never assumed.

### 6.2 Tables Overview (22 tables — v76 patch)

| # | Table | Purpose | Primary Key |
|---|-------|---------|-------------|
| 1 | `url_queue` | URL tracking, Strategy-E state | UUID |
| 2 | `hotels` | Core hotel data per language | UUID |
| 3 | `hotels_description` | Long description (STRUCT-001) | UUID |
| 4 | `hotels_policies` | Check-in/out, rules (STRUCT-006) | BIGSERIAL |
| 5 | `hotels_legal` | Legal text + `has_legal_content` flag (STRUCT-007) | UUID |
| 6 | `hotels_popular_services` | Curated services subset (STRUCT-008) | BIGSERIAL |
| 7 | `url_language_status` | Per-language scraping state | UUID |
| 8 | `scraping_logs` | Event log — partitioned by month (RANGE) | UUID |
| 9 | `image_downloads` | Image download tracking | UUID |
| 10 | `image_data` | Photo metadata | UUID |
| 11 | `system_metrics` | Pool + queue health snapshots | BIGSERIAL |
| 12 | `hotels_fine_print` | Fine print HTML (STRUCT-013) | UUID |
| 13 | `hotels_all_services` | All services flat list (STRUCT-014) | BIGSERIAL |
| 14 | `hotels_faqs` | FAQ question + answer (STRUCT-015) | BIGSERIAL |
| 15 | `hotels_guest_reviews` | **Category scores only** (STRUCT-016) | BIGSERIAL |
| 16 | `hotels_property_highlights` | Highlight category + detail (STRUCT-017) | BIGSERIAL |
| 17 | `hotels_extra_info` | "Good to know" block (STRUCT-021) | UUID |
| 18 | `hotels_nearby_places` | POI name + distance + category (STRUCT-022) | BIGSERIAL |
| 19 | `hotels_room_types` | Normalized room types (STRUCT-023) | BIGSERIAL |
| 20 | `hotels_seo` | Meta description + keywords (STRUCT-024) | UUID |
| 21 | `hotels_individual_reviews` | Individual guest reviews — text (STRUCT-025) | BIGSERIAL |
| — | `scraping_logs_YYYY_MM` | Monthly partition children | — |

> `hotels_amenities` was permanently eliminated in Build 65 (0 rows across all scraping cycles).
> `hotels_category_scores` and `hotels_guest_qa` were proposed in the v76 audit and **rejected** as exact duplicates of `hotels_guest_reviews` and `hotels_faqs` respectively.

### 6.3 Key Table Structures

#### `url_queue`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID PK | Primary key |
| `url` | VARCHAR(2048) | Full URL (UNIQUE) |
| `base_url` | VARCHAR(2048) | URL without language params |
| `external_ref` | VARCHAR(64) | CSV column 0 — numeric ID |
| `external_url` | VARCHAR(2048) | CSV column 2 — alternate URL |
| `status` | VARCHAR(32) | `pending`/`processing`/`done`/`error`/`incomplete`/`skipped` |
| `priority` | SMALLINT | 1–10 (default 5) |
| `retry_count` | SMALLINT | Current retry count |
| `max_retries` | SMALLINT | Max allowed (default 3) |
| `last_error` | VARCHAR(2000) | Truncated error message |
| `languages_completed` | VARCHAR(64) | CSV of successful language codes |
| `languages_failed` | VARCHAR(64) | CSV of failed language codes |
| `version_id` | INTEGER | Optimistic locking counter |
| `scraped_at` | TIMESTAMPTZ | Completion timestamp |

#### `hotels`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID PK | Primary key |
| `url_id` | UUID FK | → `url_queue.id` |
| `url` | VARCHAR(2048) | Language-specific URL |
| `language` | VARCHAR(10) | ISO 639-1 code |
| `hotel_name` | VARCHAR(512) | Hotel name in language |
| `hotel_id_booking` | VARCHAR(64) | Booking.com internal ID |
| `address_city` | TEXT | City/region (JSON-LD `addressRegion`) |
| `latitude` | DOUBLE PRECISION | Geographic latitude |
| `longitude` | DOUBLE PRECISION | Geographic longitude |
| `star_rating` | DOUBLE PRECISION | Normalized 0–5 (raw ÷ 2) |
| `review_score` | DOUBLE PRECISION | Aggregate rating 0–10 |
| `review_count` | INTEGER | JSON-LD `aggregateRating.reviewCount` |
| `main_image_url` | VARCHAR(2048) | Primary image from JSON-LD |
| `short_description` | TEXT | JSON-LD description |
| `rating_value` | DOUBLE PRECISION | JSON-LD `ratingValue` |
| `best_rating` | DOUBLE PRECISION | JSON-LD `bestRating` (usually 10) |
| `street_address` | VARCHAR(512) | JSON-LD `streetAddress` |
| `address_locality` | VARCHAR(256) | JSON-LD `addressLocality` |
| `address_country` | VARCHAR(128) | JSON-LD `addressCountry` |
| `postal_code` | VARCHAR(20) | JSON-LD `postalCode` |
| `room_types` | JSONB | Quick-access JSONB (complement to `hotels_room_types`) |
| `price_range` | VARCHAR(64) | Visible price (NULL without date params) |
| `rooms_quantity` | SMALLINT | DOM room-block count or JSON-LD `numberOfRooms` |
| `accommodation_type` | VARCHAR(64) | **NEW** JSON-LD `@type` (e.g. 'Hotel', 'Apartment') |
| `raw_data` | JSONB | Full extracted data snapshot |
| `scrape_engine` | VARCHAR(32) | Always `"selenium"` |
| `version_id` | INTEGER | Optimistic locking |
| `created_at` / `updated_at` | TIMESTAMPTZ | Timestamps with trigger |

UNIQUE: `(url_id, language)` — one row per URL per language.

#### `hotels_room_types`

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL PK | Surrogate key |
| `hotel_id` / `url_id` | UUID FK | → `hotels` / `url_queue` |
| `language` | VARCHAR(10) | ISO code |
| `room_name` | VARCHAR(256) | Room type name |
| `description` | TEXT | Room description |
| `facilities` | JSONB | `["WiFi","Air conditioning",...]` — GIN indexed |
| `adults` | SMALLINT | **NEW** Max adult occupancy (NULL if SVG incomplete) |
| `children` | SMALLINT | **NEW** Max child occupancy (NULL if SVG incomplete) |
| `images` | JSONB | **NEW** Room photo URL array |
| `info` | TEXT | **NEW** Additional room info (nullable) |

UNIQUE: `(hotel_id, language, room_name)`.

#### `hotels_individual_reviews` _(STRUCT-025 — new in patch)_

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL PK | Surrogate key |
| `hotel_id` / `url_id` | UUID FK | → `hotels` / `url_queue` |
| `language` | VARCHAR(10) | ISO code |
| `reviewer_name` | VARCHAR(128) | Guest name |
| `score` | NUMERIC(4,1) | Individual score 0–10 |
| `title` | TEXT | Review headline |
| `positive_comment` | TEXT | "Liked" text |
| `negative_comment` | TEXT | "Disliked" text |
| `reviewer_country` | VARCHAR(128) | Guest country |
| `booking_id` | VARCHAR(64) | Booking.com review ID (nullable) |

> **Semantic distinction**: `hotels_guest_reviews` stores **category scores** (Cleanliness: 9.3, Comfort: 9.2). `hotels_individual_reviews` stores **individual textual reviews** with positive/negative commentary. These are different data structures serving different API fields.

#### `hotels_guest_reviews`

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL PK | Surrogate key |
| `hotel_id` / `url_id` | UUID FK | → `hotels` / `url_queue` |
| `language` | VARCHAR(10) | ISO code |
| `reviews_categories` | VARCHAR(256) | Category name (e.g. "Cleanliness", "Limpieza") |
| `reviews_score` | TEXT | Score string (e.g. "9.3") |

UNIQUE: `(hotel_id, language, reviews_categories)`.

#### `scraping_logs` (partitioned)

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `url_id` | UUID FK | → `url_queue` |
| `hotel_id` | UUID | Hotel reference |
| `language` | VARCHAR(10) | ISO code |
| `event_type` | VARCHAR | `scrape_success` / `scrape_failed` / `upsert_failed` |
| `status` | VARCHAR | `done` / `error` |
| `error_message` | TEXT | Error details |
| `duration_ms` | BIGINT | Scrape duration |
| `scraped_at` | TIMESTAMPTZ | **Partition key** (RANGE by month) |

Partitions exist for 2025-01 through 2027-12, plus a `_default` partition.

### 6.4 Table Relationships

```
url_queue (1)
    ├── hotels (N)                  [url_id]
    ├── scraping_logs (N)           [url_id]
    ├── url_language_status (N)     [url_id]
    ├── image_downloads (N)         [url_id]
    ├── hotels_extra_info (N)       [url_id]
    ├── hotels_nearby_places (N)    [url_id]
    ├── hotels_room_types (N)       [url_id]
    ├── hotels_seo (N)              [url_id]
    └── hotels_individual_reviews (N) [url_id]

hotels (1)
    ├── hotels_description (1:1 per lang)
    ├── hotels_policies (N)
    ├── hotels_legal (1:1 per lang)
    ├── hotels_popular_services (N)
    ├── hotels_fine_print (1:1 per lang)
    ├── hotels_all_services (N)
    ├── hotels_faqs (N)
    ├── hotels_guest_reviews (N)
    ├── hotels_property_highlights (N)
    ├── hotels_extra_info (1:1 per lang)
    ├── hotels_nearby_places (N)
    ├── hotels_room_types (N)
    ├── hotels_seo (1:1 per lang)
    ├── hotels_individual_reviews (N)
    ├── image_data (N)              [hotel_id]
    └── image_downloads (N)         [hotel_id]
```

### 6.5 Views

| View | Description |
|------|-------------|
| `v_hotels_full` | Full denormalized hotel row with all satellite tables as JSONB arrays |
| `v_scraping_summary` | Completeness summary per URL (languages done/error/total) |

`v_hotels_full` includes: `description`, `fine_print`, `highlights`, `popular_services`, `all_services`, `faqs`, `policies`, `guest_reviews`, `legal`, `price_range`, `rooms_quantity`, `accommodation_type`, `extra_info`, `seo_description`, `keywords`, `nearby_places`, `room_types_detail`, `individual_reviews`.

### 6.6 URL Status State Machine

```
pending → processing → done       (all 6 languages succeeded)
                     → error      (all languages failed after retries)
                     → incomplete (partial — Strategy-E enables targeted retry)
         ↑ reset (stale recovery task resets processing → pending after 60min)
```

---

## 7. Configuration

### 7.1 Configuration Source

The `.env` file (copied from `env.example`) is the sole configuration source. `env.example` is the **canonical reference** for all parameters. All new parameters must be added there with documentation before being used in code.

### 7.2 Configuration Parameters

#### Security

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SECRET_KEY` | (generated) | Application secret key |
| `API_KEY` | (empty) | API authentication key |
| `REQUIRE_API_KEY` | `false` | Enforce API key on endpoints |

#### Database

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `bookingscraper` | Database name |
| `DB_USER` | (required) | Database username |
| `DB_PASSWORD` | (required) | Database password |
| `DB_POOL_SIZE` | `10` | Connection pool size |
| `DB_MAX_OVERFLOW` | `5` | Overflow connections |
| `DB_POOL_TIMEOUT` | `30` | Pool acquisition timeout (s) |
| `DB_POOL_RECYCLE` | `3600` | Connection recycle interval (s) |

#### Redis / Memurai

| Parameter | Default | Description |
|-----------|---------|-------------|
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `REDIS_MAX_CONNECTIONS` | `20` | Max connections |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | Celery broker |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/1` | Celery results |

#### Scraper

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SCRAPER_MAX_WORKERS` | `2` | Parallel workers |
| `SCRAPER_REQUEST_TIMEOUT` | `30` | Request timeout (s) |
| `SCRAPER_RETRY_DELAY` | `2.0` | Delay between retries (s) |
| `MAX_RETRIES` | `3` | Max retries per URL |
| `MAX_LANG_RETRIES` | `3` | Max retries per language |
| `LANG_SCRAPE_DELAY` | `10.0` | Inter-language delay (s) |
| `LANG_SCRAPE_DELAY_IT` | `5.0` | Extra pre-scrape delay for Italian (BUG-PERF-001) |
| `MAX_CONSECUTIVE_LANG_FAILURES` | `1` | Failures before VPN rotation |
| `SHORT_HTML_THRESHOLD` | `5000` | Min HTML length — below = challenge page |
| `SELENIUM_CONTENT_WAIT_TIMEOUT_S` | `10.0` | WebDriverWait timeout (BUG-PERF-001) |

#### VPN (NordVPN)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `VPN_ENABLED` | `true` | Enable VPN rotation |
| `VPN_COUNTRIES` | `Spain,Germany,France,...` | Rotation country list |
| `VPN_ROTATION_INTERVAL` | `50` | Seconds between rotations |

#### Languages

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ENABLED_LANGUAGES` | `en,es,de,it,fr,pt` | Languages to scrape |

English (`en`) is always processed first, regardless of list order.

#### Browser

| Parameter | Default | Description |
|-----------|---------|-------------|
| `HEADLESS_BROWSER` | `false` | Headless mode (required for server) |

#### Logging

| Parameter | Default | Description |
|-----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Log level |
| `LOG_MAX_BYTES` | `10485760` | Max log file size (10 MB) |
| `LOG_BACKUP_COUNT` | `5` | Rotating backup count |

#### Debug

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DEBUG` | `false` | Enable debug mode |
| `DEBUG_HTML_SAVE` | `false` | Save raw HTML to disk |
| `DEBUG_HTML_MAX_AGE_HOURS` | `24` | HTML retention before purge |

### 7.3 Configuration Impact on Execution

| Parameter | Impact |
|-----------|--------|
| `SCRAPER_MAX_WORKERS` | Higher = more parallelism but higher Cloudflare detection risk |
| `VPN_ROTATION_INTERVAL` | Lower = better IP diversity; higher = fewer reconnection delays |
| `SELENIUM_CONTENT_WAIT_TIMEOUT_S` | Critical: 4 sequential waits — cumulative worst-case = 4× value |
| `LANG_SCRAPE_DELAY_IT` | Italian pages require extra load time — prevents empty HTML |
| `SHORT_HTML_THRESHOLD` | Below this length = blocked session — retrying is wasteful |
| `MAX_CONSECUTIVE_LANG_FAILURES` | Set to 1 to rotate VPN aggressively on first failure |
| `DEBUG_HTML_SAVE` | Increases disk use significantly — disable in production |

---

## 8. Build History & Bug Fixes

### Build 76 — Patch 2026-04-04 _(current)_

| ID | Severity | Fix |
|----|----------|-----|
| **BUG-PERSIST-002** | 🔴 Critical | 4 upsert methods (`extra_info`, `nearby_places`, `room_types`, `seo`) were defined but never called from `_persist_hotel_data()`. Tables were always empty. |
| **BUG-MAIN-001** | 🟠 High | `main.py` did not import or expose v76 models. `GET /hotel/{id}` was missing 8 fields. |
| **BUG-SCHEMA-VIEW-001** | 🔴 Critical | Missing comma after `AS legal` in `v_hotels_full` caused SQL syntax error — view failed to create on startup. |
| **GAP-EXTRACT-001** | 🟡 Medium | `accommodation_type` was validated from JSON-LD `@type` but discarded. Now extracted and persisted. |
| **GAP-SCHEMA-001** | 🟠 High | No table for individual guest reviews (text). New `hotels_individual_reviews` (STRUCT-025). |
| **GAP-SCHEMA-002** | 🟡 Medium | `hotels_room_types` was missing `adults`, `children`, `images`, `info` columns. |

### Build 76 — Initial release

| STRUCT | Change |
|--------|--------|
| STRUCT-019 | `hotels.price_range VARCHAR(64)` added |
| STRUCT-020 | `hotels.rooms_quantity SMALLINT` added |
| STRUCT-021 | `hotels_extra_info` new table |
| STRUCT-022 | `hotels_nearby_places` new table |
| STRUCT-023 | `hotels_room_types` new table |
| STRUCT-024 | `hotels_seo` new table |

### Build 65

- `hotels_amenities` eliminated — 0 rows produced across all scraping cycles.

### Build 64

- **BUG-DATA-001**: `hotels_amenities` Fallback 1 used same DOM element as `hotels_popular_services` → duplicate data. Fix: Fallback 1 removed from `_extract_amenities()`.
- **BUG-PERF-001**: Italian scrapes had extreme latency (120s+ outliers) from 4 sequential `WebDriverWait(30s)` calls. Fix: `SELENIUM_CONTENT_WAIT_TIMEOUT_S` (10s) + `set_page_load_timeout()` + `LANG_SCRAPE_DELAY_IT` (5s).

### Build 63

- `CloudScraperEngine` eliminated — confirmed 0% success rate.
- SQLAlchemy model class names corrected from plural to singular.
- **BUG-PERSIST-001**: 7 upsert methods defined but never called from `_persist_hotel_data()` — all satellite table data was silently discarded.

### Build 62

- **BUG-LANG-002**: Booking.com session cookies (`bkng_lang=es`) persisted across language requests causing language content mismatch. Fix: CDP `Accept-Language` injection + `delete_all_cookies()` before each `driver.get()` + `reset_browser()` after forced VPN rotation.

### Build 61

- **BUG-LANG-001**: No inter-language delay causing Cloudflare detection; VPN rotation only on time interval (not on consecutive failures); short HTML detection retried with a blocked session.

---

## Document Information

| Property | Value |
|----------|-------|
| **Document** | Guide_Documentation_BookingScraper_EN.md |
| **Version** | 2.0 |
| **Build** | 76 (patch 2026-04-04) |
| **Schema** | `schema_v76_complete.sql` |
| **Date** | 2026-04-04 |
| **Status** | Current Baseline |
| **Previous version** | Guide_Documentation_BookingScraper_EN.md v1.0 (Build 60, 2026-03-29) |

---

*This documentation reflects the BookingScraper Pro system as of Build 76 patch (2026-04-04). All table structures, extraction methods, and configuration parameters are current. The schema_v76_complete.sql file remains the single authoritative source of truth for all database definitions.*
