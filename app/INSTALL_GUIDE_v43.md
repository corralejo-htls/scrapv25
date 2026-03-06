# BookingScraper Pro v43 — Installation and Verification Guide

**Date:** 2026-03-06
**Script:** `app/install_clean_v43.sql`
**Confirmed tested environment:** Windows 11 x64 | PostgreSQL 18.1 | psql 18.1

---

## Confirmed Tested Versions

| Component | Version | Status |
|-----------|---------|--------|
| Windows | 11 x64 | Tested |
| PostgreSQL | 18.1 (x86_64-windows, msvc-19.44.35221) | Tested |
| psql | 18.1 | Tested |
| pg_stat_statements | 1.12 | Tested |
| btree_gin | 1.3 | Tested |
| pg_trgm | 1.6 | Tested |

Compatible with PostgreSQL 15, 16, 17, 18 on Windows 11.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [What Changed from v42](#2-what-changed-from-v42)
3. [Pre-Installation Checklist](#3-pre-installation-checklist)
4. [Installation Procedure](#4-installation-procedure)
5. [Expected Output — All Assertions Pass](#5-expected-output--all-assertions-pass)
6. [Post-Installation Verification](#6-post-installation-verification)
7. [Troubleshooting](#7-troubleshooting)
8. [Schema Reference](#8-schema-reference)
9. [Complete Fix History](#9-complete-fix-history)

---

## 1. Prerequisites

**Verify before starting:**

```cmd
pg_isready -U postgres -h localhost
:: Expected: localhost:5432 - aceptando conexiones

psql --version
:: Expected: psql (PostgreSQL) 18.1
```

**Navigate to the project root:**

```cmd
cd C:\BookingScraper
```

---

## 2. What Changed from v42

### NEW-EXEC-004 — View count reported 4 instead of 2

**v42 warning:**
```
WARNING: [FAIL] Views: 4 / 2 - unexpected objects in schema.
```

**Root cause:** The `pg_stat_statements` extension automatically creates two system views in the schema where it is installed:

```
pg_stat_statements       -- query statistics view
pg_stat_statements_info  -- extension metadata view
```

These are not application views, but `information_schema.views` includes them with no distinction from user-created views. The v42 count query used `information_schema.views`, which counted all 4.

**v43 fix:** The view count query now uses `pg_class` joined to `pg_depend`, excluding any view that is owned by an extension (`deptype = 'e'`):

```sql
SELECT COUNT(*) INTO view_count
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'v'
  AND n.nspname = 'public'
  AND NOT EXISTS (
      SELECT 1 FROM pg_depend d
      WHERE d.objid   = c.oid
        AND d.deptype = 'e'
  );
```

`deptype = 'e'` is PostgreSQL's internal marker for objects created by an extension. This filter is stable across all PostgreSQL versions 9.1+. The count now correctly returns 2 (application views only).

**The 4 views are expected and correct:**

| View | Owner | Type |
|------|-------|------|
| `v_scraping_dashboard` | postgres | Application view |
| `v_language_completeness` | postgres | Application view |
| `pg_stat_statements` | postgres | Extension view (pg_stat_statements) |
| `pg_stat_statements_info` | postgres | Extension view (pg_stat_statements) |

---

## 3. Pre-Installation Checklist

- [ ] `pg_isready` confirms PostgreSQL is accepting connections
- [ ] You are in `C:\BookingScraper`
- [ ] The script file exists:
  ```cmd
  dir app\install_clean_v43.sql
  ```
- [ ] If you have data to preserve in `booking_scraper`, take a backup first:
  ```cmd
  :: Windows-safe backup command — avoids %DATE% path issues
  for /f "tokens=1-3 delims=/" %a in ("%DATE: =0%") do set d=%c%b%a
  pg_dump -U postgres -F c booking_scraper > backup_%d%.dump
  ```
  > **Note:** The simple `backup_%DATE%.dump` syntax fails on Windows because `%DATE%` expands to a locale-specific string containing slashes (e.g., `jue 06/03/2026`), which are invalid in file paths. Use the `for /f` form above, or specify a fixed filename such as `backup_20260306.dump`.

---

## 4. Installation Procedure

### Step 1 — Run the script from the `postgres` context

```cmd
psql -U postgres -f app/install_clean_v43.sql
```

Enter the postgres password when prompted.

The script detects it is connected to `postgres`, then:

1. Terminates active connections to `booking_scraper`
2. `DROP DATABASE IF EXISTS booking_scraper` (top-level, not in a function)
3. `CREATE DATABASE booking_scraper` (UTF8, C locale)
4. `\connect booking_scraper`
5. Verifies context and installs the full schema

On PostgreSQL 18.1 and Windows 11, `\connect` succeeds inside `psql -f` mode. **Step 1 alone is sufficient.** The script will complete with all assertions passing.

### Step 2 — Only if Step 1 aborted at `\connect`

If Step 1 aborts with the `[CRIT-INST-001]` error (indicating `\connect` failed silently), run:

```cmd
psql -U postgres -d booking_scraper -f app/install_clean_v43.sql
```

The script detects the `booking_scraper` context, skips DROP/CREATE, and installs the schema directly.

---

## 5. Expected Output — All Assertions Pass

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
NOTICE:  no existe la base de datos "booking_scraper", omitiendo
DROP DATABASE
NOTICE:    booking_scraper dropped.
DO
CREATE DATABASE
COMMENT
NOTICE:    booking_scraper created.
NOTICE:    Switching context via \connect ...
DO
Ahora esta conectado a la base de datos "booking_scraper" con el usuario "postgres".
NOTICE:  ================================================
NOTICE:    [OK] Context verified: [booking_scraper]
NOTICE:    Installing schema...
NOTICE:  ================================================
DO
NOTICE:    Role scraper_app already exists - skipped.
DO
NOTICE:    Role scraper_readonly already exists - skipped.
DO
CREATE EXTENSION     (x3)
CREATE TABLE         (url_queue)
COMMENT  COMMENT
CREATE TABLE         (hotels)
COMMENT
CREATE TABLE         (url_language_status)
COMMENT
CREATE TABLE         (scraping_logs)
COMMENT
CREATE FUNCTION      (check_scraping_log_url_id)
CREATE TRIGGER
CREATE FUNCTION      (nullify_scraping_log_url_id)
DO
CREATE FUNCTION      (create_scraping_logs_partition)
NOTICE:    Partition created: scraping_logs_2026_03
NOTICE:    Partition created: scraping_logs_2026_04
NOTICE:    Partition created: scraping_logs_2026_05
CREATE TABLE         (vpn_rotations)
COMMENT
CREATE TABLE         (system_metrics)
COMMENT
CREATE INDEX         (x27)
CREATE FUNCTION      (trg_set_updated_at)
NOTICE:    Trigger trg_url_queue_updated_at created.
NOTICE:    Trigger trg_url_language_status_updated_at created.
DO
DROP VIEW            (v_scraping_dashboard - not exists, skipping)
CREATE VIEW
COMMENT
DROP VIEW            (v_language_completeness - not exists, skipping)
CREATE VIEW
COMMENT
CREATE TABLE         (schema_migrations)
COMMENT
INSERT 0 1
GRANT  GRANT  GRANT  GRANT
ALTER DEFAULT PRIVILEGES  (x2)

NOTICE:  =====================================================
NOTICE:    BookingScraper Pro v43 - Install Verification
NOTICE:  =====================================================
NOTICE:    Database    : booking_scraper
NOTICE:    PostgreSQL  : PostgreSQL 18.1 on x86_64-windows...
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
-------------------------+-------------------+-------------------------------
 scraping_logs           | partitioned table | not analyzed yet - run ANALYZE
 hotels                  | table             | not analyzed yet - run ANALYZE
 ...all tables...        | table             | not analyzed yet - run ANALYZE
(10 filas)

 indexname                     | tablename
-------------------------------+----------------------
 ix_hotels_facilities_gin      | hotels
 ...27 indexes...              | ...
(27 filas)

ANALYZE
NOTICE:    [OK] ANALYZE complete - statistics initialized.
DO
NOTICE:    BookingScraper Pro v43 is ready.
DO
```

---

## 6. Post-Installation Verification

```cmd
:: Confirm database and version
psql -U postgres -d booking_scraper -c "SELECT current_database(), version();"

:: Confirm 7 base tables + 3 partition children (10 rows total)
psql -U postgres -d booking_scraper -c "\dt public.*"

:: Confirm 4 views total (2 application + 2 extension — this is correct)
psql -U postgres -d booking_scraper -c "\dv public.*"

:: Confirm schema version v43
psql -U postgres -d booking_scraper -c "SELECT version, applied_at FROM schema_migrations;"

:: Confirm 3 extensions with their tested versions
psql -U postgres -d booking_scraper -c "SELECT extname, extversion FROM pg_extension WHERE extname IN ('pg_stat_statements','btree_gin','pg_trgm');"

:: Confirm 27 application indexes
psql -U postgres -d booking_scraper -c "SELECT COUNT(*) FROM pg_indexes WHERE schemaname='public' AND indexname LIKE 'ix_%';"

:: Confirm ANALYZE ran (reltuples = 0, not -1)
psql -U postgres -d booking_scraper -c "SELECT relname, reltuples FROM pg_class WHERE relnamespace='public'::regnamespace AND relkind IN ('r','p') ORDER BY relname;"

:: Confirm postgres system database is clean (no application tables)
psql -U postgres -c "\dt public.*"
:: Expected: "No se encontraron tablas con el nombre 'public.*'."
```

### Expected `\dv` output (4 views is CORRECT)

```
Listado de vistas
 Esquema |           Nombre            | Tipo  |  Dueno
---------+-----------------------------+-------+----------
 public  | pg_stat_statements          | vista | postgres   <- extension view
 public  | pg_stat_statements_info     | vista | postgres   <- extension view
 public  | v_language_completeness     | vista | postgres   <- application view
 public  | v_scraping_dashboard        | vista | postgres   <- application view
(4 filas)
```

The 2 `pg_stat_statements*` views are created automatically by the extension. They are read-only system views. Their presence is expected and correct.

---

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No such file or directory` | Wrong directory | `cd C:\BookingScraper` |
| `pg_isready` fails | Service stopped | `net start postgresql-x64-18` |
| `backup_%DATE%.dump` path error | `%DATE%` contains slashes on Windows | Use `backup_20260306.dump` as filename |
| `FATAL: database "booking_scraper" does not exist` | Step 1 not completed | Run Step 1 first |
| `Views: 4 / 2` warning | Would only happen if 2+ extra app views exist | Check `\dv public.*`; the pg_stat_statements views are expected and do not trigger this warning in v43 |
| `[CRIT-INST-001]` error | `\connect` failed silently | Run Step 2 with `-d booking_scraper` |
| Tables appear in `postgres` DB | Previous v36/v41 install polluted it | See cleanup script below |

**Clean up residual objects in the `postgres` system database** (only needed if a prior broken install left them):

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

## 8. Schema Reference

### Tables (7 base + 3 partition children = 10 in \dt)

| Table | Type | fillfactor | Description |
|-------|------|-----------|-------------|
| `url_queue` | Ordinary | 70 | Work queue: one row per unique hotel URL |
| `hotels` | Ordinary | default | Scraped hotel data: one row per (url × language) |
| `url_language_status` | Ordinary | 70 | Per-(url, language) scraping state |
| `scraping_logs` | Partitioned (RANGE/monthly) | — | Audit log: one row per scraping attempt |
| `vpn_rotations` | Ordinary | default | NordVPN rotation event log |
| `system_metrics` | Ordinary | default | Periodic resource snapshots |
| `schema_migrations` | Ordinary | default | Applied schema version history |

### Partition Schedule

| Partition | Range |
|-----------|-------|
| `scraping_logs_2026_03` | 2026-03-01 → 2026-04-01 |
| `scraping_logs_2026_04` | 2026-04-01 → 2026-05-01 |
| `scraping_logs_2026_05` | 2026-05-01 → 2026-06-01 |

The Celery cleanup task calls `create_scraping_logs_partition()` monthly to pre-create future partitions.

### Views (4 total — 2 application + 2 extension)

| View | Type | Description |
|------|------|-------------|
| `v_scraping_dashboard` | Application | Per-URL summary: hotel count, languages, images, avg rating |
| `v_language_completeness` | Application | Per-URL language completion percentage |
| `pg_stat_statements` | Extension (read-only) | Query execution statistics |
| `pg_stat_statements_info` | Extension (read-only) | Extension metadata and reset info |

### Roles

| Role | Permissions |
|------|-------------|
| `postgres` | Superuser — installation and maintenance only |
| `scraper_app` | SELECT, INSERT, UPDATE, DELETE on all tables |
| `scraper_readonly` | SELECT only |

---

## 9. Complete Fix History

| ID | Severity | Introduced In | Fixed In | Description |
|----|----------|---------------|----------|-------------|
| CRIT-INST-001 | CRITICAL | v36 | v41+v42 | Schema installed in `postgres` instead of `booking_scraper` |
| NEW-EXEC-001 | CRITICAL | v41 | v42 | `DROP DATABASE` fails inside `DO $$` block |
| NEW-EXEC-002 | CRITICAL | v41 | v42 | Bare `RAISE NOTICE` invalid outside PL/pgSQL context |
| NEW-EXEC-003 | MEDIUM | v41 | v42 | Residual views cause false `Views: 4/2` warning on re-run |
| **NEW-EXEC-004** | **MEDIUM** | **v42** | **v43** | **`pg_stat_statements` extension views counted as application views** |
| MED-VER-001 | MEDIUM | v36 | v41 | Hardcoded denominator `/6` should be `/7` |
| MED-VER-002 | MEDIUM | v36 | v41 | `relkind='r'` excluded partitioned parent `scraping_logs` |
| MED-VIEW-001 | MEDIUM | v36 | v41+v42 | 4 views reported, only 2 defined |
| LOW-ENC-001 | LOW | v36 | v41 | Em dash encoded as `â?"` in Windows console |
| LOW-PATH-001 | LOW | v36 | v41 | Script header documented wrong execution path |
| LOW-BACKUP-001 | LOW | guide | v43 guide | `%DATE%` in backup command produces invalid path on Windows |
| INFO-PG18-001 | INFO | v36 | v43 | PostgreSQL 18.1 not in documented test matrix; now confirmed tested |
| INFO-STATS-001 | INFO | v36 | v41 | `estimated_rows = -1` not annotated as expected behavior |

---

*BookingScraper Pro — Installation Guide v43 | 2026-03-06 | Tested: Windows 11 / PostgreSQL 18.1*
