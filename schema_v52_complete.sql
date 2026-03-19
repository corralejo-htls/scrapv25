-- =============================================================================
-- BookingScraper Pro — Schema Completo v6.0.0 build 52
-- PostgreSQL 14+ / Windows 11 Single-Node Deployment
-- =============================================================================
--
-- INSTRUCCIONES DE EJECUCIÓN (Windows 11):
--   psql -U postgres -f schema_v52_complete.sql
--   O desde pgAdmin 4: Tools > Query Tool > Ejecutar este archivo
--
-- CAMBIOS v52 respecto a v51:
--
--   STRUCT-009 : url_queue.external_url — nueva columna VARCHAR(2048).
--                Almacena la URL alternativa/externa del hotel (3ª columna CSV).
--                Formato CSV actualizado: external_ref, url, external_url.
--
--   STRUCT-010 : url_queue.hotel_id_booking — ELIMINADO.
--                Campo redundante: el valor correcto se persiste en
--                hotels.hotel_id_booking durante el scraping.
--                Índice ix_url_queue_hotel_id_booking ELIMINADO.
--
--   STRUCT-011 : hotels.city RENOMBRADO a hotels.address_city.
--                Alineación con convención address_* (address_locality,
--                address_country). Índice ix_hotels_city_country ELIMINADO.
--                Nuevo índice ix_hotels_address_city creado.
--
--   STRUCT-012 : hotels.country — ELIMINADO.
--                Duplicado de hotels.address_country (ambos provienen de
--                addressCountry JSON-LD). Índice ix_hotels_city_country ELIMINADO.
--
--   FIX-LEGAL-001 : No impacta esquema. Corrección en extractor.py.
--
-- TABLAS CREADAS:
--   1. url_queue               — Cola de URLs a scrapeear
--   2. hotels                  — Datos principales del hotel por idioma
--   3. hotels_description      — Descripción larga por hotel/idioma (STRUCT-001)
--   4. hotels_amenities        — Amenidades normalizadas (STRUCT-005, v51)
--   5. hotels_policies         — Políticas del alojamiento (STRUCT-006, v51)
--   6. hotels_legal            — Información legal (STRUCT-007, v51)
--   7. hotels_popular_services — Servicios más populares (STRUCT-008, v51)
--   8. url_language_status     — Estado de scraping por URL/idioma
--   9. scraping_logs           — Log particionado por mes (RANGE)
--  10. image_downloads         — Tracking de descargas de imágenes
--  11. image_data              — Metadatos completos de fotos
--  12. system_metrics          — Snapshots de salud del sistema
--
-- VISTAS:
--   v_hotels_full      — Hotel completo denormalizado (con amenities, legal, etc.)
--   v_scraping_summary — Resumen de completitud de scraping por URL
--
-- NOTA WINDOWS 11:
--   max_connections ≤ 100 (Desktop Heap limitation)
--   No usar POSIX signals para reload — usar pg_reload_conf()
--   Antivirus: excluir directorio de datos de PostgreSQL del escaneo en tiempo real
-- =============================================================================

-- Configuración de sesión
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Extensión UUID (requerida para gen_random_uuid())
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =============================================================================
-- 1. URL_QUEUE
-- =============================================================================
-- STRUCT-009 (v52): external_url — URL alternativa/externa del hotel.
-- STRUCT-010 (v52): hotel_id_booking ELIMINADO — redundante con hotels.hotel_id_booking.

CREATE TABLE IF NOT EXISTS url_queue (
    id              UUID          NOT NULL DEFAULT gen_random_uuid(),
    url             VARCHAR(2048) NOT NULL,
    base_url        VARCHAR(2048) NOT NULL,
    external_ref    VARCHAR(64)   NULL,
    -- STRUCT-009 (v52): URL alternativa/externa del hotel (3ª columna CSV)
    external_url    VARCHAR(2048) NULL,
    -- STRUCT-010 (v52): hotel_id_booking ELIMINADO
    status          VARCHAR(32)   NOT NULL DEFAULT 'pending',
    priority        SMALLINT      NOT NULL DEFAULT 5,
    retry_count     SMALLINT      NOT NULL DEFAULT 0,
    max_retries     SMALLINT      NOT NULL DEFAULT 3,
    last_error      VARCHAR(2000) NULL,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    scraped_at      TIMESTAMPTZ   NULL,
    version_id      INTEGER       NOT NULL DEFAULT 1,

    CONSTRAINT pk_url_queue PRIMARY KEY (id),
    CONSTRAINT uq_url_queue_url UNIQUE (url),
    CONSTRAINT chk_url_queue_status CHECK (
        status IN ('pending','processing','done','error','skipped')
    ),
    CONSTRAINT chk_url_queue_priority CHECK (
        priority BETWEEN 1 AND 10
    )
);

-- Índices url_queue
CREATE INDEX IF NOT EXISTS ix_url_queue_status_priority ON url_queue (status, priority);
CREATE INDEX IF NOT EXISTS ix_url_queue_created_at      ON url_queue (created_at);
CREATE INDEX IF NOT EXISTS ix_url_queue_external_ref    ON url_queue (external_ref);
-- ix_url_queue_hotel_id_booking: ELIMINADO (STRUCT-010, v52)

COMMENT ON TABLE  url_queue IS 'Cola de URLs a scrapeear con estado y prioridad (v52)';
COMMENT ON COLUMN url_queue.external_ref  IS 'ID numérico del CSV origen (e.g. 1001) — 1ª columna';
COMMENT ON COLUMN url_queue.external_url  IS 'URL alternativa/externa del hotel — 3ª columna CSV (STRUCT-009, v52)';
COMMENT ON COLUMN url_queue.version_id    IS 'Optimistic locking counter';


-- =============================================================================
-- 2. HOTELS
-- =============================================================================
-- v52: city RENOMBRADO a address_city (STRUCT-011)
--      country ELIMINADO — duplicado de address_country (STRUCT-012)
-- v51: amenities (JSONB) ELIMINADO → hotels_amenities
--      policies  (JSONB) ELIMINADO → hotels_policies
-- v50: description ELIMINADO → hotels_description
--      photos    ELIMINADO → image_downloads
--      address   ELIMINADO (siempre NULL)

CREATE TABLE IF NOT EXISTS hotels (
    id                  UUID          NOT NULL DEFAULT gen_random_uuid(),
    url_id              UUID          NOT NULL,
    url                 VARCHAR(2048) NOT NULL,
    language            VARCHAR(10)   NOT NULL,
    hotel_name          VARCHAR(512)  NULL,
    hotel_id_booking    VARCHAR(64)   NULL,
    -- STRUCT-011 (v52): renombrado desde 'city'
    address_city        TEXT          NULL,
    -- STRUCT-012 (v52): 'country' ELIMINADO — usar address_country
    latitude            DOUBLE PRECISION NULL,
    longitude           DOUBLE PRECISION NULL,
    star_rating         DOUBLE PRECISION NULL,
    review_score        DOUBLE PRECISION NULL,
    review_count        INTEGER       NULL,
    -- schema.org / JSON-LD enrichment (NEW-COLS-001, v49)
    main_image_url      VARCHAR(2048) NULL,
    short_description   TEXT          NULL,
    rating_value        DOUBLE PRECISION NULL,
    best_rating         DOUBLE PRECISION NULL,
    street_address      VARCHAR(512)  NULL,
    address_locality    VARCHAR(256)  NULL,
    address_country     VARCHAR(128)  NULL,
    postal_code         VARCHAR(20)   NULL,
    -- Estructura de habitaciones
    room_types          JSONB         NULL DEFAULT '[]'::jsonb,
    raw_data            JSONB         NULL DEFAULT '{}'::jsonb,
    scrape_duration_s   DOUBLE PRECISION NULL,
    scrape_engine       VARCHAR(32)   NULL,
    created_at          TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    version_id          INTEGER       NOT NULL DEFAULT 1,

    CONSTRAINT pk_hotels PRIMARY KEY (id),
    CONSTRAINT fk_hotels_url_queue FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hotels_url_lang UNIQUE (url_id, language),
    CONSTRAINT chk_hotels_star_rating CHECK (
        star_rating IS NULL OR (star_rating >= 0 AND star_rating <= 5)
    ),
    CONSTRAINT chk_hotels_review_score CHECK (
        review_score IS NULL OR review_score BETWEEN 0 AND 10
    ),
    CONSTRAINT chk_hotels_review_count CHECK (
        review_count IS NULL OR review_count >= 0
    )
);

-- Índices hotels
CREATE INDEX IF NOT EXISTS ix_hotels_url_id           ON hotels (url_id);
CREATE INDEX IF NOT EXISTS ix_hotels_language          ON hotels (language);
CREATE INDEX IF NOT EXISTS ix_hotels_hotel_id_booking  ON hotels (hotel_id_booking);
-- STRUCT-011 (v52): ix_hotels_city_country ELIMINADO → ix_hotels_address_city
CREATE INDEX IF NOT EXISTS ix_hotels_address_city      ON hotels (address_city);
CREATE INDEX IF NOT EXISTS ix_hotels_created_at        ON hotels (created_at);

COMMENT ON TABLE  hotels IS 'Datos principales del hotel por idioma (v52)';
COMMENT ON COLUMN hotels.star_rating    IS 'Estrellas normalizadas 0-5 (valor raw Booking ÷ 2)';
COMMENT ON COLUMN hotels.review_count   IS 'aggregateRating.reviewCount de JSON-LD (language-independent)';
COMMENT ON COLUMN hotels.address_city   IS 'Ciudad/región del hotel — fuente: addressRegion JSON-LD o breadcrumb (renombrado desde city, STRUCT-011 v52)';
COMMENT ON COLUMN hotels.address_country IS 'Código/nombre de país — fuente: addressCountry JSON-LD (address_country es la única fuente canónica, STRUCT-012 v52)';


-- =============================================================================
-- 3. HOTELS_DESCRIPTION (STRUCT-001, v50)
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels_description (
    id          UUID        NOT NULL DEFAULT gen_random_uuid(),
    hotel_id    UUID        NOT NULL,
    url_id      UUID        NOT NULL,
    language    VARCHAR(10) NOT NULL,
    description TEXT        NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_description PRIMARY KEY (id),
    CONSTRAINT fk_hdesc_hotel  FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hdesc_url    FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hdesc_url_lang UNIQUE (url_id, language)
);

CREATE INDEX IF NOT EXISTS ix_hdesc_hotel_id ON hotels_description (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hdesc_language  ON hotels_description (language);

COMMENT ON TABLE hotels_description IS
    'Descripción larga del hotel por idioma — separada de hotels para reducir tamaño de fila (STRUCT-001)';


-- =============================================================================
-- 4. HOTELS_AMENITIES (STRUCT-005, v51)
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels_amenities (
    id          BIGSERIAL    NOT NULL,
    hotel_id    UUID         NOT NULL,
    url_id      UUID         NOT NULL,
    language    VARCHAR(10)  NOT NULL,
    amenity     VARCHAR(512) NOT NULL,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_amenities PRIMARY KEY (id),
    CONSTRAINT fk_hamenity_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hamenity_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hamenity_hotel_lang_amenity UNIQUE (hotel_id, language, amenity)
);

CREATE INDEX IF NOT EXISTS ix_hamenity_hotel_id ON hotels_amenities (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hamenity_language  ON hotels_amenities (language);
CREATE INDEX IF NOT EXISTS ix_hamenity_amenity   ON hotels_amenities (amenity);

COMMENT ON TABLE  hotels_amenities IS
    'Amenidades del hotel normalizadas — una fila por amenidad (STRUCT-005, v51)';
COMMENT ON COLUMN hotels_amenities.amenity IS
    'Texto de la amenidad (e.g. ''Piscina al aire libre'', ''Free WiFi'')';


-- =============================================================================
-- 5. HOTELS_POLICIES (STRUCT-006, v51)
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels_policies (
    id              BIGSERIAL    NOT NULL,
    hotel_id        UUID         NOT NULL,
    url_id          UUID         NOT NULL,
    language        VARCHAR(10)  NOT NULL,
    policy_name     VARCHAR(256) NOT NULL,
    policy_details  TEXT         NULL,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_policies PRIMARY KEY (id),
    CONSTRAINT fk_hpolicy_hotel  FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hpolicy_url    FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hpolicy_hotel_lang_name UNIQUE (hotel_id, language, policy_name)
);

CREATE INDEX IF NOT EXISTS ix_hpolicy_hotel_id   ON hotels_policies (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hpolicy_language    ON hotels_policies (language);
CREATE INDEX IF NOT EXISTS ix_hpolicy_policy_name ON hotels_policies (policy_name);

COMMENT ON TABLE  hotels_policies IS
    'Políticas del alojamiento — una fila por política (STRUCT-006, v51)';
COMMENT ON COLUMN hotels_policies.policy_name IS
    'Nombre de la política (e.g. ''Check-in'', ''Mascotas'', ''Cancelación / prepago'')';
COMMENT ON COLUMN hotels_policies.policy_details IS
    'Texto completo de la política extraído del HTML de Booking.com';


-- =============================================================================
-- 6. HOTELS_LEGAL (STRUCT-007, v51)
-- =============================================================================
-- FIX-LEGAL-001 (v52): extractor.py corregido para detectar el título del
-- bloque legal en múltiples idiomas (ES, JA, AR, FR, etc.).
-- No impacta el esquema — el fix es exclusivamente en extractor.py.

CREATE TABLE IF NOT EXISTS hotels_legal (
    id              BIGSERIAL    NOT NULL,
    hotel_id        UUID         NOT NULL,
    url_id          UUID         NOT NULL,
    language        VARCHAR(10)  NOT NULL,
    legal           VARCHAR(256) NULL,
    legal_info      TEXT         NULL,
    legal_details   TEXT         NULL,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_legal PRIMARY KEY (id),
    CONSTRAINT fk_hlegal_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hlegal_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hlegal_hotel_lang UNIQUE (hotel_id, language)
);

CREATE INDEX IF NOT EXISTS ix_hlegal_hotel_id ON hotels_legal (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hlegal_language  ON hotels_legal (language);

COMMENT ON TABLE  hotels_legal IS
    'Información legal del alojamiento por idioma (STRUCT-007, v51). FIX-LEGAL-001 en extractor.py (v52)';
COMMENT ON COLUMN hotels_legal.legal IS
    'Título del bloque legal (e.g. ''Información legal'' / ''Legal information'')';
COMMENT ON COLUMN hotels_legal.legal_info IS
    'Texto introductorio del bloque legal (quién gestiona el alojamiento)';
COMMENT ON COLUMN hotels_legal.legal_details IS
    'Detalles extendidos (normalmente vacío en Booking.com)';


-- =============================================================================
-- 7. HOTELS_POPULAR_SERVICES (STRUCT-008, v51)
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels_popular_services (
    id              BIGSERIAL    NOT NULL,
    hotel_id        UUID         NOT NULL,
    url_id          UUID         NOT NULL,
    language        VARCHAR(10)  NOT NULL,
    popular_service VARCHAR(512) NOT NULL,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_popular_services PRIMARY KEY (id),
    CONSTRAINT fk_hpopservice_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hpopservice_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hpopservice_hotel_lang_service UNIQUE (hotel_id, language, popular_service)
);

CREATE INDEX IF NOT EXISTS ix_hpopservice_hotel_id ON hotels_popular_services (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hpopservice_language  ON hotels_popular_services (language);
CREATE INDEX IF NOT EXISTS ix_hpopservice_service   ON hotels_popular_services (popular_service);

COMMENT ON TABLE  hotels_popular_services IS
    'Servicios más populares del hotel — selección editorial de Booking.com (STRUCT-008, v51)';
COMMENT ON COLUMN hotels_popular_services.popular_service IS
    'Nombre del servicio popular (e.g. ''WiFi gratis'', ''Piscina al aire libre'')';


-- =============================================================================
-- 8. URL_LANGUAGE_STATUS
-- =============================================================================

CREATE TABLE IF NOT EXISTS url_language_status (
    id          UUID         NOT NULL DEFAULT gen_random_uuid(),
    url_id      UUID         NOT NULL,
    language    VARCHAR(10)  NOT NULL,
    status      VARCHAR(32)  NOT NULL DEFAULT 'pending',
    attempts    SMALLINT     NOT NULL DEFAULT 0,
    last_error  VARCHAR(2000) NULL,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_url_language_status PRIMARY KEY (id),
    CONSTRAINT fk_uls_url  FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_uls_url_lang UNIQUE (url_id, language),
    CONSTRAINT chk_uls_status_valid CHECK (
        status IN ('pending','processing','done','error','skipped','incomplete')
    )
);

CREATE INDEX IF NOT EXISTS ix_uls_url_id  ON url_language_status (url_id);
CREATE INDEX IF NOT EXISTS ix_uls_status  ON url_language_status (status);

COMMENT ON TABLE url_language_status IS 'Tracking de completitud de scraping por URL y lenguaje';


-- =============================================================================
-- 9. SCRAPING_LOGS (PARTITIONED BY RANGE — por mes)
-- =============================================================================
-- ⚠️ PostgreSQL NO soporta FK constraints en tablas particionadas (BUG-003/103).
-- La integridad referencial se garantiza via trigger trg_scraping_logs_fk_check.

CREATE TABLE IF NOT EXISTS scraping_logs (
    id              UUID         NOT NULL DEFAULT gen_random_uuid(),
    url_id          UUID         NOT NULL,
    hotel_id        UUID         NULL,
    language        VARCHAR(10)  NULL,
    event_type      VARCHAR(64)  NOT NULL,
    status          VARCHAR(32)  NOT NULL,
    error_message   TEXT         NULL,
    duration_ms     INTEGER      NULL,
    worker_id       VARCHAR(128) NULL,
    extra_data      JSONB        NULL DEFAULT '{}'::jsonb,
    scraped_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (scraped_at);

-- Particiones 2025
CREATE TABLE IF NOT EXISTS scraping_logs_2025_01 PARTITION OF scraping_logs FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_02 PARTITION OF scraping_logs FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_03 PARTITION OF scraping_logs FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_04 PARTITION OF scraping_logs FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_05 PARTITION OF scraping_logs FOR VALUES FROM ('2025-05-01') TO ('2025-06-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_06 PARTITION OF scraping_logs FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_07 PARTITION OF scraping_logs FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_08 PARTITION OF scraping_logs FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_09 PARTITION OF scraping_logs FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_10 PARTITION OF scraping_logs FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_11 PARTITION OF scraping_logs FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2025_12 PARTITION OF scraping_logs FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');

-- Particiones 2026
CREATE TABLE IF NOT EXISTS scraping_logs_2026_01 PARTITION OF scraping_logs FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_02 PARTITION OF scraping_logs FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_03 PARTITION OF scraping_logs FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_04 PARTITION OF scraping_logs FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_05 PARTITION OF scraping_logs FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_06 PARTITION OF scraping_logs FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_07 PARTITION OF scraping_logs FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_08 PARTITION OF scraping_logs FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_09 PARTITION OF scraping_logs FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_10 PARTITION OF scraping_logs FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_11 PARTITION OF scraping_logs FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2026_12 PARTITION OF scraping_logs FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');

-- Partición DEFAULT para fechas fuera de rango
CREATE TABLE IF NOT EXISTS scraping_logs_default PARTITION OF scraping_logs DEFAULT;

COMMENT ON TABLE scraping_logs IS
    'Log particionado por mes de eventos de scraping. FK via trigger (BUG-003/103)';

-- =============================================================================
-- Trigger FK check en scraping_logs
-- =============================================================================

CREATE OR REPLACE FUNCTION fn_scraping_logs_fk_check()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM url_queue WHERE id = NEW.url_id) THEN
        RAISE EXCEPTION 'scraping_logs.url_id % no existe en url_queue', NEW.url_id;
    END IF;
    IF NEW.hotel_id IS NOT NULL AND
       NOT EXISTS (SELECT 1 FROM hotels WHERE id = NEW.hotel_id) THEN
        RAISE EXCEPTION 'scraping_logs.hotel_id % no existe en hotels', NEW.hotel_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_scraping_logs_fk_check
    BEFORE INSERT OR UPDATE ON scraping_logs
    FOR EACH ROW EXECUTE FUNCTION fn_scraping_logs_fk_check();


-- =============================================================================
-- 10. IMAGE_DOWNLOADS
-- =============================================================================

CREATE TABLE IF NOT EXISTS image_downloads (
    id              UUID         NOT NULL DEFAULT gen_random_uuid(),
    hotel_id        UUID         NOT NULL,
    id_photo        VARCHAR(32)  NULL,
    category        VARCHAR(16)  NULL,
    url             VARCHAR(2048) NOT NULL,
    local_path      VARCHAR(1024) NULL,
    file_size_bytes INTEGER      NULL,
    content_type    VARCHAR(64)  NULL,
    status          VARCHAR(32)  NOT NULL DEFAULT 'pending',
    error_message   VARCHAR(2000) NULL,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    downloaded_at   TIMESTAMPTZ  NULL,

    CONSTRAINT pk_image_downloads PRIMARY KEY (id),
    CONSTRAINT fk_imgdl_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_imgdl_hotel_url UNIQUE (hotel_id, url),
    CONSTRAINT chk_imgdl_status CHECK (
        status IN ('pending','downloading','done','error','skipped')
    ),
    CONSTRAINT chk_imgdl_category CHECK (
        category IS NULL OR category IN ('thumb_url','large_url','highres_url')
    )
);

CREATE INDEX IF NOT EXISTS ix_imgdl_hotel_id ON image_downloads (hotel_id);
CREATE INDEX IF NOT EXISTS ix_imgdl_status   ON image_downloads (status);
CREATE INDEX IF NOT EXISTS ix_imgdl_id_photo ON image_downloads (id_photo);

COMMENT ON TABLE  image_downloads IS 'Tracking de descargas individuales de imágenes por hotel';
COMMENT ON COLUMN image_downloads.id_photo IS 'Booking.com photo ID (e.g. ''49312038'')';
COMMENT ON COLUMN image_downloads.category IS 'Variante de tamaño: thumb_url | large_url | highres_url';


-- =============================================================================
-- 11. IMAGE_DATA
-- =============================================================================

CREATE TABLE IF NOT EXISTS image_data (
    id               UUID        NOT NULL DEFAULT gen_random_uuid(),
    id_photo         VARCHAR(32) NOT NULL,
    hotel_id         UUID        NOT NULL,
    orientation      VARCHAR(16) NULL,
    photo_width      INTEGER     NULL,
    photo_height     INTEGER     NULL,
    alt              TEXT        NULL,
    created_at_photo TIMESTAMPTZ NULL,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_image_data PRIMARY KEY (id),
    CONSTRAINT uq_image_data_id_photo UNIQUE (id_photo),
    CONSTRAINT fk_imgdata_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_imgdata_orientation CHECK (
        orientation IS NULL OR orientation IN ('landscape','portrait','square')
    ),
    CONSTRAINT chk_imgdata_width_positive  CHECK (photo_width  IS NULL OR photo_width  > 0),
    CONSTRAINT chk_imgdata_height_positive CHECK (photo_height IS NULL OR photo_height > 0)
);

CREATE INDEX IF NOT EXISTS ix_imgdata_hotel_id ON image_data (hotel_id);

COMMENT ON TABLE  image_data IS 'Metadatos completos de fotos desde JS hotelPhotos de Booking.com';
COMMENT ON COLUMN image_data.id_photo         IS 'Booking.com photo ID — globalmente único';
COMMENT ON COLUMN image_data.created_at_photo IS 'Timestamp de creación de la foto en Booking.com';


-- =============================================================================
-- 12. SYSTEM_METRICS
-- =============================================================================

CREATE TABLE IF NOT EXISTS system_metrics (
    id                  BIGSERIAL        NOT NULL,
    recorded_at         TIMESTAMPTZ      NOT NULL DEFAULT NOW(),
    cpu_usage           DOUBLE PRECISION NULL,
    memory_usage        DOUBLE PRECISION NULL,
    active_workers      SMALLINT         NULL,
    db_pool_checked_out SMALLINT         NULL,
    redis_connected     BOOLEAN          NULL,
    urls_pending        INTEGER          NULL,
    urls_done           INTEGER          NULL,
    extra_data          JSONB            NULL DEFAULT '{}'::jsonb,

    CONSTRAINT pk_system_metrics PRIMARY KEY (id)
);

-- BUG-019: índices compuestos en columnas de series temporales
CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_at  ON system_metrics (recorded_at);
CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_cpu ON system_metrics (recorded_at, cpu_usage);
CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_mem ON system_metrics (recorded_at, memory_usage);

COMMENT ON TABLE system_metrics IS 'Snapshots periódicos de salud del sistema (BUG-019)';


-- =============================================================================
-- TRIGGER: updated_at automático en url_queue y hotels
-- =============================================================================

CREATE OR REPLACE FUNCTION fn_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_url_queue_updated_at
    BEFORE UPDATE ON url_queue
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE OR REPLACE TRIGGER trg_hotels_updated_at
    BEFORE UPDATE ON hotels
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE OR REPLACE TRIGGER trg_hotels_description_updated_at
    BEFORE UPDATE ON hotels_description
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE OR REPLACE TRIGGER trg_url_language_status_updated_at
    BEFORE UPDATE ON url_language_status
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();


-- =============================================================================
-- VISTAS AUXILIARES
-- =============================================================================

-- Vista: hotel completo con datos denormalizados de tablas satélite
CREATE OR REPLACE VIEW v_hotels_full AS
SELECT
    h.id,
    h.url_id,
    h.url,
    h.language,
    h.hotel_name,
    h.hotel_id_booking,
    -- STRUCT-011 (v52): address_city (renombrado desde city)
    h.address_city,
    -- STRUCT-012 (v52): country eliminado — usar address_country
    h.latitude,
    h.longitude,
    h.star_rating,
    h.review_score,
    h.review_count,
    h.rating_value,
    h.best_rating,
    h.main_image_url,
    h.short_description,
    h.street_address,
    h.address_locality,
    h.address_country,
    h.postal_code,
    h.scrape_engine,
    h.created_at,
    h.updated_at,
    -- url_queue: incluye external_ref y external_url (STRUCT-009)
    uq.external_ref,
    uq.external_url,
    -- Descripción larga
    hd.description,
    -- Amenidades como array
    COALESCE(
        (SELECT array_agg(a.amenity ORDER BY a.id)
         FROM hotels_amenities a
         WHERE a.hotel_id = h.id AND a.language = h.language),
        ARRAY[]::TEXT[]
    ) AS amenities,
    -- Servicios populares como array
    COALESCE(
        (SELECT array_agg(p.popular_service ORDER BY p.id)
         FROM hotels_popular_services p
         WHERE p.hotel_id = h.id AND p.language = h.language),
        ARRAY[]::TEXT[]
    ) AS popular_services,
    -- Políticas como JSON array
    COALESCE(
        (SELECT jsonb_agg(
            jsonb_build_object(
                'policy_name',    pol.policy_name,
                'policy_details', pol.policy_details
            ) ORDER BY pol.id
        )
         FROM hotels_policies pol
         WHERE pol.hotel_id = h.id AND pol.language = h.language),
        '[]'::jsonb
    ) AS policies,
    -- Legal
    jsonb_build_object(
        'legal',         hl.legal,
        'legal_info',    hl.legal_info,
        'legal_details', hl.legal_details
    ) AS legal
FROM hotels h
LEFT JOIN url_queue uq
       ON uq.id = h.url_id
LEFT JOIN hotels_description hd
       ON hd.hotel_id = h.id AND hd.language = h.language
LEFT JOIN hotels_legal hl
       ON hl.hotel_id = h.id AND hl.language = h.language;

COMMENT ON VIEW v_hotels_full IS
    'Vista denormalizada de hotel con description, amenities, popular_services, policies, legal y url_queue data (v52)';


-- Vista: resumen de completitud de scraping
CREATE OR REPLACE VIEW v_scraping_summary AS
SELECT
    uq.id               AS url_id,
    uq.url,
    uq.external_ref,
    -- STRUCT-009 (v52): external_url incluido en la vista
    uq.external_url,
    uq.status           AS queue_status,
    uq.retry_count,
    uq.scraped_at,
    COUNT(uls.id)        AS languages_tracked,
    SUM(CASE WHEN uls.status = 'done'  THEN 1 ELSE 0 END) AS languages_done,
    SUM(CASE WHEN uls.status = 'error' THEN 1 ELSE 0 END) AS languages_error,
    MAX(uls.attempts)    AS max_attempts
FROM url_queue uq
LEFT JOIN url_language_status uls ON uls.url_id = uq.id
GROUP BY uq.id, uq.url, uq.external_ref, uq.external_url,
         uq.status, uq.retry_count, uq.scraped_at;

COMMENT ON VIEW v_scraping_summary IS 'Resumen de completitud de scraping por URL (v52)';


-- =============================================================================
-- CORRECCIÓN DE DATOS: hotels_legal ES (FIX-LEGAL-001)
-- =============================================================================
-- Ejecutar SOLO si existen registros erróneos en idioma 'es' donde
-- legal_info contiene el título y legal está vacío.
-- Los registros IT son correctos y sirven como referencia.
--
-- Estrategia:
--   Para registros ES donde legal IS NULL o legal = '' Y legal_info
--   parece ser un título (longitud corta, coincide con patrón de título legal):
--   mover legal_info → legal, y legal_details → legal_info.
--
-- ⚠️ Verificar ANTES de ejecutar con la consulta de diagnóstico al final.

DO $$
DECLARE
    v_updated INTEGER := 0;
BEGIN
    -- Detectar si existen registros problemáticos
    -- (legal vacío, legal_info corto = probable título)
    IF EXISTS (
        SELECT 1
        FROM hotels_legal
        WHERE language = 'es'
          AND (legal IS NULL OR TRIM(legal) = '')
          AND legal_info IS NOT NULL
          AND LENGTH(TRIM(legal_info)) > 0
          AND LENGTH(TRIM(legal_info)) <= 120
    ) THEN
        RAISE NOTICE 'FIX-LEGAL-001: Corrigiendo registros ES con título en legal_info...';

        UPDATE hotels_legal
        SET
            legal         = TRIM(legal_info),     -- mover título a campo correcto
            legal_info    = TRIM(legal_details),   -- promover detalles a info
            legal_details = ''                     -- limpiar campo de detalles
        WHERE language = 'es'
          AND (legal IS NULL OR TRIM(legal) = '')
          AND legal_info IS NOT NULL
          AND LENGTH(TRIM(legal_info)) > 0
          AND LENGTH(TRIM(legal_info)) <= 120;

        GET DIAGNOSTICS v_updated = ROW_COUNT;
        RAISE NOTICE 'FIX-LEGAL-001: % registros corregidos.', v_updated;
        RAISE NOTICE 'ACCIÓN RECOMENDADA: Re-scrape de las URLs afectadas para regenerar';
        RAISE NOTICE '  datos limpios con el extractor v52 corregido.';
    ELSE
        RAISE NOTICE 'FIX-LEGAL-001: No se encontraron registros ES problemáticos — omitido.';
    END IF;
END $$;


-- =============================================================================
-- CONSULTAS DE VALIDACIÓN POST-INSTALACIÓN
-- =============================================================================

/*
-- 1. Verificar que todas las tablas existen
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
      'url_queue','hotels','hotels_description',
      'hotels_amenities','hotels_policies','hotels_legal',
      'hotels_popular_services','url_language_status',
      'scraping_logs','image_downloads','image_data','system_metrics'
  )
ORDER BY table_name;

-- 2. Verificar columnas clave de url_queue (v52)
SELECT column_name, data_type, character_maximum_length, is_nullable
FROM information_schema.columns
WHERE table_name = 'url_queue'
ORDER BY ordinal_position;
-- Esperado: external_url presente, hotel_id_booking AUSENTE

-- 3. Verificar columnas clave de hotels (v52)
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'hotels'
ORDER BY ordinal_position;
-- Esperado: address_city presente, city AUSENTE, country AUSENTE

-- 4. Verificar índices de hotels
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public' AND tablename = 'hotels'
ORDER BY indexname;
-- Esperado: ix_hotels_address_city presente, ix_hotels_city_country AUSENTE

-- 5. Diagnóstico hotels_legal ES antes de FIX-LEGAL-001
SELECT id, hotel_id, language,
       LEFT(legal, 60)      AS legal_col,
       LEFT(legal_info, 80) AS legal_info_col,
       LENGTH(legal_info)   AS legal_info_len
FROM hotels_legal
WHERE language = 'es'
ORDER BY id
LIMIT 30;
-- Si legal_col está vacío y legal_info_col contiene texto corto (~título),
-- el DO-block de FIX-LEGAL-001 habrá corregido los datos.

-- 6. Comparar ES vs IT (IT = referencia correcta)
SELECT language,
       COUNT(*) AS total,
       SUM(CASE WHEN legal IS NOT NULL AND legal != '' THEN 1 ELSE 0 END) AS with_title,
       SUM(CASE WHEN legal IS NULL OR legal = '' THEN 1 ELSE 0 END)      AS without_title
FROM hotels_legal
WHERE language IN ('es','it')
GROUP BY language;
-- Esperado: ambos idiomas deben tener with_title = total (0 without_title)
*/

-- =============================================================================
-- FIN DEL SCHEMA v52
-- =============================================================================
