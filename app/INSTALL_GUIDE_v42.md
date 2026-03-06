# BookingScraper Pro v42 — Installation and Verification Guide

**Date:** 2026-03-06  
**Environment:** Windows 11 Local | PostgreSQL 15+ / 18+  
**Script:** `app/install_clean_v42.sql`  
**Fixes:** All errors from Audit Report v37 + all execution errors from v41

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [What Changed from v41](#2-what-changed-from-v41)
3. [Pre-Installation Checklist](#3-pre-installation-checklist)
4. [Installation Procedure](#4-installation-procedure)
5. [Expected Output Reference](#5-expected-output-reference)
6. [Post-Installation Verification](#6-post-installation-verification)
7. [Troubleshooting](#7-troubleshooting)
8. [Schema Reference](#8-schema-reference)
9. [Full Fix History v37 to v42](#9-full-fix-history-v37-to-v42)

---

## 1. Prerequisites

| Component | Minimum | Tested | Verification command |
|-----------|---------|--------|----------------------|
| PostgreSQL | 15.x | 18.1 | `pg_isready -U postgres -h localhost` |
| psql CLI | 15.x | 18.1 | `psql --version` |
| Windows | 10/11 | 11 x64 | — |

If `psql` is not found, add `C:\Program Files\PostgreSQL\<version>\bin` to the system PATH.

---

## 2. What Changed from v41

Three new execution errors were found during v41 testing and are fixed in v42.

### NEW-EXEC-001 — `DROP DATABASE` cannot run inside a `DO $$` block

**v41 error:**
```
ERROR: DROP DATABASE no puede ser ejecutado desde una funcion
```

PostgreSQL prohibits `DROP DATABASE` (and `CREATE DATABASE`) inside any PL/pgSQL function or anonymous `DO $$` block. v41 used `EXECUTE 'DROP DATABASE ...'` inside a `DO $$`, which always fails.

**v42 fix:** Uses psql `\if` / `\gset` metacommands to conditionally execute `DROP DATABASE` as a **top-level SQL statement**, which is the only valid context for this command.

```sql
-- Store current database into psql variable
SELECT (current_database() = 'postgres') AS in_postgres_ctx \gset

-- Conditionally execute top-level DDL
\if :in_postgres_ctx
DROP DATABASE IF EXISTS booking_scraper;
CREATE DATABASE booking_scraper ...;
\endif
```

### NEW-EXEC-002 — Bare `RAISE NOTICE` is invalid top-level SQL

**v41 error:**
```
ERROR: error de sintaxis en o cerca de «RAISE»
LINEA 1: RAISE NOTICE '  [OK] ANALYZE complete...
```

`RAISE NOTICE` is PL/pgSQL syntax and can only run inside a `DO $$` block or a function body. v41 placed a bare `RAISE NOTICE` as the last line of the script after the `ANALYZE` statement.

**v42 fix:** Every standalone `RAISE NOTICE` is wrapped in a `DO $$ BEGIN ... END $$;` block:

```sql
DO $$ BEGIN RAISE NOTICE '  [OK] ANALYZE complete - statistics initialized.'; END $$;
DO $$ BEGIN RAISE NOTICE '  BookingScraper Pro v42 is ready.'; END $$;
```

### NEW-EXEC-003 — Residual views from prior installs cause `Views: 4 / 2`

**v41 warning:**
```
WARNING: [POST-VERIFY] Expected 2 views, found 4. Unexpected objects in schema.
```

When Step 1 fails to drop the database (due to NEW-EXEC-001), Step 2 runs against the existing `booking_scraper` that may already contain views from a prior installation. `CREATE OR REPLACE VIEW` updates the definition but does not change the view count.

**v42 fix:** Explicit `DROP VIEW IF EXISTS` before each `CREATE OR REPLACE VIEW`:

```sql
DROP VIEW IF EXISTS v_scraping_dashboard;
CREATE OR REPLACE VIEW v_scraping_dashboard AS ...;

DROP VIEW IF EXISTS v_language_completeness;
CREATE OR REPLACE VIEW v_language_completeness AS ...;
```

---

## 3. Pre-Installation Checklist

- [ ] PostgreSQL service is running:
  ```cmd
  pg_isready -U postgres -h localhost
  :: Expected: localhost:5432 - aceptando conexiones
  ```
- [ ] psql 15+ is accessible from the command line:
  ```cmd
  psql --version
  ```
- [ ] You are in the project root directory:
  ```cmd
  cd C:\BookingScraper
  ```
- [ ] If existing `booking_scraper` data needs preservation, take a backup first:
  ```cmd
  pg_dump -U postgres -F c booking_scraper > backup_%DATE%.dump
  ```
- [ ] The script is in the correct location:
  ```cmd
  dir app\install_clean_v42.sql
  ```

---

## 4. Installation Procedure

### Step 1 — Drop and recreate the database

Run from the project root. psql connects to `postgres` by default (no `-d` flag).

```cmd
psql -U postgres -f app/install_clean_v42.sql
```

Enter your postgres password when prompted.

**What this step does:**

The script detects `current_database() = 'postgres'` via `\gset` / `\if` and executes:

1. Terminates any active connections to `booking_scraper`
2. `DROP DATABASE IF EXISTS booking_scraper` (top-level statement, not in DO block)
3. `CREATE DATABASE booking_scraper` with UTF8 / C locale
4. `\connect booking_scraper`

**Expected Step 1 output:**

```
SET
 postgresql_version
--------------------------------------------------------------------------
 PostgreSQL 18.1 on x86_64-windows, compiled by msvc-19.44.35221, 64-bit
(1 fila)

NOTICE:  ================================================
NOTICE:    Step 1: connected to [postgres]
NOTICE:    Dropping and recreating booking_scraper...
NOTICE:  ================================================
DO
 pg_terminate_backend
----------------------
(0 filas)

NOTICE:    Active connections terminated.
DO
NOTICE:    booking_scraper dropped.
DO
CREATE DATABASE
COMMENT
NOTICE:    booking_scraper created.
NOTICE:    Switching context via \connect ...
DO
You are now connected to database "booking_scraper" as user "postgres".
NOTICE:  ================================================
NOTICE:    [OK] Context verified: [booking_scraper]
NOTICE:    Installing schema...
NOTICE:  ================================================
DO
```

After context verification, the full schema installation continues automatically.

> **If `\connect` fails silently on Windows:** The Section 1b verification guard will raise an exception and psql aborts cleanly. Proceed to Step 2 in that case.

### Step 2 — (Only if Step 1 aborted after `\connect`) Install schema directly

If Step 1 successfully installed the full schema (check for `BookingScraper Pro v42 is ready` in the output), **Step 2 is not needed**.

If Step 1 aborted at the `\connect` line, run Step 2:

```cmd
psql -U postgres -d booking_scraper -f app/install_clean_v42.sql
```

The `-d booking_scraper` flag connects directly. The script detects `current_database() = 'booking_scraper'`, skips DROP/CREATE, and installs the schema.

---

## 5. Expected Output Reference

### Complete successful output (Step 1 or Step 2)

```
SET
 postgresql_version
-----------------------------------------------------------------------
 PostgreSQL 18.1 on x86_64-windows, compiled by msvc-19.44.35221, 64-bit

NOTICE:  ================================================
NOTICE:    [OK] Context verified: [booking_scraper]
NOTICE:    Installing schema...
NOTICE:  ================================================
DO
NOTICE:    Role scraper_app created.           (or: already exists - skipped)
NOTICE:    Role scraper_readonly created.      (or: already exists - skipped)
DO
DO
CREATE EXTENSION    (pg_stat_statements)
CREATE EXTENSION    (btree_gin)
CREATE EXTENSION    (pg_trgm)
CREATE TABLE        (url_queue)
COMMENT
COMMENT
CREATE TABLE        (hotels)
COMMENT
CREATE TABLE        (url_language_status)
COMMENT
CREATE TABLE        (scraping_logs)
COMMENT
CREATE FUNCTION     (check_scraping_log_url_id)
CREATE TRIGGER      (trg_scraping_logs_fk_check)
CREATE FUNCTION     (nullify_scraping_log_url_id)
DO
CREATE FUNCTION     (create_scraping_logs_partition)
NOTICE:    Partition created: scraping_logs_2026_03
NOTICE:    Partition created: scraping_logs_2026_04
NOTICE:    Partition created: scraping_logs_2026_05
 create_scraping_logs_partition
--------------------------------
(1 fila)     x3

CREATE TABLE        (vpn_rotations)
COMMENT
CREATE TABLE        (system_metrics)
COMMENT
CREATE INDEX        x27
CREATE FUNCTION     (trg_set_updated_at)
DO
NOTICE:    Trigger trg_url_queue_updated_at created.
NOTICE:    Trigger trg_url_language_status_updated_at created.
DROP VIEW
CREATE VIEW         (v_scraping_dashboard)
COMMENT
DROP VIEW
CREATE VIEW         (v_language_completeness)
COMMENT
CREATE TABLE        (schema_migrations)
COMMENT
INSERT 0 1
GRANT x4
ALTER DEFAULT PRIVILEGES x2

NOTICE:  =====================================================
NOTICE:    BookingScraper Pro v42 - Install Verification
NOTICE:  =====================================================
NOTICE:    Database    : booking_scraper
NOTICE:    PostgreSQL  : PostgreSQL 18.1 ...
NOTICE:    Tables      : 7 / 7
NOTICE:    App Indexes : 27 / 27
NOTICE:    Views       : 2 / 2
NOTICE:    Extensions  : 3 / 3
NOTICE:  =====================================================
NOTICE:    [OK] Database context: booking_scraper
NOTICE:    [OK] Tables: 7 / 7
NOTICE:    [OK] App indexes: 27 / 27
NOTICE:    [OK] Views: 2 / 2
NOTICE:    [OK] Extensions: 3 / 3
NOTICE:  =====================================================
NOTICE:    [OK] All assertions passed.
NOTICE:  =====================================================
DO

 extname             | extversion
---------------------+------------
 btree_gin           | 1.3
 pg_stat_statements  | 1.12
 pg_trgm             | 1.6
(3 filas)

 table_name              | table_type        | estimated_rows
-------------------------+-------------------+---------------------------
 scraping_logs           | partitioned table | not analyzed yet - run ANALYZE
 hotels                  | table             | not analyzed yet - run ANALYZE
 schema_migrations       | table             | not analyzed yet - run ANALYZE
 scraping_logs_2026_03   | table             | not analyzed yet - run ANALYZE
 scraping_logs_2026_04   | table             | not analyzed yet - run ANALYZE
 scraping_logs_2026_05   | table             | not analyzed yet - run ANALYZE
 system_metrics          | table             | not analyzed yet - run ANALYZE
 url_language_status     | table             | not analyzed yet - run ANALYZE
 url_queue               | table             | not analyzed yet - run ANALYZE
 vpn_rotations           | table             | not analyzed yet - run ANALYZE
(10 filas)

 indexname                    | tablename
------------------------------+-----------------------
 ix_hotels_facilities_gin     | hotels
 ix_hotels_images_gin         | hotels
 ...                          | ...
(27 filas)

ANALYZE
NOTICE:    [OK] ANALYZE complete - statistics initialized.
NOTICE:    BookingScraper Pro v42 is ready.
DO
DO
```

---

## 6. Post-Installation Verification

### Quick checks

```cmd
:: Verify database exists and is accessible
psql -U postgres -d booking_scraper -c "SELECT current_database(), version();"

:: Verify all 7 tables exist
psql -U postgres -d booking_scraper -c "\dt public.*"

:: Verify exactly 2 views
psql -U postgres -d booking_scraper -c "\dv public.*"

:: Verify schema version
psql -U postgres -d booking_scraper -c "SELECT version, applied_at FROM schema_migrations;"

:: Verify extensions
psql -U postgres -d booking_scraper -c "SELECT extname, extversion FROM pg_extension WHERE extname IN ('pg_stat_statements','btree_gin','pg_trgm');"

:: Verify application indexes (expected: 27)
psql -U postgres -d booking_scraper -c "SELECT COUNT(*) FROM pg_indexes WHERE schemaname='public' AND indexname LIKE 'ix_%';"

:: Verify ANALYZE ran (expected: reltuples = 0 for all tables, not -1)
psql -U postgres -d booking_scraper -c "SELECT relname, reltuples FROM pg_class WHERE relnamespace='public'::regnamespace AND relkind IN ('r','p') ORDER BY relname;"
```

### Verify postgres system database is clean

If the v36 or v41 script previously polluted the `postgres` database, clean it:

```cmd
psql -U postgres -c "\dt public.*"
```

If application tables appear there, remove them:

```sql
\c postgres
DROP TABLE IF EXISTS url_queue, hotels, url_language_status,
    vpn_rotations, system_metrics, schema_migrations CASCADE;
DROP TABLE IF EXISTS scraping_logs CASCADE;
DROP VIEW  IF EXISTS v_scraping_dashboard, v_language_completeness;
DROP FUNCTION IF EXISTS trg_set_updated_at CASCADE;
DROP FUNCTION IF EXISTS check_scraping_log_url_id CASCADE;
DROP FUNCTION IF EXISTS nullify_scraping_log_url_id CASCADE;
DROP FUNCTION IF EXISTS create_scraping_logs_partition CASCADE;
```

---

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No such file or directory` | Wrong working directory | `cd C:\BookingScraper` then retry |
| `pg_isready` fails | PostgreSQL not running | `net start postgresql-x64-18` |
| `password authentication failed` | Wrong password | Check `.env` for `DB_PASSWORD` |
| `FATAL: database "booking_scraper" does not exist` | Step 1 not completed | Run Step 1 first |
| `Views: 4 / 2` warning | Residual objects from prior install | The DROP VIEW fix in v42 prevents this; if it still appears, manually run `DROP VIEW IF EXISTS v_scraping_dashboard, v_language_completeness;` then rerun Step 2 |
| `\connect` fails, schema goes to `postgres` | Windows psql -f behavior | Section 1b aborts with clear message; run Step 2 |
| `ERROR: [POST-VERIFY] Wrong database` | Schema installed in wrong DB | Full reinstall: Step 1 then Step 2 |
| Garbled characters in terminal | Windows code page mismatch | Run `chcp 65001` before psql; v42 uses ASCII-only NOTICE strings |

---

## 8. Schema Reference

### Tables

| Table | Type | Rows/day (est.) | Notes |
|-------|------|-----------------|-------|
| `url_queue` | Ordinary | ~1000 | fillfactor=70 for HOT updates |
| `hotels` | Ordinary | ~5000 | One per URL × language |
| `url_language_status` | Ordinary | ~5000 | fillfactor=70 |
| `scraping_logs` | Partitioned (monthly) | ~50,000 | Range on timestamp |
| `vpn_rotations` | Ordinary | ~100 | NordVPN event log |
| `system_metrics` | Ordinary | ~1440 | Snapshot every minute |
| `schema_migrations` | Ordinary | 0 | Version history |

### Active Partitions After Install

| Partition | Range |
|-----------|-------|
| `scraping_logs_2026_03` | 2026-03-01 → 2026-04-01 |
| `scraping_logs_2026_04` | 2026-04-01 → 2026-05-01 |
| `scraping_logs_2026_05` | 2026-05-01 → 2026-06-01 |

New partitions are created monthly by the Celery cleanup task via `create_scraping_logs_partition()`.

### Roles

| Role | Permissions | Used by |
|------|-------------|---------|
| `postgres` | Superuser | Installation / maintenance only |
| `scraper_app` | SELECT, INSERT, UPDATE, DELETE | FastAPI / Celery processes |
| `scraper_readonly` | SELECT only | Monitoring, BI tools |

### Views

| View | Description |
|------|-------------|
| `v_scraping_dashboard` | Per-URL summary: hotel count, languages, images, avg rating |
| `v_language_completeness` | Per-URL language completion percentage |

---

## 9. Full Fix History v37 to v42

| ID | Severity | Source Audit | Description | Fix in version |
|----|----------|--------------|-------------|----------------|
| CRIT-INST-001 | CRITICAL | v37 | Schema installed in `postgres` instead of `booking_scraper` | v41 + v42 |
| NEW-EXEC-001 | CRITICAL | v41 execution | `DROP DATABASE` fails inside `DO $$` block | **v42** |
| NEW-EXEC-002 | CRITICAL | v41 execution | Bare `RAISE NOTICE` invalid outside PL/pgSQL context | **v42** |
| NEW-EXEC-003 | MEDIUM | v41 execution | Residual views cause `Views: 4 / 2` warning | **v42** |
| MED-VER-001 | MEDIUM | v37 | Hardcoded denominator `/6` incorrect (should be `/7`) | v41 |
| MED-VER-002 | MEDIUM | v37 | `pg_class relkind='r'` excluded partitioned parent `scraping_logs` | v41 |
| MED-VIEW-001 | MEDIUM | v37 | 4 views reported, only 2 defined | v41 + v42 |
| LOW-ENC-001 | LOW | v37 | Em dash encoded as `â?"` in Windows console NOTICE | v41 |
| LOW-PATH-001 | LOW | v37 | Script header documented wrong execution path | v41 |
| INFO-PG18-001 | INFO | v37 | PostgreSQL 18.1 outside documented test matrix | v41 |
| INFO-STATS-001 | INFO | v37 | `estimated_rows = -1` not annotated | v41 |

---

*BookingScraper Pro — Installation Guide v42 | 2026-03-06 | Windows 11 Local Environment*
