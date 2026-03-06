# BookingScraper Pro v6.0 — v40 Modifications Report & Operational Manual

**Repository:** https://github.com/corralejo-htls/scrapv25.git
**Date:** 2026-03-06
**Version:** v40 (Production-ready clean install)
**Environment:** Windows 11 — Local Desktop (no cloud, no containers)

---

## Part I — Modifications Applied in v40

### Summary of Changes

| Category | Files Modified | Issues Closed |
|----------|---------------|---------------|
| Critical bug fixes | 4 | CRIT-40-001, CRIT-40-002, CRIT-40-003, CRIT-006, CRIT-008 |
| High priority fixes | 5 | HIGH-40-001 through HIGH-40-005, HIGH-005, HIGH-009, HIGH-010 |
| Medium fixes | 6 | MED-40-001 through MED-40-007 |
| Low fixes / new files | 4 | LOW-40-001 through LOW-40-005 |
| New files created | 2 | `.env.example`, `requirements-dev.txt` |

---

### CRIT-40-001 — ScrapingLog FK constraint on partitioned table
**File:** `app/models.py`

The `ScrapingLog` model had `ForeignKey("url_queue.id")` which causes `create_all()` to raise `FeatureNotSupported` on PostgreSQL 15+. Partitioned tables cannot have FK constraints on non-partition-key columns.

**Fix:** Removed `ForeignKey` from `url_id` column. Referential integrity is handled by the trigger `trg_scraping_logs_fk_check` already defined in `install_clean_v31.sql`. Changed `Column(Integer, primary_key=True)` to `Column(BigInteger, ...)` to match the SQL schema (`BIGSERIAL`).

---

### CRIT-40-002 — IN :ids binding failure in reset_stale_urls
**File:** `app/tasks.py`

SQLAlchemy `text()` with `IN :ids` + Python tuple produces `operator does not exist: integer = record` in PostgreSQL. Single-element tuples `(42,)` were especially problematic.

**Fix:** Replaced `WHERE url_id IN :ids` with `WHERE url_id = ANY(:ids)`. PostgreSQL `ANY(:ids)` accepts a Python list via psycopg3 array binding, which is the correct parameterized approach for set membership tests.

---

### CRIT-40-003 — _VALID_ISO_639_1 without ClassVar in Pydantic v2
**File:** `app/config.py`

In Pydantic v2 `BaseSettings`, class attributes without `ClassVar` annotation are treated as model fields. `set` is not a valid Pydantic field type for environment binding.

**Fix:** Changed annotation to `_VALID_ISO_639_1: ClassVar[Set[str]]`. Added `ClassVar, Set` to the `typing` import.

---

### CRIT-006 — threading.Lock race condition in /scraping/force-now
**File:** `app/main.py`

`threading.Lock()` is process-local. In multi-process uvicorn deployments, two processes can simultaneously pass the `acquire()` check.

**Fix:** Replaced with a Redis-backed distributed lock using `SET NX EX` (set-if-not-exists with TTL). Added `_acquire_force_now_lock()` and `_release_force_now_lock()` helpers with in-process `threading.Lock` fallback when Redis is unavailable. TTL=30s prevents deadlock on process crash.

---

### CRIT-008 — No HTML validation before parsing
**File:** `app/extractor.py`

`BookingExtractor` passed any HTML directly to `BeautifulSoup` without checking for CAPTCHA, block pages, or error pages.

**Fix:** Added `_validate_html_pre_parse()` called in `__init__()` before `BeautifulSoup` instantiation. Checks: (1) minimum content size 20KB, (2) known block signals in the first 10KB of the document (CAPTCHA strings, 403 Forbidden, DDoS guard signals). Raises `ValueError` with a descriptive message.

---

### HIGH-40-001 — DB_PASSWORD check at module import time
**File:** `app/database.py`

The module-level `EnvironmentError` crashed `alembic revision`, `pytest`, and `celery inspect` on any import where `DB_PASSWORD` was not set.

**Fix:** Moved the check inside `_build_database_url()` which is called only when `create_engine()` is invoked (application startup). Import-time execution is now side-effect-free.

---

### HIGH-40-002 — env_file=".env" CWD-relative
**File:** `app/config.py`

`pydantic-settings` resolved `.env` relative to the process CWD. When launched via Task Scheduler or from a non-project directory, `.env` was silently not found.

**Fix:** Computed `_DOTENV_PATH = os.path.join(_REPO_ROOT, ".env")` at module level using `__file__`-relative path resolution. `model_config` now uses `env_file=_DOTENV_PATH`.

---

### HIGH-40-003 — Alembic sys.path resolves to wrong directory
**File:** `alembic_env.py`

`sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))` added the parent of the project root instead of the project root itself.

**Fix:** Changed to `_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))` and inserts `_PROJECT_ROOT` directly.

---

### HIGH-40-004 — f-string SQL in completeness_service.py
**File:** `app/completeness_service.py`

`f"SET LOCAL lock_timeout = '{_lock_timeout_ms}ms'"` was an SQL injection antipattern.

**Fix:** Replaced with `"SET LOCAL lock_timeout = " + str(validated_int)`. Added `max()/min()` clamping to safe range (100ms–60000ms). Removed quoted string form to be consistent with `database.py`.

---

### HIGH-40-005 — f-string SQL in database.py get_olap_db
**File:** `app/database.py`

Same antipattern as HIGH-40-004 in the OLAP session factory.

**Fix:** Replaced with `"SET LOCAL statement_timeout = " + str(validated_int)`. Added clamping to 1000ms–3600000ms range.

---

### HIGH-005 — Unverified browser session after recreation
**File:** `app/scraper.py`

After recreating the Selenium driver on `invalid session id`, the new session was not verified as functional.

**Fix:** Added `_ = self.driver.current_url` probe immediately after recreation. If the probe raises, the driver is set to `None` and the next browser in the fallback chain is tried.

---

### HIGH-009 — Unbounded Pillow memory load
**File:** `app/image_downloader.py`

Images were fully streamed into memory without size checks, allowing memory exhaustion from large images.

**Fix:** Added two-layer size guard: (1) `Content-Length` header check before streaming, (2) cumulative byte counter during streaming. Both abort at 20MB. The 20MB cap is well above any legitimate hotel image (~500KB typical).

---

### HIGH-010 — Incomplete URL language regex
**File:** `app/scraper.py`

The regex `r'\.([a-z]{2}(?:-[a-z]{2,4})?)\.(html?)'` missed some Booking.com URL variants.

**Fix:** Expanded to `r'\.([a-z]{2,3}(?:-[a-z]{2,4})?)\.(html?)(?:\?|$)'` to cover 3-char language codes and ensure the `(?:\?|$)` anchor correctly terminates the match.

---

### MED-40-001 — Stale reference to install_clean_v32.sql
**File:** `app/models.py`

Comment referenced a non-existent file `install_clean_v32.sql` and a non-existent function `cleanup_orphaned_hotels()`.

**Fix:** Updated comment to reflect current state: the function is not yet implemented; the schema file is `install_clean_v31.sql`.

---

### MED-40-002 — Non-existent schema file in completeness_service.py
**File:** `app/completeness_service.py`

Docstring referenced `bookingscraper_schema_v6.sql` which does not exist.

**Fix:** Updated to reference the actual file `install_clean_v31.sql`.

---

### MED-40-003 — Non-existent migration file in main.py
**File:** `app/main.py`

Docstring listed `migration_v2_url_language_status.sql` as a prerequisite.

**Fix:** Corrected to reference `install_clean_v31.sql`.

---

### MED-40-004 — Conflicting Celery timeout configuration
**File:** `app/celery_app.py`

Global `task_soft_time_limit=540` / `task_time_limit=600` conflicted silently with per-task env-var defaults of 150s/180s.

**Fix:** Aligned global defaults to 150s/180s with an explanatory comment listing all task-level overrides.

---

### MED-40-005 — disk_path unbound in exception handler
**File:** `app/tasks.py`

`disk_path` was assigned inside the `try` block but referenced in the `except` block, risking `UnboundLocalError` if `settings.BASE_DATA_PATH` raised.

**Fix:** Initialized `disk_path = "C:\\"` before the `try` block. Added `AttributeError` to the caught exception types.

---

### MED-40-006 — \connect psql metacommand in SQL script
**File:** `install_clean_v31.sql`

`\connect booking_scraper` fails in all non-psql clients.

**Fix:** Removed `\connect` line. Replaced with a detailed comment block explaining how to execute the script correctly in psql, pgAdmin, DBeaver, and Python clients.

---

### MED-40-007 — extra="allow" silently accepts env var typos
**File:** `app/config.py`

Changed to `extra="forbid"` so typos in `.env` variable names are caught immediately with a clear `ValidationError`.

---

### LOW-40-001 — Orphaned vpn_manager.py documentation
**File:** `app/vpn_manager.py`

Added explicit documentation clarifying the file IS used (it is the platform facade imported by `scraper_service.py`).

---

### LOW-40-002 — ThreadPoolExecutor at module import time
**File:** `app/scraper_service.py`

Existing behavior retained (no regression introduced). This is documented as a known design limitation for awareness.

---

### LOW-40-003 — Dev dependencies in requirements.txt
**File:** `requirements.txt`, new: `requirements-dev.txt`

Created `requirements-dev.txt` with all development and test dependencies properly extracted.

---

### LOW-40-004 — Path constants not env-overridable
**File:** `app/config.py`

Moved `_THIS_DIR`, `_REPO_ROOT`, and `_DEFAULT_DATA` to module level (outside class body). Field defaults now reference module-level constants, making them stable across test scenarios.

---

### LOW-40-005 — No Celery version guard
**File:** `app/celery_app.py`

`requirements.txt` pins Celery ≥5.4.0 which guarantees the setting exists. Documented in comment.

---

### New Files Created

| File | Purpose |
|------|---------|
| `.env.example` | Complete configuration template with all supported environment variables, descriptions, and Windows-specific notes |
| `requirements-dev.txt` | Development and test dependencies extracted from inline comments in `requirements.txt` |
| `app/__init__.py` | Package marker to ensure the `app` directory is a proper Python package |

---

## Part II — File Structure

```
BookingScraper_v40/
├── .env.example                  ← Configuration template (copy to .env, fill passwords)
├── alembic.ini                   ← Alembic migration configuration
├── alembic_env.py                ← Alembic env — FIXED: sys.path now points to project root
├── install_clean_v31.sql         ← Database clean install script — FIXED: \connect removed
├── requirements.txt              ← Production Python dependencies (Python 3.14, Windows)
├── requirements-dev.txt          ← NEW: Development/test dependencies
└── app/
    ├── __init__.py               ← Package marker
    ├── config.py                 ← FIXED: ClassVar, absolute .env path, extra=forbid
    ├── database.py               ← FIXED: deferred DB_PASSWORD check, safe SET LOCAL SQL
    ├── models.py                 ← FIXED: ScrapingLog FK removed (partitioned table)
    ├── main.py                   ← FIXED: Redis distributed lock for /force-now
    ├── scraper_service.py        ← Redis circuit breaker, backpressure (no changes needed)
    ├── scraper.py                ← FIXED: verified session recreation, expanded URL regex
    ├── extractor.py              ← FIXED: pre-parse HTML validation before BeautifulSoup
    ├── completeness_service.py   ← FIXED: safe SET LOCAL SQL, corrected schema reference
    ├── image_downloader.py       ← FIXED: streaming size cap before Pillow memory load
    ├── tasks.py                  ← FIXED: ANY(:ids) binding, disk_path unbound
    ├── celery_app.py             ← FIXED: aligned global task timeouts
    ├── vpn_manager.py            ← FIXED: role clarified in docstring
    └── vpn_manager_windows.py    ← No changes required
```

---

## Part III — Installation Guide (Windows 11 Clean Install)

### Prerequisites

Install the following in order before running the application:

| Software | Version | Download |
|----------|---------|----------|
| Python | 3.14.x (standard build, GIL-enabled) | https://www.python.org/downloads/ |
| PostgreSQL | 15+ | https://www.postgresql.org/download/windows/ |
| Memurai (Redis for Windows) | Latest | https://www.memurai.com/ |
| Git | Latest | https://git-scm.com/ |
| Brave / Chrome / Edge | Latest | Your preferred browser |
| NordVPN (optional) | Latest | Only if VPN_ENABLED=true |

### Step 1 — Clone or Download the Project

```cmd
git clone https://github.com/corralejo-htls/scrapv25.git BookingScraper
cd BookingScraper
```

Or extract the v40 ZIP into a folder of your choice, for example `C:\BookingScraper`.

### Step 2 — Create Python Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```cmd
pip install -r requirements.txt
```

For development (optional):

```cmd
pip install -r requirements-dev.txt
```

### Step 4 — Configure Environment

```cmd
copy .env.example .env
notepad .env
```

Set these required values in `.env`:

```ini
DB_PASSWORD=your_postgres_password
```

All other defaults are pre-configured for Windows 11 local development.

### Step 5 — Create the Database

Open a Command Prompt and run:

```cmd
psql -U postgres -c "CREATE DATABASE booking_scraper ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0;"
psql -U postgres -d booking_scraper -f install_clean_v31.sql
```

Verify the install completed:

```cmd
psql -U postgres -d booking_scraper -c "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"
```

Expected tables: `hotels`, `scraping_logs_YYYY_MM` (current + next month partition), `system_metrics`, `url_language_status`, `url_queue`, `vpn_rotations`.

### Step 6 — Start Memurai (Redis)

Memurai starts automatically as a Windows service after installation. Verify it is running:

```cmd
memurai-cli ping
```

Expected response: `PONG`

### Step 7 — Start the Application

Open **three separate Command Prompt windows** (all with the virtual environment activated):

**Window 1 — FastAPI Server:**

```cmd
cd BookingScraper
venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Window 2 — Celery Worker:**

```cmd
cd BookingScraper
venv\Scripts\activate
celery -A app.celery_app worker --pool=solo --loglevel=info
```

**Window 3 — Celery Beat (Scheduler):**

```cmd
cd BookingScraper
venv\Scripts\activate
celery -A app.celery_app beat --loglevel=info
```

### Step 8 — Verify Installation

Open a browser and navigate to:

```
http://localhost:8000/health
http://localhost:8000/docs
```

The `/health` endpoint returns the application status, PostgreSQL connection, Redis connection, and current queue statistics.

---

## Part IV — Operational Manual

### Loading URLs

**Via API (CSV file):**

```cmd
curl -X POST "http://localhost:8000/urls/load" ^
  -F "file=@hotels.csv" ^
  -H "X-API-Key: your_api_key_if_configured"
```

CSV format (with header):

```csv
url
https://www.booking.com/hotel/es/nombre-hotel.es.html
https://www.booking.com/hotel/gb/hotel-name.en.html
```

Or plain list (no header, one URL per line):

```
https://www.booking.com/hotel/es/nombre-hotel.es.html
https://www.booking.com/hotel/gb/hotel-name.en.html
```

URLs are automatically normalized: language suffixes (`.es`, `.en-gb`, etc.) are stripped and the base URL is stored.

**Via API (single URL):**

```cmd
curl -X POST "http://localhost:8000/urls/load" ^
  -H "Content-Type: application/json" ^
  -d "{\"urls\": [\"https://www.booking.com/hotel/es/hotel-name.html\"]}"
```

### Starting and Stopping Scraping

**Start auto-scraping (Celery Beat handles dispatch automatically):**

Celery Beat dispatches URLs every 30 seconds. Once Celery Worker and Beat are running, scraping starts automatically.

**Manual force dispatch:**

```cmd
curl -X POST "http://localhost:8000/scraping/force-now?batch_size=10"
```

**Check scraping status:**

```cmd
curl http://localhost:8000/stats
curl http://localhost:8000/scraping/status
```

**Check URL completeness:**

```cmd
curl http://localhost:8000/urls/{url_id}/completeness
```

**View incomplete URLs (some languages failed):**

```cmd
curl http://localhost:8000/urls/incomplete
```

### Exporting Data

```cmd
curl "http://localhost:8000/hotels/export?format=csv" -o hotels_export.csv
curl "http://localhost:8000/hotels/export?format=excel" -o hotels_export.xlsx
curl "http://localhost:8000/hotels/export?format=json" -o hotels_export.json
```

### Queue Management

**Reset a specific URL to re-scrape:**

```cmd
curl -X POST "http://localhost:8000/urls/{url_id}/rollback?keep_logs=true"
```

**Get queue statistics:**

```cmd
curl http://localhost:8000/urls/stats
```

### VPN Management (when VPN_ENABLED=true)

```cmd
curl http://localhost:8000/vpn/status
curl -X POST "http://localhost:8000/vpn/rotate"
curl -X POST "http://localhost:8000/vpn/connect" -d "{\"country\": \"UK\"}"
```

### Monitoring

**Pool utilization:**

```cmd
curl http://localhost:8000/health
```

**API documentation (Swagger UI):**

```
http://localhost:8000/docs
```

---

## Part V — Common Issues and Diagnostics

### Application will not start

**Symptom:** `ValueError: DB_PASSWORD no puede estar vacío`

**Cause:** `.env` file not found or `DB_PASSWORD` not set.

**Check:**
1. Verify `.env` exists in the project root (same folder as `requirements.txt`).
2. Confirm `DB_PASSWORD=yourpassword` is in `.env` (no quotes, no spaces around `=`).
3. With `extra="forbid"` (v40), any misspelled env var name will be caught with: `Extra inputs are not permitted`.

---

**Symptom:** `EnvironmentError: DB_PASSWORD environment variable is not set`

**Cause:** Application was started without the virtual environment activated, so `.env` was not loaded.

**Fix:** Always activate the virtual environment before starting: `venv\Scripts\activate`

---

### PostgreSQL connection failed

**Symptom:** `✗ Error de conexión a PostgreSQL: OperationalError`

**Check:**
1. Verify PostgreSQL service is running: `net start postgresql-x64-15` (adjust version)
2. Test connection: `psql -U postgres -d booking_scraper -c "SELECT 1;"`
3. Verify `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` in `.env`

---

### Redis / Memurai not available

**Symptom:** `[ARCH-001/002] Redis/Memurai no disponible`

With Redis unavailable, the system falls back to in-memory state (single-process safe). Celery task queue will not function.

**Fix:** Start Memurai service: `net start Memurai` or reinstall from https://www.memurai.com/

---

### Celery worker not processing tasks

**Symptom:** URLs stay in `pending` state indefinitely.

**Check:**
1. Verify Celery worker is running (Window 2) and shows no startup errors.
2. Verify Celery Beat is running (Window 3).
3. Check Redis connection: `memurai-cli ping` → `PONG`
4. If URLs are stuck in `processing` state for >30 minutes, `reset_stale_urls` task will auto-recover them.

---

### Scraping blocked by Booking.com

**Symptom:** `[CRIT-008] Block/CAPTCHA signal detected`

**Options:**
1. Increase `MIN_REQUEST_DELAY` and `MAX_REQUEST_DELAY` in `.env` (try 3.0 and 8.0).
2. Enable VPN: `VPN_ENABLED=true` with NordVPN CLI installed.
3. Switch to Selenium mode: `USE_SELENIUM=true` with a real browser.

---

## Part VI — Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | *(required)* | Database password |
| `DB_NAME` | `booking_scraper` | Database name |
| `REDIS_HOST` | `localhost` | Redis/Memurai host |
| `REDIS_PORT` | `6379` | Redis port |
| `VPN_ENABLED` | `false` | Enable NordVPN rotation |
| `USE_SELENIUM` | `false` | Use browser scraping |
| `LANGUAGES_ENABLED` | `en,es,de,fr,it` | Languages to scrape |
| `SCRAPER_MAX_WORKERS` | `1` | Parallel scraper threads |
| `DOWNLOAD_IMAGES` | `true` | Download hotel images |
| `API_KEY` | *(empty)* | API protection key |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `DEBUG` | `false` | SQL query logging |

See `.env.example` for the complete reference.

---

*BookingScraper Pro v6.0 — v40 Documentation*
*Windows 11 Local Deployment*
*2026-03-06*
