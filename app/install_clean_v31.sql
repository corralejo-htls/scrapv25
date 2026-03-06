-- =============================================================================
-- BookingScraper Pro v6.0  —  CLEAN INSTALL Script
-- PostgreSQL 15+  |  Windows 11 Local Deployment
-- Version: v36 (Enterprise Audit v35 — All Critical Issues Fixed 2026-03-06)
--
-- PURPOSE:
--   Full clean installation of the BookingScraper database from scratch.
--   Run this on a fresh PostgreSQL instance OR after DROP DATABASE.
--   For in-place upgrades on existing databases, use migration_v30_enterprise_audit.sql
--
-- REQUIREMENTS:
--   PostgreSQL 15+ running locally
--   Run as superuser (postgres):
--     psql -U postgres -f install_clean_v31.sql
--
-- SECTIONS:
--   0. Pre-flight checks
--   1. Database creation
--   2. Roles & Permissions
--   3. Extensions
--   4. Tables
--   5. Indexes (including v30 additions)
--   6. Constraints
--   7. Triggers
--   8. Views
--   9. Seed data (empty — application populates via load_urls.py)
--  10. Post-install verification
-- =============================================================================

-- =============================================================================
-- SECTION 0 — PRE-FLIGHT
-- =============================================================================

-- Set client encoding explicitly to avoid locale issues on Windows
SET client_encoding = 'UTF8';

-- Display PostgreSQL version for install log
SELECT version() AS postgresql_version;


-- =============================================================================
-- SECTION 1 — DATABASE CREATION
-- Run this block as postgres superuser from the default 'postgres' database.
-- If booking_scraper already exists, skip this section or drop it first:
--   DROP DATABASE IF EXISTS booking_scraper;
-- =============================================================================

CREATE DATABASE booking_scraper
    ENCODING    = 'UTF8'
    LC_COLLATE  = 'C'
    LC_CTYPE    = 'C'
    TEMPLATE    = template0;

COMMENT ON DATABASE booking_scraper IS
    'BookingScraper Pro — hotel data extraction. Created v31 2026-03-05.';

-- Connect to the new database before running remaining sections
\connect booking_scraper


-- =============================================================================
-- SECTION 2 — ROLES & PERMISSIONS
-- =============================================================================

-- Application role (write access for the FastAPI process)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'scraper_app') THEN
        CREATE ROLE scraper_app LOGIN PASSWORD 'CHANGE_ME_IN_DOTENV';
    END IF;
END $$;

-- Read-only role (for monitoring, reporting, BI tools)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'scraper_readonly') THEN
        CREATE ROLE scraper_readonly LOGIN PASSWORD 'CHANGE_ME_READONLY';
    END IF;
END $$;

-- NOTE: Replace passwords with strong values in production.
-- For Windows 11 local development, you may use the postgres superuser directly
-- by setting DB_USER=postgres and DB_PASSWORD=<your postgres password> in .env.


-- =============================================================================
-- SECTION 3 — EXTENSIONS
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS pg_stat_statements;  -- slow query monitoring
CREATE EXTENSION IF NOT EXISTS btree_gin;            -- GIN on B-tree types
CREATE EXTENSION IF NOT EXISTS pg_trgm;              -- trigram fuzzy search


-- =============================================================================
-- SECTION 4 — TABLES
-- =============================================================================

-- ── url_queue ─────────────────────────────────────────────────────────────────
-- Primary work queue: one row per unique Booking.com hotel URL.

CREATE TABLE IF NOT EXISTS url_queue (
    id          SERIAL PRIMARY KEY,
    url         VARCHAR(512)    NOT NULL,

    status      VARCHAR(50)     NOT NULL DEFAULT 'pending',
    priority    INTEGER         NOT NULL DEFAULT 0,
    version_id  INTEGER         NOT NULL DEFAULT 0,   -- optimistic locking
    language    VARCHAR(10)     NOT NULL DEFAULT 'en',

    retry_count INTEGER         NOT NULL DEFAULT 0,
    max_retries INTEGER         NOT NULL DEFAULT 3,
    last_error  VARCHAR(2000),

    scraped_at  TIMESTAMPTZ,
    created_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_url_queue_url           UNIQUE (url),
    CONSTRAINT chk_urlqueue_retry_nonneg  CHECK (retry_count >= 0),
    CONSTRAINT chk_urlqueue_max_nonneg    CHECK (max_retries >= 0),
    CONSTRAINT chk_urlqueue_retry_lte_max CHECK (retry_count <= max_retries),
    CONSTRAINT chk_urlqueue_status_valid  CHECK (
        status IN ('pending','processing','completed','failed','incomplete')
    )
) WITH (fillfactor = 70);
-- [FIX ERR-DB-007] fillfactor=70: reserves 30% of each page for HOT updates.
-- url_queue has frequent status/retry_count UPDATEs — reduces table bloat.
-- HOT (Heap-Only Tuple) updates avoid index update overhead for non-indexed cols.

COMMENT ON TABLE url_queue IS 'Work queue: one row per unique hotel URL.';
COMMENT ON COLUMN url_queue.version_id IS 'Optimistic locking counter — incremented on every UPDATE.';


-- ── hotels ────────────────────────────────────────────────────────────────────
-- Scraped hotel data: one row per (url_queue entry × language).

CREATE TABLE IF NOT EXISTS hotels (
    id          SERIAL PRIMARY KEY,
    url_id      INTEGER REFERENCES url_queue(id) ON DELETE SET NULL,
    url         VARCHAR(512),
    language    VARCHAR(10)     NOT NULL DEFAULT 'en',

    -- Basic information
    name        VARCHAR(255),
    address     TEXT,
    description TEXT,

    -- Ratings
    rating          DOUBLE PRECISION,
    total_reviews   INTEGER,
    rating_category VARCHAR(100),
    review_scores   JSONB,

    -- Amenities
    services    JSONB,
    facilities  JSONB,

    -- Policies
    house_rules     TEXT,
    important_info  TEXT,

    -- Rooms
    rooms_info  JSONB,

    -- Images
    images_urls     JSONB,
    images_local    JSONB,
    images_count    INTEGER NOT NULL DEFAULT 0,

    scraped_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_hotel_rating_range CHECK (
        rating IS NULL OR (rating >= 0.0 AND rating <= 10.0)
    ),
    CONSTRAINT chk_hotel_services_array CHECK (
        services IS NULL OR jsonb_typeof(services) = 'array'
    ),
    CONSTRAINT chk_hotel_facilities_object CHECK (
        facilities IS NULL OR jsonb_typeof(facilities) = 'object'
    ),
    CONSTRAINT chk_hotel_review_scores_object CHECK (
        review_scores IS NULL OR jsonb_typeof(review_scores) = 'object'
    ),
    CONSTRAINT chk_hotel_images_urls_array CHECK (
        images_urls IS NULL OR jsonb_typeof(images_urls) = 'array'
    )
);

COMMENT ON TABLE hotels IS 'Extracted hotel data: one row per (url × language).';


-- ── url_language_status ───────────────────────────────────────────────────────
-- Per-(url, language) processing state for completeness tracking.

CREATE TABLE IF NOT EXISTS url_language_status (
    id          SERIAL PRIMARY KEY,
    url_id      INTEGER NOT NULL REFERENCES url_queue(id) ON DELETE CASCADE,
    language    VARCHAR(10) NOT NULL,
    status      VARCHAR(50) NOT NULL DEFAULT 'pending',

    retry_count INTEGER     NOT NULL DEFAULT 0,
    max_retries INTEGER     NOT NULL DEFAULT 3,
    last_error  VARCHAR(2000),
    scraped_at  TIMESTAMPTZ,
    version_id  INTEGER     NOT NULL DEFAULT 0,

    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uls_url_lang_unique        UNIQUE (url_id, language),
    CONSTRAINT chk_uls_retry_nonneg       CHECK (retry_count >= 0),
    CONSTRAINT chk_uls_max_nonneg         CHECK (max_retries >= 0),
    CONSTRAINT chk_uls_retry_lte_max      CHECK (retry_count <= max_retries),
    CONSTRAINT chk_uls_status_valid       CHECK (
        status IN ('pending','processing','completed','failed','skipped_existing')
    )
) WITH (fillfactor = 70);
-- [FIX ERR-DB-007] fillfactor=70: same rationale as url_queue.
-- url_language_status has one UPDATE per language per URL per scraping cycle.

COMMENT ON TABLE url_language_status IS
    'Per-(url, language) scraping state for completeness tracking.';


-- ── scraping_logs ─────────────────────────────────────────────────────────────
-- [FIX-025 / MED-015 / CRIT-006] Monthly RANGE partitioning on timestamp.
--
-- MOTIVATION: scraping_logs grows at ~1 row per URL×language per run.
-- At 1000 URLs × 5 languages × 10 runs/day = 50,000 rows/day → ~18M rows/year.
-- Without partitioning, queries filtered by timestamp (e.g., last 30 days) require
-- full table scan: O(n) → O(18M) after 1 year. With monthly partitions,
-- PostgreSQL's partition pruning reduces the scan to ≤2 partitions → O(1.5M max).
--
-- STRATEGY: PARTITION BY RANGE (timestamp), monthly granularity.
-- Partition management: a PostgreSQL function creates the next month's partition
-- automatically when called. On a fresh install, the current month and next month
-- are pre-created so scraping can start immediately.
--
-- IMPORTANT: 'id SERIAL PRIMARY KEY' is NOT compatible with declarative partitioning.
-- In PostgreSQL 10+, the PRIMARY KEY must include the partition key (timestamp).
-- The surrogate key is implemented as BIGSERIAL (not PRIMARY KEY) with a UNIQUE
-- constraint on (id, timestamp), satisfying uniqueness without blocking partitioning.
-- References to scraping_logs.id from external code use this surrogate id.

CREATE TABLE IF NOT EXISTS scraping_logs (
    id               BIGSERIAL,
    url_id           INTEGER,          -- FK enforced by trigger (partitioned tables
                                       -- cannot have FK constraints to non-partition keys)
    status           VARCHAR(50)  NOT NULL,
    language         VARCHAR(10),
    duration_seconds DOUBLE PRECISION,
    items_extracted  INTEGER      NOT NULL DEFAULT 0,
    error_message    TEXT,

    http_status_code INTEGER,
    user_agent       TEXT,
    vpn_ip           VARCHAR(50),
    task_id          VARCHAR(100),

    timestamp        TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    -- Composite primary key: surrogate id + partition key (timestamp)
    PRIMARY KEY (id, timestamp)
) PARTITION BY RANGE (timestamp);

COMMENT ON TABLE scraping_logs IS
    'Audit log: one row per scraping attempt. Monthly range-partitioned on timestamp.';


-- ── FK enforcement trigger for scraping_logs.url_id ─────────────────────────
-- [FIX CRIT-002] Partitioned tables in PostgreSQL cannot have FK constraints
-- referencing non-partition-key columns. Solution: BEFORE INSERT/UPDATE trigger
-- that enforces referential integrity manually.
--
-- Behaviour:
--   INSERT/UPDATE with url_id NOT NULL + NOT IN url_queue → RAISE EXCEPTION
--   INSERT/UPDATE with url_id IS NULL → allowed (no queue entry, standalone log)
--   INSERT/UPDATE with url_id IN url_queue → allowed (valid FK)
--
-- CASCADE-like cleanup: a separate trigger fires AFTER DELETE on url_queue
-- to NULL-out dangling references in scraping_logs, matching ON DELETE SET NULL.

CREATE OR REPLACE FUNCTION check_scraping_log_url_id()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.url_id IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM url_queue WHERE id = NEW.url_id) THEN
            RAISE EXCEPTION
                '[CRIT-002] FK violation: scraping_logs.url_id=% does not exist in url_queue.',
                NEW.url_id
            USING ERRCODE = 'foreign_key_violation';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

-- Attach trigger to partitioned parent; PostgreSQL 13+ propagates to all partitions.
CREATE OR REPLACE TRIGGER trg_scraping_logs_fk_check
    BEFORE INSERT OR UPDATE OF url_id ON scraping_logs
    FOR EACH ROW EXECUTE FUNCTION check_scraping_log_url_id();

-- Cascade NULL when url_queue row is deleted (matches ON DELETE SET NULL behaviour)
CREATE OR REPLACE FUNCTION nullify_scraping_log_url_id()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    UPDATE scraping_logs
    SET url_id = NULL
    WHERE url_id = OLD.id;
    RETURN OLD;
END;
$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'trg_url_queue_cascade_logs'
    ) THEN
        CREATE TRIGGER trg_url_queue_cascade_logs
            AFTER DELETE ON url_queue
            FOR EACH ROW EXECUTE FUNCTION nullify_scraping_log_url_id();
    END IF;
END $$;


-- ── Partition creation helper function ────────────────────────────────────────
-- Creates a monthly partition for the given year+month if it does not exist.
-- Call this function once per month (e.g., from the cleanup Celery task or a
-- pg_cron job) to ensure the next month's partition exists before the month starts.
CREATE OR REPLACE FUNCTION create_scraping_logs_partition(p_year INT, p_month INT)
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    _partition_name TEXT;
    _start_date     TEXT;
    _end_date       TEXT;
BEGIN
    _partition_name := format('scraping_logs_%s_%s',
                              to_char(p_year, 'FM0000'),
                              to_char(p_month, 'FM00'));
    _start_date := format('%s-%s-01', to_char(p_year, 'FM0000'), to_char(p_month, 'FM00'));
    -- End date: first day of the following month
    _end_date := to_char(
                     (to_date(_start_date, 'YYYY-MM-DD') + INTERVAL '1 month'),
                     'YYYY-MM-DD'
                 );

    IF NOT EXISTS (
        SELECT 1 FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = _partition_name AND n.nspname = 'public'
    ) THEN
        EXECUTE format(
            'CREATE TABLE %I PARTITION OF scraping_logs '
            'FOR VALUES FROM (%L) TO (%L)',
            _partition_name,
            _start_date::TIMESTAMPTZ,
            _end_date::TIMESTAMPTZ
        );
        RAISE NOTICE 'Created partition: %', _partition_name;
    ELSE
        RAISE NOTICE 'Partition already exists: %', _partition_name;
    END IF;
END;
$$;

-- ── Pre-create partitions for current month + next two months ─────────────────
-- Ensures INSERT works immediately on a fresh install without waiting for the
-- partition management task to run.
SELECT create_scraping_logs_partition(
    EXTRACT(YEAR FROM NOW())::INT,
    EXTRACT(MONTH FROM NOW())::INT
);
SELECT create_scraping_logs_partition(
    EXTRACT(YEAR FROM (NOW() + INTERVAL '1 month'))::INT,
    EXTRACT(MONTH FROM (NOW() + INTERVAL '1 month'))::INT
);
SELECT create_scraping_logs_partition(
    EXTRACT(YEAR FROM (NOW() + INTERVAL '2 months'))::INT,
    EXTRACT(MONTH FROM (NOW() + INTERVAL '2 months'))::INT
);


-- ── vpn_rotations ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS vpn_rotations (
    id              SERIAL PRIMARY KEY,
    old_ip          VARCHAR(45),
    new_ip          VARCHAR(45),
    country         VARCHAR(100),
    rotation_reason VARCHAR(100),
    requests_count  INTEGER NOT NULL DEFAULT 0,
    success         BOOLEAN NOT NULL DEFAULT TRUE,
    error_message   TEXT,
    rotated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE vpn_rotations IS 'Log of NordVPN rotation events.';


-- ── system_metrics ────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS system_metrics (
    id                  SERIAL PRIMARY KEY,

    urls_pending        INTEGER NOT NULL DEFAULT 0,
    urls_processing     INTEGER NOT NULL DEFAULT 0,
    urls_completed      INTEGER NOT NULL DEFAULT 0,
    urls_failed         INTEGER NOT NULL DEFAULT 0,

    hotels_scraped      INTEGER NOT NULL DEFAULT 0,
    images_downloaded   INTEGER NOT NULL DEFAULT 0,
    active_workers      INTEGER NOT NULL DEFAULT 0,

    avg_scraping_time   DOUBLE PRECISION,
    total_scraping_time DOUBLE PRECISION NOT NULL DEFAULT 0.0,

    cpu_usage           DOUBLE PRECISION,
    memory_usage        DOUBLE PRECISION,
    disk_usage          DOUBLE PRECISION,

    recorded_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE system_metrics IS 'Periodic system resource snapshots.';


-- =============================================================================
-- SECTION 5 — INDEXES
-- All created with IF NOT EXISTS for idempotency.
-- =============================================================================

-- ── url_queue ─────────────────────────────────────────────────────────────────

-- Primary dispatch index: partial, covers only dispatchable rows
-- CREATE INDEX CONCURRENTLY avoids locking on a live database:
-- For clean install, simple CREATE INDEX is fine.
CREATE INDEX IF NOT EXISTS ix_urlqueue_pending_dispatch
    ON url_queue (priority DESC, created_at ASC)
    WHERE status = 'pending' AND retry_count < max_retries;

CREATE INDEX IF NOT EXISTS ix_urlqueue_status
    ON url_queue (status);

CREATE INDEX IF NOT EXISTS ix_urlqueue_status_priority
    ON url_queue (status, priority);

CREATE INDEX IF NOT EXISTS ix_urlqueue_dispatch
    ON url_queue (status, priority, created_at);

CREATE INDEX IF NOT EXISTS ix_urlqueue_url
    ON url_queue (url);

CREATE INDEX IF NOT EXISTS ix_urlqueue_updated_at
    ON url_queue (updated_at);


-- ── hotels ────────────────────────────────────────────────────────────────────

-- Composite unique: (url_id, language) — primary deduplication key
CREATE UNIQUE INDEX IF NOT EXISTS ix_hotels_url_language
    ON hotels (url_id, language);

-- Partial unique for url_id IS NULL case (PostgreSQL NULLs are distinct)
CREATE UNIQUE INDEX IF NOT EXISTS ix_hotels_url_lang_null
    ON hotels (url, language)
    WHERE url_id IS NULL;

CREATE INDEX IF NOT EXISTS ix_hotels_language
    ON hotels (language);

CREATE INDEX IF NOT EXISTS ix_hotels_url_id
    ON hotels (url_id);

-- [FIX HIGH-003] B-Tree index on hotels.url (text column)
-- Prevents full table scans on deduplication queries WHERE url = :url
CREATE INDEX IF NOT EXISTS ix_hotels_url
    ON hotels (url);

CREATE INDEX IF NOT EXISTS ix_hotels_scraped_at
    ON hotels (scraped_at);

CREATE INDEX IF NOT EXISTS ix_hotels_updated_at
    ON hotels (updated_at);

-- Trigram index for fuzzy hotel name search
CREATE INDEX IF NOT EXISTS ix_hotels_name_trgm
    ON hotels USING GIN (name gin_trgm_ops);

-- GIN indexes for JSONB containment queries (@> operator)
CREATE INDEX IF NOT EXISTS ix_hotels_review_scores_gin
    ON hotels USING GIN (review_scores);

CREATE INDEX IF NOT EXISTS ix_hotels_services_gin
    ON hotels USING GIN (services);

CREATE INDEX IF NOT EXISTS ix_hotels_facilities_gin
    ON hotels USING GIN (facilities);

-- [FIX HIGH-010] GIN index on images_urls JSONB
-- Enables: WHERE images_urls @> '["https://..."]' with index scan
CREATE INDEX IF NOT EXISTS ix_hotels_images_gin
    ON hotels USING GIN (images_urls);


-- ── url_language_status ───────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS ix_uls_url_status
    ON url_language_status (url_id, status);

CREATE INDEX IF NOT EXISTS ix_uls_status
    ON url_language_status (status);

CREATE INDEX IF NOT EXISTS ix_urllangs_updated_at
    ON url_language_status (updated_at);


-- ── scraping_logs ─────────────────────────────────────────────────────────────
-- [FIX-025] Indexes on partitioned table: PostgreSQL 11+ propagates these
-- automatically to all existing and future child partitions.

CREATE INDEX IF NOT EXISTS ix_scraping_logs_url_id
    ON scraping_logs (url_id);

CREATE INDEX IF NOT EXISTS ix_scraping_logs_timestamp
    ON scraping_logs (timestamp DESC);

CREATE INDEX IF NOT EXISTS ix_scraping_logs_status
    ON scraping_logs (status);

CREATE INDEX IF NOT EXISTS ix_scraping_logs_task_id
    ON scraping_logs (task_id)
    WHERE task_id IS NOT NULL;


-- ── system_metrics / vpn_rotations ───────────────────────────────────────────

CREATE INDEX IF NOT EXISTS ix_system_metrics_recorded_at
    ON system_metrics (recorded_at DESC);

CREATE INDEX IF NOT EXISTS ix_vpn_rotations_rotated_at
    ON vpn_rotations (rotated_at DESC);


-- =============================================================================
-- SECTION 6 — TRIGGERS (auto-update updated_at)
-- =============================================================================

CREATE OR REPLACE FUNCTION trg_set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DO $$
DECLARE
    t TEXT;
BEGIN
    FOR t IN VALUES ('url_queue'), ('url_language_status') LOOP
        IF NOT EXISTS (
            SELECT 1 FROM pg_trigger
            WHERE tgname = 'trg_' || t || '_updated_at'
        ) THEN
            EXECUTE format(
                'CREATE TRIGGER trg_%I_updated_at
                 BEFORE UPDATE ON %I
                 FOR EACH ROW EXECUTE FUNCTION trg_set_updated_at()',
                t, t
            );
        END IF;
    END LOOP;
END $$;


-- =============================================================================
-- SECTION 7 — VIEWS
-- =============================================================================

-- Scraping dashboard view
CREATE OR REPLACE VIEW v_scraping_dashboard AS
SELECT
    uq.id                                           AS url_id,
    uq.url,
    uq.status,
    uq.priority,
    uq.retry_count,
    uq.max_retries,
    uq.scraped_at,
    COUNT(h.id)                                     AS hotel_count,
    COUNT(DISTINCT h.language)                      AS languages_scraped,
    COALESCE(SUM(h.images_count), 0)                AS total_images,
    COALESCE(AVG(h.rating), 0)                      AS avg_rating
FROM url_queue uq
LEFT JOIN hotels h ON h.url_id = uq.id
GROUP BY uq.id, uq.url, uq.status, uq.priority,
         uq.retry_count, uq.max_retries, uq.scraped_at;

COMMENT ON VIEW v_scraping_dashboard IS
    'Summary view: one row per URL with aggregated hotel/language counts.';


-- Language completeness view
CREATE OR REPLACE VIEW v_language_completeness AS
SELECT
    uq.id                                           AS url_id,
    uq.url,
    COUNT(uls.id)                                   AS total_languages,
    COUNT(uls.id) FILTER (WHERE uls.status = 'completed')  AS completed,
    COUNT(uls.id) FILTER (WHERE uls.status = 'failed')     AS failed,
    COUNT(uls.id) FILTER (WHERE uls.status = 'pending')    AS pending,
    ROUND(
        100.0 * COUNT(uls.id) FILTER (WHERE uls.status = 'completed')
        / NULLIF(COUNT(uls.id), 0),
        1
    )                                               AS completion_pct
FROM url_queue uq
LEFT JOIN url_language_status uls ON uls.url_id = uq.id
GROUP BY uq.id, uq.url;

COMMENT ON VIEW v_language_completeness IS
    'Per-URL language scraping completion percentage.';


-- =============================================================================
-- SECTION 7b — SCHEMA VERSION TRACKING
-- [FIX MED-004] Track applied schema changes to support future migrations.
-- This table is the authoritative record of database schema history.
-- =============================================================================

CREATE TABLE IF NOT EXISTS schema_migrations (
    id          SERIAL PRIMARY KEY,
    version     VARCHAR(50)  NOT NULL UNIQUE,
    description TEXT,
    applied_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    applied_by  VARCHAR(100) NOT NULL DEFAULT CURRENT_USER,
    checksum    VARCHAR(64),
    CONSTRAINT uq_schema_migration_version UNIQUE (version)
);

COMMENT ON TABLE schema_migrations IS
    'Schema version tracking. Each row represents one applied migration script.';

-- Record this clean install as migration 000
INSERT INTO schema_migrations (version, description, checksum)
VALUES (
    'v36.0.0-clean-install',
    'BookingScraper Pro v36 clean install — all enterprise audit fixes applied',
    md5('v36.0.0-clean-install-2026-03-06')
) ON CONFLICT DO NOTHING;


-- =============================================================================
-- SECTION 8 — PERMISSIONS
-- =============================================================================

-- Grant schema usage
GRANT USAGE ON SCHEMA public TO scraper_app, scraper_readonly;

-- Application role: full CRUD on all tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO scraper_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO scraper_app;

-- Read-only role: SELECT only
GRANT SELECT ON ALL TABLES IN SCHEMA public TO scraper_readonly;

-- Ensure future tables inherit these grants
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO scraper_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO scraper_readonly;


-- =============================================================================
-- SECTION 9 — POST-INSTALL VERIFICATION
-- Run this to confirm the installation was successful.
-- =============================================================================

DO $$
DECLARE
    tbl_count  INTEGER;
    idx_count  INTEGER;
    view_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO tbl_count
    FROM information_schema.tables
    WHERE table_schema = current_schema()
      AND table_name IN (
          'url_queue','hotels','url_language_status',
          'scraping_logs','vpn_rotations','system_metrics',
          'schema_migrations'
      );

    SELECT COUNT(*) INTO idx_count
    FROM pg_indexes
    WHERE schemaname = 'public'
      AND indexname LIKE 'ix_%';

    SELECT COUNT(*) INTO view_count
    FROM information_schema.views
    WHERE table_schema = 'public';

    RAISE NOTICE '===============================================';
    RAISE NOTICE '  BookingScraper Pro v31 — Install Verification';
    RAISE NOTICE '===============================================';
    RAISE NOTICE '  Database    : %', current_database();
    RAISE NOTICE '  PostgreSQL  : %', version();
    RAISE NOTICE '  Tables      : % / 6', tbl_count;
    RAISE NOTICE '  Indexes     : %', idx_count;
    RAISE NOTICE '  Views       : %', view_count;
    RAISE NOTICE '===============================================';
    RAISE NOTICE '  Extensions:';
END $$;

-- List installed extensions
SELECT extname, extversion
FROM pg_extension
WHERE extname IN ('pg_stat_statements', 'btree_gin', 'pg_trgm');

-- List created tables
SELECT
    relname  AS table_name,
    reltuples::bigint AS estimated_rows
FROM pg_class
WHERE relkind = 'r'
  AND relnamespace = 'public'::regnamespace
ORDER BY relname;

-- List all indexes
SELECT
    indexname,
    tablename,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
