# BookingScraper Pro — Execution Audit Report v37 (EN)
**Date:** 2026-03-06 | **Auditor:** Enterprise Architecture Review  
**Scope:** Execution analysis of `install_clean_v31.sql` on Windows 11  
**Environment:** Windows 11 Local | PostgreSQL 18.1 | psql CLI  
**Command executed:** `psql -U postgres -f app/install_clean_v31.sql`  
**Preceding report:** Audit v36 (2026-03-06)

---

## Executive Summary

This report documents errors and anomalies detected during the **live execution** of `install_clean_v31.sql` (schema v36) on a Windows 11 local environment with PostgreSQL 18.1. The analysis is based exclusively on the psql terminal output produced during this execution.

| Severity   | Count |
|------------|-------|
| CRITICAL   | 1     |
| MEDIUM     | 3     |
| LOW        | 2     |
| INFO       | 2     |
| **Total**  | **8** |

> ⚠️ **CRIT-INST-001 requires immediate operator action before using the application.** The schema may have been installed in the wrong database.

---

## Error Registry

---

### CRIT-INST-001 — Schema Installed in Wrong Database (`postgres` Instead of `booking_scraper`)

| Field        | Value                                      |
|--------------|--------------------------------------------|
| **Severity** | CRITICAL                                   |
| **File**     | `install_clean_v31.sql`                    |
| **Line**     | 58                                         |
| **Section**  | Section 1 — Database Creation              |
| **Category** | Installation / Database Context            |

**Description:**

The post-installation verification NOTICE reports:

```
NOTICE:    Database    : postgres
```

The `current_database()` function at line 708 of the script returns `postgres`, which is the PostgreSQL system default database. This means the `\connect booking_scraper` metacommand at line 58 did not switch the active connection to the newly created `booking_scraper` database.

As a result, all DDL executed after line 58 — including all `CREATE TABLE`, `CREATE INDEX`, `CREATE FUNCTION`, `CREATE TRIGGER`, `CREATE VIEW`, `GRANT`, and `INSERT` statements — was applied to the `postgres` system database, not to `booking_scraper`.

The `booking_scraper` database was successfully created (line 48 produced `CREATE DATABASE`) but remains empty. The schema resides in the wrong database.

**Root Cause:**

When psql is invoked with the `-f` flag in non-interactive mode on Windows 11, the `\connect` metacommand may fail silently if a connection to the new database cannot be established. By default, psql does **not** abort the script on a failed `\connect`; it prints a warning and continues executing subsequent statements in the current connection context (`postgres`).

**Evidence from execution output:**

```
CREATE DATABASE          ← booking_scraper created successfully
...
NOTICE:    Database    : postgres   ← context was never switched
```

**Impact:**

- The `booking_scraper` database is empty.
- All schema objects (tables, indexes, triggers, views, role grants) exist in `postgres`.
- Application startup will fail: `DATABASE_URL` points to `booking_scraper`, which has no schema.
- The `postgres` system database is polluted with application objects, violating separation of concerns.
- Any `pg_dump` or backup targeting `booking_scraper` will produce an empty export.

**Required Operator Action:**

Step 1 — Verify the current state:
```sql
\c booking_scraper
\dt
-- Expected if bug confirmed: "Did not find any relations."
```

Step 2 — If confirmed, drop and reinstall using an explicit two-step process:
```bash
# Drop the empty booking_scraper database
psql -U postgres -c "DROP DATABASE IF EXISTS booking_scraper;"

# Step 1: Create the database only (no \connect needed)
psql -U postgres -c "CREATE DATABASE booking_scraper ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0;"

# Step 2: Connect DIRECTLY to booking_scraper and run all DDL
psql -U postgres -d booking_scraper -f app/install_clean_v31.sql
```

The `-d booking_scraper` flag on the second command guarantees execution in the correct database context, bypassing any `\connect` metacommand behavior entirely.

Step 3 — Also clean application objects from the `postgres` database:
```sql
\c postgres
DROP TABLE IF EXISTS url_queue, hotels, url_language_status, vpn_rotations, system_metrics, schema_migrations CASCADE;
DROP TABLE IF EXISTS scraping_logs CASCADE;
DROP VIEW  IF EXISTS v_scraping_dashboard, v_language_completeness;
DROP FUNCTION IF EXISTS trg_set_updated_at, check_scraping_log_url_id, nullify_scraping_log_url_id, create_scraping_logs_partition CASCADE;
```

---

### MED-VER-001 — Hardcoded Denominator `/6` Does Not Match Table Count in IN List

| Field        | Value                                      |
|--------------|--------------------------------------------|
| **Severity** | MEDIUM                                     |
| **File**     | `install_clean_v31.sql`                    |
| **Line**     | 710                                        |
| **Section**  | Section 9 — Post-Install Verification      |
| **Category** | Verification Logic / Accuracy              |

**Description:**

The verification DO block at line 687 queries `information_schema.tables` against an explicit `IN` list of 7 table names:

```sql
table_name IN (
    'url_queue','hotels','url_language_status',
    'scraping_logs','vpn_rotations','system_metrics',
    'schema_migrations'        -- 7th entry added in v36
)
```

However, the NOTICE on line 710 formats the result against a hardcoded denominator of 6:

```sql
RAISE NOTICE '  Tables      : % / 6', tbl_count;
```

**Evidence from execution output:**

```
NOTICE:    Tables      : 7 / 6
```

The output `7 / 6` incorrectly implies that more tables exist than expected, creating a false alarm for operators. The actual count of 7 is correct; the denominator was not updated when `schema_migrations` was added to the IN list in v36.

**Impact:**

Operators monitoring installation logs will interpret `7 / 6` as a schema anomaly. In automated pipelines or monitoring scripts that parse NOTICE output, this false mismatch may trigger erroneous alerts.

---

### MED-VER-002 — `pg_class` Table Listing Excludes `scraping_logs` Partitioned Parent Table

| Field        | Value                                      |
|--------------|--------------------------------------------|
| **Severity** | MEDIUM                                     |
| **File**     | `install_clean_v31.sql`                    |
| **Line**     | 727                                        |
| **Section**  | Section 9 — Post-Install Verification      |
| **Category** | Verification Logic / Observability         |

**Description:**

The table listing query at line 723 uses the filter `relkind = 'r'`:

```sql
SELECT relname AS table_name, reltuples::bigint AS estimated_rows
FROM pg_class
WHERE relkind = 'r'
  AND relnamespace = 'public'::regnamespace
ORDER BY relname;
```

In PostgreSQL, declaratively partitioned tables have `relkind = 'p'` (partitioned relation), not `'r'` (ordinary heap relation). The `scraping_logs` parent table is therefore excluded from this listing. Only the three monthly partition children appear because they are ordinary heap tables (`relkind = 'r'`).

**Evidence from execution output:**

```
table_name             | estimated_rows
-----------------------+----------------
scraping_logs_2026_03  |             -1   ← partition child
scraping_logs_2026_04  |             -1   ← partition child
scraping_logs_2026_05  |             -1   ← partition child
-- scraping_logs parent is absent with no explanatory notice
```

The absence of `scraping_logs` from this listing is not annotated anywhere in the verification output. An operator performing a post-install check could conclude the partitioned parent table was not created, despite it being present in `information_schema.tables` (as evidenced by MED-VER-001 count of 7).

---

### MED-VIEW-001 — Verification Reports `Views: 4` — Only 2 Views Defined in Script

| Field        | Value                                      |
|--------------|--------------------------------------------|
| **Severity** | MEDIUM                                     |
| **File**     | `install_clean_v31.sql`                    |
| **Line**     | 702–703                                    |
| **Section**  | Section 9 — Post-Install Verification      |
| **Category** | Schema Integrity / Verification Accuracy   |

**Description:**

The script defines exactly 2 views: `v_scraping_dashboard` (line 583) and `v_language_completeness` (line 606). The verification query at line 702 counts views in schema `public`:

```sql
SELECT COUNT(*) INTO view_count
FROM information_schema.views
WHERE table_schema = 'public';
```

**Evidence from execution output:**

```
NOTICE:    Views       : 4
```

Four views were found, not two. Two unaccounted views exist in the schema at verification time.

**Analysis:**

This anomaly is consistent with CRIT-INST-001: if DDL ran inside the `postgres` database rather than `booking_scraper`, and the `postgres` database already contained 2 application views from a prior incomplete installation, the count would total 4. This finding provides corroborating evidence for CRIT-INST-001.

**Impact:**

Two views with unknown definitions and dependencies exist in the active schema. Their presence without documentation violates schema governance requirements. ORM introspection tools (e.g., SQLAlchemy `automap_base`) may reflect these unknown views and generate unexpected model classes.

---

### LOW-ENC-001 — Windows Console Encoding Corruption in NOTICE Output

| Field        | Value                                          |
|--------------|------------------------------------------------|
| **Severity** | LOW                                            |
| **File**     | `install_clean_v31.sql`                        |
| **Line**     | 706                                            |
| **Section**  | Section 9 — Post-Install Verification          |
| **Category** | Encoding / Windows Compatibility               |

**Description:**

The NOTICE output contains garbled text:

```
NOTICE:   BookingScraper Pro v31 â?" Install Verification
```

The intended character is an em dash (`—`, U+2014, UTF-8 bytes: `E2 80 94`). The Windows `cmd.exe` console defaults to OEM code page 850 or ANSI code page 1252. Neither can decode the 3-byte UTF-8 sequence `E2 80 94` correctly, producing the display artifact `â?"`.

The `SET client_encoding = 'UTF8'` directive at line 35 configures the encoding of the psql client-to-server communication channel only. It does not affect how the Windows terminal interprets the byte stream sent to the console output buffer.

**Impact:**

Log files captured from `cmd.exe` or PowerShell will contain corrupted characters. Automated log parsers expecting ASCII-safe output may malfunction. Installation verification records in audit trails will contain garbled text.

---

### LOW-PATH-001 — Script Header Documents Incorrect Execution Path

| Field        | Value                                      |
|--------------|--------------------------------------------|
| **Severity** | LOW                                        |
| **File**     | `install_clean_v31.sql`                    |
| **Line**     | 14                                         |
| **Section**  | File Header Comment                        |
| **Category** | Documentation Accuracy                     |

**Description:**

The script header at line 14 documents the execution command as:

```bash
psql -U postgres -f install_clean_v31.sql
```

The actual execution command used was:

```bash
psql -U postgres -f app/install_clean_v31.sql
```

The file physically resides at `app/install_clean_v31.sql` relative to the project root `C:\BookingScraper`. Additionally, the v36 audit report (Part IV — Project File Structure) specifies the canonical location as `sql/install_clean_v31.sql`, creating a three-way discrepancy:

| Source                    | Documented Path                     |
|---------------------------|-------------------------------------|
| Script header (line 14)   | `install_clean_v31.sql` (no subdir) |
| v36 audit report Part IV  | `sql/install_clean_v31.sql`         |
| Actual execution (confirmed) | `app/install_clean_v31.sql`      |

**Impact:**

Operators following the header comment will receive `No such file or directory`. New team members onboarding from the audit report will use a different path than what exists. The authoritative file location is undefined across documentation sources.

---

### INFO-PG18-001 — PostgreSQL 18.1 Outside Documented Support Matrix

| Field        | Value                                      |
|--------------|--------------------------------------------|
| **Severity** | INFO                                       |
| **File**     | `install_clean_v31.sql`                    |
| **Line**     | 3                                          |
| **Section**  | File Header Comment                        |
| **Category** | Compatibility / Version Matrix             |

**Description:**

The script header declares support for `PostgreSQL 15+`. The detected runtime version is:

```
PostgreSQL 18.1 on x86_64-windows, compiled by msvc-19.44.35221, 64-bit
```

PostgreSQL 18.x is not listed in any documentation, requirements file, or prior audit report within this project. No functional regressions were observed during this specific execution. However, PostgreSQL 18.x introduces catalog changes, updated partition pruning behaviors, and new extension versions that have not been validated against this schema.

**Observed extension versions on PostgreSQL 18.1:**

```
pg_stat_statements  1.12
btree_gin           1.3
pg_trgm             1.6
```

These extension versions differ from those documented in v36 audit report references and have not been part of any test matrix.

---

### INFO-STATS-001 — `estimated_rows = -1` Not Annotated as Expected Behavior

| Field        | Value                                      |
|--------------|--------------------------------------------|
| **Severity** | INFO                                       |
| **File**     | `install_clean_v31.sql`                    |
| **Line**     | 723–729                                    |
| **Section**  | Section 9 — Post-Install Verification      |
| **Category** | Observability / Documentation              |

**Description:**

The table listing query returns `estimated_rows = -1` for all tables:

```
table_name             | estimated_rows
-----------------------+----------------
hotels                 |             -1
url_queue              |             -1
(all tables)           |             -1
```

A value of `-1` in `pg_class.reltuples` indicates that `ANALYZE` has never been executed on the table. This is the expected PostgreSQL 14+ behavior on a fresh installation before any data has been inserted and before the autovacuum daemon has run its first `ANALYZE`. The verification script contains no comment or NOTICE explaining this value.

**Note:** PostgreSQL 14+ changed the initial `reltuples` value from `0` to `-1` for unanalyzed tables. An operator familiar only with PostgreSQL 13 or earlier may interpret `-1` as an error condition.

---

## Summary Table

| ID              | Severity | Description                                                        | File                   | Line |
|-----------------|----------|--------------------------------------------------------------------|------------------------|------|
| CRIT-INST-001   | CRITICAL | Schema installed in `postgres` instead of `booking_scraper`       | install_clean_v31.sql  | 58   |
| MED-VER-001     | MEDIUM   | Hardcoded denominator `/6` incorrect — IN list has 7 table names  | install_clean_v31.sql  | 710  |
| MED-VER-002     | MEDIUM   | `pg_class relkind='r'` excludes `scraping_logs` parent (relkind=p)| install_clean_v31.sql  | 727  |
| MED-VIEW-001    | MEDIUM   | Verification reports 4 views — only 2 defined in script           | install_clean_v31.sql  | 702  |
| LOW-ENC-001     | LOW      | Em dash `—` encoded as `â?"` in Windows console NOTICE output     | install_clean_v31.sql  | 706  |
| LOW-PATH-001    | LOW      | Script header documents wrong execution path (3-way discrepancy)  | install_clean_v31.sql  | 14   |
| INFO-PG18-001   | INFO     | PostgreSQL 18.1 outside documented support matrix (declared 15+)  | install_clean_v31.sql  | 3    |
| INFO-STATS-001  | INFO     | `estimated_rows = -1` not annotated as expected on fresh install  | install_clean_v31.sql  | 723  |

---

*BookingScraper Pro — Enterprise Execution Audit Report v37 | Generated 2026-03-06 | Windows 11 Local Environment*
