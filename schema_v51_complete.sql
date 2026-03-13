-- =============================================================================
-- BookingScraper Pro — Schema Completo v6.0.0 build 51
-- PostgreSQL 14+ / Windows 11 Single-Node Deployment
-- =============================================================================
--
-- INSTRUCCIONES DE EJECUCIÓN (Windows 11):
--   psql -U postgres -f schema_v51_complete.sql
--   O desde pgAdmin 4: Tools > Query Tool > Ejecutar este archivo
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

CREATE TABLE IF NOT EXISTS url_queue (
    id              UUID        NOT NULL DEFAULT gen_random_uuid(),
    url             VARCHAR(2048) NOT NULL,
    base_url        VARCHAR(2048) NOT NULL,
    external_ref    VARCHAR(64)   NULL,
    hotel_id_booking VARCHAR(64)  NULL,
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
CREATE INDEX IF NOT EXISTS ix_url_queue_hotel_id_booking ON url_queue (hotel_id_booking);

COMMENT ON TABLE  url_queue IS 'Cola de URLs a scrapeear con estado y prioridad';
COMMENT ON COLUMN url_queue.external_ref IS 'ID numérico del CSV origen (e.g. 1001)';
COMMENT ON COLUMN url_queue.version_id IS 'Optimistic locking counter';


-- =============================================================================
-- 2. HOTELS
-- =============================================================================
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
    city                TEXT          NULL,
    country             TEXT          NULL,
    latitude            DOUBLE PRECISION NULL,
    longitude           DOUBLE PRECISION NULL,
    star_rating         DOUBLE PRECISION NULL,
    review_score        DOUBLE PRECISION NULL,
    review_count        INTEGER       NULL,
    -- schema.org / JSON-LD enrichment
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
CREATE INDEX IF NOT EXISTS ix_hotels_url_id         ON hotels (url_id);
CREATE INDEX IF NOT EXISTS ix_hotels_language        ON hotels (language);
CREATE INDEX IF NOT EXISTS ix_hotels_hotel_id_booking ON hotels (hotel_id_booking);
CREATE INDEX IF NOT EXISTS ix_hotels_city_country    ON hotels (city, country);
CREATE INDEX IF NOT EXISTS ix_hotels_created_at      ON hotels (created_at);

COMMENT ON TABLE  hotels IS 'Datos principales del hotel por idioma (v51)';
COMMENT ON COLUMN hotels.star_rating IS 'Estrellas normalizadas 0-5 (valor raw Booking ÷ 2)';
COMMENT ON COLUMN hotels.review_count IS 'aggregateRating.reviewCount de JSON-LD (language-independent)';


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
-- Reemplaza hotels.amenities (JSONB array).
-- Una fila por amenidad. Permite filtrado exacto sin operadores JSONB.

CREATE TABLE IF NOT EXISTS hotels_amenities (
    id          BIGSERIAL   NOT NULL,
    hotel_id    UUID        NOT NULL,
    url_id      UUID        NOT NULL,
    language    VARCHAR(10) NOT NULL,
    amenity     VARCHAR(512) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

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
-- Reemplaza hotels.policies (JSONB dict).
-- Una fila por política. Permite consultas directas sin deserialización.

CREATE TABLE IF NOT EXISTS hotels_policies (
    id              BIGSERIAL   NOT NULL,
    hotel_id        UUID        NOT NULL,
    url_id          UUID        NOT NULL,
    language        VARCHAR(10) NOT NULL,
    policy_name     VARCHAR(256) NOT NULL,
    policy_details  TEXT        NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

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
-- Nueva tabla. Un registro por hotel/idioma.

CREATE TABLE IF NOT EXISTS hotels_legal (
    id              BIGSERIAL   NOT NULL,
    hotel_id        UUID        NOT NULL,
    url_id          UUID        NOT NULL,
    language        VARCHAR(10) NOT NULL,
    legal           VARCHAR(256) NULL,
    legal_info      TEXT        NULL,
    legal_details   TEXT        NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

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
    'Información legal del alojamiento por idioma — (STRUCT-007, v51)';
COMMENT ON COLUMN hotels_legal.legal IS
    'Título del bloque legal (e.g. ''Información legal'' / ''Legal information'')';
COMMENT ON COLUMN hotels_legal.legal_info IS
    'Texto introductorio del bloque legal (quién gestiona el alojamiento)';
COMMENT ON COLUMN hotels_legal.legal_details IS
    'Detalles extendidos (normalmente vacío en Booking.com)';


-- =============================================================================
-- 7. HOTELS_POPULAR_SERVICES (STRUCT-008, v51)
-- =============================================================================
-- Nueva tabla. Servicios populares curados por Booking.com (8-12 ítems).
-- Difiere de hotels_amenities: es una selección editorial del proveedor.

CREATE TABLE IF NOT EXISTS hotels_popular_services (
    id              BIGSERIAL   NOT NULL,
    hotel_id        UUID        NOT NULL,
    url_id          UUID        NOT NULL,
    language        VARCHAR(10) NOT NULL,
    popular_service VARCHAR(512) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

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
    id          UUID        NOT NULL DEFAULT gen_random_uuid(),
    url_id      UUID        NOT NULL,
    language    VARCHAR(10) NOT NULL,
    status      VARCHAR(32) NOT NULL DEFAULT 'pending',
    attempts    SMALLINT    NOT NULL DEFAULT 0,
    last_error  VARCHAR(2000) NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

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
    id              UUID        NOT NULL DEFAULT gen_random_uuid(),
    url_id          UUID        NOT NULL,
    hotel_id        UUID        NULL,
    language        VARCHAR(10) NULL,
    event_type      VARCHAR(64) NOT NULL,
    status          VARCHAR(32) NOT NULL,
    error_message   TEXT        NULL,
    duration_ms     INTEGER     NULL,
    worker_id       VARCHAR(128) NULL,
    extra_data      JSONB       NULL DEFAULT '{}'::jsonb,
    scraped_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (scraped_at);

-- Particiones iniciales (ajustar año/mes según necesidad)
CREATE TABLE IF NOT EXISTS scraping_logs_2025_01
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_02
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_03
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_04
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_05
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-05-01') TO ('2025-06-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_06
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_07
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_08
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_09
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_10
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_11
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2025_12
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_01
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_02
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_03
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_04
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_05
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_06
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_07
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_08
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_09
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_10
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_11
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');

CREATE TABLE IF NOT EXISTS scraping_logs_2026_12
    PARTITION OF scraping_logs
    FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');

-- Partition DEFAULT para fechas fuera de rango definido
CREATE TABLE IF NOT EXISTS scraping_logs_default
    PARTITION OF scraping_logs DEFAULT;

COMMENT ON TABLE scraping_logs IS
    'Log particionado por mes de eventos de scraping. FK via trigger (no soportada en partitioned tables)';

-- =============================================================================
-- Trigger para FK check en scraping_logs (BUG-003/103)
-- =============================================================================

CREATE OR REPLACE FUNCTION fn_scraping_logs_fk_check()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar url_id existe en url_queue
    IF NOT EXISTS (SELECT 1 FROM url_queue WHERE id = NEW.url_id) THEN
        RAISE EXCEPTION 'scraping_logs.url_id % no existe en url_queue', NEW.url_id;
    END IF;
    -- Verificar hotel_id existe en hotels (si no es NULL)
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
    id              UUID        NOT NULL DEFAULT gen_random_uuid(),
    hotel_id        UUID        NOT NULL,
    id_photo        VARCHAR(32) NULL,
    category        VARCHAR(16) NULL,
    url             VARCHAR(2048) NOT NULL,
    local_path      VARCHAR(1024) NULL,
    file_size_bytes INTEGER     NULL,
    content_type    VARCHAR(64) NULL,
    status          VARCHAR(32) NOT NULL DEFAULT 'pending',
    error_message   VARCHAR(2000) NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    downloaded_at   TIMESTAMPTZ NULL,

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
    id              UUID        NOT NULL DEFAULT gen_random_uuid(),
    id_photo        VARCHAR(32) NOT NULL,
    hotel_id        UUID        NOT NULL,
    orientation     VARCHAR(16) NULL,
    photo_width     INTEGER     NULL,
    photo_height    INTEGER     NULL,
    alt             TEXT        NULL,
    created_at_photo TIMESTAMPTZ NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_image_data PRIMARY KEY (id),
    CONSTRAINT fk_imgdata_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_imgdata_id_photo UNIQUE (id_photo),
    CONSTRAINT chk_imgdata_orientation CHECK (
        orientation IS NULL OR orientation IN ('landscape','portrait','square')
    ),
    CONSTRAINT chk_imgdata_width_positive CHECK (
        photo_width IS NULL OR photo_width > 0
    ),
    CONSTRAINT chk_imgdata_height_positive CHECK (
        photo_height IS NULL OR photo_height > 0
    )
);

CREATE INDEX IF NOT EXISTS ix_imgdata_hotel_id ON image_data (hotel_id);

COMMENT ON TABLE  image_data IS 'Metadatos completos de fotos del JS hotelPhotos de Booking.com';
COMMENT ON COLUMN image_data.id_photo IS 'Booking.com photo ID — globalmente único';
COMMENT ON COLUMN image_data.created_at_photo IS 'Timestamp de creación de la foto en Booking.com';


-- =============================================================================
-- 12. SYSTEM_METRICS
-- =============================================================================

CREATE TABLE IF NOT EXISTS system_metrics (
    id                  BIGSERIAL   NOT NULL,
    recorded_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    cpu_usage           DOUBLE PRECISION NULL,
    memory_usage        DOUBLE PRECISION NULL,
    active_workers      SMALLINT    NULL,
    db_pool_checked_out SMALLINT    NULL,
    redis_connected     BOOLEAN     NULL,
    urls_pending        INTEGER     NULL,
    urls_done           INTEGER     NULL,
    extra_data          JSONB       NULL DEFAULT '{}'::jsonb,

    CONSTRAINT pk_system_metrics PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_at  ON system_metrics (recorded_at);
CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_cpu ON system_metrics (recorded_at, cpu_usage);
CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_mem ON system_metrics (recorded_at, memory_usage);

COMMENT ON TABLE system_metrics IS 'Snapshots periódicos de salud del sistema (BUG-019)';


-- =============================================================================
-- FUNCIÓN: updated_at automático vía trigger
-- =============================================================================

CREATE OR REPLACE FUNCTION fn_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger updated_at en url_queue
CREATE OR REPLACE TRIGGER trg_url_queue_updated_at
    BEFORE UPDATE ON url_queue
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

-- Trigger updated_at en hotels
CREATE OR REPLACE TRIGGER trg_hotels_updated_at
    BEFORE UPDATE ON hotels
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

-- Trigger updated_at en hotels_description
CREATE OR REPLACE TRIGGER trg_hotels_description_updated_at
    BEFORE UPDATE ON hotels_description
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

-- Trigger updated_at en url_language_status
CREATE OR REPLACE TRIGGER trg_uls_updated_at
    BEFORE UPDATE ON url_language_status
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();


-- =============================================================================
-- MIGRACIÓN DE DATOS: hotels.amenities → hotels_amenities
-- =============================================================================
-- Ejecutar SOLO si la tabla hotels aún contiene la columna 'amenities'.
-- Verifica existencia de la columna antes de intentar la migración.
-- Tras confirmar la migración exitosa, ejecutar ALTER TABLE hotels DROP COLUMN amenities.

DO $$
DECLARE
    v_col_exists BOOLEAN;
    v_migrated   INTEGER := 0;
BEGIN
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'hotels'
          AND column_name = 'amenities'
    ) INTO v_col_exists;

    IF v_col_exists THEN
        RAISE NOTICE 'Migrando hotels.amenities → hotels_amenities...';

        INSERT INTO hotels_amenities (hotel_id, url_id, language, amenity)
        SELECT
            h.id          AS hotel_id,
            h.url_id      AS url_id,
            h.language    AS language,
            TRIM(amenity_text) AS amenity
        FROM hotels h
        CROSS JOIN LATERAL (
            SELECT jsonb_array_elements_text(
                CASE
                    WHEN jsonb_typeof(h.amenities) = 'array' THEN h.amenities
                    ELSE '[]'::jsonb
                END
            ) AS amenity_text
        ) AS expanded
        WHERE h.amenities IS NOT NULL
          AND jsonb_typeof(h.amenities) = 'array'
          AND jsonb_array_length(h.amenities) > 0
          AND TRIM(amenity_text) <> ''
        ON CONFLICT (hotel_id, language, amenity) DO NOTHING;

        GET DIAGNOSTICS v_migrated = ROW_COUNT;
        RAISE NOTICE 'Migración hotels_amenities: % filas insertadas.', v_migrated;
        RAISE NOTICE 'ACCIÓN REQUERIDA: Verificar datos y luego ejecutar:';
        RAISE NOTICE '  ALTER TABLE hotels DROP COLUMN amenities;';
    ELSE
        RAISE NOTICE 'Columna hotels.amenities no existe — migración omitida.';
    END IF;
END $$;


-- =============================================================================
-- MIGRACIÓN DE DATOS: hotels.policies → hotels_policies
-- =============================================================================
-- Ejecutar SOLO si la tabla hotels aún contiene la columna 'policies'.
-- El JSONB de policies puede tener estructura variable; se intenta mapear
-- las claves del dict como policy_name y sus valores como policy_details.

DO $$
DECLARE
    v_col_exists BOOLEAN;
    v_migrated   INTEGER := 0;
BEGIN
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'hotels'
          AND column_name = 'policies'
    ) INTO v_col_exists;

    IF v_col_exists THEN
        RAISE NOTICE 'Migrando hotels.policies → hotels_policies...';

        -- Caso 1: policies es un objeto JSON (dict de key→value)
        INSERT INTO hotels_policies (hotel_id, url_id, language, policy_name, policy_details)
        SELECT
            h.id    AS hotel_id,
            h.url_id AS url_id,
            h.language AS language,
            TRIM(kv.key)   AS policy_name,
            TRIM(kv.value #>> '{}') AS policy_details
        FROM hotels h
        CROSS JOIN LATERAL jsonb_each(
            CASE
                WHEN jsonb_typeof(h.policies) = 'object' THEN h.policies
                ELSE '{}'::jsonb
            END
        ) AS kv
        WHERE h.policies IS NOT NULL
          AND jsonb_typeof(h.policies) = 'object'
          AND TRIM(kv.key) <> ''
        ON CONFLICT (hotel_id, language, policy_name) DO NOTHING;

        GET DIAGNOSTICS v_migrated = ROW_COUNT;
        RAISE NOTICE 'Migración hotels_policies: % filas insertadas.', v_migrated;
        RAISE NOTICE 'ACCIÓN REQUERIDA: Verificar datos y luego ejecutar:';
        RAISE NOTICE '  ALTER TABLE hotels DROP COLUMN policies;';
    ELSE
        RAISE NOTICE 'Columna hotels.policies no existe — migración omitida.';
    END IF;
END $$;


-- =============================================================================
-- VISTAS AUXILIARES
-- =============================================================================

-- Vista: hotel completo con amenidades agregadas (array_agg)
CREATE OR REPLACE VIEW v_hotels_full AS
SELECT
    h.id,
    h.url_id,
    h.url,
    h.language,
    h.hotel_name,
    h.hotel_id_booking,
    h.city,
    h.country,
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
                'policy_name', pol.policy_name,
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
LEFT JOIN hotels_description hd
       ON hd.hotel_id = h.id AND hd.language = h.language
LEFT JOIN hotels_legal hl
       ON hl.hotel_id = h.id AND hl.language = h.language;

COMMENT ON VIEW v_hotels_full IS
    'Vista denormalizada de hotel con description, amenities, popular_services, policies y legal';


-- Vista: resumen de completitud de scraping
CREATE OR REPLACE VIEW v_scraping_summary AS
SELECT
    uq.id               AS url_id,
    uq.url,
    uq.external_ref,
    uq.status           AS queue_status,
    uq.retry_count,
    uq.scraped_at,
    COUNT(uls.id)       AS languages_tracked,
    SUM(CASE WHEN uls.status = 'done'  THEN 1 ELSE 0 END) AS languages_done,
    SUM(CASE WHEN uls.status = 'error' THEN 1 ELSE 0 END) AS languages_error,
    MAX(uls.attempts)   AS max_attempts
FROM url_queue uq
LEFT JOIN url_language_status uls ON uls.url_id = uq.id
GROUP BY uq.id, uq.url, uq.external_ref, uq.status, uq.retry_count, uq.scraped_at;

COMMENT ON VIEW v_scraping_summary IS 'Resumen de completitud de scraping por URL';


-- =============================================================================
-- CONSULTAS DE VALIDACIÓN POST-INSTALACIÓN
-- =============================================================================

-- Ejecutar tras la instalación para verificar que todas las tablas existen:
/*
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
      'url_queue', 'hotels', 'hotels_description',
      'hotels_amenities', 'hotels_policies', 'hotels_legal',
      'hotels_popular_services', 'url_language_status',
      'scraping_logs', 'image_downloads', 'image_data', 'system_metrics'
  )
ORDER BY table_name;

-- Verificar constraints
SELECT conname, contype, conrelid::regclass AS table_name
FROM pg_constraint
WHERE conrelid::regclass::text IN (
    'hotels_amenities', 'hotels_policies', 'hotels_legal', 'hotels_popular_services'
)
ORDER BY table_name, contype;

-- Verificar índices
SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN (
      'hotels_amenities', 'hotels_policies', 'hotels_legal', 'hotels_popular_services'
  )
ORDER BY tablename, indexname;
*/

-- =============================================================================
-- FIN DEL SCHEMA
-- =============================================================================
