-- ============================================================================
-- install_clean_v48.sql - BookingScraper Pro v6.0
-- Full schema installation for CLEAN / EMPTY environments.
-- Platform: PostgreSQL 15+ on Windows 11
-- USAGE: psql -U postgres -d bookingscraper -f install_clean_v48.sql
-- ============================================================================

\set ON_ERROR_STOP on

BEGIN;

-- ============================================================================
-- 1. EXTENSIONS
-- ============================================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- trigram search on hotel names
CREATE EXTENSION IF NOT EXISTS "btree_gin";  -- GIN indexes on scalar types

-- ============================================================================
-- 2. ROLES (application role separation)
-- ============================================================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_read') THEN
        CREATE ROLE app_read NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_write') THEN
        CREATE ROLE app_write NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_scraper') THEN
        CREATE ROLE app_scraper NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'bookingscraper_user') THEN
        CREATE ROLE bookingscraper_user LOGIN PASSWORD 'CHANGE_THIS_PASSWORD_IN_PRODUCTION';
        GRANT app_read TO bookingscraper_user;
        GRANT app_write TO bookingscraper_user;
        GRANT app_scraper TO bookingscraper_user;
    END IF;
END
$$;

-- ============================================================================
-- 3. TABLES
-- ============================================================================

-- url_queue ------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS url_queue (
    id              UUID        NOT NULL DEFAULT uuid_generate_v4(),
    url             VARCHAR(2048) NOT NULL,
    base_url        VARCHAR(2048) NOT NULL,
    hotel_id_booking VARCHAR(64) NULL,
    status          VARCHAR(32) NOT NULL DEFAULT 'pending',
    priority        SMALLINT    NOT NULL DEFAULT 5,
    retry_count     SMALLINT    NOT NULL DEFAULT 0,
    max_retries     SMALLINT    NOT NULL DEFAULT 3,
    last_error      VARCHAR(2000) NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    scraped_at      TIMESTAMPTZ NULL,
    version_id      INTEGER     NOT NULL DEFAULT 1,
    CONSTRAINT pk_url_queue             PRIMARY KEY (id),
    CONSTRAINT uq_url_queue_url         UNIQUE (url),
    CONSTRAINT chk_url_queue_status     CHECK (status IN ('pending','processing','done','error','skipped')),
    CONSTRAINT chk_url_queue_priority   CHECK (priority BETWEEN 1 AND 10)
);

CREATE INDEX IF NOT EXISTS ix_url_queue_status_priority ON url_queue (status, priority DESC);
CREATE INDEX IF NOT EXISTS ix_url_queue_created_at      ON url_queue (created_at DESC);
CREATE INDEX IF NOT EXISTS ix_url_queue_hotel_id        ON url_queue (hotel_id_booking);

-- hotels ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS hotels (
    id                  UUID        NOT NULL DEFAULT uuid_generate_v4(),
    url_id              UUID        NOT NULL,
    url                 VARCHAR(2048) NOT NULL,
    language            VARCHAR(10) NOT NULL,
    hotel_name          VARCHAR(512) NULL,
    hotel_id_booking    VARCHAR(64) NULL,
    city                VARCHAR(256) NULL,
    country             VARCHAR(128) NULL,
    address             VARCHAR(512) NULL,
    latitude            FLOAT       NULL,
    longitude           FLOAT       NULL,
    star_rating         FLOAT       NULL,
    review_score        FLOAT       NULL,
    review_count        INTEGER     NULL,
    description         TEXT        NULL,
    amenities           JSONB       NULL DEFAULT '[]'::jsonb,
    room_types          JSONB       NULL DEFAULT '[]'::jsonb,
    policies            JSONB       NULL DEFAULT '{}'::jsonb,
    photos              JSONB       NULL DEFAULT '[]'::jsonb,
    raw_data            JSONB       NULL DEFAULT '{}'::jsonb,
    scrape_duration_s   FLOAT       NULL,
    scrape_engine       VARCHAR(32) NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version_id          INTEGER     NOT NULL DEFAULT 1,
    CONSTRAINT pk_hotels                    PRIMARY KEY (id),
    CONSTRAINT fk_hotels_url_id             FOREIGN KEY (url_id) REFERENCES url_queue(id) ON DELETE CASCADE,
    CONSTRAINT uq_hotels_url_lang           UNIQUE (url_id, language),
    CONSTRAINT chk_hotels_star_rating       CHECK (star_rating BETWEEN 0 AND 5),
    CONSTRAINT chk_hotels_review_score      CHECK (review_score BETWEEN 0 AND 10),
    CONSTRAINT chk_hotels_review_count      CHECK (review_count >= 0)
);

-- BUG-007 mitigation: partial unique index (cannot be declared via SQLAlchemy create_all)
CREATE UNIQUE INDEX IF NOT EXISTS ix_hotels_url_lang_null
    ON hotels (url_id, language)
    WHERE hotel_name IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_hotels_city_country   ON hotels (city, country);
CREATE INDEX IF NOT EXISTS ix_hotels_hotel_id       ON hotels (hotel_id_booking);
CREATE INDEX IF NOT EXISTS ix_hotels_created_at     ON hotels (created_at DESC);
CREATE INDEX IF NOT EXISTS ix_hotels_amenities_gin  ON hotels USING GIN (amenities);
CREATE INDEX IF NOT EXISTS ix_hotels_name_trgm      ON hotels USING GIN (hotel_name gin_trgm_ops);

-- url_language_status --------------------------------------------------------
CREATE TABLE IF NOT EXISTS url_language_status (
    id          UUID        NOT NULL DEFAULT uuid_generate_v4(),
    url_id      UUID        NOT NULL,
    language    VARCHAR(10) NOT NULL,
    status      VARCHAR(32) NOT NULL DEFAULT 'pending',
    attempts    SMALLINT    NOT NULL DEFAULT 0,
    last_error  VARCHAR(2000) NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_uls               PRIMARY KEY (id),
    CONSTRAINT fk_uls_url_id        FOREIGN KEY (url_id) REFERENCES url_queue(id) ON DELETE CASCADE,
    CONSTRAINT uq_uls_url_lang      UNIQUE (url_id, language),
    -- BUG-016 fix: 'incomplete' included
    CONSTRAINT chk_uls_status       CHECK (status IN ('pending','processing','done','error','skipped','incomplete'))
);

CREATE INDEX IF NOT EXISTS ix_uls_url_id ON url_language_status (url_id);
CREATE INDEX IF NOT EXISTS ix_uls_status ON url_language_status (status);

-- image_downloads -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS image_downloads (
    id              UUID        NOT NULL DEFAULT uuid_generate_v4(),
    hotel_id        UUID        NOT NULL,
    url             VARCHAR(2048) NOT NULL,
    local_path      VARCHAR(1024) NULL,
    file_size_bytes INTEGER     NULL,
    content_type    VARCHAR(64) NULL,
    status          VARCHAR(32) NOT NULL DEFAULT 'pending',
    error_message   VARCHAR(2000) NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    downloaded_at   TIMESTAMPTZ NULL,
    CONSTRAINT pk_imgdl                 PRIMARY KEY (id),
    CONSTRAINT fk_imgdl_hotel_id        FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
    CONSTRAINT uq_imgdl_hotel_url       UNIQUE (hotel_id, url),
    CONSTRAINT chk_imgdl_status         CHECK (status IN ('pending','downloading','done','error','skipped'))
);

CREATE INDEX IF NOT EXISTS ix_imgdl_hotel_id ON image_downloads (hotel_id);
CREATE INDEX IF NOT EXISTS ix_imgdl_status   ON image_downloads (status);

-- system_metrics --------------------------------------------------------------
CREATE TABLE IF NOT EXISTS system_metrics (
    id                  BIGSERIAL   PRIMARY KEY,
    recorded_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    cpu_usage           FLOAT       NULL,
    memory_usage        FLOAT       NULL,
    active_workers      SMALLINT    NULL,
    db_pool_checked_out SMALLINT    NULL,
    redis_connected     BOOLEAN     NULL,
    urls_pending        INTEGER     NULL,
    urls_done           INTEGER     NULL,
    extra_data          JSONB       NULL DEFAULT '{}'::jsonb
);

-- BUG-019 fix: time-series indexes
CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_cpu ON system_metrics (recorded_at DESC, cpu_usage);
CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_mem ON system_metrics (recorded_at DESC, memory_usage);

-- ============================================================================
-- 4. PARTITIONED TABLE: scraping_logs
-- BUG-003 / BUG-103: Foreign key constraints cannot be declared on partitioned
-- tables (PostgreSQL limitation). Referential integrity is enforced via the
-- trigger below. This trigger MUST be present for data integrity.
-- ============================================================================

CREATE TABLE IF NOT EXISTS scraping_logs (
    id              UUID        NOT NULL DEFAULT uuid_generate_v4(),
    url_id          UUID        NOT NULL,   -- NO FK CONSTRAINT - enforced by trigger
    hotel_id        UUID        NULL,
    language        VARCHAR(10) NULL,
    event_type      VARCHAR(64) NOT NULL,
    status          VARCHAR(32) NOT NULL,
    error_message   TEXT        NULL,
    duration_ms     INTEGER     NULL,
    worker_id       VARCHAR(128) NULL,
    extra_data      JSONB       NULL DEFAULT '{}'::jsonb,
    scraped_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_scraping_logs PRIMARY KEY (id, scraped_at)
) PARTITION BY RANGE (scraped_at);

-- -- BUG-003 fix: FK enforcement trigger --------------------------------------
CREATE OR REPLACE FUNCTION trg_fn_scraping_logs_fk_check()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validate url_id references url_queue
    IF NOT EXISTS (SELECT 1 FROM url_queue WHERE id = NEW.url_id) THEN
        RAISE EXCEPTION
            'scraping_logs FK violation: url_id=% not found in url_queue', NEW.url_id
            USING ERRCODE = 'foreign_key_violation';
    END IF;
    -- Validate hotel_id references hotels (if provided)
    IF NEW.hotel_id IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM hotels WHERE id = NEW.hotel_id) THEN
            RAISE EXCEPTION
                'scraping_logs FK violation: hotel_id=% not found in hotels', NEW.hotel_id
                USING ERRCODE = 'foreign_key_violation';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

-- -- Initial monthly partitions (current + 2 months ahead) -----------------
DO $$
DECLARE
    y  INT;
    m  INT;
    pname TEXT;
    pstart TEXT;
    pend   TEXT;
    nm INT;
    ny INT;
BEGIN
    FOR delta IN 0..2 LOOP
        y  := EXTRACT(YEAR  FROM CURRENT_DATE + (delta || ' months')::interval)::int;
        m  := EXTRACT(MONTH FROM CURRENT_DATE + (delta || ' months')::interval)::int;
        pname  := FORMAT('scraping_logs_%s_%s', LPAD(y::text,4,'0'), LPAD(m::text,2,'0'));
        pstart := FORMAT('%s-%s-01', LPAD(y::text,4,'0'), LPAD(m::text,2,'0'));
        IF m = 12 THEN ny := y+1; nm := 1; ELSE ny := y; nm := m+1; END IF;
        pend := FORMAT('%s-%s-01', LPAD(ny::text,4,'0'), LPAD(nm::text,2,'0'));
        IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = pname) THEN
            EXECUTE FORMAT(
                'CREATE TABLE %I PARTITION OF scraping_logs FOR VALUES FROM (%L) TO (%L)',
                pname, pstart::timestamptz, pend::timestamptz
            );
            EXECUTE FORMAT('CREATE INDEX ON %I (url_id)', pname);
            RAISE NOTICE 'Created partition: %', pname;
        END IF;
    END LOOP;
END;
$$;

-- Attach trigger to each partition (must re-run for new partitions)
DO $$
DECLARE
    partition_name TEXT;
BEGIN
    FOR partition_name IN
        SELECT tablename
        FROM pg_tables
        WHERE tablename LIKE 'scraping_logs_%'
          AND schemaname = 'public'
    LOOP
        EXECUTE FORMAT(
            'DROP TRIGGER IF EXISTS trg_scraping_logs_fk_check ON %I; '
            'CREATE TRIGGER trg_scraping_logs_fk_check '
            'BEFORE INSERT OR UPDATE ON %I '
            'FOR EACH ROW EXECUTE FUNCTION trg_fn_scraping_logs_fk_check()',
            partition_name, partition_name
        );
    END LOOP;
END;
$$;

-- ============================================================================
-- 5. UPDATED_AT trigger (auto-update timestamp on all main tables)
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trg_url_queue_updated_at
    BEFORE UPDATE ON url_queue
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE OR REPLACE TRIGGER trg_hotels_updated_at
    BEFORE UPDATE ON hotels
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE OR REPLACE TRIGGER trg_uls_updated_at
    BEFORE UPDATE ON url_language_status
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

-- ============================================================================
-- 6. GRANTS
-- ============================================================================
GRANT SELECT                            ON ALL TABLES IN SCHEMA public TO app_read;
GRANT SELECT, INSERT, UPDATE, DELETE    ON ALL TABLES IN SCHEMA public TO app_write;
GRANT USAGE, SELECT                     ON ALL SEQUENCES IN SCHEMA public TO app_write;
GRANT SELECT, INSERT, UPDATE, DELETE    ON ALL TABLES IN SCHEMA public TO app_scraper;
GRANT USAGE, SELECT                     ON ALL SEQUENCES IN SCHEMA public TO app_scraper;

-- ============================================================================
-- 7. POSTGRESQL WINDOWS 11 TUNING COMMENTS
-- ============================================================================
-- Apply these settings in postgresql.conf:
--
--   max_connections             = 50          # Windows Desktop Heap limitation
--   shared_buffers              = 512MB       # ~25% RAM (4GB system)
--   effective_cache_size        = 1024MB      # ~50% RAM
--   work_mem                    = 8MB         # per-connection; 50 conn * 8MB = 400MB max
--   maintenance_work_mem        = 128MB
--   wal_buffers                 = 16MB
--   checkpoint_completion_target= 0.9
--   random_page_cost            = 1.1         # NVMe SSD
--   effective_io_concurrency    = 1           # Windows async I/O
--   log_min_duration_statement  = 1000        # ms - slow query log
--   autovacuum                  = on
--   autovacuum_vacuum_cost_delay= 2ms

COMMIT;

-- ============================================================================
-- 8. VERIFICATION QUERIES
-- ============================================================================
DO $$
DECLARE
    tbl TEXT;
    missing BOOLEAN := FALSE;
BEGIN
    FOR tbl IN VALUES ('url_queue'),('hotels'),('url_language_status'),
                       ('image_downloads'),('system_metrics'),('scraping_logs') LOOP
        IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = tbl AND schemaname='public') THEN
            RAISE WARNING 'MISSING TABLE: %', tbl;
            missing := TRUE;
        END IF;
    END LOOP;
    IF NOT missing THEN
        RAISE NOTICE '[OK] All tables created successfully.';
    END IF;
END;
$$;
