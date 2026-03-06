-- =============================================================================
-- BookingScraper Pro v6.0  -  CLEAN INSTALL Script
-- PostgreSQL 15+ / 18+  |  Windows 11 Local Deployment
-- Version: v42 (Audit v37 + Execution Errors v41 Fixed 2026-03-06)
--
-- PURPOSE:
--   Full clean installation of the BookingScraper database from scratch.
--   Drops booking_scraper completely, recreates it, installs all objects.
--
-- [FIX NEW-EXEC-001] DROP DATABASE cannot run inside a DO $$ block in
--   PostgreSQL (not even via EXECUTE). This version uses psql \if metacommands
--   for conditional execution of top-level DDL statements.
--
-- [FIX NEW-EXEC-002] RAISE NOTICE is PL/pgSQL syntax. Cannot be used as a
--   bare SQL statement outside a DO $$ block. All standalone RAISE NOTICE
--   calls are now wrapped inside DO $$ BEGIN ... END $$.
--
-- [FIX NEW-EXEC-003] Residual views from prior installs remain in
--   booking_scraper. DROP VIEW IF EXISTS added before every CREATE VIEW.
--
-- CANONICAL FILE LOCATION (relative to project root C:\BookingScraper):
--   app/install_clean_v42.sql
--
-- EXECUTION METHOD (Windows 11 - mandatory two-step):
--
--   STEP 1 - From postgres database (drops and creates booking_scraper):
--     psql -U postgres -f app/install_clean_v42.sql
--
--   STEP 2 - Directly into booking_scraper (installs schema):
--     psql -U postgres -d booking_scraper -f app/install_clean_v42.sql
--
-- The script uses \if metacommands to detect the current database context
-- and execute only the relevant section.
--
-- SECTIONS:
--   0.  Pre-flight and ON_ERROR_STOP
--   1.  Conditional DROP/CREATE (postgres context only, via \if)
--   1b. Context verification guard
--   2.  Roles
--   3.  Extensions
--   4.  Tables
--   5.  Indexes
--   6.  Triggers
--   7.  Views (with DROP IF EXISTS before each CREATE)
--   7b. Schema version tracking
--   8.  Grants
--   9.  Post-install verification
-- =============================================================================


-- =============================================================================
-- SECTION 0 - PRE-FLIGHT
-- =============================================================================

\set ON_ERROR_STOP on
SET client_encoding = 'UTF8';

SELECT version() AS postgresql_version;


-- =============================================================================
-- SECTION 1 - CONDITIONAL DROP / CREATE
--
-- [FIX NEW-EXEC-001] DROP DATABASE cannot execute inside DO $$ EXECUTE.
-- PostgreSQL raises: "DROP DATABASE cannot be executed from a function".
-- Solution: use psql \if / \gset metacommands to run DROP DATABASE as a
-- top-level statement, which is the only valid context for this command.
--
-- \gset stores the SELECT result into psql variables.
-- \if :variable_name branches psql execution conditionally.
-- This is fully supported in psql 10+ (bundled with PostgreSQL 10+).
--
-- When connected to 'postgres'      -> in_postgres_ctx = t -> section runs
-- When connected to 'booking_scraper' -> in_postgres_ctx = f -> section skips
-- =============================================================================

SELECT (current_database() = 'postgres') AS in_postgres_ctx \gset

\if :in_postgres_ctx

DO $$
BEGIN
    RAISE NOTICE '================================================';
    RAISE NOTICE '  Step 1: connected to [postgres]';
    RAISE NOTICE '  Dropping and recreating booking_scraper...';
    RAISE NOTICE '================================================';
END $$;

-- Terminate active connections before dropping.
-- pg_terminate_backend is safe: clients will reconnect automatically.
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'booking_scraper'
  AND pid <> pg_backend_pid();

DO $$ BEGIN RAISE NOTICE '  Active connections terminated.'; END $$;

-- [FIX NEW-EXEC-001] DROP DATABASE runs here as a top-level statement,
-- NOT inside a DO block. This is the only valid context in PostgreSQL.
DROP DATABASE IF EXISTS booking_scraper;

DO $$ BEGIN RAISE NOTICE '  booking_scraper dropped.'; END $$;

-- Create the database with correct encoding for hotel name data (UTF8)
-- and C locale for deterministic text comparisons.
CREATE DATABASE booking_scraper
    ENCODING    = 'UTF8'
    LC_COLLATE  = 'C'
    LC_CTYPE    = 'C'
    TEMPLATE    = template0;

COMMENT ON DATABASE booking_scraper IS
    'BookingScraper Pro - hotel data extraction. Created v42 2026-03-06.';

DO $$ BEGIN RAISE NOTICE '  booking_scraper created.'; END $$;
DO $$ BEGIN RAISE NOTICE '  Switching context via \\connect ...'; END $$;

-- Switch to booking_scraper for the remainder of the script.
-- ON Windows 11, \connect may fail silently in psql -f mode.
-- Section 1b detects and aborts if the switch did not succeed.
\connect booking_scraper

\endif


-- =============================================================================
-- SECTION 1b - CONTEXT VERIFICATION GUARD
--
-- Executes in both Step 1 and Step 2.
-- If current_database() is not 'booking_scraper', RAISE EXCEPTION triggers
-- ON_ERROR_STOP and aborts psql before any DDL is executed.
-- =============================================================================

SELECT (current_database() = 'booking_scraper') AS in_correct_ctx \gset

\if :in_correct_ctx

DO $$
BEGIN
    RAISE NOTICE '================================================';
    RAISE NOTICE '  [OK] Context verified: [%]', current_database();
    RAISE NOTICE '  Installing schema...';
    RAISE NOTICE '================================================';
END $$;

\else

DO $$
BEGIN
    RAISE EXCEPTION
        E'[CRIT-INST-001] Wrong database context: [%]\n'
        E'Expected: [booking_scraper]\n'
        E'The \\connect metacommand failed silently on Windows.\n'
        'FIX: Use two-step method:\n'
        '  Step 1: psql -U postgres -f app/install_clean_v42.sql\n'
        '  Step 2: psql -U postgres -d booking_scraper -f app/install_clean_v42.sql',
        current_database();
END $$;

\endif


-- =============================================================================
-- SECTION 2 - ROLES
-- =============================================================================

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'scraper_app') THEN
        CREATE ROLE scraper_app LOGIN PASSWORD 'CHANGE_ME_IN_DOTENV';
        RAISE NOTICE '  Role scraper_app created.';
    ELSE
        RAISE NOTICE '  Role scraper_app already exists - skipped.';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'scraper_readonly') THEN
        CREATE ROLE scraper_readonly LOGIN PASSWORD 'CHANGE_ME_READONLY';
        RAISE NOTICE '  Role scraper_readonly created.';
    ELSE
        RAISE NOTICE '  Role scraper_readonly already exists - skipped.';
    END IF;
END $$;


-- =============================================================================
-- SECTION 3 - EXTENSIONS
-- Verified compatible: PostgreSQL 15-18. Versions on PG18.1:
--   pg_stat_statements 1.12, btree_gin 1.3, pg_trgm 1.6
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS btree_gin;
CREATE EXTENSION IF NOT EXISTS pg_trgm;


-- =============================================================================
-- SECTION 4 - TABLES
-- All use CREATE TABLE IF NOT EXISTS for idempotency on re-runs.
-- =============================================================================

-- ── url_queue ─────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS url_queue (
    id          SERIAL PRIMARY KEY,
    url         VARCHAR(512)    NOT NULL,

    status      VARCHAR(50)     NOT NULL DEFAULT 'pending',
    priority    INTEGER         NOT NULL DEFAULT 0,
    version_id  INTEGER         NOT NULL DEFAULT 0,
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

COMMENT ON TABLE  url_queue            IS 'Work queue: one row per unique hotel URL.';
COMMENT ON COLUMN url_queue.version_id IS 'Optimistic locking counter - incremented on every UPDATE.';


-- ── hotels ────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS hotels (
    id          SERIAL PRIMARY KEY,
    url_id      INTEGER REFERENCES url_queue(id) ON DELETE SET NULL,
    url         VARCHAR(512),
    language    VARCHAR(10)     NOT NULL DEFAULT 'en',

    name            VARCHAR(255),
    address         TEXT,
    description     TEXT,

    rating          DOUBLE PRECISION,
    total_reviews   INTEGER,
    rating_category VARCHAR(100),
    review_scores   JSONB,

    services    JSONB,
    facilities  JSONB,

    house_rules     TEXT,
    important_info  TEXT,

    rooms_info  JSONB,

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

COMMENT ON TABLE hotels IS 'Extracted hotel data: one row per (url x language).';


-- ── url_language_status ───────────────────────────────────────────────────────

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

COMMENT ON TABLE url_language_status IS
    'Per-(url, language) scraping state for completeness tracking.';


-- ── scraping_logs (partitioned) ───────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS scraping_logs (
    id               BIGSERIAL,
    url_id           INTEGER,
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
    PRIMARY KEY (id, timestamp)
) PARTITION BY RANGE (timestamp);

COMMENT ON TABLE scraping_logs IS
    'Audit log: one row per scraping attempt. Monthly range-partitioned on timestamp.';


-- FK enforcement trigger (partitioned tables cannot have FK constraints)
CREATE OR REPLACE FUNCTION check_scraping_log_url_id()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.url_id IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM url_queue WHERE id = NEW.url_id) THEN
            RAISE EXCEPTION
                '[FK] scraping_logs.url_id=% does not exist in url_queue.',
                NEW.url_id
            USING ERRCODE = 'foreign_key_violation';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trg_scraping_logs_fk_check
    BEFORE INSERT OR UPDATE OF url_id ON scraping_logs
    FOR EACH ROW EXECUTE FUNCTION check_scraping_log_url_id();

-- Cascade NULL on url_queue delete (equivalent to ON DELETE SET NULL)
CREATE OR REPLACE FUNCTION nullify_scraping_log_url_id()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    UPDATE scraping_logs SET url_id = NULL WHERE url_id = OLD.id;
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


-- Partition helper function
CREATE OR REPLACE FUNCTION create_scraping_logs_partition(p_year INT, p_month INT)
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    _name  TEXT;
    _start TEXT;
    _end   TEXT;
BEGIN
    _name  := format('scraping_logs_%s_%s',
                     to_char(p_year,  'FM0000'),
                     to_char(p_month, 'FM00'));
    _start := format('%s-%s-01',
                     to_char(p_year,  'FM0000'),
                     to_char(p_month, 'FM00'));
    _end   := to_char(
                  (to_date(_start, 'YYYY-MM-DD') + INTERVAL '1 month'),
                  'YYYY-MM-DD'
              );

    IF NOT EXISTS (
        SELECT 1 FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = _name AND n.nspname = 'public'
    ) THEN
        EXECUTE format(
            'CREATE TABLE %I PARTITION OF scraping_logs FOR VALUES FROM (%L) TO (%L)',
            _name, _start::TIMESTAMPTZ, _end::TIMESTAMPTZ
        );
        RAISE NOTICE '  Partition created: %', _name;
    ELSE
        RAISE NOTICE '  Partition already exists: %', _name;
    END IF;
END;
$$;

-- Pre-create current month + next two months
SELECT create_scraping_logs_partition(
    EXTRACT(YEAR  FROM NOW())::INT,
    EXTRACT(MONTH FROM NOW())::INT
);
SELECT create_scraping_logs_partition(
    EXTRACT(YEAR  FROM (NOW() + INTERVAL '1 month'))::INT,
    EXTRACT(MONTH FROM (NOW() + INTERVAL '1 month'))::INT
);
SELECT create_scraping_logs_partition(
    EXTRACT(YEAR  FROM (NOW() + INTERVAL '2 months'))::INT,
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
-- SECTION 5 - INDEXES
-- =============================================================================

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


CREATE UNIQUE INDEX IF NOT EXISTS ix_hotels_url_language
    ON hotels (url_id, language);

CREATE UNIQUE INDEX IF NOT EXISTS ix_hotels_url_lang_null
    ON hotels (url, language)
    WHERE url_id IS NULL;

CREATE INDEX IF NOT EXISTS ix_hotels_language
    ON hotels (language);

CREATE INDEX IF NOT EXISTS ix_hotels_url_id
    ON hotels (url_id);

CREATE INDEX IF NOT EXISTS ix_hotels_url
    ON hotels (url);

CREATE INDEX IF NOT EXISTS ix_hotels_scraped_at
    ON hotels (scraped_at);

CREATE INDEX IF NOT EXISTS ix_hotels_updated_at
    ON hotels (updated_at);

CREATE INDEX IF NOT EXISTS ix_hotels_name_trgm
    ON hotels USING GIN (name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS ix_hotels_review_scores_gin
    ON hotels USING GIN (review_scores);

CREATE INDEX IF NOT EXISTS ix_hotels_services_gin
    ON hotels USING GIN (services);

CREATE INDEX IF NOT EXISTS ix_hotels_facilities_gin
    ON hotels USING GIN (facilities);

CREATE INDEX IF NOT EXISTS ix_hotels_images_gin
    ON hotels USING GIN (images_urls);


CREATE INDEX IF NOT EXISTS ix_uls_url_status
    ON url_language_status (url_id, status);

CREATE INDEX IF NOT EXISTS ix_uls_status
    ON url_language_status (status);

CREATE INDEX IF NOT EXISTS ix_urllangs_updated_at
    ON url_language_status (updated_at);


CREATE INDEX IF NOT EXISTS ix_scraping_logs_url_id
    ON scraping_logs (url_id);

CREATE INDEX IF NOT EXISTS ix_scraping_logs_timestamp
    ON scraping_logs (timestamp DESC);

CREATE INDEX IF NOT EXISTS ix_scraping_logs_status
    ON scraping_logs (status);

CREATE INDEX IF NOT EXISTS ix_scraping_logs_task_id
    ON scraping_logs (task_id)
    WHERE task_id IS NOT NULL;


CREATE INDEX IF NOT EXISTS ix_system_metrics_recorded_at
    ON system_metrics (recorded_at DESC);

CREATE INDEX IF NOT EXISTS ix_vpn_rotations_rotated_at
    ON vpn_rotations (rotated_at DESC);


-- =============================================================================
-- SECTION 6 - TRIGGERS (auto-update updated_at)
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
            RAISE NOTICE '  Trigger trg_%_updated_at created.', t;
        ELSE
            RAISE NOTICE '  Trigger trg_%_updated_at already exists - skipped.', t;
        END IF;
    END LOOP;
END $$;


-- =============================================================================
-- SECTION 7 - VIEWS
--
-- [FIX NEW-EXEC-003] Residual views from prior installs persist in
-- booking_scraper because the DB was never fully dropped and recreated.
-- DROP VIEW IF EXISTS before each CREATE OR REPLACE VIEW ensures a clean
-- definition on every run, regardless of what version was previously installed.
-- =============================================================================

DROP VIEW IF EXISTS v_scraping_dashboard;

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


DROP VIEW IF EXISTS v_language_completeness;

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
-- SECTION 7b - SCHEMA VERSION TRACKING
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
    'Schema version tracking. Each row represents one applied migration.';

INSERT INTO schema_migrations (version, description, checksum)
VALUES (
    'v42.0.0-clean-install',
    'BookingScraper Pro v42 - all v37 audit + v41 execution errors fixed 2026-03-06',
    md5('v42.0.0-clean-install-2026-03-06')
) ON CONFLICT DO NOTHING;


-- =============================================================================
-- SECTION 8 - GRANTS
-- =============================================================================

GRANT USAGE ON SCHEMA public TO scraper_app, scraper_readonly;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES    IN SCHEMA public TO scraper_app;
GRANT USAGE, SELECT                  ON ALL SEQUENCES IN SCHEMA public TO scraper_app;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO scraper_readonly;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO scraper_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO scraper_readonly;


-- =============================================================================
-- SECTION 9 - POST-INSTALL VERIFICATION
-- =============================================================================

DO $$
DECLARE
    tbl_count  INTEGER;
    idx_count  INTEGER;
    view_count INTEGER;
    ext_count  INTEGER;
    ok         BOOLEAN := TRUE;
BEGIN
    -- Count core tables (information_schema includes partitioned parents)
    SELECT COUNT(*) INTO tbl_count
    FROM information_schema.tables
    WHERE table_schema = current_schema()
      AND table_name IN (
          'url_queue', 'hotels', 'url_language_status',
          'scraping_logs', 'vpn_rotations', 'system_metrics',
          'schema_migrations'
      );

    -- Count only application indexes (ix_% prefix)
    SELECT COUNT(*) INTO idx_count
    FROM pg_indexes
    WHERE schemaname = 'public'
      AND indexname LIKE 'ix_%';

    -- Count views in public schema
    SELECT COUNT(*) INTO view_count
    FROM information_schema.views
    WHERE table_schema = 'public';

    -- Count required extensions
    SELECT COUNT(*) INTO ext_count
    FROM pg_extension
    WHERE extname IN ('pg_stat_statements', 'btree_gin', 'pg_trgm');

    RAISE NOTICE '=====================================================';
    RAISE NOTICE '  BookingScraper Pro v42 - Install Verification';
    RAISE NOTICE '=====================================================';
    RAISE NOTICE '  Database    : %', current_database();
    RAISE NOTICE '  PostgreSQL  : %', version();
    RAISE NOTICE '  Tables      : % / 7', tbl_count;
    RAISE NOTICE '  App Indexes : % / 27', idx_count;
    RAISE NOTICE '  Views       : % / 2', view_count;
    RAISE NOTICE '  Extensions  : % / 3', ext_count;
    RAISE NOTICE '=====================================================';

    -- Assert database context
    IF current_database() <> 'booking_scraper' THEN
        RAISE EXCEPTION '[POST-VERIFY] Wrong database: [%]. Expected [booking_scraper].',
            current_database();
    END IF;
    RAISE NOTICE '  [OK] Database context: booking_scraper';

    -- Assert table count
    IF tbl_count = 7 THEN
        RAISE NOTICE '  [OK] Tables: 7 / 7';
    ELSE
        RAISE WARNING '  [FAIL] Tables: % / 7 - review schema.', tbl_count;
        ok := FALSE;
    END IF;

    -- Assert application index count
    IF idx_count = 27 THEN
        RAISE NOTICE '  [OK] App indexes: 27 / 27';
    ELSE
        RAISE WARNING '  [FAIL] App indexes: % / 27 - review indexes.', idx_count;
        ok := FALSE;
    END IF;

    -- Assert view count
    IF view_count = 2 THEN
        RAISE NOTICE '  [OK] Views: 2 / 2';
    ELSE
        RAISE WARNING '  [FAIL] Views: % / 2 - unexpected objects in schema.', view_count;
        ok := FALSE;
    END IF;

    -- Assert extensions
    IF ext_count = 3 THEN
        RAISE NOTICE '  [OK] Extensions: 3 / 3';
    ELSE
        RAISE WARNING '  [FAIL] Extensions: % / 3 - check pg_stat_statements, btree_gin, pg_trgm.', ext_count;
        ok := FALSE;
    END IF;

    RAISE NOTICE '=====================================================';
    IF ok THEN
        RAISE NOTICE '  [OK] All assertions passed.';
    ELSE
        RAISE NOTICE '  [!!] One or more assertions failed. Review WARNINGs above.';
    END IF;
    RAISE NOTICE '=====================================================';
END $$;


-- List installed extensions
SELECT extname, extversion
FROM pg_extension
WHERE extname IN ('pg_stat_statements', 'btree_gin', 'pg_trgm')
ORDER BY extname;


-- List tables including partitioned parent (relkind IN ('r','p'))
-- estimated_rows label: -1 = ANALYZE not yet run (expected on fresh install)
SELECT
    relname                                     AS table_name,
    CASE relkind
        WHEN 'r' THEN 'table'
        WHEN 'p' THEN 'partitioned table'
    END                                         AS table_type,
    CASE
        WHEN reltuples = -1 THEN 'not analyzed yet - run ANALYZE'
        ELSE reltuples::bigint::text || ' rows (estimated)'
    END                                         AS estimated_rows
FROM pg_class
WHERE relkind IN ('r', 'p')
  AND relnamespace = 'public'::regnamespace
ORDER BY table_type DESC, relname;


-- List all application indexes
SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public'
  AND indexname LIKE 'ix_%'
ORDER BY tablename, indexname;


-- Initialize statistics for all tables.
-- ANALYZE is non-blocking on an empty database.
-- After ANALYZE, reltuples shows 0 instead of -1 for all tables.
ANALYZE;

-- [FIX NEW-EXEC-002] RAISE NOTICE must be inside a DO block.
-- Bare RAISE NOTICE as top-level SQL is invalid PL/pgSQL outside a function.
DO $$ BEGIN RAISE NOTICE '  [OK] ANALYZE complete - statistics initialized.'; END $$;
DO $$ BEGIN RAISE NOTICE '  BookingScraper Pro v42 is ready.'; END $$;
