# BookingScraper System Documentation
## Version 6.0.0 Build 59

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Repository Structure](#2-repository-structure)
3. [Application Architecture](#3-application-architecture)
4. [Workflow Description](#4-workflow-description)
5. [Functions and Procedures](#5-functions-and-procedures)
6. [Database Structure](#6-database-structure)
7. [Configuration](#7-configuration)

---

## 1. System Overview

**BookingScraper Pro** is a Python-based web scraping system designed to extract hotel information from Booking.com. The system supports multi-language scraping, parallel processing, VPN rotation for IP management, and comprehensive data persistence.

### Key Characteristics

| Attribute | Description |
|-----------|-------------|
| **Application Name** | BookingScraper Pro |
| **Version** | 6.0.0 |
| **Build** | 59 |
| **Platform** | Windows 11 (primary) |
| **Language** | Python 3.x |
| **Database** | PostgreSQL |
| **Task Queue** | Celery with Redis/Memurai |
| **Scraping Engines** | CloudScraper, Selenium (fallback) |

### Core Capabilities

- **Multi-language Support**: Scrapes hotel data in multiple languages (en, es, de, fr, it, pt, and more)
- **Parallel Processing**: Uses ThreadPoolExecutor for concurrent scraping
- **VPN Integration**: NordVPN support for IP rotation
- **Image Download**: Downloads hotel images with metadata
- **Comprehensive Logging**: Detailed scraping logs with partitioning
- **Automatic Scheduling**: Celery Beat for periodic task execution

---

## 2. Repository Structure

```
scrapv25/
├── app/                          # Main application folder
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration management (Settings class)
│   ├── database.py              # Database connection and session management
│   ├── extractor.py             # Data extraction from HTML
│   ├── image_downloader.py      # Hotel image download functionality
│   ├── main.py                  # Application entry point
│   ├── models.py                # SQLAlchemy ORM models
│   ├── scraper.py               # Core scraping engines
│   ├── scraper_service.py       # High-level scraping orchestration
│   └── tasks.py                 # Celery background tasks
├── documentations/              # Audits and application documentation
├── pruebas/                     # CSV exports and sample HTML files
│   ├── _table__*.csv           # Database table exports
│   └── _HTML-view-source__*.md  # Sample HTML content
├── scripts/                     # Utility scripts
├── tests/                       # Test files
├── env.example                  # Configuration template
├── requirements.txt             # Python dependencies
└── *.bat                        # Windows batch scripts for operations
```

### Directory Purposes

| Directory | Purpose |
|-----------|---------|
| `/app` | Core application code |
| `/documentations` | System audits and documentation |
| `/pruebas` | CSV table exports and HTML samples for testing/analysis |
| `/scripts` | Utility and helper scripts |
| `/tests` | Unit and integration tests |

---

## 3. Application Architecture

### 3.1 Module Overview

#### `config.py`
Centralized configuration management using Pydantic Settings. Handles:
- Environment variable loading from `.env` file
- Database connection parameters
- Scraper configuration
- VPN settings
- Language mappings

#### `database.py`
Database connectivity and session management:
- SQLAlchemy engine creation with connection pooling
- Session factory with context managers
- Pool status monitoring
- Serializable isolation level support for DDL operations

#### `models.py`
SQLAlchemy ORM models defining database schema:
- `URLQueue`: URL management and tracking
- `Hotels`: Hotel data storage
- `ScrapingLogs`: Event logging with partitioning
- `ImageData` / `ImageDownload`: Image metadata and download tracking
- `SystemMetrics`: Performance monitoring

#### `scraper.py`
Core scraping functionality:
- `BaseScraper`: Abstract base class
- `CloudScraperEngine`: Primary scraping using cloudscraper
- `SeleniumScraperEngine`: Fallback using Selenium WebDriver

#### `extractor.py`
HTML data extraction:
- `BookingExtractor`: Extracts structured data from Booking.com HTML
- JSON-LD parsing
- XPath-based element extraction

#### `scraper_service.py`
High-level orchestration:
- `ScraperService`: Manages batch processing
- Language iteration
- VPN rotation coordination
- Error handling and retry logic

#### `image_downloader.py`
Image handling:
- `ImageDownloader`: Downloads hotel images
- Parallel download with ThreadPoolExecutor
- Metadata persistence

#### `tasks.py`
Celery background tasks:
- `scrape_pending_urls`: Auto-scraping task
- `ensure_log_partitions`: Database partition management
- `collect_system_metrics`: Performance monitoring
- `reset_stale_processing_urls`: Cleanup task

### 3.2 File Organization Patterns

| Pattern | Description |
|---------|-------------|
| `__init__.py` | Package initialization with version constants |
| `*.py` | Module files with specific responsibilities |
| `get_*()` functions | Factory functions for singleton instances |
| Context managers | Database session handling (`with get_db()`) |

---

## 4. Workflow Description

### 4.1 Phase 1: Initialization

1. **Configuration Loading**
   - `config.py` loads settings from `.env` file
   - Validates required parameters (DB_USER, DB_PASSWORD)
   - Creates necessary directories (logs, data, backups)

2. **Database Setup**
   - `database.py` creates SQLAlchemy engine with connection pool
   - Pool size: 10 connections (configurable via DB_POOL_SIZE)
   - Max overflow: 5 connections

3. **Celery Initialization**
   - Redis/Memurai as broker and result backend
   - Queue definitions: default, maintenance, monitoring

### 4.2 Phase 2: URL Loading

1. **URL Import Process**
   - URLs loaded from external source into `url_queue` table
   - Each URL receives:
     - UUID (`id`)
     - Base URL
     - External reference ID
     - Initial status: `pending`
     - Priority level (default: 5)

2. **URL Structure**
   ```
   Base URL: https://www.booking.com/hotel/{country}/{hotel-name}.html
   Language variants generated by appending language parameters
   ```

### 4.3 Phase 3: Processing

1. **Batch Selection**
   - `ScraperService.dispatch_batch()` queries URLs with `status='pending'`
   - Limited by `SCRAPER_MAX_WORKERS` (default: 2)

2. **Status Transition**
   - URL status changes: `pending` → `processing`
   - `updated_at` timestamp refreshed

3. **Language Processing Order**
   - English (`en`) always processed first
   - Remaining languages from `ENABLED_LANGUAGES` follow

### 4.4 Phase 4: Web Scraping Engines

#### Primary Engine: CloudScraper
```python
CloudScraperEngine._fetch_with_cloudscraper()
```
- Uses `cloudscraper` library to bypass Cloudflare
- Headers include User-Agent and Referer
- Timeout: 30 seconds (configurable)

#### Fallback Engine: Selenium
```python
SeleniumScraperEngine._fetch_with_selenium()
```
- Chrome WebDriver with Brave browser support
- Headless mode configurable via `HEADLESS_BROWSER`
- Automatic retry on failure

#### VPN Rotation (if enabled)
- NordVPN integration via `vpn_manager_windows.py`
- Country rotation every `VPN_ROTATION_INTERVAL` seconds
- Supported countries: Spain, Germany, France, Netherlands, etc.

### 4.5 Phase 5: Data Extraction

1. **HTML Parsing**
   - `BookingExtractor` receives raw HTML
   - JSON-LD structured data extraction
   - XPath fallback for missing fields

2. **Extracted Fields**
   | Field | Source |
   |-------|--------|
   | hotel_name | JSON-LD `@graph` or XPath |
   | address | JSON-LD or meta tags |
   | review_score | JSON-LD `aggregateRating` |
   | latitude/longitude | JSON-LD `geo` |
   | images | JSON-LD `photo` array |
   | description | Meta description |

3. **Image Metadata Extraction**
   - `id_photo`: Unique photo identifier
   - `thumb_url`, `large_url`, `highres_url`: Size variants
   - `orientation`: landscape/portrait
   - `photo_width`, `photo_height`: Dimensions

### 4.6 Phase 6: Persistence

1. **Hotel Data Storage**
   - Insert/Update `hotels` table
   - One row per URL-language combination
   - Tracks: scrape duration, engine used, timestamps

2. **Logging**
   - `scraping_logs` table records each attempt
   - Partitioned by month (`scraping_logs_YYYY_MM`)
   - Event types: `scrape_success`, `scrape_failed`

3. **Image Data Storage**
   - `image_data`: Photo metadata
   - `image_downloads`: Download status tracking

4. **URL Status Update**
   - `languages_completed`: Comma-separated list of successful languages
   - `languages_failed`: Comma-separated list of failed languages
   - Final status: `done` or `error`

### 4.7 Phase 7: Image Handling

1. **Download Trigger**
   - After successful hotel data extraction
   - `ImageDownloader.download_photo_batch()` called

2. **Parallel Download**
   - ThreadPoolExecutor with max 3 workers
   - Downloads all size variants (thumb, large, highres)

3. **File Storage**
   - Location: `data/images/{hotel_id}/`
   - Filename format: `{id_photo}_{category}.{ext}`

4. **Database Recording**
   - `ImageDownload` records created with:
     - Local path
     - File size
     - Content type
     - Status (done/error)

### 4.8 Phase 8: Error Handling

1. **Retry Logic**
   - `MAX_RETRIES`: 3 attempts per URL-language
   - `MAX_LANG_RETRIES`: 3 attempts per language
   - Exponential backoff with `SCRAPER_RETRY_DELAY`

2. **Error Recording**
   - Error messages truncated to 2000 characters
   - Stored in `url_queue.last_error`
   - Logged to `scraping_logs.error_message`

3. **Stale URL Recovery**
   - Celery task `reset_stale_processing_urls`
   - Resets URLs stuck in `processing` for >60 minutes
   - Clears language tracking fields

---

## 5. Functions and Procedures

### 5.1 Core Functions by Module

#### `config.py`

| Function | Description |
|----------|-------------|
| `get_settings()` | Returns Settings singleton instance |
| `reset_settings()` | Forces Settings re-instantiation |

#### `database.py`

| Function | Description |
|----------|-------------|
| `get_db()` | Context manager for database sessions |
| `get_serializable_db()` | Session with SERIALIZABLE isolation |
| `get_pool_status()` | Returns connection pool statistics |
| `init_db()` | Creates all tables |

#### `scraper.py`

| Function | Description |
|----------|-------------|
| `BaseScraper.fetch()` | Abstract fetch method |
| `CloudScraperEngine._fetch_with_cloudscraper()` | Cloudscraper-based fetching |
| `SeleniumScraperEngine._fetch_with_selenium()` | Selenium-based fetching |
| `BaseScraper._save_debug_html()` | Saves HTML for debugging |

#### `extractor.py`

| Function | Description |
|----------|-------------|
| `BookingExtractor.extract()` | Main extraction entry point |
| `BookingExtractor._extract_from_jsonld()` | JSON-LD data extraction |
| `BookingExtractor._extract_photos()` | Photo metadata extraction |
| `BookingExtractor._extract_room_types()` | Room type extraction |

#### `scraper_service.py`

| Function | Description |
|----------|-------------|
| `ScraperService.dispatch_batch()` | Processes pending URL batch |
| `ScraperService._process_single_url()` | Single URL processing |
| `ScraperService._process_language()` | Single language processing |
| `ScraperService._should_retry()` | Retry decision logic |

#### `image_downloader.py`

| Function | Description |
|----------|-------------|
| `ImageDownloader.download_batch()` | Legacy URL list download |
| `ImageDownloader.download_photo_batch()` | Photo dict download |
| `ImageDownloader._download_one()` | Single image download |
| `ImageDownloader._upsert_image_data()` | Metadata persistence |

#### `tasks.py`

| Function | Description |
|----------|-------------|
| `scrape_pending_urls()` | Auto-scraping Celery task |
| `ensure_log_partitions()` | Partition creation task |
| `purge_old_debug_html()` | Debug file cleanup |
| `collect_system_metrics()` | Metrics collection |
| `reset_stale_processing_urls()` | Stale URL recovery |

### 5.2 Function Interactions

```
Celery Beat (30s)
    └── scrape_pending_urls()
        └── ScraperService.dispatch_batch()
            └── _process_single_url()
                ├── BaseScraper.fetch()
                │   ├── CloudScraperEngine._fetch_with_cloudscraper()
                │   └── SeleniumScraperEngine._fetch_with_selenium() [fallback]
                ├── BookingExtractor.extract()
                │   ├── _extract_from_jsonld()
                │   └── _extract_photos()
                ├── ImageDownloader.download_photo_batch()
                │   └── _download_one()
                └── Database persistence (get_db())
```

---

## 6. Database Structure

### 6.1 Tables Overview

Based on CSV exports in `/pruebas`:

| Table | Purpose |
|-------|---------|
| `url_queue` | URL management and status tracking |
| `hotels` | Hotel data per language |
| `hotels_description` | Extended hotel descriptions |
| `hotels_amenities` | Hotel amenities |
| `hotels_all_services` | Complete service listings |
| `hotels_policies` | Hotel policies |
| `hotels_fine_print` | Additional terms |
| `hotels_legal` | Legal information |
| `hotels_guest_reviews` | Review data |
| `hotels_popular_services` | Featured services |
| `hotels_property_highlights` | Key property features |
| `hotels_faqs` | Frequently asked questions |
| `scraping_logs` | Event logging (partitioned) |
| `image_data` | Photo metadata |
| `image_downloads` | Download tracking |
| `url_language_status` | Per-language status |
| `system_metrics` | Performance metrics |

### 6.2 Key Table Structures

#### `url_queue`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `url` | VARCHAR | Full Booking.com URL |
| `base_url` | VARCHAR | Base URL without language params |
| `external_ref` | VARCHAR | External reference ID |
| `external_url` | VARCHAR | Original source URL |
| `status` | VARCHAR | pending/processing/done/error |
| `priority` | INTEGER | Processing priority (1-10) |
| `retry_count` | INTEGER | Number of retry attempts |
| `max_retries` | INTEGER | Maximum allowed retries |
| `last_error` | TEXT | Last error message |
| `languages_completed` | VARCHAR | Comma-separated successful languages |
| `languages_failed` | VARCHAR | Comma-separated failed languages |
| `created_at` | TIMESTAMP | Creation time |
| `updated_at` | TIMESTAMP | Last update time |
| `scraped_at` | TIMESTAMP | Completion time |
| `version_id` | INTEGER | Data version |

#### `hotels`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `url_id` | UUID | Foreign key to url_queue |
| `url` | VARCHAR | Language-specific URL |
| `language` | VARCHAR | ISO 639-1 language code |
| `hotel_name` | VARCHAR | Hotel name in language |
| `hotel_id_booking` | VARCHAR | Booking.com hotel ID |
| `address_city` | VARCHAR | City name |
| `latitude` | FLOAT | Geographic latitude |
| `longitude` | FLOAT | Geographic longitude |
| `star_rating` | FLOAT | Star rating |
| `review_score` | FLOAT | Review score |
| `review_count` | INTEGER | Number of reviews |
| `main_image_url` | VARCHAR | Primary image URL |
| `short_description` | TEXT | Hotel description |
| `rating_value` | FLOAT | Rating value |
| `best_rating` | FLOAT | Maximum possible rating |
| `street_address` | VARCHAR | Street address |
| `address_locality` | VARCHAR | Locality |
| `address_country` | VARCHAR | Country name (localized) |
| `postal_code` | VARCHAR | Postal code |
| `room_types` | JSON | Room type information |
| `raw_data` | JSON | Complete extracted data |
| `scrape_duration_s` | FLOAT | Scrape time in seconds |
| `scrape_engine` | VARCHAR | Engine used (cloudscraper/selenium) |
| `created_at` | TIMESTAMP | Creation time |
| `updated_at` | TIMESTAMP | Update time |
| `version_id` | INTEGER | Data version |

#### `scraping_logs`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `url_id` | UUID | Foreign key to url_queue |
| `hotel_id` | UUID | Foreign key to hotels |
| `language` | VARCHAR | Language code |
| `event_type` | VARCHAR | Event type (scrape_success/scrape_failed) |
| `status` | VARCHAR | done/error |
| `error_message` | TEXT | Error details |
| `duration_ms` | BIGINT | Duration in milliseconds |
| `worker_id` | VARCHAR | Celery worker ID |
| `extra_data` | JSON | Additional context |
| `scraped_at` | TIMESTAMP | Event timestamp |

#### `image_data`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `id_photo` | VARCHAR | Booking.com photo ID |
| `hotel_id` | UUID | Foreign key to hotels |
| `orientation` | VARCHAR | landscape/portrait |
| `photo_width` | INTEGER | Width in pixels |
| `photo_height` | INTEGER | Height in pixels |
| `alt` | TEXT | Alt text description |
| `created_at_photo` | TIMESTAMP | Photo creation date |
| `created_at` | TIMESTAMP | Record creation time |

### 6.3 Table Relationships

```
url_queue (1)
    ├── hotels (N) [via url_id]
    ├── scraping_logs (N) [via url_id]
    └── image_downloads (N) [via hotel_id]

hotels (1)
    ├── image_data (N) [via hotel_id]
    └── image_downloads (N) [via hotel_id]
```

### 6.4 The `done` Field

The `status` field in `url_queue` indicates processing state:

| Status | Meaning |
|--------|---------|
| `pending` | URL awaiting processing |
| `processing` | URL currently being scraped |
| `done` | All languages completed successfully |
| `error` | One or more languages failed after retries |

### 6.5 Language Structure per URL

Each URL is processed for multiple languages. The `languages_completed` and `languages_failed` fields track per-language status as comma-separated values.

Example:
```
languages_completed: "en,es,de,it,fr,pt"
languages_failed: ""
```

Language codes follow ISO 639-1 standard:
- `en`: English
- `es`: Spanish
- `de`: German
- `fr`: French
- `it`: Italian
- `pt`: Portuguese

---

## 7. Configuration

### 7.1 Configuration File: `env.example`

The `env.example` file serves as a template for the `.env` configuration file. It documents all available configuration parameters.

### 7.2 Configuration Parameters

#### Security

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SECRET_KEY` | (generated) | Application secret key |
| `API_KEY` | (empty) | API authentication key |
| `REQUIRE_API_KEY` | false | Enforce API key requirement |

#### Database

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DB_HOST` | localhost | PostgreSQL host |
| `DB_PORT` | 5432 | PostgreSQL port |
| `DB_NAME` | bookingscraper | Database name |
| `DB_USER` | (required) | Database username |
| `DB_PASSWORD` | (required) | Database password |
| `DB_POOL_SIZE` | 10 | Connection pool size |
| `DB_MAX_OVERFLOW` | 5 | Max overflow connections |
| `DB_POOL_TIMEOUT` | 30 | Pool timeout (seconds) |
| `DB_POOL_RECYCLE` | 3600 | Connection recycle time |

#### Redis/Memurai

| Parameter | Default | Description |
|-----------|---------|-------------|
| `REDIS_URL` | redis://localhost:6379/0 | Redis connection URL |
| `REDIS_MAX_CONNECTIONS` | 20 | Max Redis connections |
| `CELERY_BROKER_URL` | redis://localhost:6379/0 | Celery broker |
| `CELERY_RESULT_BACKEND` | redis://localhost:6379/1 | Celery results |

#### Scraper

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SCRAPER_MAX_WORKERS` | 2 | Parallel scraping workers |
| `SCRAPER_REQUEST_TIMEOUT` | 30 | Request timeout (seconds) |
| `SCRAPER_RETRY_DELAY` | 2.0 | Delay between retries |
| `MAX_RETRIES` | 3 | Max retries per URL |
| `MAX_LANG_RETRIES` | 3 | Max retries per language |

#### VPN (NordVPN)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `VPN_ENABLED` | true | Enable VPN rotation |
| `VPN_COUNTRIES` | Spain,Germany,France... | Country list for rotation |
| `VPN_ROTATION_INTERVAL` | 50 | Seconds between rotations |

#### Languages

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ENABLED_LANGUAGES` | en,es,de,it,fr,pt | Languages to scrape |

Note: English (`en`) is always processed first regardless of list order.

#### Browser

| Parameter | Default | Description |
|-----------|---------|-------------|
| `HEADLESS_BROWSER` | false | Run browser without GUI |

#### Logging

| Parameter | Default | Description |
|-----------|---------|-------------|
| `LOG_LEVEL` | INFO | Logging level |
| `LOG_MAX_BYTES` | 10485760 | Max log file size (10MB) |
| `LOG_BACKUP_COUNT` | 5 | Number of backup files |

#### Debug

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DEBUG` | false | Enable debug mode |
| `DEBUG_HTML_SAVE` | false | Save HTML for debugging |
| `DEBUG_HTML_MAX_AGE_HOURS` | 24 | HTML retention time |

### 7.3 Configuration Impact on Execution

| Parameter | Impact |
|-----------|--------|
| `SCRAPER_MAX_WORKERS` | Higher values increase parallelism but may trigger rate limiting |
| `VPN_ROTATION_INTERVAL` | Lower values provide better IP diversity but increase VPN overhead |
| `HEADLESS_BROWSER` | false enables visual debugging; true required for server deployment |
| `DEBUG_HTML_SAVE` | Increases disk usage; useful for troubleshooting extraction issues |
| `MAX_RETRIES` | Higher values improve success rate but increase processing time |

---

## Document Information

| Property | Value |
|----------|-------|
| **Version** | 1.0 |
| **Date** | 2026-03-29 |
| **Status** | Baseline Reference |
| **Purpose** | Pre-audit documentation |

---

*This documentation describes the BookingScraper system as it exists. It is intended to serve as a stable reference for future audits.*
