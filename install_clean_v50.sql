-- ============================================================================
-- install_clean_v50.sql — BookingScraper Pro v6.0.0 build 50
-- Esquema completo para instalación en DB NUEVA (clean install only).
-- Plataforma: PostgreSQL 15+ en Windows 11
--
-- USO:
--   psql -U postgres -d bookingscraper -f install_clean_v50.sql
--
-- ⚠ SOLO PARA BASES DE DATOS NUEVAS / VACÍAS.
-- ⚠ Para pruebas: DROP DATABASE bookingscraper; CREATE DATABASE bookingscraper;
--   y luego ejecutar este script.
--
-- CHANGELOG v50 (respecto a v49):
--   STRUCT-001  : Nueva tabla hotels_description (hotel_id, url_id, language, description).
--                 hotels.description eliminado de la tabla principal.
--   STRUCT-002  : hotels.photos eliminado. image_downloads es la fuente única de fotos.
--   STRUCT-003  : hotels.review_count_schema renombrado a hotels.review_count.
--                 El campo review_count anterior (regex, siempre NULL) fue eliminado.
--   STRUCT-004  : hotels.address eliminado (campo muerto, usar street_address).
--   BUG-STAR    : hotels.star_rating CHECK ajustado a 0-5 (extractor normaliza ÷2).
--   BUG-LOAD-001: Documentado en load_urls.py — ON CONFLICT DO UPDATE para external_ref.
--   BUG-EXTR-001: review_score corregido (data-review-score attr / JSON-LD).
--   BUG-EXTR-002: amenities corregido (selector React actualizado).
--   BUG-EXTR-003: review_count desde JSON-LD (language-independent).
--   BUG-EXTR-006: city/country desde JSON-LD (no breadcrumb).
--   BUG-EXTR-007: star_rating normalizado ÷2 en extractor.
--
-- Fixes heredados (v49 y anteriores):
--   BUG-STARRATING-002  : hotels.star_rating CHECK 0-5 (normalizado)
--   BUG-VARCHAR-003     : hotels.city / country TEXT (no VARCHAR)
--   BUG-IMG-SCHEMA      : image_downloads.id_photo + category
--   NEW-TABLE-001       : image_data (metadatos completos por foto)
--   BUG-003/BUG-103     : scraping_logs FK via trigger (tabla particionada)
--   BUG-016             : url_language_status incluye status 'incomplete'
--   BUG-019             : system_metrics índices para series temporales
-- ============================================================================

\set ON_ERROR_STOP on

BEGIN;

-- ============================================================================
-- 1. EXTENSIONS
-- ============================================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
DO $$
BEGIN
    CREATE EXTENSION IF NOT EXISTS "btree_gin";
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'btree_gin no disponible (opcional) — continuando sin ella.';
END;
$$;

-- ============================================================================
-- 2. ROLES
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
        GRANT app_read    TO bookingscraper_user;
        GRANT app_write   TO bookingscraper_user;
        GRANT app_scraper TO bookingscraper_user;
    END IF;
END
$$;

-- ============================================================================
-- 3. TABLAS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- url_queue
-- Cola principal de scraping.
-- external_ref: ID numérico del CSV origen (e.g. 1001, 1002...).
-- BUG-LOAD-001: load_urls.py usa ON CONFLICT DO UPDATE para garantizar
--               que external_ref siempre se graba aunque la URL ya exista.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS url_queue (
    id               UUID          NOT NULL DEFAULT uuid_generate_v4(),
    url              VARCHAR(2048) NOT NULL,
    base_url         VARCHAR(2048) NOT NULL,
    external_ref     VARCHAR(64)   NULL,
    hotel_id_booking VARCHAR(64)   NULL,
    status           VARCHAR(32)   NOT NULL DEFAULT 'pending',
    priority         SMALLINT      NOT NULL DEFAULT 5,
    retry_count      SMALLINT      NOT NULL DEFAULT 0,
    max_retries      SMALLINT      NOT NULL DEFAULT 3,
    last_error       VARCHAR(2000) NULL,
    created_at       TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    scraped_at       TIMESTAMPTZ   NULL,
    version_id       INTEGER       NOT NULL DEFAULT 1,

    CONSTRAINT pk_url_queue           PRIMARY KEY (id),
    CONSTRAINT uq_url_queue_url       UNIQUE (url),
    CONSTRAINT chk_url_queue_status   CHECK (status IN ('pending','processing','done','error','skipped')),
    CONSTRAINT chk_url_queue_priority CHECK (priority BETWEEN 1 AND 10)
);

CREATE INDEX IF NOT EXISTS ix_url_queue_external_ref    ON url_queue (external_ref) WHERE external_ref IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_url_queue_status_priority ON url_queue (status, priority DESC);
CREATE INDEX IF NOT EXISTS ix_url_queue_created_at      ON url_queue (created_at DESC);
CREATE INDEX IF NOT EXISTS ix_url_queue_hotel_id        ON url_queue (hotel_id_booking);

-- ----------------------------------------------------------------------------
-- hotels
-- Datos principales del hotel por idioma (un registro por url × idioma).
--
-- v50 — cambios respecto a v49:
--   ELIMINADOS : description (→ hotels_description), photos (→ image_downloads),
--                address (muerto), review_count_schema (renombrado).
--   RENOMBRADO : review_count_schema → review_count (JSON-LD, fiable).
--   AJUSTADO   : star_rating CHECK 0-5 (extractor normaliza Booking ÷2).
--
-- Campos JSON-LD / schema.org (NEW-COLS-001, v49):
--   main_image_url   — Hotel.image
--   short_description— Hotel.description (resumen corto del schema.org)
--   rating_value     — aggregateRating.ratingValue
--   best_rating      — aggregateRating.bestRating
--   review_count     — aggregateRating.reviewCount (JSON-LD, antes review_count_schema)
--   street_address   — address.streetAddress
--   address_locality — address.addressLocality
--   address_country  — address.addressCountry
--   postal_code      — address.postalCode
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS hotels (
    id                   UUID          NOT NULL DEFAULT uuid_generate_v4(),
    url_id               UUID          NOT NULL,
    url                  VARCHAR(2048) NOT NULL,
    language             VARCHAR(10)   NOT NULL,
    hotel_name           VARCHAR(512)  NULL,
    hotel_id_booking     VARCHAR(64)   NULL,
    city                 TEXT          NULL,
    country              TEXT          NULL,
    latitude             FLOAT         NULL,
    longitude            FLOAT         NULL,
    star_rating          FLOAT         NULL,
    review_score         FLOAT         NULL,
    -- STRUCT-003: review_count = reviewCount JSON-LD (language-independent, fiable)
    review_count         INTEGER       NULL,
    -- Campos JSON-LD / schema.org
    main_image_url       VARCHAR(2048) NULL,
    short_description    TEXT          NULL,
    rating_value         FLOAT         NULL,
    best_rating          FLOAT         NULL,
    street_address       VARCHAR(512)  NULL,
    address_locality     VARCHAR(256)  NULL,
    address_country      VARCHAR(128)  NULL,
    postal_code          VARCHAR(20)   NULL,
    -- Datos estructurados JSONB
    amenities            JSONB         NULL DEFAULT '[]'::jsonb,
    room_types           JSONB         NULL DEFAULT '[]'::jsonb,
    policies             JSONB         NULL DEFAULT '{}'::jsonb,
    raw_data             JSONB         NULL DEFAULT '{}'::jsonb,
    -- Metadatos de scraping
    scrape_duration_s    FLOAT         NULL,
    scrape_engine        VARCHAR(32)   NULL,
    created_at           TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version_id           INTEGER       NOT NULL DEFAULT 1,

    CONSTRAINT pk_hotels              PRIMARY KEY (id),
    CONSTRAINT fk_hotels_url_id       FOREIGN KEY (url_id)
                                          REFERENCES url_queue(id) ON DELETE CASCADE,
    CONSTRAINT uq_hotels_url_lang     UNIQUE (url_id, language),
    -- BUG-STAR: escala 0-5 (extractor divide Booking raw ÷ 2)
    CONSTRAINT chk_hotels_star_rating CHECK (star_rating IS NULL
                                          OR (star_rating >= 0 AND star_rating <= 5)),
    CONSTRAINT chk_hotels_review_score CHECK (review_score IS NULL
                                          OR (review_score >= 0 AND review_score <= 10)),
    CONSTRAINT chk_hotels_review_count CHECK (review_count IS NULL OR review_count >= 0),
    CONSTRAINT chk_hotels_rating_value CHECK (rating_value IS NULL
                                          OR (rating_value >= 0 AND rating_value <= 10)),
    CONSTRAINT chk_hotels_best_rating  CHECK (best_rating IS NULL
                                          OR (best_rating >= 0 AND best_rating <= 10))
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_hotels_url_lang_notnull
    ON hotels (url_id, language)
    WHERE hotel_name IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_hotels_city_country  ON hotels (city, country);
CREATE INDEX IF NOT EXISTS ix_hotels_hotel_id      ON hotels (hotel_id_booking);
CREATE INDEX IF NOT EXISTS ix_hotels_created_at    ON hotels (created_at DESC);
CREATE INDEX IF NOT EXISTS ix_hotels_amenities_gin ON hotels USING GIN (amenities);
CREATE INDEX IF NOT EXISTS ix_hotels_name_trgm     ON hotels USING GIN (hotel_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS ix_hotels_lat_lon       ON hotels (latitude, longitude)
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

-- ----------------------------------------------------------------------------
-- hotels_description
-- STRUCT-001: Descripción larga del hotel separada de la tabla principal.
--
-- Justificación arquitectónica:
--   - Reduce el tamaño de hotels (TEXT de 500-2000 chars por fila × 7 idiomas).
--   - Permite queries sobre hotels sin cargar el campo TEXT de mayor peso.
--   - Permite indexado GIN full-text sobre descriptions de forma independiente.
--   - Un registro por (url_id, language) — misma cardinalidad que hotels.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS hotels_description (
    id          UUID          NOT NULL DEFAULT uuid_generate_v4(),
    hotel_id    UUID          NOT NULL,
    url_id      UUID          NOT NULL,
    language    VARCHAR(10)   NOT NULL,
    description TEXT          NULL,
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_description  PRIMARY KEY (id),
    CONSTRAINT fk_hdesc_hotel_id      FOREIGN KEY (hotel_id)
                                          REFERENCES hotels(id) ON DELETE CASCADE,
    CONSTRAINT fk_hdesc_url_id        FOREIGN KEY (url_id)
                                          REFERENCES url_queue(id) ON DELETE CASCADE,
    CONSTRAINT uq_hdesc_url_lang      UNIQUE (url_id, language)
);

CREATE INDEX IF NOT EXISTS ix_hdesc_hotel_id ON hotels_description (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hdesc_language ON hotels_description (language);

-- Índice GIN para búsqueda full-text sobre descriptions (activar si se requiere):
-- CREATE INDEX ix_hdesc_desc_fts ON hotels_description
--     USING GIN (to_tsvector('simple', COALESCE(description, '')));

-- ----------------------------------------------------------------------------
-- url_language_status
-- Tracking de completitud de scraping por URL y lenguaje.
-- BUG-016: status incluye 'incomplete'.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS url_language_status (
    id         UUID          NOT NULL DEFAULT uuid_generate_v4(),
    url_id     UUID          NOT NULL,
    language   VARCHAR(10)   NOT NULL,
    status     VARCHAR(32)   NOT NULL DEFAULT 'pending',
    attempts   SMALLINT      NOT NULL DEFAULT 0,
    last_error VARCHAR(2000) NULL,
    created_at TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_uls          PRIMARY KEY (id),
    CONSTRAINT fk_uls_url_id   FOREIGN KEY (url_id)
                                   REFERENCES url_queue(id) ON DELETE CASCADE,
    CONSTRAINT uq_uls_url_lang UNIQUE (url_id, language),
    CONSTRAINT chk_uls_status  CHECK (status IN
        ('pending','processing','done','error','skipped','incomplete'))
);

CREATE INDEX IF NOT EXISTS ix_uls_url_id ON url_language_status (url_id);
CREATE INDEX IF NOT EXISTS ix_uls_status ON url_language_status (status);

-- ----------------------------------------------------------------------------
-- image_downloads
-- Tracking de descargas individuales por hotel, foto y categoría de tamaño.
-- STRUCT-002: fuente única de verdad para fotos (hotels.photos eliminado).
-- BUG-IMG-SCHEMA (v49): columnas id_photo + category.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS image_downloads (
    id              UUID          NOT NULL DEFAULT uuid_generate_v4(),
    hotel_id        UUID          NOT NULL,
    id_photo        VARCHAR(32)   NULL,
    category        VARCHAR(16)   NULL,
    url             VARCHAR(2048) NOT NULL,
    local_path      VARCHAR(1024) NULL,
    file_size_bytes INTEGER       NULL,
    content_type    VARCHAR(64)   NULL,
    status          VARCHAR(32)   NOT NULL DEFAULT 'pending',
    error_message   VARCHAR(2000) NULL,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    downloaded_at   TIMESTAMPTZ   NULL,

    CONSTRAINT pk_imgdl           PRIMARY KEY (id),
    CONSTRAINT fk_imgdl_hotel_id  FOREIGN KEY (hotel_id)
                                      REFERENCES hotels(id) ON DELETE CASCADE,
    CONSTRAINT uq_imgdl_hotel_url UNIQUE (hotel_id, url),
    CONSTRAINT chk_imgdl_status   CHECK (status IN
        ('pending','downloading','done','error','skipped')),
    CONSTRAINT chk_imgdl_category CHECK (category IS NULL OR category IN
        ('thumb_url','large_url','highres_url'))
);

CREATE INDEX IF NOT EXISTS ix_imgdl_hotel_id ON image_downloads (hotel_id);
CREATE INDEX IF NOT EXISTS ix_imgdl_status   ON image_downloads (status);
CREATE INDEX IF NOT EXISTS ix_imgdl_id_photo ON image_downloads (id_photo)
    WHERE id_photo IS NOT NULL;

-- Índice único parcial: un registro por (hotel, foto, tamaño) cuando id_photo conocido
CREATE UNIQUE INDEX IF NOT EXISTS uq_imgdl_hotel_photo_cat
    ON image_downloads (hotel_id, id_photo, category)
    WHERE id_photo IS NOT NULL AND category IS NOT NULL;

-- ----------------------------------------------------------------------------
-- image_data
-- Metadatos completos por foto única de Booking.com.
-- NEW-TABLE-001 (v49): orientación, dimensiones, alt text, timestamp de la foto.
-- Un registro por id_photo (globalmente único en Booking.com).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS image_data (
    id               UUID        NOT NULL DEFAULT uuid_generate_v4(),
    id_photo         VARCHAR(32) NOT NULL,
    hotel_id         UUID        NOT NULL,
    orientation      VARCHAR(16) NULL,
    photo_width      INTEGER     NULL,
    photo_height     INTEGER     NULL,
    alt              TEXT        NULL,
    created_at_photo TIMESTAMPTZ NULL,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_image_data           PRIMARY KEY (id),
    CONSTRAINT uq_image_data_id_photo  UNIQUE (id_photo),
    CONSTRAINT fk_image_data_hotel     FOREIGN KEY (hotel_id)
                                           REFERENCES hotels(id) ON DELETE CASCADE,
    CONSTRAINT chk_imgdata_orientation CHECK (orientation IS NULL OR orientation IN
        ('landscape','portrait','square')),
    CONSTRAINT chk_imgdata_width       CHECK (photo_width  IS NULL OR photo_width  > 0),
    CONSTRAINT chk_imgdata_height      CHECK (photo_height IS NULL OR photo_height > 0)
);

CREATE INDEX IF NOT EXISTS ix_imgdata_hotel_id ON image_data (hotel_id);

-- ----------------------------------------------------------------------------
-- system_metrics
-- Snapshots periódicos de salud del sistema (CPU, RAM, workers, Redis).
-- BUG-019: índices compuestos para queries de series temporales.
-- ----------------------------------------------------------------------------
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

CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_cpu ON system_metrics (recorded_at DESC, cpu_usage);
CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_mem ON system_metrics (recorded_at DESC, memory_usage);

-- ============================================================================
-- 4. TABLA PARTICIONADA: scraping_logs
-- BUG-003/BUG-103: PostgreSQL no soporta FK en tablas particionadas.
--                  Integridad referencial garantizada via trigger.
-- ============================================================================
CREATE TABLE IF NOT EXISTS scraping_logs (
    id            UUID         NOT NULL DEFAULT uuid_generate_v4(),
    url_id        UUID         NOT NULL,
    hotel_id      UUID         NULL,
    language      VARCHAR(10)  NULL,
    event_type    VARCHAR(64)  NOT NULL,
    status        VARCHAR(32)  NOT NULL,
    error_message TEXT         NULL,
    duration_ms   INTEGER      NULL,
    worker_id     VARCHAR(128) NULL,
    extra_data    JSONB        NULL DEFAULT '{}'::jsonb,
    scraped_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_scraping_logs PRIMARY KEY (id, scraped_at)
) PARTITION BY RANGE (scraped_at);

-- Función de validación FK para scraping_logs (BUG-003/BUG-103)
CREATE OR REPLACE FUNCTION trg_fn_scraping_logs_fk_check()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM url_queue WHERE id = NEW.url_id) THEN
        RAISE EXCEPTION 'scraping_logs FK violation: url_id=% not found in url_queue', NEW.url_id
            USING ERRCODE = 'foreign_key_violation';
    END IF;
    IF NEW.hotel_id IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM hotels WHERE id = NEW.hotel_id) THEN
            RAISE EXCEPTION 'scraping_logs FK violation: hotel_id=% not found in hotels', NEW.hotel_id
                USING ERRCODE = 'foreign_key_violation';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

-- Crear particiones mensuales: mes actual + 2 meses siguientes
DO $$
DECLARE
    delta INT; y INT; m INT;
    pname TEXT; pstart TEXT; pend TEXT;
    nm INT; ny INT;
BEGIN
    FOR delta IN 0..2 LOOP
        y     := EXTRACT(YEAR  FROM CURRENT_DATE + (delta || ' months')::interval)::int;
        m     := EXTRACT(MONTH FROM CURRENT_DATE + (delta || ' months')::interval)::int;
        pname := FORMAT('scraping_logs_%s_%s', LPAD(y::text,4,'0'), LPAD(m::text,2,'0'));
        pstart:= FORMAT('%s-%s-01', LPAD(y::text,4,'0'), LPAD(m::text,2,'0'));
        IF m = 12 THEN ny := y+1; nm := 1; ELSE ny := y; nm := m+1; END IF;
        pend  := FORMAT('%s-%s-01', LPAD(ny::text,4,'0'), LPAD(nm::text,2,'0'));
        IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = pname AND schemaname = 'public') THEN
            EXECUTE FORMAT(
                'CREATE TABLE %I PARTITION OF scraping_logs FOR VALUES FROM (%L) TO (%L)',
                pname, pstart::timestamptz, pend::timestamptz
            );
            EXECUTE FORMAT('CREATE INDEX ON %I (url_id)', pname);
            RAISE NOTICE 'Partición creada: %', pname;
        END IF;
    END LOOP;
END;
$$;

-- Instalar trigger FK en cada partición existente
DO $$
DECLARE pname TEXT;
BEGIN
    FOR pname IN
        SELECT tablename FROM pg_tables
        WHERE tablename LIKE 'scraping_logs_%' AND schemaname = 'public'
    LOOP
        EXECUTE FORMAT(
            'DROP TRIGGER IF EXISTS trg_scraping_logs_fk_check ON %I; '
            'CREATE TRIGGER trg_scraping_logs_fk_check '
            'BEFORE INSERT OR UPDATE ON %I '
            'FOR EACH ROW EXECUTE FUNCTION trg_fn_scraping_logs_fk_check()',
            pname, pname
        );
    END LOOP;
END;
$$;

-- ============================================================================
-- 5. FUNCIÓN Y TRIGGERS updated_at
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_url_queue_updated_at ON url_queue;
CREATE TRIGGER trg_url_queue_updated_at
    BEFORE UPDATE ON url_queue
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

DROP TRIGGER IF EXISTS trg_hotels_updated_at ON hotels;
CREATE TRIGGER trg_hotels_updated_at
    BEFORE UPDATE ON hotels
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

DROP TRIGGER IF EXISTS trg_hdesc_updated_at ON hotels_description;
CREATE TRIGGER trg_hdesc_updated_at
    BEFORE UPDATE ON hotels_description
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

DROP TRIGGER IF EXISTS trg_uls_updated_at ON url_language_status;
CREATE TRIGGER trg_uls_updated_at
    BEFORE UPDATE ON url_language_status
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

-- ============================================================================
-- 6. GRANTS
-- ============================================================================
GRANT SELECT                         ON ALL TABLES    IN SCHEMA public TO app_read;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES    IN SCHEMA public TO app_write;
GRANT USAGE, SELECT                  ON ALL SEQUENCES IN SCHEMA public TO app_write;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES    IN SCHEMA public TO app_scraper;
GRANT USAGE, SELECT                  ON ALL SEQUENCES IN SCHEMA public TO app_scraper;

-- ============================================================================
-- 7. VERIFICACIÓN FINAL
-- ============================================================================
DO $$
DECLARE
    t TEXT;
    missing TEXT := '';
    expected_tables TEXT[] := ARRAY[
        'url_queue',
        'hotels',
        'hotels_description',
        'url_language_status',
        'image_downloads',
        'image_data',
        'system_metrics',
        'scraping_logs'
    ];
BEGIN
    FOREACH t IN ARRAY expected_tables LOOP
        IF NOT EXISTS (
            SELECT 1 FROM pg_tables
            WHERE tablename = t AND schemaname = 'public'
        ) THEN
            missing := missing || t || ' ';
        END IF;
    END LOOP;

    IF missing <> '' THEN
        RAISE EXCEPTION 'install_clean_v50: tablas faltantes: [%]', missing;
    END IF;

    -- Verificar que hotels NO tiene columnas eliminadas
    IF EXISTS (SELECT 1 FROM information_schema.columns
               WHERE table_name = 'hotels' AND column_name IN ('description','photos','address','review_count_schema')) THEN
        RAISE EXCEPTION 'install_clean_v50: hotels contiene columnas obsoletas (description/photos/address/review_count_schema).';
    END IF;

    -- Verificar hotels_description tiene las columnas correctas
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                   WHERE table_name = 'hotels_description' AND column_name = 'description') THEN
        RAISE EXCEPTION 'install_clean_v50: hotels_description.description no existe.';
    END IF;

    RAISE NOTICE '';
    RAISE NOTICE '=======================================================';
    RAISE NOTICE ' install_clean_v50.sql — INSTALACIÓN COMPLETADA OK';
    RAISE NOTICE ' Tablas: url_queue | hotels | hotels_description';
    RAISE NOTICE '         url_language_status | image_downloads';
    RAISE NOTICE '         image_data | system_metrics | scraping_logs';
    RAISE NOTICE '=======================================================';
END;
$$;

COMMIT;

-- ============================================================================
-- ESTRUCTURA FINAL — v50
-- ============================================================================
--
-- url_queue
--   id, url, base_url, external_ref, hotel_id_booking
--   status, priority, retry_count, max_retries, last_error
--   created_at, updated_at, scraped_at, version_id
--
-- hotels  (sin description, sin photos, sin address, sin review_count_schema)
--   id, url_id (FK), url, language, hotel_name, hotel_id_booking
--   city, country, latitude, longitude, star_rating [0-5], review_score
--   review_count                    ← antes review_count_schema (JSON-LD)
--   main_image_url, short_description, rating_value, best_rating
--   street_address, address_locality, address_country, postal_code
--   amenities (JSONB), room_types (JSONB), policies (JSONB), raw_data (JSONB)
--   scrape_duration_s, scrape_engine
--   created_at, updated_at, version_id
--
-- hotels_description  (NUEVA — STRUCT-001)
--   id, hotel_id (FK hotels), url_id (FK url_queue), language, description
--   created_at, updated_at
--
-- url_language_status
--   id, url_id (FK), language, status, attempts, last_error
--   created_at, updated_at
--
-- image_downloads  (fuente única de fotos — STRUCT-002)
--   id, hotel_id (FK), id_photo, category, url
--   local_path, file_size_bytes, content_type, status, error_message
--   created_at, downloaded_at
--
-- image_data
--   id, id_photo (UK), hotel_id (FK)
--   orientation, photo_width, photo_height, alt, created_at_photo
--   created_at
--
-- system_metrics
--   id, recorded_at, cpu_usage, memory_usage, active_workers
--   db_pool_checked_out, redis_connected, urls_pending, urls_done, extra_data
--
-- scraping_logs  (PARTITIONED BY RANGE scraped_at)
--   id, url_id, hotel_id, language, event_type, status
--   error_message, duration_ms, worker_id, extra_data, scraped_at
--
-- ============================================================================
