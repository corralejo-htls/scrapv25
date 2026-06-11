# SCRAPV25 — BookingScraper Pro
**State-Aware Multilingual Scraping System (Strategy E)**

---

| | |
|---|---|
| **Repository** | https://github.com/corralejo-htls/scrapv25 |
| **Version** | v6.0.0 Build 120 |
| **Core Concept** | Data Integrity First |
| **Platform** | Windows 11 · Python · Celery · Memurai (Redis) · PostgreSQL · Selenium |
| **Architecture** | Hybrid — Service + Script-based + Automation Layer |
| **Readme:** | https://raw.githubusercontent.com/corralejo-htls/scrapv25/main/documentations/readme.md
| **Schema Source of Truth (raw)** | https://raw.githubusercontent.com/corralejo-htls/scrapv25/main/schema_v77_complete.sql |
| **File tree** | https://raw.githubusercontent.com/corralejo-htls/scrapv25/main/documentations/_path-file.md |
| **Python code** | https://github.com/corralejo-htls/scrapv25/tree/main/app |
| **Windows file tree** | https://github.com/corralejo-htls/scrapv25/blob/main/pruebas/_arbol_.csv |

---

## Overview

BookingScraper Pro (SCRAPV25) v6.0.0 Build 120 is a distributed, state-aware multilingual scraping system for Booking.com hotel data. It runs as a single-node deployment on Windows 11 using Python, Selenium/Brave, PostgreSQL, Celery, and Memurai (Redis).

**Critical constraint:** The database is destroyed and recreated from `schema_v77_complete.sql` on every system startup. There are no migrations. All data is ephemeral between restarts. The SQL file is the single source of truth for schema and model definitions.

---

## Build 120 Changelog

| Fix ID | Description |
|---|---|
| **BUG-DISPATCH-001-FIX** | `dispatch_batch()` no longer uses `.limit(SCRAPER_MAX_WORKERS)`. New `SCRAPER_BATCH_SIZE` parameter decouples batch size from thread count. |
| **BUG-LOCK-TTL-001-FIX** | Redis lock TTL (previously hardcoded to 280 s) now derived from `TASK_WATCHDOG_TIMEOUT_S + 60`. Prevents lock expiry mid-batch. |
| **SEC-UI-001-FIX** | `/export/ui` and `/export/languages` now require Bearer token when `REQUIRE_API_KEY=True`. |
| **BUG-SCHEMA-COUNT-001-FIX** | Schema header comment corrected from "22 total" to "21 total" tables. |
| **BUG-PARTITION-002-FIX** | 12 partitions for `scraping_logs` 2029 added (coverage extended: 2025-01 to 2029-12). |
| **GAP-VIEW-001-FIX** | `v_scraping_summary` now includes `is_complete` boolean column. |
| **BUG-DB-READONLY-001-FIX** | `get_readonly_db()`: `BEGIN READ ONLY` replaced with `SET TRANSACTION READ ONLY` (SQLAlchemy 2.0 + psycopg3 autobegin compatibility). |
| **BUG-RETRY-001-FIX** (Build 118) | `retry_count` now correctly incremented in `_finalize_url()` and `_mark_url_error()`. |
| **GAP-MODULE-001** (prior) | Export pipeline (`api_export_system.py`, `api_payload_builder.py`) confirmed fully implemented. |

---

## 1. Python Core (`app/*.py`)

| File | Build | Role |
|---|---|---|
| `scraper_service.py` | 120 | Strategy E engine. URL dispatch, language iteration (EN/ES/DE/IT/FR/PT), state machine, 15-table persist pipeline. |
| `extractor.py` | 107 | DOM parsing. Extracts hotel data from Booking.com HTML via DOM (primary) and Apollo JSON (fallback). |
| `scraper.py` | 117 | Selenium/Brave automation. Page navigation, gallery modal, 3-layer challenge detection. |
| `main.py` | 120 | FastAPI server. REST endpoints for data, scraping control, and export. |
| `models.py` | 120 | SQLAlchemy ORM. Maps 21 database tables. |
| `database.py` | 120 | PostgreSQL connection layer. `get_db()`, `get_readonly_db()`, pool management. |
| `config.py` | 120 | Pydantic `Settings`. All environment variables and feature flags. |
| `language_config.py` | 103 | Language codes, labels, URL parameter mappings. |
| `celery_app.py` | 115 | Celery + Memurai/Redis. Task routing, Beat schedule, queue declarations. |
| `tasks.py` | 120 | Background tasks: `scrape_pending_urls`, `reset_stale_processing_urls`, `ensure_log_partitions`, `collect_system_metrics`. |
| `completeness_service.py` | 120 | Strategy E state machine. Validates 6/6 language completeness per URL. Uses `SELECT FOR UPDATE`. |
| `api_export_system.py` | — | Export orchestration to external hotel API. |
| `api_payload_builder.py` | — | Constructs API payload from DB records per `_API_.md` contract. |
| `image_downloader.py` | 108 | Image download pipeline: thumb / large / highres per photo. |
| `image_classifier.py` | 115 | Photo classification: `gallery_visible`, `source`, `subcategory`, `gallery_order`. |
| `vpn_manager_windows.py` | 118 | Windows NordVPN integration. IP rotation, circuit breaker, connection diagnostics. |
| `vpn_manager.py` | — | VPN abstraction layer. |
| `alembic_env.py` | — | Alembic environment (unused in production — DB always recreated). |
| `__init__.py` | 120 | Package init. `BUILD_VERSION = 120`. |

---

## 2. Database Schema (`schema_v77_complete.sql`)

The schema is the **single source of truth**. The database is always recreated from it on startup, never migrated.

### 2.1 Tables (21 user tables)

| Table | Purpose |
|---|---|
| `url_queue` | URL queue: `status`, `priority`, `retry_count`, Strategy E fields (`languages_completed`, `languages_failed`, `last_error`, `base_url`). |
| `hotels` | Core hotel data per language: name, address, geo, star rating, review score/count, accommodation type, price range, rooms quantity, city metadata (`city_name`, `dest_ufi`, `atnm_en`, `dest_id`, `region_name`, `district_name`). |
| `hotels_description` | Long description text per hotel/language. |
| `hotels_policies` | Check-in/out and house policies. One row per policy name per hotel/language. |
| `hotels_legal` | Legal information per language. Includes `has_legal_content` (BOOLEAN) flag. |
| `hotels_popular_services` | Popular facilities (editorial selection by Booking.com). Canonical source since Build 65. |
| `hotels_fine_print` | Fine print HTML per language. Sanitized: SVG/img removed, `<br>` preserved. |
| `hotels_all_services` | Full facility list per hotel/language with `service_category` (verbatim from DOM heading). |
| `hotels_faqs` | FAQs: `ask` and `answer` per hotel/language. |
| `hotels_guest_reviews` | Guest review category scores per language (Cleanliness, Comfort, Location, WiFi, etc.). |
| `hotels_property_highlights` | Property highlights: `highlight_category` + `highlight_detail`. One row per pair per hotel/language. |
| `hotels_extra_info` | "Good to know" / property important info per language. Always inserted (nullable field). |
| `hotels_nearby_places` | Nearby places with `category_code` (1=airport 2=restaurant 3=beach 4=transport 5=nature 6=attraction). |
| `hotels_room_types` | Room types: `room_name`, `description`, `facilities` (JSONB), `adults`, `children`, `images` (JSONB), `info`. Note: `adults`/`children` are NULL without check-in/out URL params. |
| `hotels_seo` | SEO meta tags per language: `seo_description` and `keywords`. |
| `hotels_individual_reviews` | Individual guest reviews: `reviewer_name`, `score`, `title`, `positive_comment`, `negative_comment`, `reviewer_country`, `booking_id`. Extracted from Apollo JSON `FeaturedReview` objects (Build 81). |
| `url_language_status` | Per-URL per-language scraping state: `{pending, processing, done, error, skipped, incomplete}`. |
| `scraping_logs` | RANGE-partitioned by month (2025-01 to 2029-12). 60 partitions + default. 5 indexes on parent table propagated to all partitions (PostgreSQL 14+). FK via trigger. |
| `image_data` | Photo metadata: `id_photo`, dimensions, alt text, `gallery_visible`, `source`, `subcategory`, `gallery_order`. |
| `image_downloads` | Download tracking per photo variant (thumb/large/highres): URL, local path, file size, status. |
| `system_metrics` | Health snapshots: CPU, memory, active workers, DB pool status, pending/done URL counts. |

### 2.2 Views

| View | Purpose |
|---|---|
| `v_hotels_full` | Fully denormalized hotel record with JSONB aggregates. Used by `GET /hotels/{id}`. Note: correlated scalar subqueries — O(n) at scale >1000 hotels. |
| `v_scraping_summary` | Completeness per URL: `languages_done`, `languages_error`, `max_attempts`, `is_complete` (TRUE when all tracked languages are done). Added in Build 120. |
| `v_api_export_images` | One row per gallery photo with best URL (highres > large > thumb). `DISTINCT ON` deduplication (Build 112). |

### 2.3 Triggers and Functions

- **`fn_set_updated_at()`** — Auto-updates `updated_at` on row modification.
- **`trg_scraping_logs_fk_check`** — FK validation for the partitioned `scraping_logs` table.

### 2.4 Partition Maintenance

`scraping_logs` is RANGE-partitioned monthly. Current coverage: `2025-01` to `2029-12`. The `ensure_log_partitions` Beat task (daily 00:05) auto-creates partitions `months_ahead=2`.

**Next manual check:** Q4 2028 — verify 2030 partitions will be created automatically.

---

## 3. Key Configuration (`config.py` / `env.example`)

| Variable | Default | Description |
|---|---|---|
| `ENABLED_LANGUAGES` | `en,es,de,it,fr,pt` | Comma-separated ISO 639-1 codes to scrape. |
| `SCRAPER_MAX_WORKERS` | `2` | ThreadPoolExecutor threads per batch. Selenium lock serializes browser ops — effective concurrency is 1 URL at a time. |
| `SCRAPER_BATCH_SIZE` | `2` | URLs fetched per `dispatch_batch()` call (Build 120). Independent of `SCRAPER_MAX_WORKERS`. Increase to 10–20 for large queues. |
| `TASK_WATCHDOG_TIMEOUT_S` | `600` | Seconds before watchdog kills a hung task via `os._exit(1)`. Set to `SCRAPER_BATCH_SIZE × 270` when increasing batch size. |
| `VPN_ENABLED` | `False` | Enable NordVPN IP rotation. |
| `VPN_ROTATION_INTERVAL` | `120` | Seconds between time-based VPN rotations. |
| `LANG_SCRAPE_DELAY` | `10.0` | Inter-language delay (seconds) within a single hotel. |
| `MAX_LANG_RETRIES` | `3` | Selenium retry attempts per language. |
| `MAX_CONSECUTIVE_LANG_FAILURES` | `1` | Consecutive failures before error-triggered VPN rotation. |
| `IMAGE_CLASSIFICATION_ENABLED` | `True` | Enable gallery modal capture and photo classification. |
| `REQUIRE_API_KEY` | `False` | Enforce Bearer token on all API endpoints. **Set True in production.** |
| `API_KEY` | `""` | Bearer token. Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DEBUG_HTML_SAVE` | `False` | Save raw HTML to disk for debugging. |

**Recommended production `.env` for queues > 50 URLs:**
```ini
ENABLED_LANGUAGES=en,es,de,it,fr,pt
SCRAPER_BATCH_SIZE=20
TASK_WATCHDOG_TIMEOUT_S=5400
REQUIRE_API_KEY=True
API_KEY=<generated-secret>
VPN_ENABLED=True
```

---

## 4. Architecture

### 4.1 Processing Flow

```
Celery Beat (every 30s)
  └─ scrape_pending_urls [Redis lock: LOCK_TTL = watchdog_s + 60]
       └─ dispatch_batch()
            SELECT LIMIT SCRAPER_BATCH_SIZE WHERE status='pending'
            → mark as 'processing'
            └─ ThreadPoolExecutor(max_workers=SCRAPER_MAX_WORKERS)
                 [Selenium _lock serializes all browser ops → 1 URL at a time]
                 └─ _process_url(url_obj)
                      for lang in ENABLED_LANGUAGES:
                        ├─ VPN time-based / error-triggered rotation
                        ├─ _scrape_language(url_obj, lang)
                        │    ├─ Brave/Selenium.get(lang_url)
                        │    ├─ Challenge detection (3 layers)
                        │    ├─ gallery modal capture (en only)
                        │    └─ returns HTML
                        ├─ BookingExtractor(html, url, lang).extract_all()
                        ├─ _persist_hotel_data() → 15 upsert methods
                        └─ _checkpoint_lang_success()  [Strategy E]
                      └─ _finalize_url() → status = done / error
                           retry_count++ on failure
       └─ selenium_engine.quit()  [clean browser teardown]
```

### 4.2 Strategy E — Smart Resume

Ensures no language is re-scraped after a crash or worker restart:

1. After each successful language, `_checkpoint_lang_success()` writes `languages_completed` to `url_queue`.
2. `reset_stale_processing_urls()` (Beat: every 30 min) detects stuck `processing` URLs, rebuilds `languages_completed` from the `hotels` table, and resets `status='pending'`.
3. On next pickup, `_process_url()` skips all languages already in `languages_completed`.

### 4.3 Watchdog Chain (Windows 11)

```
threading.Timer(TASK_WATCHDOG_TIMEOUT_S)
    → psutil.kill_proc_tree()  [terminates Brave + ChromeDriver orphans]
    → os._exit(1)              [bypasses all Python exception handlers]
    → start_celery.bat auto-restart loop
```

URLs being processed at kill time stay in `processing`. `reset_stale_processing_urls()` recovers them on the next Beat tick.

### 4.4 Throughput Profile

| Metric | Value |
|---|---|
| Avg time per hotel (6 languages) | ~245 s |
| English pass (gallery modal) | ~110 s (45% of total) |
| Other 5 languages combined | ~135 s (55% of total) |
| Throughput (single Selenium instance) | ~14–16 hotels/hour |
| Time for 141 URLs at `BATCH_SIZE=2` | ~10 hours |
| Time for 141 URLs at `BATCH_SIZE=20` | ~5 hours (less Beat overhead) |

English is 3.5–5.5× slower than other languages because `take_gallery_photos()` (gallery modal scroll + photo ID capture) runs exclusively on the `en` pass. Photos are language-independent.

---

## 5. Celery Beat Schedule

| Task | Schedule | Queue | Description |
|---|---|---|---|
| `scrape_pending_urls` | Every 30 s | `default` | Main scraping loop. Redis lock prevents overlapping batches. |
| `reset_stale_processing_urls` | Every 30 min | `maintenance` | Resets URLs stuck in `processing` to `pending` with Strategy E smart-resume. |
| `collect_system_metrics` | Every 5 min | `monitoring` | CPU, memory, pool stats → `system_metrics`. |
| `ensure_log_partitions` | Daily 00:05 | `maintenance` | Creates `scraping_logs` partitions `months_ahead=2`. |
| `purge_old_debug_html` | Every 30 min | `maintenance` | Removes debug HTML files older than `DEBUG_HTML_MAX_AGE_HOURS`. |

---

## 6. REST API Reference (`main.py`)

All endpoints require `Authorization: Bearer <API_KEY>` when `REQUIRE_API_KEY=True`.

### Hotel Data

| Method | Path | Description |
|---|---|---|
| `GET` | `/hotels` | List hotels with pagination. Filters: `language`, `status`. |
| `GET` | `/hotels/{hotel_id}` | Full hotel from `v_hotels_full` (denormalized). |

### URL Queue

| Method | Path | Description |
|---|---|---|
| `POST` | `/urls/load` | Bulk-load URLs into `url_queue` from CSV or JSON. |
| `GET` | `/urls` | List URLs with status filters. |
| `DELETE` | `/urls/{url_id}` | Remove a URL. |

### Scraping Control

| Method | Path | Description |
|---|---|---|
| `POST` | `/scraping/force-now` | Trigger `dispatch_batch()` immediately. |
| `GET` | `/scraping/status` | Queue stats: pending, done, processing, error counts. |

### Export

| Method | Path | Auth (Build 120) | Description |
|---|---|---|---|
| `GET` | `/export/ui` | ✅ Required | Interactive HTML export panel. |
| `GET` | `/export/languages` | ✅ Required | `ENABLED_LANGUAGES` list. |
| `GET` | `/export/config` | ✅ | Current external API credentials. |
| `POST` | `/export/config` | ✅ | Update credentials at runtime. |
| `GET` | `/export/resolve` | ✅ | Resolve `external_ref` → `url_id` + completeness status. |
| `POST` | `/export/preview/refs` | ✅ | Dry-run by `external_ref` list. |
| `POST` | `/export/send/refs` | ✅ | Send hotels by `external_ref` list. |
| `POST` | `/export/send/csv` | ✅ | Upload CSV with `external_ref` column → send. |
| `GET` | `/export/preview/{url_id}` | ✅ | Dry-run by internal `url_id`. |
| `GET` | `/export/preview` | ✅ | Dry-run all completed hotels. |
| `POST` | `/export/send/{url_id}` | ✅ | Send single hotel by `url_id`. |
| `POST` | `/export/send` | ✅ | Send all completed hotels. |

---

## 7. Data Export Contract (`_API_.md`)

```
PATCH https://web.com/api/en/543-clave-api/update/:hotel_id.json
Content-Type: application/json
```

| Field | Type | Notes |
|---|---|---|
| `name` | Object | Multilingual. `en` must be listed first. |
| `rating` | Number | Overall numeric rating. |
| `address` | Object | Multilingual full address. |
| `geoPosition` | Object | `latitude`, `longitude`. |
| `services` | Array | Multilingual categorized services. |
| `conditions` | Array | Multilingual check-in/out policies. |
| `toConsider` | String | Fine print. Use `\n` for line breaks. |
| `images` | Array | Gallery-visible photo URLs (highres priority). |
| `scoreReview` | Number | Overall review score. |
| `roomsQuantity` | Number | Number of room types. |
| `accommodationType` | String | Hotel, Apartment, Villa, etc. |
| `extraInfo` | String/Null | "Good to know" block. |
| `longDescription` | Object | Multilingual description. |
| `reviews` | Array | Individual guest reviews (Apollo FeaturedReview). |
| `categoryScoreReview` | Object | Category scores (Facilities, Cleanliness, Comfort, Value, Location, WiFi). |
| `rooms` | Array | Room types with `adults`, `children`, `images`, `facilities`, `info`. |
| `nearbyPlaces` | Array | Nearby places with integer `category` code. |
| `guestValues` | Array | Multilingual FAQs. |
| `seoDescription` | Object | Multilingual SEO meta description. |
| `keywords` | Object | Multilingual SEO keywords. |

**Rules:** English first in all multi-language arrays. All fields optional (omit to leave unchanged). Use `\n`, not `<br>`.

---

## 8. Data Quality Baseline

From a production run on 2026-06-08 (141 URLs):

| Metric | Value |
|---|---|
| Hotels completed (6/6 languages) | **31** |
| Hotels partially scraped (5/6) | 1 |
| URLs pending (never reached) | 105 |
| URLs stale in `processing` | 5 |
| Total language-level scrapes | 191 |
| Scraping errors (block, VPN, extraction) | **0** (100% success) |
| `hotels_all_services` rows | 14,726 (~77 avg/hotel) |
| `hotels_popular_services` rows | 1,772 (~9 avg/hotel) |
| `image_data` photos | 3,035 |
| `image_downloads` records | 9,105 (exactly 3.00/photo: thumb+large+highres) |
| Download error rate | 0.2% (18/9105) |

**Root cause of 31/141:** `SCRAPER_BATCH_SIZE=2` (default) limits each Beat tick to 2 URLs. At ~245 s/hotel, completing 141 URLs requires ~10 hours of continuous operation. The run covered ~2 hours. Fixed: set `SCRAPER_BATCH_SIZE=20` in `.env`.

### Diagnostic Queries

**Queue state snapshot:**
```sql
SELECT status, COUNT(*) AS n,
       MIN(updated_at) AS oldest, MAX(updated_at) AS newest
FROM url_queue GROUP BY status ORDER BY n DESC;
```

**Validate 5 tables missing from standard Q24 (added Builds 76–81):**
```sql
SELECT t, filas,
       CASE WHEN filas = 0 THEN '❌ EMPTY' ELSE '✅ OK' END AS result
FROM (
  SELECT 'hotels_extra_info'            AS t, COUNT(*) AS filas FROM hotels_extra_info
  UNION ALL SELECT 'hotels_seo',               COUNT(*) FROM hotels_seo
  UNION ALL SELECT 'hotels_nearby_places',     COUNT(*) FROM hotels_nearby_places
  UNION ALL SELECT 'hotels_individual_reviews',COUNT(*) FROM hotels_individual_reviews
  UNION ALL SELECT 'hotels_room_types',        COUNT(*) FROM hotels_room_types
) sub ORDER BY result, t;
```

**Stale processing URLs (reset before re-running):**
```sql
SELECT id, external_ref, status, retry_count, languages_completed, updated_at
FROM url_queue WHERE status = 'processing' ORDER BY updated_at;
-- Reset: celery -A app.celery_app call tasks.reset_stale_processing_urls
```

**Per-language performance:**
```sql
SELECT language, COUNT(*) AS scrapes,
       ROUND(AVG(duration_ms)/1000.0,1) AS avg_s,
       ROUND(MAX(duration_ms)/1000.0,1) AS max_s
FROM scraping_logs WHERE status='done'
GROUP BY language ORDER BY avg_s DESC;
```

---

## 9. `_persist_hotel_data()` — Upsert Chain

All 15 satellite table upsert methods confirmed wired in `scraper_service.py` (Build 120):

| # | Method | Table | On empty data |
|---|---|---|---|
| 1 | `_upsert_hotel()` | `hotels` | Always inserts |
| 2 | `_upsert_hotel_description()` | `hotels_description` | Always inserts |
| 3 | `_upsert_hotel_policies()` | `hotels_policies` | Always inserts |
| 4 | `_upsert_hotel_legal()` | `hotels_legal` | Always inserts |
| 5 | `_upsert_hotel_popular_services()` | `hotels_popular_services` | Skips if list empty |
| 6 | `_upsert_hotel_fine_print()` | `hotels_fine_print` | Always inserts (nullable) |
| 7 | `_upsert_hotel_all_services()` | `hotels_all_services` | Skips if list empty |
| 8 | `_upsert_hotel_faqs()` | `hotels_faqs` | Skips if list empty |
| 9 | `_upsert_hotel_guest_reviews()` | `hotels_guest_reviews` | Skips if list empty |
| 10 | `_upsert_hotel_property_highlights()` | `hotels_property_highlights` | Skips if list empty |
| 11 | `_upsert_hotel_nearby_places()` | `hotels_nearby_places` | Skips if list empty |
| 12 | `_upsert_hotel_room_types()` | `hotels_room_types` | Skips if list empty |
| 13 | `_upsert_hotel_seo()` | `hotels_seo` | Skips if both fields NULL |
| 14 | `_upsert_hotel_extra_info()` | `hotels_extra_info` | Always inserts (nullable) |
| 15 | `_upsert_hotel_individual_reviews()` | `hotels_individual_reviews` | Skips if list empty |

---

## 10. HTML Tag Analysis

### 10.1 Data Layers

| Layer | Format | Location | Usage |
|---|---|---|---|
| JSON-LD | `application/ld+json` | `<script type="application/ld+json">` | Name, address, geo, rating, review count, accommodation type |
| booking.env | JavaScript object | `<script>` with `booking.env = {...}` | `city_name` (`b_city_name`), `dest_ufi` (`b_ufi`), `atnm_en`, `dest_id` |
| Apollo Cache | JSON | `<script type="application/json">` | Individual reviews (`FeaturedReview`). Primary for `hotels_individual_reviews`. |
| hotelPhotos | JSON | `<script>` | Image metadata, URL variants, dimensions |
| DOM | HTML | `data-testid` + CSS classes | Primary source for all visible content |

### 10.2 DOM Selectors by Table

#### `hotels` — Core Hotel Data

| Field | Source | Selector |
|---|---|---|
| `hotel_name`, `latitude`, `longitude`, `star_rating`, `review_score`, `review_count`, `accommodation_type`, `street_address`, `rooms_quantity`, `main_image_url` | JSON-LD | `<script type="application/ld+json">` |
| `city_name`, `dest_ufi`, `dest_id`, `atnm_en` | booking.env | `<script>` with `booking.env = {...}` |
| `region_name` | Breadcrumb | `<nav><ol><li>` items[3] |
| `district_name` | Breadcrumb | `<nav><ol><li>` items[5] (7-item breadcrumb only) |

#### `hotels_policies`
`data-testid="property-section--policies"` → `<h2>/<h3>` for `policy_name`, `<div>/<p>/<span>` for `policy_details`.

#### `hotels_legal`
Multilingual keyword match on headings. `has_legal_content=TRUE` if block found with content; `FALSE` if absent (common in BR/UY markets).

#### `hotels_popular_services`
`property-most-popular-facilities-wrapper` → `<div>/<span>` with popular-facility class or similar.

#### `hotels_fine_print`
`data-testid` or class matching `property-section--fine-print`. HTML sanitized: SVG/img removed, `<br>` preserved.

#### `hotels_all_services`
`<li>/<span>` within `facility-group` blocks (`service`). `<h3>/<div>` heading of same block (`service_category`, verbatim since Build 103). Phase 1 ("Great for your stay") eliminated Build 103.

#### `hotels_faqs`
`<div>/<button>` with FAQ question `data-testid` → `ask`. `<div>/<p>` expanded content → `answer`.

#### `hotels_guest_reviews`
`<span>/<div>` with category name (`reviews_categories`) and numeric score (`reviews_score`) within review score block.

#### `hotels_property_highlights`
`<h3>/<div>` heading → `highlight_category`. `<li>/<span>/<div>` within group → `highlight_detail`. One row per pair.

#### `hotels_extra_info`
`data-testid="property-important-info"` (primary). Fallbacks: `house-rules` → `hotelPoliciesInc` → `hp--important_info` class.

#### `hotels_nearby_places`
```html
<section id="surroundings_block">
  <div data-testid="poi-block">
    <h3>Top attractions</h3>
    <ul data-testid="poi-block-list">
      <li><span role="listitem">
        <div class="d1bc97eb82">Place Name</div>
        <div class="cbf0753d0c">2.1 km</div>
      </span></li>
    </ul>
  </div>
</section>
```
`category_code` mapped: 1=airport 2=restaurant 3=beach 4=transport 5=nature 6=attraction.

#### `hotels_room_types`
```html
<table class="cdd0659f86">
  <tbody><tr>
    <th scope="row">
      <a data-testid="rt-name-link">Room Name</a>
      <span class="d7a50099f7">1 extra-large double bed</span>
    </th>
  </tr></tbody>
</table>
```
`adults`/`children` are NULL without `?checkin=&checkout=` URL params.

#### `hotels_seo`
`<meta name="description">` or `<meta property="og:description">` → `seo_description`.
`<meta name="keywords">` → `keywords`.

#### `hotels_individual_reviews`
**Primary:** Apollo JSON `FeaturedReview:ID` objects in `<script type="application/json">`. Fields: `guestName`, `averageScore`, `title`, `positiveText`, `negativeText`, `guestCountryCode`, `id`.
DOM `data-testid="review-card"` is secondary fallback (Booking.com uses React hydration, not static HTML).

#### `image_data` + `image_downloads`

| Field | Source |
|---|---|
| `id_photo`, `photo_width`, `photo_height`, `alt`, `thumb_url`, `large_url`, `highres_url` | `hotelPhotos` JS array |
| `gallery_visible`, `gallery_order` | Gallery modal capture (en pass only) |
| `source` | `gallery_modal` / `js_array` / `dom_scan` / `unknown` |
| `subcategory` | `gallery` / `room` / `facility` / `exterior` / `thumbnail` / `review_photo` / `unknown` |

### 10.3 HTML Test Snapshots (`pruebas/*.html`)

| File | Hotel ID | Location | Size | Purpose |
|---|---|---|---|---|
| `HTML_1001_Villa-Dvor_Ohrid.html` | 1001 | Ohrid, North Macedonia | ~1.4 MB | Service extraction |
| `HTML_76033__Hotel-Topazz.html` | 76033 | Austria | ~29 KB | Policy/legal extraction |
| `HTML_76224__Radisson-Hotel-Graz.html` | 76224 | Austria | ~1.4 MB | Room type extraction |
| `HTML_76569__Hotel-Aquamarin.html` | 76569 | Austria | ~28 KB | Amenity extraction |
| `HTML_76972__haus-mobene-garni.html` | 76972 | Austria | ~63 KB | Service category testing |
| `HTML_77149__trofana-royal.html` | 77149 | Austria | ~1.4 MB | Highlight extraction |
| `HTML_77414__Arlberg.html` | 77414 | Austria | ~1.6 MB | Nearby places extraction |
| `HTML_77736__bruecklwirt.html` | 77736 | Austria | ~1.4 MB | Review extraction |
| `HTML_78465_wild-&-bolz-eMotel.html` | 78465 | Austria | ~1.2 MB | Image gallery extraction |

### 10.4 Extraction Strategy Principles

1. **Priority:** DOM (strategies 1 → 1.5 → 2) primary; Apollo JSON fallback (3) — except `individual_reviews` where Apollo is primary.
2. **Multilingual:** Selectors must work across all 6 languages. Structural position preferred over text content.
3. **Dynamic content:** FAQ answers and availability table require JS-rendered DOM (HTML snapshots capture post-render state).
4. **Sanitization:** HTML stored in DB (`hotels_fine_print`) is sanitized: SVG/img removed, attributes stripped, `<br>` preserved.
5. **JSON-LD:** Most stable source for core metadata (name, address, geo, rating). Always primary.
6. **booking.env:** Provides city metadata via inline `<script>`. Breadcrumb DOM is the fallback.

### 10.5 Extraction Opportunities (Unimplemented)

| Data Point | DOM Source | Suggested Target | Priority |
|---|---|---|---|
| Sustainability / Eco certifications | `data-testid="property-section--sustainability"` | New column in `hotels` | Medium |
| Property labels / badges | "Genius", "Travel Sustainable" badge elements | New column in `hotels` | Medium |
| Host / property manager info | `data-testid="host-profile"` | New table `hotels_host` | Low |
| Payment methods | `data-testid="payment-methods"` | New table `hotels_payment_methods` | Low |
| Check-in instructions | Within `property-important-info` | `hotels_extra_info` / `hotels_policies` | Low |

---

## 11. Supporting Files

### Windows Automation (`.bat`)

| Category | Files |
|---|---|
| Server | `start_server.bat`, `stop_server.bat`, `restart_all.bat` |
| Celery | `start_celery.bat`, `start_celery_beat.bat`, `stop_celery.bat` |
| Database | `backup_db.bat`, `create_db.bat`, `export_data.bat` |
| Maintenance | `cleanup_logs.bat`, `limpiar_cache.bat`, `verify_system.bat`, `verify_memurai.bat`, `show_status.bat`, `diagnostico_vpn.bat`, `purge_queues.bat` |
| Startup | `iniciar.bat` (recreates DB + starts all services), `inicio_rapido.bat` |

### Utility Scripts (`scripts/*.py`)

| Script | Purpose |
|---|---|
| `load_urls.py` | Load URLs from CSV into `url_queue`. |
| `retry_incomplete.py` | Retry failed languages (Strategy E aware). |
| `export_data.py` | Execute data export to external API. |
| `verify_system.py` | System health checks. |
| `gen_memurai_conf.py` | Memurai/Redis config generator. |

### Test Suite

`tests/test_extractor.py` · `tests/test_models.py` · `tests/test_scraper.py` · `tests/test_strategy_e.py` · `tests/test_completeness.py` · `tests/test_config.py`

### Root Configuration

| File | Purpose |
|---|---|
| `schema_v77_complete.sql` | **Single source of truth SQL schema.** |
| `env.example` | Environment variable template. |
| `config.ini` | Application configuration. |
| `languages.json` | Language definitions and URL mappings. |
| `requirements.txt` | Production dependencies (`webdriver-manager>=4.0.0,<5.0.0` mandatory). |
| `requirements-optional.txt` | Optional: `lxml` (30–40% faster HTML parsing). |
| `memurai.conf` | Memurai (Redis for Windows) configuration. |
| `windows_service.py` | Windows service wrapper. |

---

## 12. Known Architecture Constraints

| Item | Impact | Mitigation |
|---|---|---|
| DB destroyed on every startup | Total data loss on restart | Strategy E smart-resume |
| Single Selenium `_lock` | Effective concurrency = 1 URL at a time | Multiple `SeleniumEngine` instances in separate Celery processes |
| `v_hotels_full` correlated subqueries | O(n) at scale >1000 hotels | Refactor at scale; accept now |
| Python 3.14 (pre-release) | Potential ABI instability | Consider migration to Python 3.12 |
| `lxml` not installed by default | HTML parsing 30–40% slower | `pip install lxml --break-system-packages` |
| `REQUIRE_API_KEY=False` default | All endpoints open | Set `True` + strong `API_KEY` in production |
| Partition gap after 2029-12 | Logs fall to `_default` partition | `ensure_log_partitions` Beat task auto-manages; verify before Q4 2028 |

---

## 13. Security Checklist

- [ ] `REQUIRE_API_KEY=True` in production `.env`
- [ ] Strong `API_KEY` set (32+ bytes random hex)
- [ ] PostgreSQL `DATABASE_URL` in env var, not in code
- [ ] NordVPN credentials in env vars (`NORDVPN_USERNAME`, `NORDVPN_PASSWORD`)
- [ ] External API key in env var (`EXT_API_KEY`), configurable at runtime via `POST /export/config`
- [ ] `/export/ui` and `/export/languages` now protected (Build 120 — SEC-UI-001-FIX)
- [ ] FastAPI server not exposed to public internet (Windows 11 single-node, localhost only)

---

*Generated from repository state and audit findings — Build 120 · 2026-06-11.*
