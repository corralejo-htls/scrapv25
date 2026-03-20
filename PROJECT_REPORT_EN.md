# BookingScraper Pro v6.0 — Project Report
## Version: 48 | Platform: Windows 11 + Python 3.11+ + PostgreSQL 15+

---

## 1. ISSUE SUMMARY & CORRECTIONS LOG

### Critical Issues Resolved

| ID | Original Severity | File | Fix Applied |
|----|-------------------|------|-------------|
| SCRAP-SEC-001 / BUG-101 | **Critical** | `config.py` | `SECRET_KEY` auto-generates a random secure key if missing/default; logs CRITICAL warning. Default key `change-this-to-a-random-secret-key` is rejected. |
| SCRAP-BUG-009 / BUG-101 | **Critical** | `tasks.py` | SQL injection eliminated. Partition names validated via strict regex `^scraping_logs_\d{4}_(?:0[1-9]|1[0-2])$` before any interpolation. Date literals validated via regex. |
| SCRAP-BUG-004 / BUG-001 | **Critical** | `database.py` | Database URL construction is **lazy** — engine created only on first access, not at import time. Alembic/pytest can import `app.database` without DB credentials. |
| BUG-002 | **Critical** | `main.py` | Multi-process lock fallback now logs an explicit `WARNING` that threading.Lock is NOT safe with `uvicorn --workers > 1`. Deployment guide mandates `workers=1`. |
| BUG-003 / BUG-103 | **Critical** | `models.py`, `install_clean_v48.sql` | ScrapingLog FK absence documented with prominent warning. Trigger `trg_scraping_logs_fk_check` created by SQL script and attached to every partition. |
| BUG-004 | **Critical** | `scraper.py` | `build_language_url()` rewritten. Strips existing language suffix before appending new one. No double-`.html` possible. Tested in `tests/test_config.py`. |

### High Issues Resolved

| ID | Original Severity | File | Fix Applied |
|----|-------------------|------|-------------|
| SCRAP-SEC-002 | High | `config.py` | `API_KEY` still defaults empty but `REQUIRE_API_KEY=true` enforces it at startup with `ValueError`. |
| BUG-102 / SCRAP-BUG-001 | High | `main.py` | `_rate_buckets` has TTL-based eviction (`_RATE_BUCKET_TTL_S=300`). Cleanup runs periodically. Memory is bounded. |
| BUG-104 / SCRAP-CON-003 | High | `scraper_service.py`, `main.py` | Redis uses a `ConnectionPool` singleton. All Redis clients share the pool via `_get_redis_client()`. |
| BUG-006 | High | `database.py` | `get_olap_db()` casts timeout to `int()` before interpolation. |
| BUG-007 | High | `models.py` | Partial unique index `ix_hotels_url_lang_null` documented as requiring `install_clean_v48.sql`. Created explicitly in SQL script. |
| BUG-008 | High | `scraper.py` | `BOOKING_BYPASS_COOKIES` no longer captured at import time. `get_bypass_cookies()` generates fresh random GA IDs on every call. |
| BUG-010 | High | `database.py` | `execute_with_retry()` logs `type(exc).__name__` AND `str(exc)` — full context preserved. |

### Medium Issues Resolved

| ID | Original Severity | File | Fix Applied |
|----|-------------------|------|-------------|
| SCRAP-BUG-005 / BUG-005 | Medium | `config.py` | `ENABLED_LANGUAGES` validated once at `model_validator` time via `@cached_property`. No per-call revalidation. |
| SCRAP-BUG-005 | Medium | `database.py` | `get_readonly_db()` opens with `BEGIN READ ONLY` as the first statement. |
| BUG-013 | Medium | `scraper.py` | `_is_blocked()` wrapped in `try/except`; parse failures return `True` (safe default). |
| BUG-014 | Medium | `config.py` | `DEBUG_HTML_MAX_AGE_HOURS` uses `@field_validator` with `try/except ValueError`. Non-numeric values default to `24` with WARNING. |
| BUG-015 | Medium | `database.py` | `get_pool_status()` returns `error_type` + `error_message` instead of just type name. |
| BUG-016 | Medium | `models.py`, `install_clean_v48.sql` | `chk_uls_status_valid` constraint includes `'incomplete'`. |
| BUG-017 | Medium | `config.py` | `LANGUAGE_EXT` keys validated against `ENABLED_LANGUAGES` in `model_validator`. Missing mappings default to ISO code with WARNING. |
| SCRAP-BUG-010 | Medium | `vpn_manager_windows.py` | Country names validated against `_VALID_VPN_COUNTRIES` canonical set. Subprocess uses `shell=False` with list arguments. |
| BUG-108 | Medium | `vpn_manager_windows.py` | Subprocess failures log `returncode`, `stderr`, `stdout` for full diagnostics. |
| SCRAP-BUG-014 | Medium | `extractor.py` | `lxml` parser with `html.parser` stdlib fallback. `FeatureNotFound` caught. |
| BUG-107 | Medium | `extractor.py` | 5-strategy language detection: html-lang, meta content-language, og:locale, meta[name=language], URL path. |
| SCRAP-BUG-016 | Medium | `scraper_service.py` | `max_workers` clamped to `SCRAPER_MAX_WORKERS` at runtime. |
| SCRAP-BUG-017 | Medium | `scraper_service.py` | Worker timeout from `settings`, not hardcoded. |
| SCRAP-BUG-019 | Medium | `windows_service.py` | `_SHUTDOWN_TIMEOUT_MS = 30_000` (was too short). |
| SCRAP-BUG-023 | Medium | `completeness_service.py` | `update_language_status()` uses `SELECT FOR UPDATE` to prevent race conditions. |
| SCRAP-BUG-024 | Medium | `main.py` | URL validation uses regex + netloc check. Rejects non-HTTPS, non-booking.com, path injection. |
| SCRAP-BUG-028 | Medium | `tasks.py` | All tasks assigned to named queues (`maintenance`, `monitoring`, `default`). |
| SCRAP-BUG-033 | Medium | `tasks.py` | Partition creation uses `get_serializable_db()`. |
| SCRAP-BUG-034 | Medium | `completeness_service.py` | State machine transition table `_VALID_TRANSITIONS` rejects invalid moves. |
| Circuit Breaker | Medium | `vpn_manager_windows.py` | `is_open` check + state change atomised via `_is_open_unsafe()` with lock held. |

### Low Issues Resolved

| ID | Original Severity | File | Fix Applied |
|----|-------------------|------|-------------|
| BUG-106 | Low | `scraper.py` | SHA-256 replaces MD5 for filename generation (`url_to_filename()`). |
| BUG-018 | Low | `scraper.py` | `USER_AGENTS_WIN` weighted by real market share. `random.choices()` with weights. |
| BUG-019 | Low | `models.py` | `SystemMetrics` gets composite indexes on `(recorded_at, cpu_usage)` and `(recorded_at, memory_usage)`. |
| BUG-111 | Low | `alembic.ini` | `script_location = migrations`. Directory created with `env.py` and `script.py.mako`. |
| BUG-112 | Low | All | Unified JSON structured logging format across all modules. |
| Version drift | Low | All | Single source of truth: `APP_VERSION="6.0.0"`, `BUILD_VERSION=48` in `app/__init__.py`. |
| Dead code | Low | `database.py` | `log_pool_status()` retained as documented utility function. |

---

## 2. ARCHITECTURE MAP

```
Windows 11 Desktop — Single-Node Deployment
═══════════════════════════════════════════════════════════════
│
│  ENTRY POINTS
│  ┌────────────────────┐  ┌──────────────────────────────┐
│  │   main.py          │  │   windows_service.py         │
│  │   FastAPI/Uvicorn  │  │   Windows SCM Integration    │
│  │   Port 8000        │  │   Auto-start on boot         │
│  │   workers=1 ⚠️     │  │   30s graceful shutdown      │
│  └────────┬───────────┘  └──────────────────────────────┘
│           │
│  MIDDLEWARE
│  ┌────────────────────────────────────────────────────────┐
│  │  Rate Limiter (TTL-bounded dict, 10 rps/IP)           │
│  │  CORS Middleware (localhost only)                      │
│  │  API Key Auth (optional Bearer token)                  │
│  └────────┬───────────────────────────────────────────────┘
│           │
│  BUSINESS LOGIC
│  ┌────────────────────┐  ┌────────────────────────────────┐
│  │  scraper_service   │  │  completeness_service          │
│  │  - ThreadPoolExec  │  │  - SELECT FOR UPDATE           │
│  │  - Redis distrib.  │  │  - State machine validation    │
│  │    lock (pool)     │  │  - Multi-language tracking     │
│  └────────┬───────────┘  └────────────────────────────────┘
│           │
│  ┌────────────────────┐  ┌────────────────────────────────┐
│  │  scraper.py        │  │  extractor.py                  │
│  │  - CloudScraper    │  │  - 5-strategy lang detection   │
│  │  - SeleniumEngine  │  │  - lxml / html.parser fallback │
│  │  - Weighted UA     │  │  - Structured field extraction │
│  │  - SHA-256 names   │  └────────────────────────────────┘
│  └────────────────────┘
│
│  TASK QUEUE (Celery / Redis broker)
│  ┌────────────────────────────────────────────────────────┐
│  │  tasks.py                                              │
│  │  - ensure_log_partitions (validated SQL, SERIALIZABLE) │
│  │  - purge_old_debug_html                                │
│  │  - collect_system_metrics                              │
│  │  - reset_stale_processing_urls                         │
│  └────────┬───────────────────────────────────────────────┘
│           │
│  DATA ACCESS (lazy engine — no import-time failures)
│  ┌────────────────────────────────────────────────────────┐
│  │  database.py                                           │
│  │  - get_db()            READ/WRITE session              │
│  │  - get_readonly_db()   BEGIN READ ONLY                 │
│  │  - get_olap_db()       statement_timeout per session   │
│  │  - get_serializable_db() SERIALIZABLE isolation        │
│  │  - execute_with_retry() exponential backoff            │
│  └────────┬───────────────────────────────────────────────┘
│           │
│  STORAGE
│  ┌────────────────────┐  ┌───────────────┐  ┌───────────┐
│  │  PostgreSQL 15+    │  │  Redis/Memurai│  │  NordVPN  │
│  │  Windows Service   │  │  Broker+Cache │  │  CLI      │
│  │  max_conn=50       │  │  Pool=20 conn │  │  Optional │
│  │  Partitioned logs  │  └───────────────┘  └───────────┘
│  │  FK triggers       │
│  └────────────────────┘
═══════════════════════════════════════════════════════════════
```

---

## 3. INSTALLATION GUIDE (Windows 11 — Clean Environment)

### Prerequisites Checklist

- [ ] Windows 11 Pro or Enterprise (21H2+)
- [ ] "High Performance" power plan enabled (`powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c`)
- [ ] PostgreSQL 16 installed via [EnterpriseDB installer](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- [ ] Redis or [Memurai](https://www.memurai.com/) installed and running
- [ ] Python 3.11+ x64 installed from [python.org](https://www.python.org/downloads/)
- [ ] Git installed
- [ ] Visual C++ Redistributables installed (required for lxml wheels)
- [ ] Long Path Support enabled:
  ```
  reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
  ```

### Windows Defender Exclusions (REQUIRED before installation)

```powershell
# Run as Administrator
Add-MpPreference -ExclusionPath "C:\Program Files\PostgreSQL"
Add-MpPreference -ExclusionPath "C:\Program Files\Redis"
Add-MpPreference -ExclusionPath "C:\BookingScraper"
Add-MpPreference -ExclusionProcess "python.exe"
Add-MpPreference -ExclusionProcess "celery.exe"
```

### Firewall Rule

```powershell
# PostgreSQL port (local access only — do NOT open to network on single-node)
New-NetFirewallRule -DisplayName "PostgreSQL Local" -Direction Inbound `
  -LocalPort 5432 -Protocol TCP -Action Allow -RemoteAddress LocalSubnet
```

### Step-by-Step Installation

```batch
REM 1. Clone repository
git clone https://github.com/corralejo-htls/scrapv25.git BookingScraper
cd BookingScraper

REM 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate.bat

REM 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

REM 4. Configure environment
copy .env.example .env
REM  → Edit .env: set DB_USER, DB_PASSWORD, SECRET_KEY (mandatory)

REM 5. Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE bookingscraper;"

REM 6. Apply schema (REQUIRED — not just create_tables.py)
psql -U postgres -d bookingscraper -f install_clean_v48.sql

REM 7. Verify system
python scripts\verify_system.py

REM 8. Load URLs
python scripts\load_urls.py urls_ejemplo.csv

REM 9. Start services (3 terminals)
start_api.bat         (Terminal 1 — API server)
start_worker.bat      (Terminal 2 — Celery worker)
start_beat.bat        (Terminal 3 — Celery Beat scheduler)
```

### PostgreSQL Windows 11 Configuration

Edit `C:\Program Files\PostgreSQL\16\data\postgresql.conf`:

```conf
max_connections             = 50
shared_buffers              = 512MB
effective_cache_size        = 1536MB
work_mem                    = 8MB
maintenance_work_mem        = 128MB
wal_buffers                 = 16MB
checkpoint_completion_target = 0.9
random_page_cost            = 1.1
effective_io_concurrency    = 1
log_min_duration_statement  = 1000
autovacuum                  = on
```

---

## 4. CONFIGURATION REFERENCE

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | **Yes** | auto-generated | 48+ char random key. Set in `.env`. |
| `DB_USER` | **Yes** | — | PostgreSQL username |
| `DB_PASSWORD` | **Yes** | — | PostgreSQL password |
| `DB_NAME` | No | `bookingscraper` | Database name |
| `DB_POOL_SIZE` | No | `10` | SQLAlchemy pool size |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis connection URL |
| `SCRAPER_MAX_WORKERS` | No | `2` | Thread pool size (max 4) |
| `ENABLED_LANGUAGES` | No | `es,en,de,fr,it,nl,pt` | ISO 639-1 codes |
| `VPN_ENABLED` | No | `false` | Enable NordVPN rotation |
| `REQUIRE_API_KEY` | No | `false` | Enforce Bearer token auth |

---

## 5. VALIDATION CHECKLIST (Post-Installation)

- [ ] `python scripts/verify_system.py` — all 5 checks pass
- [ ] `curl http://localhost:8000/health` — returns `{"status":"healthy"}`
- [ ] `psql -U bookingscraper_user -d bookingscraper -c "\dt"` — lists 6+ tables
- [ ] `psql -d bookingscraper -c "SELECT tablename FROM pg_tables WHERE tablename LIKE 'scraping_logs_%'"` — shows partition tables
- [ ] `psql -d bookingscraper -c "SELECT tgname FROM pg_trigger WHERE tgname = 'trg_scraping_logs_fk_check' LIMIT 1"` — trigger present
- [ ] `python scripts/load_urls.py urls_ejemplo.csv` — reports `inserted > 0`
- [ ] `curl -X POST http://localhost:8000/scraping/force-now` — returns `{"status":"dispatched",...}`
- [ ] Check `logs/bookingscraper.log` for JSON-formatted entries
- [ ] Windows Event Viewer → Application Log — BookingScraper entries visible

---

## 6. TROUBLESHOOTING

| Symptom | Cause | Resolution |
|---------|-------|------------|
| `EnvironmentError: DB_PASSWORD is not configured` | `.env` not loaded or DB_PASSWORD empty | Ensure `.env` exists with `DB_PASSWORD=...` set |
| `CRITICAL: SECRET_KEY is not configured` | `SECRET_KEY` missing from `.env` | Copy the generated key from the log into `.env` |
| `ConnectionRefusedError` on startup | PostgreSQL not running | Start PostgreSQL Windows service |
| `rate limit exceeded` on API | Too many requests from client | Increase `_RATE_LIMIT_RPS` or add client-side retry |
| `StaleDataError` from SQLAlchemy | Concurrent updates to same URL | Retry logic handles this; check `version_id` usage |
| Selenium driver not found | ChromeDriver not installed | Set `CHROMEDRIVER_PATH` env var or install `webdriver-manager` |
| VPN connect fails | NordVPN not installed | Set `VPN_ENABLED=false` |
| Slow partition creation | PostgreSQL autovacuum interference | Schedule `ensure_log_partitions` at low-traffic hours |
| Alembic fails with `No migrations dir` | `migrations/` deleted | Re-create `migrations/` with `env.py` from repo |

---

## 7. RISKS & REMAINING CONSIDERATIONS

| Risk | Impact | Mitigation |
|------|--------|------------|
| Single point of failure (no HA) | High | Daily `pg_dump` backup; Windows VSS snapshots |
| Windows Update service restart | Medium | Configure maintenance window; service auto-restart |
| Booking.com DOM changes | High | CSS selectors in `extractor.py` may need updates; monitor 404 rate |
| Desktop Heap exhaustion | Medium | `max_connections=50` in postgresql.conf; pool_size=10 |
| Single uvicorn worker | Low | Intentional for Windows 11 desktop; scale up to server if needed |

