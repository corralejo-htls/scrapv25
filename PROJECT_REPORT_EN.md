# BookingScraper Pro v6.0 — Project Report (EN)
**Version:** 46 | **Date:** 2026-03-07 | **Platform:** Windows 11 + Python 3.11+ + PostgreSQL 15-18

---

## 1. Issue Summary & Corrections Log

| ID | Sev | File | Description | v46 Status |
|----|-----|------|-------------|------------|
| BUG-001 | Critical | database.py | DB credentials validated at engine creation (deferred) | ✅ Fixed |
| BUG-002 | Critical | models.py | Partial unique index only in comment, not Index() | ✅ Fixed |
| BUG-003 | Critical | requirements.txt | File in app/ not project root | ✅ Fixed |
| BUG-004 | High | config.py | VPN+multi-worker incompatibility validated late | ✅ Fixed |
| BUG-005 | High | models.py | version_id no DB-level trigger | ✅ Fixed in SQL |
| BUG-006 | High | database.py | get_serializable_db() SET TRANSACTION inside active txn | ✅ Fixed |
| BUG-007 | High | install_clean_v43.sql | GIN indexes manual step only | ✅ Fixed in SQL |
| BUG-008 | High | main.py | Version drift v4.0 vs 6.0.0 | ✅ Fixed |
| BUG-009 | Medium | extractor.py | _extract_images() complexity 23 | ✅ Refactored |
| BUG-010 | Medium | config.py | LANGUAGE_EXT["en"]=".en-gb" undocumented dependency | ✅ Documented |
| BUG-011 | Medium | database.py | execute_with_retry() catches broad exceptions | ✅ Fixed |
| BUG-012 | Medium | models.py | ScrapingLog FK gap undocumented | ✅ Fixed (trigger) |
| BUG-014 | Medium | config.py | MAX_ERROR_LEN duplicated | ✅ Fixed (constant) |
| BUG-015 | Low | verify_system.py | Import app.core.database (non-existent) | ✅ Fixed |
| BUG-016 | Low | verify_system.py | Import app.core.config (non-existent) | ✅ Fixed |
| BUG-017 | Low | verify_system.py | Import app.core.database 2nd ref | ✅ Fixed |
| BUG-018 | Low | verify_system.py | Import app.tasks.celery_app (non-existent) | ✅ Fixed |
| BUG-019 | Medium | scraper_service.py | Redis claim catches broad exceptions | ✅ Fixed |
| BUG-020 | Medium | main.py | POSIX signal handler on Windows | ✅ Fixed (RotatingFileHandler) |
| BUG-021 | Low | models.py | ScrapingLog FK absence unexplained | ✅ Fixed (docstring) |
| BUG-022 | Low | completeness_service.py | MAX_LANG_RETRIES hardcoded=1 | ✅ Fixed (.env) |
| BUG-023 | Low | image_downloader.py | Batch timeout too short | ✅ Fixed |
| BUG-024 | Medium | scraper.py | cloudscraper 403 reset loops infinitely | ✅ Fixed |
| BUG-EN-001 | High | scraper_service.py | scrape_one() complexity 63 | ✅ Refactored |
| BUG-EN-002 | High | scraper.py | scrape_hotel() Selenium complexity 37 | ✅ Refactored |
| BUG-EN-003 | Medium | load_urls.py | Bare except swallows KeyboardInterrupt (×3) | ✅ Fixed |

---

## 2. Architecture Map

```
[Entry Points]
  app/main.py          FastAPI + Uvicorn (Windows ProactorEventLoop)
  app/celery_app.py    Celery worker (--pool=threads, Windows required)
  scripts/*.py         CLI utilities
  windows_service.py   SCM registration (pywin32)
  *.bat                15 Windows operational scripts

[Business Logic]
  app/scraper_service.py   URL dispatch, ThreadPoolExecutor, VPN, stats
  app/scraper.py           CloudScraperEngine + SeleniumEngine (fallback)
  app/completeness_service.py  Per-language tracking (MAX_LANG_RETRIES configurable)
  app/image_downloader.py  Parallel image download (bounded timeout)
  app/vpn_manager_windows.py   NordVPN CLI (single-worker only)

[Data Layer]
  app/database.py      SQLAlchemy engine (psycopg v3, Windows tuned)
  app/models.py        ORM: URLQueue, Hotel, ScrapingLog (partitioned), etc.
  app/extractor.py     BeautifulSoup HTML extraction

[Infrastructure]
  PostgreSQL 15-18     Primary store (Windows Service, NTFS)
  Memurai/Redis        Celery broker (Windows-native Redis port)
  NordVPN CLI          IP rotation (optional)
```

---

## 3. Installation Guide

### Prerequisites
- Windows 11 Pro/Enterprise 64-bit
- Python 3.11+ (64-bit): https://python.org/downloads/
- PostgreSQL 15-18: https://www.enterprisedb.com/downloads/
- Memurai (Redis for Windows): https://www.memurai.com/
- Visual C++ Redistributables: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Step-by-step

```powershell
# 1. Enable Long Path Support (run as Administrator)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

# 2. High Performance power plan
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

# 3. Windows Defender exclusions
Add-MpPreference -ExclusionPath "C:\Program Files\PostgreSQL\16\data"
Add-MpPreference -ExclusionPath "C:\BookingScraper"

# 4. Firewall rule for PostgreSQL
New-NetFirewallRule -DisplayName "PostgreSQL 5432" -Direction Inbound `
    -Protocol TCP -LocalPort 5432 -Action Allow -Profile Private
```

```cmd
:: 5. Clone and setup
git clone https://github.com/corralejo-htls/scrapv25.git
cd scrapv25
setup_env.bat

:: 6. Configure credentials
copy .env.example .env
notepad .env          :: Set DB_USER, DB_PASSWORD at minimum

:: 7. Create database schema (BUG-007 FIX: all indexes in one script)
create_db.bat

:: 8. Verify installation
verify_system.bat

:: 9. Start
start_redis.bat
start_server.bat      :: in new window
start_celery.bat      :: in new window
```

### PostgreSQL tuning (postgresql.conf)
```ini
max_connections = 75          # Windows Desktop Heap limit
shared_buffers = 2GB          # 25% RAM
effective_cache_size = 4GB    # 50% RAM
work_mem = 8MB
maintenance_work_mem = 256MB
wal_buffers = 16MB
checkpoint_completion_target = 0.9
random_page_cost = 1.1        # NVMe; use 4.0 for SATA SSD
effective_io_concurrency = 1  # Windows async I/O
log_min_duration_statement = 1000
```

---

## 4. Configuration Reference

| Variable | Default | Required | Notes |
|----------|---------|----------|-------|
| DB_USER | — | ✅ | Validated at import time (BUG-001) |
| DB_PASSWORD | — | ✅ | Validated at import time (BUG-001) |
| DB_NAME | bookingscraper | No | |
| DB_POOL_SIZE | 10 | No | Max 20 (Windows) |
| REDIS_HOST | localhost | No | Memurai recommended |
| SCRAPER_MAX_WORKERS | 4 | No | Max 8; VPN requires =1 |
| VPN_ENABLED | false | No | BUG-004: incompatible with MAX_WORKERS>1 |
| MAX_LANG_RETRIES | 3 | No | BUG-022 FIX: was hardcoded=1 |
| ENABLED_LANGUAGES_STR | en,es,de,fr,it | No | Comma-separated ISO-639-1 |
| LOG_LEVEL | INFO | No | |

---

## 5. Validation Checklist

### Pre-flight
- [ ] Python 3.11+: `python --version`
- [ ] .venv activated: `.venv\Scripts\activate`
- [ ] .env in PROJECT ROOT (not app/)
- [ ] DB_USER and DB_PASSWORD set
- [ ] PostgreSQL service running: `Get-Service postgresql*`
- [ ] Memurai service running: `Get-Service memurai`

### Dependencies (BUG-003 FIX)
- [ ] `pip install -r requirements.txt` (from PROJECT ROOT)
- [ ] `python -c "import psycopg"` — must be v3, NOT psycopg2
- [ ] `python -c "import fastapi, sqlalchemy, celery"`

### Database
- [ ] `psql -U bookingscraper_app -d bookingscraper -c "\dt"` — 6 tables
- [ ] GIN indexes: `SELECT indexname FROM pg_indexes WHERE indexname LIKE '%gin%'`
- [ ] Partial index: `SELECT indexname FROM pg_indexes WHERE indexname='ix_hotels_url_lang_null'`
- [ ] Triggers: `SELECT trigger_name FROM information_schema.triggers WHERE trigger_schema='public'`

### Application
- [ ] `python scripts/verify_system.py` exits 0
- [ ] `uvicorn app.main:app` starts without error
- [ ] `GET http://localhost:8000/health` returns 200

### Windows
- [ ] Defender exclusions set for PostgreSQL data dir and C:\BookingScraper
- [ ] Firewall rule for port 5432
- [ ] High Performance power plan active
- [ ] Long Path Support enabled

---

## 6. Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `EnvironmentError: DB_PASSWORD not set` | .env not loaded or empty | BUG-001 fix — load .env before any import |
| `FileNotFoundError: requirements.txt` | Running from app/ dir | BUG-003 fix — run from project root |
| `ImportError: app.core.database` | Old verify_system.py | BUG-015 fix — use v46 verify_system.py |
| `ImportError: psycopg2` | Wrong driver | Use `psycopg[binary]` (v3), not psycopg2 |
| Duplicate key on hotels | Missing partial index | BUG-002 fix — re-run install_clean_v46.sql |
| Slow JSONB queries | GIN indexes missing | BUG-007 fix — re-run install_clean_v46.sql |
| Celery pool error | Wrong pool type | Always `--pool=threads` on Windows |
| 403 loop on scraping | Unbounded session reset | BUG-024 fix — MAX_SESSION_RESETS=3 |

---
*BookingScraper Pro v6.0 — Technical Report v46 — 2026-03-07*
