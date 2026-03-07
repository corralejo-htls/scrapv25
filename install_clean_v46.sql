-- =============================================================================
-- BookingScraper Pro v6.0 — Full Database Schema
-- Version : 46  (corrected from v43 audit findings)
-- Platform : PostgreSQL 15-18 on Windows 11
-- Usage    : psql -U bookingscraper_app -d bookingscraper -f install_clean_v46.sql
-- =============================================================================
-- Run on an EMPTY database only.
-- Creates: tables, all indexes (B-Tree, GIN, partial unique),
--          triggers, roles, partitions, and seed data.
-- =============================================================================

\set ON_ERROR_STOP on
BEGIN;

-- ── Extensions ────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ── url_queue ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS url_queue (
    id            UUID         PRIMARY KEY DEFAULT uuid_generate_v4(),
    url           VARCHAR(2048) NOT NULL,
    language      VARCHAR(10)  NOT NULL DEFAULT 'en',
    status        VARCHAR(30)  NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending','processing','done','error','skipped')),
    priority      SMALLINT     NOT NULL DEFAULT 5
                  CHECK (priority BETWEEN 1 AND 10),
    retry_count   SMALLINT     NOT NULL DEFAULT 0 CHECK (retry_count >= 0),
    max_retries   SMALLINT     NOT NULL DEFAULT 3,
    error_message VARCHAR(2000),
    claimed_by    VARCHAR(255),
    claimed_at    TIMESTAMPTZ,
    completed_at  TIMESTAMPTZ,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    version_id    INTEGER      NOT NULL DEFAULT 0
);

-- ── url_language_status ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS url_language_status (
    id            UUID         PRIMARY KEY DEFAULT uuid_generate_v4(),
    url_id        UUID         NOT NULL REFERENCES url_queue(id) ON DELETE CASCADE,
    language      VARCHAR(10)  NOT NULL,
    status        VARCHAR(30)  NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending','processing','done','error','skipped')),
    attempt_count SMALLINT     NOT NULL DEFAULT 0,
    last_error    VARCHAR(2000),
    completed_at  TIMESTAMPTZ,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    version_id    INTEGER      NOT NULL DEFAULT 0,
    UNIQUE (url_id, language)
);

-- ── hotels ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS hotels (
    id            UUID         PRIMARY KEY DEFAULT uuid_generate_v4(),
    url           VARCHAR(2048),
    language      VARCHAR(10)  NOT NULL DEFAULT 'en',
    url_id        UUID         REFERENCES url_queue(id) ON DELETE SET NULL,
    hotel_name    VARCHAR(500),
    hotel_id_ext  VARCHAR(100),
    star_rating   NUMERIC(2,1) CHECK (star_rating IS NULL OR star_rating BETWEEN 0 AND 5),
    review_score  NUMERIC(3,1) CHECK (review_score IS NULL OR review_score BETWEEN 0 AND 10),
    review_count  INTEGER      CHECK (review_count IS NULL OR review_count >= 0),
    address       VARCHAR(1000),
    city          VARCHAR(255),
    country       VARCHAR(100),
    latitude      NUMERIC(10,7),
    longitude     NUMERIC(10,7),
    amenities     JSONB        NOT NULL DEFAULT '[]',
    room_types    JSONB        NOT NULL DEFAULT '[]',
    policies      JSONB        NOT NULL DEFAULT '{}',
    photos        JSONB        NOT NULL DEFAULT '[]',
    raw_data      JSONB        NOT NULL DEFAULT '{}',
    scrape_status VARCHAR(30)  NOT NULL DEFAULT 'pending'
                  CHECK (scrape_status IN ('pending','done','error','partial')),
    scrape_engine VARCHAR(30)
                  CHECK (scrape_engine IS NULL OR scrape_engine IN ('cloudscraper','selenium','manual')),
    error_message VARCHAR(2000),
    scraped_at    TIMESTAMPTZ,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    version_id    INTEGER      NOT NULL DEFAULT 0
);

-- ── scraping_logs (partitioned) ───────────────────────────────────────────
-- BUG-012/021 FIX: FK constraints intentionally absent (PostgreSQL limitation
-- on partitioned tables). Referential integrity via trigger below.
CREATE TABLE IF NOT EXISTS scraping_logs (
    id          BIGSERIAL,
    url_id      UUID,
    hotel_id    UUID,
    event_type  VARCHAR(50)  NOT NULL
                CHECK (event_type IN (
                    'scrape_start','scrape_done','scrape_error',
                    'vpn_rotate','vpn_error',
                    'image_download','image_error',
                    'queue_claim','queue_release',
                    'health_check','system_event')),
    engine      VARCHAR(30),
    language    VARCHAR(10),
    duration_ms INTEGER      CHECK (duration_ms IS NULL OR duration_ms >= 0),
    http_status SMALLINT,
    message     TEXT,
    metadata    JSONB        NOT NULL DEFAULT '{}',
    worker_id   VARCHAR(100),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- ── image_downloads ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS image_downloads (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    hotel_id        UUID        NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    url             TEXT        NOT NULL,
    filename        VARCHAR(500),
    file_size_bytes INTEGER,
    width           INTEGER,
    height          INTEGER,
    content_type    VARCHAR(100),
    status          VARCHAR(30) NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','done','error','skipped')),
    error_message   VARCHAR(2000),
    downloaded_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (hotel_id, url)
);

-- ── system_config ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS system_config (
    key         VARCHAR(100) PRIMARY KEY,
    value       TEXT         NOT NULL,
    description VARCHAR(500),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ── Log partitions ────────────────────────────────────────────────────────
DO $$
DECLARE
    start_date DATE := DATE_TRUNC('month', CURRENT_DATE);
    part_date  DATE;
    next_date  DATE;
    part_name  TEXT;
BEGIN
    FOR i IN 0..11 LOOP
        part_date := start_date + (i || ' months')::INTERVAL;
        next_date := part_date + '1 month'::INTERVAL;
        part_name := 'scraping_logs_' || TO_CHAR(part_date,'YYYY_MM');
        IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename=part_name AND schemaname='public') THEN
            EXECUTE FORMAT(
                'CREATE TABLE %I PARTITION OF scraping_logs FOR VALUES FROM (%L) TO (%L)',
                part_name, part_date, next_date
            );
        END IF;
    END LOOP;
END $$;

-- =============================================================================
-- INDEXES
-- BUG-002 FIX: ix_hotels_url_lang_null declared here (was only in comments)
-- BUG-007 FIX: All GIN indexes in this script (was manual step before)
-- =============================================================================

-- url_queue
CREATE INDEX IF NOT EXISTS ix_url_queue_status_priority
    ON url_queue (status, priority DESC, created_at ASC)
    WHERE status = 'pending';
CREATE INDEX IF NOT EXISTS ix_url_queue_status_claimed
    ON url_queue (status, claimed_at)
    WHERE status = 'processing';
CREATE INDEX IF NOT EXISTS ix_url_queue_url ON url_queue (url);

-- url_language_status
CREATE INDEX IF NOT EXISTS ix_url_lang_pending
    ON url_language_status (url_id, status)
    WHERE status IN ('pending','error');

-- hotels — BUG-002 FIX: partial unique indexes
CREATE UNIQUE INDEX IF NOT EXISTS ix_hotels_url_lang_null
    ON hotels (url, language)
    WHERE url_id IS NULL;
CREATE UNIQUE INDEX IF NOT EXISTS ix_hotels_url_id_lang
    ON hotels (url_id, language)
    WHERE url_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_hotels_url
    ON hotels (url) WHERE url IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_hotels_city_country ON hotels (city, country);
CREATE INDEX IF NOT EXISTS ix_hotels_scrape_status
    ON hotels (scrape_status) WHERE scrape_status != 'done';

-- BUG-007 FIX: GIN indexes included in script
CREATE INDEX IF NOT EXISTS ix_hotels_amenities_gin
    ON hotels USING GIN (amenities);
CREATE INDEX IF NOT EXISTS ix_hotels_room_types_gin
    ON hotels USING GIN (room_types);
CREATE INDEX IF NOT EXISTS ix_hotels_raw_data_gin
    ON hotels USING GIN (raw_data jsonb_path_ops);

-- scraping_logs
CREATE INDEX IF NOT EXISTS ix_slog_url_id
    ON scraping_logs (url_id) WHERE url_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_slog_hotel_id
    ON scraping_logs (hotel_id) WHERE hotel_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_slog_event
    ON scraping_logs (event_type, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_slog_worker
    ON scraping_logs (worker_id, created_at DESC) WHERE worker_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_slog_metadata_gin
    ON scraping_logs USING GIN (metadata jsonb_path_ops);

-- image_downloads
CREATE INDEX IF NOT EXISTS ix_img_hotel_status
    ON image_downloads (hotel_id, status) WHERE status != 'done';

-- =============================================================================
-- TRIGGERS
-- =============================================================================

-- updated_at maintenance
CREATE OR REPLACE FUNCTION fn_set_updated_at() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at := NOW(); RETURN NEW; END; $$;

CREATE OR REPLACE TRIGGER trg_url_queue_updated_at
    BEFORE UPDATE ON url_queue FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();
CREATE OR REPLACE TRIGGER trg_hotels_updated_at
    BEFORE UPDATE ON hotels FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();
CREATE OR REPLACE TRIGGER trg_url_lang_updated_at
    BEFORE UPDATE ON url_language_status FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

-- BUG-005 FIX: Optimistic lock enforcement at DB level
CREATE OR REPLACE FUNCTION fn_increment_version() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.version_id <= OLD.version_id THEN
        RAISE EXCEPTION 'Optimistic lock conflict: version_id % not incremented (current: %)',
            NEW.version_id, OLD.version_id USING ERRCODE='P0001';
    END IF;
    RETURN NEW;
END; $$;

CREATE OR REPLACE TRIGGER trg_url_queue_version
    BEFORE UPDATE ON url_queue FOR EACH ROW
    WHEN (OLD.version_id IS DISTINCT FROM NEW.version_id)
    EXECUTE FUNCTION fn_increment_version();
CREATE OR REPLACE TRIGGER trg_hotels_version
    BEFORE UPDATE ON hotels FOR EACH ROW
    WHEN (OLD.version_id IS DISTINCT FROM NEW.version_id)
    EXECUTE FUNCTION fn_increment_version();
CREATE OR REPLACE TRIGGER trg_url_lang_version
    BEFORE UPDATE ON url_language_status FOR EACH ROW
    WHEN (OLD.version_id IS DISTINCT FROM NEW.version_id)
    EXECUTE FUNCTION fn_increment_version();

-- BUG-012 FIX: Referential integrity for partitioned scraping_logs
CREATE OR REPLACE FUNCTION fn_scraping_logs_fk_check() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.url_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM url_queue WHERE id=NEW.url_id) THEN
        RAISE EXCEPTION 'FK violation: url_id % not in url_queue', NEW.url_id
            USING ERRCODE='foreign_key_violation';
    END IF;
    IF NEW.hotel_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM hotels WHERE id=NEW.hotel_id) THEN
        RAISE EXCEPTION 'FK violation: hotel_id % not in hotels', NEW.hotel_id
            USING ERRCODE='foreign_key_violation';
    END IF;
    RETURN NEW;
END; $$;

CREATE OR REPLACE TRIGGER trg_scraping_logs_fk_check
    BEFORE INSERT ON scraping_logs FOR EACH ROW
    EXECUTE FUNCTION fn_scraping_logs_fk_check();

-- =============================================================================
-- ROLES
-- =============================================================================
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_read')  THEN CREATE ROLE app_read  NOLOGIN; END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_write') THEN CREATE ROLE app_write NOLOGIN; END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='app_admin') THEN CREATE ROLE app_admin NOLOGIN; END IF;
END $$;

GRANT USAGE ON SCHEMA public TO app_read;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO app_read;

GRANT app_read TO app_write;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_write;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_write;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT,UPDATE,DELETE ON TABLES TO app_write;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO app_write;

GRANT app_write TO app_admin;
GRANT ALL ON ALL TABLES IN SCHEMA public TO app_admin;
GRANT CREATE ON SCHEMA public TO app_admin;

-- =============================================================================
-- SEED DATA
-- =============================================================================
INSERT INTO system_config (key, value, description) VALUES
    ('app_version',        '6.0.0', 'Application version'),
    ('schema_version',     '46',    'Database schema version (BUG-008 FIX: synced)'),
    ('schema_deployed_at', NOW()::TEXT, 'Schema deployment timestamp'),
    ('max_error_len',      '2000',  'Max error message column width'),
    ('max_lang_retries',   '3',     'BUG-022 FIX: was hardcoded=1')
ON CONFLICT (key) DO UPDATE SET value=EXCLUDED.value, updated_at=NOW();

COMMIT;

-- =============================================================================
-- VERIFICATION
-- =============================================================================
\echo '=== BookingScraper Pro v6.0 Schema v46 Installed ==='
\echo ''
SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass)) size
FROM pg_tables WHERE schemaname='public' ORDER BY tablename;
\echo ''
SELECT indexname, indexdef FROM pg_indexes
WHERE schemaname='public' AND (indexname LIKE '%gin%' OR indexname LIKE '%null%')
ORDER BY indexname;
\echo ''
SELECT key, value FROM system_config ORDER BY key;
\echo ''
\echo '=== Installation Complete ==='
