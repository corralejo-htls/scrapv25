# BookingScraper Pro — Enterprise Error Report v37
**Date:** 2026-03-06 | **Auditor:** Enterprise Architecture Review  
**Repository:** https://github.com/Aprendiz73/scrvIIpro26.git  
**Environment:** Windows 11 Local | Python 3.14.x | PostgreSQL 15+  
**Audit Scope:** Legacy SQL script (document submission) + `install_clean_v31.sql` (v36) + `tasks.py` v6.0

---

## Executive Summary

This report documents **18 new errors** identified during the post-v36 audit session, triggered by the runtime error `VACUUM cannot run inside a transaction block (SQL state: 25001)`. The audit covers the **legacy SQL initialization script** submitted in the document (hereinafter "legacy script"), the current `install_clean_v31.sql` (v36), and `tasks.py` (v6.0).

> ⚠ **Root cause of the reported runtime error:** The legacy SQL script was executed instead of `install_clean_v31.sql` (v36). The legacy script terminates with `VACUUM ANALYZE;`, which is invalid inside any PostgreSQL transaction block. Additionally, the legacy script is structurally incompatible with the v6.0 Python codebase.

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH | 4 |
| MEDIUM | 8 |
| LOW | 3 |
| INFO | 1 |
| **TOTAL** | **18** |

**Overall Production Readiness:** ❌ **BLOCKED** — The legacy script must not be executed against a v6.0 deployment. `install_clean_v31.sql` (v36) remains the valid installation artifact.

---

## Part I — Critical Errors

---

### CRIT-SQL-001 — VACUUM Executed Inside a Transaction Block

**Source:** Legacy SQL script (document) — final line  
**File Reference:** `install_clean_v31.sql` (legacy version, not v36)  
**PostgreSQL Error:** `ERROR: VACUUM cannot run inside a transaction block`  
**SQL State:** `25001`  
**Severity:** CRITICAL  
**Status:** ❌ ACTIVE — Aborts script execution at runtime

**Technical Description:**

The legacy script terminates with the unconditional statement:

```sql
VACUUM ANALYZE;
```

PostgreSQL's `VACUUM` command (and all its variants: `VACUUM FULL`, `VACUUM ANALYZE`, `ANALYZE`) cannot execute inside an active transaction block. The PostgreSQL documentation explicitly states: *"VACUUM cannot be executed inside a transaction block."*

When a SQL script is executed via `psql -f <file>` or via `\i` from the psql prompt, psql does **not** automatically wrap the file in an explicit `BEGIN/COMMIT` block. However, any DDL statement (e.g., `CREATE TABLE`, `CREATE FUNCTION`) that the psql client processes causes the connection to enter an implicit transaction state under certain client configurations or GUI tools (e.g., pgAdmin, DBeaver, TablePlus). In such environments, the session remains inside a transaction block from the first DDL statement, and `VACUUM` at the end triggers the `25001` error.

Additionally, `VACUUM ANALYZE` is operationally redundant immediately after a clean install on an empty database, as there are no dead tuples to reclaim and the statistics will be trivially minimal.

**Technical Impact:**
- Script execution terminates at the last line, after all DDL has been processed. Structural damage is unlikely but the error causes psql to exit with a non-zero status code, breaking automated CI/CD pipelines.
- In environments with `ON_ERROR_STOP=on` or equivalent, all preceding DDL may be rolled back.

**Evidence:** Reported runtime error matches exactly: `ERROR: VACUUM cannot run inside a transaction block   SQL state: 25001`.

**Corrective Action:** Remove `VACUUM ANALYZE;` from the legacy script. If post-install statistics refresh is desired, execute it as a standalone command after the script completes:

```bash
psql -U postgres -d booking_scraper -c "VACUUM ANALYZE;"
```

**Note:** This error is absent in `install_clean_v31.sql` (v36), which does not contain a `VACUUM` statement. The v36 script is the correct installation artifact.

---

### CRIT-SQL-002 — Legacy Script Structurally Incompatible with v6.0 Python Codebase

**Source:** Legacy SQL script (document)  
**Affected Python Modules:** `scraper_service.py` v6.0, `tasks.py` v6.0, `completeness_service.py`, `main.py` v4.0  
**Severity:** CRITICAL  
**Status:** ❌ ACTIVE — Runtime failures on first INSERT after application startup

**Technical Description:**

The legacy script creates the following tables and schema:

```
url_queue, hotels, hotel_facilities, rooms, images,
scraping_logs, policies, statistics, facility_categories
```

The v6.0 Python codebase (`scraper_service.py`, `tasks.py`, `completeness_service.py`) issues SQL against the following tables that **do not exist** in the legacy schema:

| Missing Table | First Python Reference | Runtime Error |
|---|---|---|
| `url_language_status` | `completeness_service.py` — `initialize_url_processing()` | `psycopg2.errors.UndefinedTable: relation "url_language_status" does not exist` |
| `system_metrics` | `tasks.py` — `save_system_metrics()` task | `psycopg2.errors.UndefinedTable: relation "system_metrics" does not exist` |
| `vpn_rotations` | `vpn_manager_windows.py` — VPN rotation log | `psycopg2.errors.UndefinedTable: relation "vpn_rotations" does not exist` |
| `schema_migrations` | `install_clean_v31.sql` (v36) — version tracking | Table missing; migration audit trail absent |

Furthermore, the legacy `hotels` table schema differs from what `scraper_service.py` v6.0 inserts:

```sql
-- Legacy schema (document):
hotel_name VARCHAR(255), booking_url VARCHAR(500), vpn_ip VARCHAR(50), ...

-- v6.0 INSERT statement (scraper_service.py _save_hotel()):
INSERT INTO hotels (url_id, url, language, name, address, description,
                    rating, total_reviews, rating_category, review_scores,
                    services, facilities, house_rules, important_info,
                    rooms_info, images_urls, images_count, scraped_at, updated_at)
```

The column `url_id` (FK to `url_queue`) does not exist in the legacy `hotels` schema, which uses `booking_url`. The INSERT will fail immediately with `column "url_id" does not exist`.

**Technical Impact:** Application startup succeeds, but the first scraping cycle raises `UndefinedTable` or `UndefinedColumn` exceptions, rendering the entire extraction pipeline non-functional.

---

## Part II — High Severity Errors

---

### HIGH-SQL-001 — Missing `'incomplete'` Value in `url_queue.status` CHECK Constraint

**Source:** Legacy SQL script (document) — `url_queue` table definition  
**Severity:** HIGH  
**Status:** ❌ ACTIVE — Runtime CHECK constraint violation

**Technical Description:**

The legacy script defines:

```sql
status VARCHAR(20) DEFAULT 'pending'
CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'skipped'))
```

`scraper_service.py` v6.0 (CAMBIOS v6.0) introduces a new status value `'incomplete'` to represent URLs where at least one language failed after exhausting retries. The relevant SQL in `scraper_service.py`:

```sql
UPDATE url_queue SET status = 'incomplete' WHERE id = :id
```

Executing this UPDATE against a database initialized with the legacy script raises:

```
ERROR: new row for relation "url_queue" violates check constraint "url_queue_status_check"
DETAIL: Failing row contains (... incomplete ...).
SQL state: 23514
```

**Technical Impact:** Any URL that reaches the `incomplete` state triggers a database constraint violation, causing the URL processing transaction to roll back. The URL remains in `processing` state indefinitely until `reset_stale_urls` recovers it.

**Note:** `install_clean_v31.sql` (v36) correctly defines: `CHECK (status IN ('pending','processing','completed','failed','incomplete'))`.

---

### HIGH-SQL-002 — `TIMESTAMP` Without Timezone — DST Comparison Failures on Windows 11

**Source:** Legacy SQL script (document) — all timestamp columns  
**Affected Columns:** `url_queue.created_at`, `url_queue.updated_at`, `url_queue.last_attempt`, `hotels.created_at`, `hotels.updated_at`, `scraping_logs.timestamp`, all timestamp columns  
**Severity:** HIGH  
**Status:** ❌ ACTIVE — Silent data corruption under DST transitions

**Technical Description:**

The legacy script uses `TIMESTAMP` (without time zone) for all temporal columns:

```sql
last_attempt TIMESTAMP,
created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

The v6.0 Python application uses `datetime.now(timezone.utc)` (timezone-aware UTC datetimes) and SQLAlchemy with `TIMESTAMPTZ` columns (as defined in `install_clean_v31.sql` v36). When the application inserts a timezone-aware Python datetime into a `TIMESTAMP` (without timezone) PostgreSQL column, psycopg2 performs an implicit timezone stripping, storing the local time component without the offset.

On Windows 11, the PostgreSQL server timezone is typically set to the Windows system timezone (e.g., `Europe/Madrid`, UTC+1/UTC+2 depending on DST). The `reset_stale_urls` task in `tasks.py` executes:

```sql
WHERE status = 'processing'
  AND updated_at < NOW() - INTERVAL '1 minute' * :minutes
```

`NOW()` returns a `TIMESTAMPTZ`, which PostgreSQL implicitly casts to `TIMESTAMP` for comparison against a `TIMESTAMP` column using the session's `TimeZone` setting. If the session timezone differs from UTC (standard during CET/CEST transitions), the comparison offset is incorrect. A URL that was updated 29 minutes ago in UTC may appear 30+ minutes old in local time, triggering a premature stale reset of an actively processing URL.

**Technical Impact:** During DST transitions (March/October), actively processing URLs may be incorrectly reset to `pending`, causing duplicate scraping of the same hotel.

**Note:** `install_clean_v31.sql` (v36) uses `TIMESTAMPTZ NOT NULL DEFAULT NOW()` throughout, eliminating this class of error.

---

### HIGH-SQL-003 — `get_pending_urls()` Function Missing `FOR UPDATE SKIP LOCKED` — Concurrent Dispatch Race Condition

**Source:** Legacy SQL script (document) — `get_pending_urls()` function  
**Severity:** HIGH  
**Status:** ❌ ACTIVE — Duplicate URL processing under concurrent callers

**Technical Description:**

```sql
CREATE OR REPLACE FUNCTION get_pending_urls(limit_count INT DEFAULT 10)
RETURNS TABLE (id INT, url VARCHAR, priority INT, retry_count INT) AS $$
BEGIN
    RETURN QUERY
    SELECT uq.id, uq.url, uq.priority, uq.retry_count
    FROM url_queue uq
    WHERE uq.status = 'pending'
      AND uq.retry_count < uq.max_retries
    ORDER BY uq.priority DESC, uq.created_at ASC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;
```

This function performs a `SELECT` without any row-level locking directive. Under concurrent execution (two processes calling `get_pending_urls()` within the same millisecond window), both callers receive identical result sets — the same `url_id` rows — before either caller has committed the status update to `'processing'`. Both callers will subsequently attempt to scrape the same URLs.

`FOR UPDATE SKIP LOCKED` is the standard PostgreSQL pattern for queue consumption: it acquires a row-level exclusive lock on selected rows and skips rows already locked by another session, ensuring each row is dispatched to exactly one consumer. Its absence is a race condition that becomes observable at `SCRAPER_MAX_WORKERS > 1` or when Celery dispatches concurrent task instances.

**Note:** `install_clean_v31.sql` (v36) and `scraper_service.py` v6.0 resolve this via a CTE with `FOR UPDATE SKIP LOCKED` in `_claim_active_url()`.

---

### HIGH-SQL-004 — Division by Zero in `v_queue_status` View on Empty Table

**Source:** Legacy SQL script (document) — `v_queue_status` view  
**Severity:** HIGH  
**Status:** ❌ ACTIVE — Runtime exception when `url_queue` is empty

**Technical Description:**

```sql
CREATE OR REPLACE VIEW v_queue_status AS
SELECT
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM url_queue
GROUP BY status;
```

When `url_queue` contains no rows, `SUM(COUNT(*)) OVER()` evaluates to `0`. The expression `COUNT(*) * 100.0 / 0` raises:

```
ERROR: division by zero
SQL state: 22012
```

This error surfaces at application startup when the `/stats` or `/health` endpoints query this view against a freshly initialized empty database. Any monitoring or health-check system that queries `v_queue_status` immediately after database creation will receive a 500 Internal Server Error.

**Correct Pattern:** `NULLIF(SUM(COUNT(*)) OVER(), 0)` converts zero to NULL, causing the division to return NULL rather than raise an exception.

---

## Part III — Medium Severity Errors

---

### MED-SQL-001 — `scraping_logs.status` Column Has No CHECK Constraint

**Source:** Legacy SQL script (document) — `scraping_logs` table  
**Severity:** MEDIUM  
**Status:** ❌ ACTIVE — Data integrity gap

**Technical Description:**

```sql
status VARCHAR(50) NOT NULL,  -- success, failed, timeout, error
```

The column is documented with valid values in a comment (`success, failed, timeout, error`) but has no `CHECK` constraint enforcing them. Any arbitrary string can be inserted without error. This contrasts with `url_queue.status`, which has a `CHECK` constraint.

Application code inserting `scraping_logs` rows (e.g., `_log()` in `scraper_service.py`) defines the vocabulary in Python logic: `"success"`, `"failed"`, `"timeout"`, `"error"`, `"skipped"`. A programming error, refactoring, or direct SQL manipulation can insert values outside this set without any database-level rejection. Dashboard queries filtering by status will silently omit unrecognized values.

---

### MED-SQL-002 — `hotel_facilities.category` Has No Foreign Key to `facility_categories` — Orphaned Reference Table

**Source:** Legacy SQL script (document) — `hotel_facilities` and `facility_categories` tables  
**Severity:** MEDIUM  
**Status:** ❌ ACTIVE — Referential integrity absent despite infrastructure presence

**Technical Description:**

```sql
-- hotel_facilities
category VARCHAR(100),          -- no FK constraint

-- facility_categories (created at end of script)
CREATE TABLE IF NOT EXISTS facility_categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL
);
```

The `facility_categories` table provides a controlled vocabulary for facility categories, pre-populated with 10 standard values (`'General'`, `'Internet'`, `'Parking'`, etc.). However, `hotel_facilities.category` is a plain `VARCHAR(100)` column with no `REFERENCES facility_categories(category_name)` constraint. Arbitrary category strings can be inserted without validation. The `facility_categories` table is structurally orphaned — it occupies storage, requires maintenance, and adds schema complexity without enforcing any integrity guarantee.

---

### MED-SQL-003 — `images.image_url VARCHAR(1000)` in UNIQUE B-Tree Index — Potential Index Entry Size Overflow

**Source:** Legacy SQL script (document) — `images` table, `UNIQUE(hotel_id, image_url)`  
**Severity:** MEDIUM  
**Status:** ⚠ LATENT — Triggered at runtime for URLs exceeding ~740 characters

**Technical Description:**

```sql
image_url VARCHAR(1000) NOT NULL,
...
UNIQUE(hotel_id, image_url)
```

PostgreSQL B-Tree index entries have a maximum size of approximately 2704 bytes for a default 8 KB page size (computed as `8192 / 3 - overhead`). The `UNIQUE(hotel_id, image_url)` constraint creates a multi-column B-Tree index on `(INTEGER, VARCHAR(1000))`. `INTEGER` consumes 4 bytes. `VARCHAR(1000)` encoded as UTF-8 can consume up to 4 bytes per character (4000 bytes for 1000 characters). In practice, Booking.com CDN URLs include base64-encoded segments that use only ASCII (1 byte/char), but the index size is bounded by the declared maximum, not the typical content.

When PostgreSQL attempts to insert a row where `hotel_id (4B) + image_url (N bytes) + overhead > 2704 bytes` — approximately at `image_url` lengths exceeding ~740 ASCII characters — the engine raises:

```
ERROR: index row size NNNN exceeds maximum 2704 for index "images_hotel_id_image_url_key"
DETAIL: Values larger than 1/3 of a buffer page cannot be indexed.
```

Booking.com gallery URLs with multiple query parameters (e.g., `?u=`, `?rs=`, `?w=`, `?h=`) routinely exceed 200–300 characters and can occasionally reach 600–800 characters in resized-image variants.

---

### MED-SQL-004 — `rooms.room_facilities TEXT[]` — No GIN Index, No Normalization Justification

**Source:** Legacy SQL script (document) — `rooms` table  
**Severity:** MEDIUM  
**Status:** ❌ ACTIVE — Full sequential scan on array queries

**Technical Description:**

```sql
room_facilities TEXT[],  -- Array de servicios de la habitación
```

The array type stores facility names as a PostgreSQL `TEXT[]` column with no index. Queries filtering by room facility:

```sql
SELECT * FROM rooms WHERE 'WiFi' = ANY(room_facilities);
-- or:
SELECT * FROM rooms WHERE room_facilities @> ARRAY['Balcony', 'Sea view'];
```

require a full sequential scan of the `rooms` table (`Seq Scan on rooms`) because no GIN index exists. For datasets with thousands of room records, this produces O(n) scan cost.

Additionally, array storage violates 1NF (First Normal Form). No justification for denormalization is documented. Without a GIN index (e.g., `CREATE INDEX ON rooms USING GIN (room_facilities)`), array containment queries are structurally unscalable.

---

### MED-SQL-005 — `policies.policy_type` Has No CHECK Constraint

**Source:** Legacy SQL script (document) — `policies` table  
**Severity:** MEDIUM  
**Status:** ❌ ACTIVE — Data integrity gap

**Technical Description:**

```sql
policy_type VARCHAR(50),  -- checkin, checkout, cancellation, payment, pets, children, etc.
```

The comment documents valid values, but no `CHECK` constraint is defined. The `UNIQUE(hotel_id, policy_type)` constraint prevents duplicate policy types per hotel but does not validate the type vocabulary. Application-layer code that filters policies by type (e.g., `WHERE policy_type = 'checkin'`) may produce empty result sets if an inconsistent value (e.g., `'check-in'`, `'check_in'`, `'CHECK IN'`) was inserted without validation.

---

### MED-SQL-006 — `statistics` Table Has No Automated Population Mechanism

**Source:** Legacy SQL script (document) — `statistics` table  
**Severity:** MEDIUM  
**Status:** ❌ ACTIVE — Table permanently empty; monitoring data unavailable

**Technical Description:**

```sql
CREATE TABLE IF NOT EXISTS statistics (
    id SERIAL PRIMARY KEY,
    stat_date DATE DEFAULT CURRENT_DATE,
    total_urls INT DEFAULT 0,
    ...
    UNIQUE(stat_date)
);
```

No trigger, scheduled function, cron expression, or application-layer call populates this table. The `get_system_stats()` function defined in the same script queries `url_queue` and `images` directly and does not insert into `statistics`. The v6.0 Python codebase does not reference `statistics` anywhere — it uses `system_metrics` (absent from the legacy schema). The `statistics` table will remain permanently empty for the entire application lifecycle.

---

### MED-PY-001 — `IN :ids` Tuple Expansion Unsupported in SQLAlchemy `text()` — `reset_stale_urls` Task

**Source:** `tasks.py` — `reset_stale_urls()` Celery task, lines ~296–306  
**Severity:** MEDIUM  
**Status:** ❌ ACTIVE — Runtime SQL error when stale URLs are detected

**Technical Description:**

```python
if reset_ids:
    db.execute(
        sa_text("""
            UPDATE url_language_status
            SET    status = 'pending', updated_at = NOW()
            WHERE  url_id IN :ids
              AND  status = 'processing'
        """),
        {"ids": tuple(reset_ids)}
    )
```

SQLAlchemy's `text()` construct does not automatically expand Python `tuple` values into SQL `IN (v1, v2, v3)` notation. When `reset_ids` contains one or more elements:

- The psycopg2 driver receives the literal string `IN :ids` with a `tuple` parameter.
- psycopg2 adapts a Python `tuple` as a PostgreSQL composite record literal `(v1, v2, v3)`, not as a list of values for the `IN` operator.
- PostgreSQL raises: `ERROR: operator does not exist: integer = record` or a `SyntaxError` depending on the psycopg2 version.

**Expected behavior:** The `url_language_status` rows corresponding to stale URLs are **not** reset. Only `url_queue` rows are correctly reset. The completeness state in `url_language_status` becomes permanently inconsistent with `url_queue`, blocking future scraping cycles for the affected URLs.

**Correct Pattern** using SQLAlchemy `text()`:

```python
db.execute(
    sa_text("""
        UPDATE url_language_status
        SET    status = 'pending', updated_at = NOW()
        WHERE  url_id = ANY(:ids)
          AND  status = 'processing'
    """),
    {"ids": reset_ids}   # list, not tuple — ANY() accepts a list via psycopg2 array adaptation
)
```

`= ANY(:ids)` with a Python `list` is correctly adapted by psycopg2 as `= ANY(ARRAY[v1, v2, v3])`.

---

### MED-SQL-007 — `v_hotels_summary` View — Aggregate Query Without Index Coverage on All Join Paths

**Source:** Legacy SQL script (document) — `v_hotels_summary` view  
**Severity:** MEDIUM  
**Status:** ⚠ LATENT — Acceptable at low volume; degrades at scale

**Technical Description:**

```sql
CREATE OR REPLACE VIEW v_hotels_summary AS
SELECT
    h.id, h.hotel_name, h.city, h.country, h.rating, h.total_reviews, h.language,
    COUNT(DISTINCT f.id) as facilities_count,
    COUNT(DISTINCT r.id) as rooms_count,
    COUNT(DISTINCT i.id) as images_count,
    SUM(CASE WHEN i.downloaded THEN 1 ELSE 0 END) as images_downloaded_count,
    h.created_at
FROM hotels h
LEFT JOIN hotel_facilities f ON h.id = f.hotel_id
LEFT JOIN rooms r ON h.id = r.hotel_id
LEFT JOIN images i ON h.id = i.hotel_id
GROUP BY h.id;
```

The view performs three `LEFT JOIN` aggregations across four tables. `COUNT(DISTINCT f.id)`, `COUNT(DISTINCT r.id)`, and `COUNT(DISTINCT i.id)` prevent hash aggregate short-circuit optimization. For a dataset with 10,000 hotels × average 20 facilities × 5 rooms × 30 images, PostgreSQL must process 10,000 × (20 + 5 + 30) = 550,000 joined rows per full scan of the view. The `GROUP BY h.id` requires a hash or sort aggregate over the full join output.

The view is not materialized. Any API endpoint that reads it performs the full computation on every request.

---

### MED-SQL-008 — `schema_migrations` Table Absent From Legacy Script — No Schema Version Audit Trail

**Source:** Legacy SQL script (document) — absence  
**Severity:** MEDIUM  
**Status:** ❌ ACTIVE — Schema version tracking unavailable

**Technical Description:**

The `install_clean_v31.sql` (v36) defines `schema_migrations` with columns `version`, `description`, `applied_at`, `applied_by`, `checksum`. This table is the authoritative record for schema history and is required by the Alembic migration environment (`alembic_env.py`) for version tracking. The legacy script creates no equivalent. Running migrations against a legacy-schema database will fail or produce undefined behavior due to the absent version baseline row `v36.0.0-clean-install`.

---

## Part IV — Low Severity Errors

---

### LOW-SQL-001 — Deprecated Quoted Language Name `'plpgsql'` in Trigger Function

**Source:** Legacy SQL script (document) — `update_updated_at_column()` function  
**Severity:** LOW  
**Status:** ⚠ DEPRECATION WARNING

**Technical Description:**

```sql
$$ language 'plpgsql';
```

PostgreSQL 14+ emits a deprecation notice for quoted language names in `CREATE FUNCTION`:

```
NOTICE:  language "plpgsql" is deprecated
HINT:    Use LANGUAGE plpgsql instead of LANGUAGE 'plpgsql'.
```

While currently non-fatal, this syntax is scheduled for removal in a future PostgreSQL major version. The correct modern syntax is:

```sql
$$ LANGUAGE plpgsql;
```

`install_clean_v31.sql` (v36) uses the correct unquoted syntax throughout.

---

### LOW-SQL-002 — Post-Install Verification `SELECT` Produces No Actionable Assertion

**Source:** Legacy SQL script (document) — end of script verification block  
**Severity:** LOW  
**Status:** ❌ DEFICIENCY — Verification provides no pass/fail signal

**Technical Description:**

```sql
SELECT schemaname, tablename, tableowner FROM pg_tables
WHERE schemaname = 'public' ORDER BY tablename;

SELECT schemaname, viewname FROM pg_views
WHERE schemaname = 'public' ORDER BY viewname;
```

When executed via `psql -f script.sql` (non-interactive mode) or from application code, these `SELECT` statements return result sets that are silently discarded. They produce no `RAISE NOTICE`, no assertion failure, and no logged output confirming or denying the presence of expected objects. If a table failed to create due to an earlier error, the verification block provides no detection.

`install_clean_v31.sql` (v36) replaces this with a `DO $$ ... RAISE NOTICE ... $$` block that counts tables, indexes, and views and emits visible diagnostic output to the psql console.

---

### LOW-PY-001 — Potential `NameError` on `disk_path` in `_disk_usage_percent()` Exception Handler

**Source:** `tasks.py` — `_disk_usage_percent()` function, line ~74  
**Severity:** LOW  
**Status:** ⚠ LATENT — Edge case on unusual `settings` configuration

**Technical Description:**

```python
def _disk_usage_percent() -> float:
    try:
        if sys.platform.startswith("win"):
            data_path = settings.BASE_DATA_PATH
            drive = os.path.splitdrive(data_path)[0] or "C:\\"
            if not drive.endswith("\\"):
                drive += "\\"
            disk_path = drive
        else:
            disk_path = "/"
        return psutil.disk_usage(disk_path).percent
    except (FileNotFoundError, PermissionError, OSError) as e:
        logger.warning(f"[BUG-15] No se pudo obtener uso de disco para '{disk_path}': {e}")
        return 0.0
```

If `settings.BASE_DATA_PATH` raises a `FileNotFoundError` or `OSError` (possible if the Pydantic settings validator performs filesystem validation), the exception is caught before `disk_path` is assigned. The `except` block then references `disk_path`, raising a secondary `NameError: name 'disk_path' is not defined`, which propagates uncaught and terminates the `save_system_metrics` Celery task with an unhandled exception rather than gracefully returning `0.0`.

**Corrective Pattern:**

```python
disk_path = "/"  # safe default before any conditional assignment
```

---

## Part V — Informational Notes

---

### INFO-SQL-001 — `LC_COLLATE = 'C'` — Multilingual String Ordering Impact Undocumented

**Source:** Legacy SQL script (document) — `CREATE DATABASE` statement  
**Severity:** INFO  
**Status:** ℹ OBSERVATION — No runtime error; potential incorrect behavior

**Technical Description:**

```sql
CREATE DATABASE booking_scraper
    ENCODING   = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE   = 'C'
    TEMPLATE   = template0;
```

`LC_COLLATE = 'C'` uses byte-order comparison for all string sorting operations. Under `C` locale, uppercase ASCII letters sort before lowercase, and accented characters (e.g., `é`, `á`, `ü`, `ñ`) sort by their Unicode code points rather than locale-specific rules. This produces incorrect alphabetical ordering for hotel names and city names in Spanish (`Ávila < Zamora` is reversed under C locale), German (`Über` sorts after `Z`), and French.

The application scrapes hotels in multiple languages and European countries. `ORDER BY hotel_name` or `ORDER BY city` in any API response will return results in byte-order rather than natural-language alphabetical order. This is not a data integrity issue but affects UX quality and search result ranking correctness.

`install_clean_v31.sql` (v36) preserves `LC_COLLATE = 'C'` for performance reasons (C locale avoids locale-aware index overhead and enables some index optimizations). The impact on multilingual ordering is not documented in the v36 schema comments or installation guide.

---

## Part VI — Error Index

| ID | Source | Severity | Category | Status |
|----|--------|----------|----------|--------|
| CRIT-SQL-001 | Legacy SQL | CRITICAL | Transaction/DDL | ❌ ACTIVE |
| CRIT-SQL-002 | Legacy SQL | CRITICAL | Schema Compatibility | ❌ ACTIVE |
| HIGH-SQL-001 | Legacy SQL | HIGH | Constraint | ❌ ACTIVE |
| HIGH-SQL-002 | Legacy SQL | HIGH | Timezone / DST | ❌ ACTIVE |
| HIGH-SQL-003 | Legacy SQL | HIGH | Concurrency | ❌ ACTIVE |
| HIGH-SQL-004 | Legacy SQL | HIGH | Division by Zero | ❌ ACTIVE |
| MED-SQL-001 | Legacy SQL | MEDIUM | Data Integrity | ❌ ACTIVE |
| MED-SQL-002 | Legacy SQL | MEDIUM | Referential Integrity | ❌ ACTIVE |
| MED-SQL-003 | Legacy SQL | MEDIUM | Index Size | ⚠ LATENT |
| MED-SQL-004 | Legacy SQL | MEDIUM | Performance / Normalization | ❌ ACTIVE |
| MED-SQL-005 | Legacy SQL | MEDIUM | Data Integrity | ❌ ACTIVE |
| MED-SQL-006 | Legacy SQL | MEDIUM | Functionality | ❌ ACTIVE |
| MED-PY-001 | tasks.py | MEDIUM | SQL / ORM | ❌ ACTIVE |
| MED-SQL-007 | Legacy SQL | MEDIUM | Performance | ⚠ LATENT |
| MED-SQL-008 | Legacy SQL | MEDIUM | Schema Governance | ❌ ACTIVE |
| LOW-SQL-001 | Legacy SQL | LOW | Code Quality | ⚠ DEPRECATION |
| LOW-SQL-002 | Legacy SQL | LOW | Operational | ❌ DEFICIENCY |
| LOW-PY-001 | tasks.py | LOW | Exception Handling | ⚠ LATENT |
| INFO-SQL-001 | Legacy SQL | INFO | Behavior | ℹ OBSERVATION |

---

## Part VII — Operational Recommendation

The legacy SQL script submitted in the document is **not the correct installation artifact** for the v6.0 codebase. It represents a prior schema generation predating the enterprise audit cycle. The correct and only supported installation script is:

```
sql/install_clean_v31.sql  (v36 schema)
```

To execute correctly on Windows 11 with PostgreSQL 15+:

```bash
psql -U postgres -f sql/install_clean_v31.sql
```

Do not execute `VACUUM ANALYZE` inside the script. If required post-install, run as a standalone command after the script completes.

---

*Report generated: 2026-03-06 | Version: v37.0.0 | Errors documented: 18 (2 CRITICAL, 4 HIGH, 8 MEDIUM, 3 LOW, 1 INFO)*
