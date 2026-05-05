-- =============================================================================
-- BookingScraper Pro — Schema Completo v6.0.0 build 99
-- PostgreSQL 14+ / Windows 11 Single-Node Deployment
-- =============================================================================
--
-- INSTRUCCIONES DE EJECUCIÓN (Windows 11):
--   psql -U postgres -d bookingscraper -f schema_v77_complete.sql
--
-- ADVERTENCIA: La base de datos se elimina y recrea en CADA arranque del sistema.
--   Este archivo genera una instalación SIEMPRE limpia. NUNCA es una migración.
--
-- =============================================================================
-- CHANGELOG
-- =============================================================================
--
-- v77 (Build 99):
--   BUG-SVC-DOM-001-FIX : Reordenacion de estrategias en extractor.py.
--                          Las estrategias DOM (1, 1.5, 2) son ahora PRIMARIAS.
--                          Apollo JSON movido a fallback (posicion 3).
--                          Sin cambios en el esquema SQL (DB siempre recreada).
--   IMPACT: hotels_all_services ahora contiene hasta 3-7x mas filas por hotel
--           (esperado para hoteles ricos como wild & bolz eMotel: 6 → ~45 items).
--   languages.json: 10 nuevos groupIds anadidos al facility_group_map (2,4,5,6,9,10,14,17,19,24).
--
-- v77 (Build 96):
--   BUG-HEADER-003-FIX : Cabecera actualizada de build 84 a build 96.
--   (Ver BUG_REPORT_Build96_EN.md para lista completa de cambios en esta versión.)
--
-- v77 (Build 84):
--   BUG-DOUBLE-COMMIT-001-FIX : scraper_service.py — session.commit() explícito
--                        eliminado de _persist_hotel_data(). El context manager
--                        get_db() ya ejecuta commit() al salir. Doble commit
--                        redundante: sin efecto en datos pero ineficiente.
--
--   BUG-API-MAIN-001-FIX : main.py — 5 tablas pobladas pero nunca consultadas
--                        en GET /hotels/{id}: hotels_fine_print, hotels_all_services,
--                        hotels_faqs, hotels_guest_reviews, hotels_property_highlights.
--                        Datos invisibles para consumidores de la API. Fix: imports
--                        añadidos, queries añadidas, campos añadidos al response dict.
--
--   BUG-API-MAIN-002-FIX : main.py — campo category_code ausente en la respuesta
--                        nearby_places de GET /hotels/{id}. El campo existe en el
--                        modelo y es escrito por _upsert_hotel_nearby_places() pero
--                        nunca se incluía en el dict de respuesta.
-- v77 (Build 80):
--   GAP-SCHEMA-002-FIX : hotels_room_types — columnas adults, children, images,
--                        info añadidas.  El ORM HotelRoomType tenia estos campos
--                        mapeados (desde v76 patch) pero la tabla SQL solo tenia
--                        id/hotel_id/url_id/language/room_name/description/
--                        facilities/created_at. Cada INSERT fallaba con
--                        UndefinedColumn bloqueando toda persistencia de rooms.
--
-- v77 (Build 79):
--   BUG-SCHEMA-002-FIX : hotels.accommodation_type — columna añadida.
--                        El ORM Hotel (models.py) tenia accommodation_type
--                        mapeada (GAP-EXTRACT-001-FIX, v76 patch) pero la
--                        columna NUNCA fue incluida en el schema SQL. Cada
--                        SELECT de SQLAlchemy fallaba con UndefinedColumn,
--                        bloqueando el 100% de los scrapes (14 URLs x 6 langs).
--                        Fix: columna VARCHAR(64) NULL añadida despues de
--                        rooms_quantity en la tabla hotels.
--
-- v77 (Build 78):
--   BUILD-82-FIX       : hotels_all_services — columna service_category VARCHAR(128) añadida.
--                        GAP-API-001: la API destino espera servicios categorizados
--                        {service_category, service}. La lista plana sin categoría
--                        impedía construir el payload correcto. La categoría se
--                        extrae del h3/heading del grupo facility-group de Booking.com.
--   BUILD-82-FIX       : hotels_nearby_places — columna category_code SMALLINT añadida.
--                        GAP-SCHEMA-003: la API espera category como INTEGER (código de
--                        ícono), pero el schema almacenaba solo texto ("airport").
--                        Mapa de conversión definido en extractor.py y scraper_service.py.
--                        Códigos: 1=airport 2=restaurant 3=beach 4=transport 5=nature 6=attraction
--   BUG-SCHEMA-001-FIX : hotels_individual_reviews — tabla creada.
--                        El modelo HotelIndividualReview existía en models.py
--                        (STRUCT-025, v76 patch) pero la tabla nunca fue
--                        incluida en el schema SQL. Al recrear la BD desde
--                        el SQL la tabla no se creaba → desincronización
--                        modelo/schema.  Añadida con PK BIGSERIAL, índices
--                        en hotel_id/language/score y CHECK score IN [0,10].
--
-- v76 (Build 76):
--   STRUCT-019 : hotels — columna price_range VARCHAR(64) añadida.
--   STRUCT-020 : hotels — columna rooms_quantity SMALLINT añadida.
--   STRUCT-021 : hotels_extra_info — nueva tabla.
--   STRUCT-022 : hotels_nearby_places — nueva tabla.
--   STRUCT-023 : hotels_room_types — nueva tabla normalizada.
--   STRUCT-024 : hotels_seo — nueva tabla.
--   REJECTED   : hotels_category_scores → DUPLICADO de hotels_guest_reviews.
--   REJECTED   : hotels_guest_qa → DUPLICADO de hotels_faqs.
--
-- v67 (Build 67):
--   BUG-SCRAPER-001-FIX : Sin cambios de esquema. Fix en scraper.py.
--
-- v65 (Build 65):
--   CLEANUP-AMENITIES   : hotels_amenities ELIMINADA del sistema completo.
--                         La tabla nunca produjo datos (0 filas en todos
--                         los ciclos). hotels_popular_services es la fuente
--                         canónica de servicios destacados.
--                         Tablas afectadas: eliminada hotels_amenities.
--                         Total tablas: 17 → 16.
--
-- v60 (Build 60):
--   BUG-DB-002-FIX  : scraper_service.py — _upsert_legal() refactorizado.
--                     SÍNTOMA: 4 URLs con 6/6 idiomas en hotels pero 0
--                              registros en hotels_legal (hoteles BR/UY).
--                     CAUSA:   llamada condicional silenciaba la ausencia
--                              de sección legal sin insertar registro ni log.
--                     FIX:     llamada SIEMPRE ejecutada. Nuevo campo
--                              has_legal_content distingue presencia/ausencia.
--   SCHEMA-002      : hotels_legal — columna has_legal_content añadida.
--                     BOOLEAN NOT NULL DEFAULT FALSE.
--                     TRUE  → bloque legal encontrado y extraído con contenido.
--                     FALSE → página procesada; Booking.com no publica esa
--                             sección para este hotel/idioma (mercados BR/UY).
--   MODEL-002       : models.py — HotelLegal.has_legal_content añadido.
--
-- v59 (Build 59):
--   FIX-FP-CONTENT-001   : extractor.py — _extract_fine_print() corregido.
--   FIX-PH-SELECTOR-001  : extractor.py — _extract_property_highlights() selector.
--   FIX-PH-STRUCTURE-001 : hotels_property_highlights — 2 columnas:
--                          highlight_category VARCHAR(256)
--                          highlight_detail   VARCHAR(512)
--
-- v57 (Build 57):
--   BUG-PH-NORMALIZATION-001: hotels_property_highlights normalizada.
--                             N filas/hotel/idioma, pk BIGSERIAL.
--
-- v56 (Build 56):
--   BUG-FAQ-ANSWERS      : hotels_faqs — columna answer añadida.
--
-- v53 (Build 53):
--   STRUCT-013 : hotels_fine_print — nueva tabla.
--   STRUCT-014 : hotels_all_services — nueva tabla.
--   STRUCT-015 : hotels_faqs — nueva tabla.
--   STRUCT-016 : hotels_guest_reviews — nueva tabla.
--   STRUCT-017 : hotels_property_highlights — nueva tabla.
--
-- v51 (Build 51):
--   STRUCT-006 : hotels_policies — nueva tabla.
--   STRUCT-007 : hotels_legal — nueva tabla.
--   STRUCT-008 : hotels_popular_services — nueva tabla.
--
-- =============================================================================
-- TABLAS (22 total — v77):
--   1.  url_queue                  — Cola de URLs con estado y prioridad
--   2.  hotels                     — Datos principales del hotel por idioma
--   3.  hotels_description         — Descripción larga (STRUCT-001)
--   4.  hotels_policies            — Políticas del alojamiento (STRUCT-006)
--   5.  hotels_legal               — Información legal (STRUCT-007)
--   6.  hotels_popular_services    — Servicios más populares (STRUCT-008)
--   7.  url_language_status        — Estado de scraping por URL/idioma
--   8.  scraping_logs              — Log particionado por mes (RANGE)
--   9.  image_downloads            — Tracking de descargas de imágenes
--  10.  image_data                 — Metadatos completos de fotos
--  11.  system_metrics             — Snapshots de salud del sistema
--  12.  hotels_fine_print          — Fine print HTML (STRUCT-013)
--  13.  hotels_all_services        — Todos los servicios del hotel (STRUCT-014)
--  14.  hotels_faqs                — Preguntas frecuentes (STRUCT-015)
--  15.  hotels_guest_reviews       — Valoraciones de huéspedes (STRUCT-016)
--  16.  hotels_property_highlights — Property Highlights (STRUCT-017)
--  17.  hotels_extra_info          — Información importante (STRUCT-021)
--  18.  hotels_nearby_places       — Lugares cercanos (STRUCT-022)
--  19.  hotels_room_types          — Tipos de habitación normalizados (STRUCT-023)
--  20.  hotels_seo                 — Meta tags SEO (STRUCT-024)
--  21.  hotels_individual_reviews  — Reseñas textuales individuales (BUG-SCHEMA-001-FIX v77)
-- (hotels.price_range + hotels.rooms_quantity: columnas en tabla hotels, no tablas nuevas)
--
-- VISTAS:
--   v_hotels_full      — Hotel completo denormalizado
--   v_scraping_summary — Resumen de completitud de scraping por URL
--
-- NOTA WINDOWS 11:
--   max_connections <= 100 (Desktop Heap limitation)
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
    id              UUID          NOT NULL DEFAULT gen_random_uuid(),
    url             VARCHAR(2048) NOT NULL,
    base_url        VARCHAR(2048) NOT NULL,
    external_ref    VARCHAR(64)   NULL,
    external_url    VARCHAR(2048) NULL,
    status          VARCHAR(32)   NOT NULL DEFAULT 'pending',
    priority        SMALLINT      NOT NULL DEFAULT 5,
    retry_count     SMALLINT      NOT NULL DEFAULT 0,
    max_retries     SMALLINT      NOT NULL DEFAULT 3,
    last_error      VARCHAR(2000) NULL,
    -- Strategy-E (v58): partial retry tracking — comma-separated language codes
    languages_completed VARCHAR(64) NULL DEFAULT '',
    languages_failed    VARCHAR(64) NULL DEFAULT '',
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    scraped_at      TIMESTAMPTZ   NULL,
    version_id      INTEGER       NOT NULL DEFAULT 1,

    CONSTRAINT pk_url_queue PRIMARY KEY (id),
    CONSTRAINT uq_url_queue_url UNIQUE (url),
    CONSTRAINT chk_url_queue_status CHECK (
        status IN ('pending','processing','done','error','skipped','incomplete')
    ),
    CONSTRAINT chk_url_queue_priority CHECK (
        priority BETWEEN 1 AND 10
    )
);

CREATE INDEX IF NOT EXISTS ix_url_queue_status_priority ON url_queue (status, priority);
CREATE INDEX IF NOT EXISTS ix_url_queue_created_at      ON url_queue (created_at);
CREATE INDEX IF NOT EXISTS ix_url_queue_external_ref    ON url_queue (external_ref);

COMMENT ON TABLE  url_queue IS 'Cola de URLs a scrapeear con estado y prioridad (Strategy-E, v58)';
COMMENT ON COLUMN url_queue.languages_completed IS 'CSV de idiomas scrapeados con éxito (Strategy-E, v58)';
COMMENT ON COLUMN url_queue.languages_failed    IS 'CSV de idiomas fallidos — para partial retry (Strategy-E, v58)';
COMMENT ON COLUMN url_queue.external_ref        IS 'ID numérico del CSV origen — 1ª columna';
COMMENT ON COLUMN url_queue.external_url        IS 'URL alternativa/externa del hotel — 3ª columna CSV (STRUCT-009, v52)';
COMMENT ON COLUMN url_queue.version_id          IS 'Optimistic locking counter';


-- =============================================================================
-- 2. HOTELS
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels (
    id                  UUID             NOT NULL DEFAULT gen_random_uuid(),
    url_id              UUID             NOT NULL,
    url                 VARCHAR(2048)    NOT NULL,
    language            VARCHAR(10)      NOT NULL,
    hotel_name          VARCHAR(512)     NULL,
    hotel_id_booking    VARCHAR(64)      NULL,
    address_city        TEXT             NULL,
    latitude            DOUBLE PRECISION NULL,
    longitude           DOUBLE PRECISION NULL,
    star_rating         DOUBLE PRECISION NULL,
    review_score        DOUBLE PRECISION NULL,
    review_count        INTEGER          NULL,
    main_image_url      VARCHAR(2048)    NULL,
    short_description   TEXT             NULL,
    rating_value        DOUBLE PRECISION NULL,
    best_rating         DOUBLE PRECISION NULL,
    street_address      VARCHAR(512)     NULL,
    address_locality    VARCHAR(256)     NULL,
    address_country     VARCHAR(128)     NULL,
    postal_code         VARCHAR(20)      NULL,
    room_types          JSONB            NULL DEFAULT '[]'::jsonb,
    raw_data            JSONB            NULL DEFAULT '{}'::jsonb,
    scrape_duration_s   DOUBLE PRECISION NULL,
    scrape_engine       VARCHAR(32)      NULL,
    created_at          TIMESTAMPTZ      NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ      NOT NULL DEFAULT NOW(),
    -- STRUCT-019 (v76): precio visible en sección de disponibilidad.
    -- NULL cuando la URL no incluye parámetros de fecha (página estática).
    price_range         VARCHAR(64)      NULL,
    -- STRUCT-020 (v76): número de tipos de habitación visibles en DOM.
    -- Fuente preferida: JSON-LD numberOfRooms. Fallback: count(room-block).
    -- No equivale al total de habitaciones físicas del hotel.
    rooms_quantity      SMALLINT         NULL,
    -- GAP-EXTRACT-001-FIX (v76 patch) / BUG-SCHEMA-002-FIX (v77):
    -- Tipo de alojamiento del JSON-LD @type (e.g. Hotel, Apartment, Villa).
    -- Esta columna existia en el ORM (models.py) pero FALTABA en el schema SQL,
    -- causando psycopg.errors.UndefinedColumn en TODOS los scrapes.
    accommodation_type  VARCHAR(64)      NULL,
    -- STRUCT-CITY-001 (Build 88): campos de metadatos urbanos extraídos de
    -- booking.env (script tag) con fallback a breadcrumb DOM.
    -- city_name: nombre de ciudad normalizado (ej. "Ohrid", "Manaus").
    -- dest_ufi : UFI de Booking.com, usado en parámetros de búsqueda.
    -- atnm_en  : tipo de alojamiento en inglés (ej. "guest_house", "hotel").
    city_name           VARCHAR(256)     NULL,
    dest_ufi            VARCHAR(64)      NULL,
    atnm_en             VARCHAR(64)      NULL,
    -- STRUCT-CITY-002 (Build 89): dest_id, region_name, district_name
    dest_id             VARCHAR(64)      NULL,
    region_name         VARCHAR(256)     NULL,
    district_name       VARCHAR(256)     NULL,
    version_id          INTEGER          NOT NULL DEFAULT 1,

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

CREATE INDEX IF NOT EXISTS ix_hotels_url_id           ON hotels (url_id);
CREATE INDEX IF NOT EXISTS ix_hotels_language          ON hotels (language);
CREATE INDEX IF NOT EXISTS ix_hotels_hotel_id_booking  ON hotels (hotel_id_booking);
CREATE INDEX IF NOT EXISTS ix_hotels_address_city      ON hotels (address_city);
CREATE INDEX IF NOT EXISTS ix_hotels_created_at        ON hotels (created_at);
CREATE INDEX IF NOT EXISTS ix_hotels_dest_id           ON hotels (dest_id);
CREATE INDEX IF NOT EXISTS ix_hotels_region_name       ON hotels (region_name);
CREATE INDEX IF NOT EXISTS ix_hotels_district_name     ON hotels (district_name);

COMMENT ON TABLE  hotels IS 'Datos principales del hotel por idioma';
COMMENT ON COLUMN hotels.star_rating    IS 'Estrellas normalizadas 0-5 (valor raw Booking.com / 2)';
COMMENT ON COLUMN hotels.review_count   IS 'aggregateRating.reviewCount de JSON-LD';
COMMENT ON COLUMN hotels.address_city   IS 'Ciudad/región del hotel — fuente: addressRegion JSON-LD o breadcrumb (STRUCT-011, v52)';
COMMENT ON COLUMN hotels.address_country IS 'Código/nombre de país — fuente: addressCountry JSON-LD (STRUCT-012, v52)';
COMMENT ON COLUMN hotels.city_name   IS 'Nombre de ciudad normalizado — fuente: booking.env script tag (b_city_name) o breadcrumb DOM (STRUCT-CITY-001, Build 88)';
COMMENT ON COLUMN hotels.dest_ufi    IS 'Booking.com UFI — fuente: booking.env script tag (b_ufi) (STRUCT-CITY-001, Build 88)';
COMMENT ON COLUMN hotels.atnm_en     IS 'Tipo alojamiento en inglés — JS atnm_en (sin prefijo b_). Regex corregida Build 89 (STRUCT-CITY-001/Build 88, BUG-ENV-REGEX-001-FIX/Build 89)';
COMMENT ON COLUMN hotels.dest_id     IS 'Booking.com destination ID — JS context_dest_id (STRUCT-CITY-002, Build 89)';
COMMENT ON COLUMN hotels.region_name IS 'Región/Estado — breadcrumb items[3] cuando NO genérico (STRUCT-CITY-002, Build 89)';
COMMENT ON COLUMN hotels.district_name IS 'Distrito — breadcrumb items[5] cuando n==7 y NO genérico (STRUCT-CITY-002, Build 89)';


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
    CONSTRAINT fk_hdesc_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hdesc_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hdesc_url_lang UNIQUE (url_id, language)
);

CREATE INDEX IF NOT EXISTS ix_hdesc_hotel_id ON hotels_description (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hdesc_language  ON hotels_description (language);

COMMENT ON TABLE hotels_description IS
    'Descripción larga del hotel por idioma — separada de hotels para reducir tamaño de fila (STRUCT-001)';


-- =============================================================================
-- 4. HOTELS_POLICIES (STRUCT-006, v51)
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
    CONSTRAINT fk_hpolicy_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hpolicy_url   FOREIGN KEY (url_id)
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
-- 5. HOTELS_LEGAL (STRUCT-007, v51 / BUG-DB-002-FIX, v60)
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels_legal (
    id                  BIGSERIAL    NOT NULL,
    hotel_id            UUID         NOT NULL,
    url_id              UUID         NOT NULL,
    language            VARCHAR(10)  NOT NULL,
    legal               VARCHAR(256) NULL,
    legal_info          TEXT         NULL,
    legal_details       TEXT         NULL,
    -- BUG-DB-002-FIX (v60): campo diagnóstico.
    -- TRUE  → bloque legal encontrado y extraído con contenido real.
    -- FALSE → página procesada; Booking.com no publica sección legal
    --         para este hotel/idioma (mercados BR, UY, etc.).
    -- Antes de v60: ausencia de sección legal producía 0 registros (fallo silencioso).
    -- Desde v60: siempre existe 1 registro por hotel/idioma (inserción incondicional).
    has_legal_content   BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_legal PRIMARY KEY (id),
    CONSTRAINT fk_hlegal_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hlegal_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hlegal_hotel_lang UNIQUE (hotel_id, language)
);

CREATE INDEX IF NOT EXISTS ix_hlegal_hotel_id   ON hotels_legal (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hlegal_language    ON hotels_legal (language);
CREATE INDEX IF NOT EXISTS ix_hlegal_has_content ON hotels_legal (has_legal_content);

COMMENT ON TABLE  hotels_legal IS
    'Información legal del alojamiento por idioma (STRUCT-007, v51). BUG-DB-002-FIX v60: inserción incondicional con has_legal_content.';
COMMENT ON COLUMN hotels_legal.legal IS
    'Título del bloque legal (e.g. ''Información legal'' / ''Legal information'')';
COMMENT ON COLUMN hotels_legal.legal_info IS
    'Texto introductorio del bloque legal (quién gestiona el alojamiento)';
COMMENT ON COLUMN hotels_legal.legal_details IS
    'Detalles extendidos (normalmente vacío en Booking.com)';
COMMENT ON COLUMN hotels_legal.has_legal_content IS
    'TRUE=bloque legal encontrado con contenido real. FALSE=página procesada sin sección legal (BUG-DB-002-FIX v60)';


-- =============================================================================
-- 6. HOTELS_POPULAR_SERVICES (STRUCT-008, v51)
-- =============================================================================
-- Fuente canónica de servicios destacados desde Build 65 (hotels_amenities eliminada).

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
    CONSTRAINT uq_hpopservice_hotel_lang_service
        UNIQUE (hotel_id, language, popular_service)
);

CREATE INDEX IF NOT EXISTS ix_hpopservice_hotel_id ON hotels_popular_services (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hpopservice_language  ON hotels_popular_services (language);
CREATE INDEX IF NOT EXISTS ix_hpopservice_service   ON hotels_popular_services (popular_service);

COMMENT ON TABLE  hotels_popular_services IS
    'Servicios más populares del hotel — selección editorial de Booking.com. Fuente canónica desde Build 65 (STRUCT-008, v51)';
COMMENT ON COLUMN hotels_popular_services.popular_service IS
    'Nombre del servicio popular (e.g. ''WiFi gratis'', ''Piscina al aire libre'')';


-- =============================================================================
-- 7. URL_LANGUAGE_STATUS
-- =============================================================================

CREATE TABLE IF NOT EXISTS url_language_status (
    id          UUID          NOT NULL DEFAULT gen_random_uuid(),
    url_id      UUID          NOT NULL,
    language    VARCHAR(10)   NOT NULL,
    status      VARCHAR(32)   NOT NULL DEFAULT 'pending',
    attempts    SMALLINT      NOT NULL DEFAULT 0,
    last_error  VARCHAR(2000) NULL,
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_url_language_status PRIMARY KEY (id),
    CONSTRAINT fk_uls_url FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_uls_url_lang UNIQUE (url_id, language),
    CONSTRAINT chk_uls_status_valid CHECK (
        status IN ('pending','processing','done','error','skipped','incomplete')
    )
);

CREATE INDEX IF NOT EXISTS ix_uls_url_id ON url_language_status (url_id);
CREATE INDEX IF NOT EXISTS ix_uls_status  ON url_language_status (status);

COMMENT ON TABLE url_language_status IS
    'Tracking de completitud de scraping por URL y lenguaje';


-- =============================================================================
-- 8. SCRAPING_LOGS (PARTITIONED BY RANGE — por mes)
-- =============================================================================
-- PostgreSQL NO soporta FK constraints en tablas particionadas (BUG-003/103).
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

-- Particiones 2027
CREATE TABLE IF NOT EXISTS scraping_logs_2027_01 PARTITION OF scraping_logs FOR VALUES FROM ('2027-01-01') TO ('2027-02-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_02 PARTITION OF scraping_logs FOR VALUES FROM ('2027-02-01') TO ('2027-03-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_03 PARTITION OF scraping_logs FOR VALUES FROM ('2027-03-01') TO ('2027-04-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_04 PARTITION OF scraping_logs FOR VALUES FROM ('2027-04-01') TO ('2027-05-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_05 PARTITION OF scraping_logs FOR VALUES FROM ('2027-05-01') TO ('2027-06-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_06 PARTITION OF scraping_logs FOR VALUES FROM ('2027-06-01') TO ('2027-07-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_07 PARTITION OF scraping_logs FOR VALUES FROM ('2027-07-01') TO ('2027-08-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_08 PARTITION OF scraping_logs FOR VALUES FROM ('2027-08-01') TO ('2027-09-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_09 PARTITION OF scraping_logs FOR VALUES FROM ('2027-09-01') TO ('2027-10-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_10 PARTITION OF scraping_logs FOR VALUES FROM ('2027-10-01') TO ('2027-11-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_11 PARTITION OF scraping_logs FOR VALUES FROM ('2027-11-01') TO ('2027-12-01');
CREATE TABLE IF NOT EXISTS scraping_logs_2027_12 PARTITION OF scraping_logs FOR VALUES FROM ('2027-12-01') TO ('2028-01-01');

-- Partición DEFAULT para fechas fuera de rango preconfigurado
CREATE TABLE IF NOT EXISTS scraping_logs_default PARTITION OF scraping_logs DEFAULT;

COMMENT ON TABLE scraping_logs IS
    'Log particionado por mes de eventos de scraping. FK via trigger (BUG-003/103)';

-- Trigger FK check (sustituto de FK nativa no soportada en tablas particionadas)
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
-- 9. IMAGE_DOWNLOADS
-- =============================================================================

CREATE TABLE IF NOT EXISTS image_downloads (
    id              UUID          NOT NULL DEFAULT gen_random_uuid(),
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
COMMENT ON COLUMN image_downloads.id_photo  IS 'Booking.com photo ID (e.g. ''49312038'')';
COMMENT ON COLUMN image_downloads.category  IS 'Variante de tamaño: thumb_url | large_url | highres_url';


-- =============================================================================
-- 10. IMAGE_DATA
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
COMMENT ON COLUMN image_data.id_photo        IS 'Booking.com photo ID — globalmente único';
COMMENT ON COLUMN image_data.created_at_photo IS 'Timestamp de creación de la foto en Booking.com';


-- =============================================================================
-- 11. SYSTEM_METRICS
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

CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_at  ON system_metrics (recorded_at);
CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_cpu ON system_metrics (recorded_at, cpu_usage);
CREATE INDEX IF NOT EXISTS ix_sysmetrics_recorded_mem ON system_metrics (recorded_at, memory_usage);

COMMENT ON TABLE system_metrics IS 'Snapshots periódicos de salud del sistema';


-- =============================================================================
-- 12. HOTELS_FINE_PRINT (STRUCT-013, v53)
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels_fine_print (
    id          UUID        NOT NULL DEFAULT gen_random_uuid(),
    hotel_id    UUID        NOT NULL,
    url_id      UUID        NOT NULL,
    language    VARCHAR(10) NOT NULL,
    -- HTML sanitizado: etiquetas <p> preservadas, SVG/img/atributos eliminados.
    fp          TEXT        NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_fine_print PRIMARY KEY (id),
    CONSTRAINT fk_hfp_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hfp_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hfp_url_lang UNIQUE (url_id, language)
);

CREATE INDEX IF NOT EXISTS ix_hfp_hotel_id ON hotels_fine_print (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hfp_language  ON hotels_fine_print (language);

COMMENT ON TABLE  hotels_fine_print IS
    'Bloque Fine Print del hotel por idioma — HTML sanitizado con <p> preservados (STRUCT-013, v53)';
COMMENT ON COLUMN hotels_fine_print.fp IS
    'HTML sanitizado del bloque Fine Print. <p> preservados, SVG/img eliminados, atributos eliminados';


-- =============================================================================
-- 13. HOTELS_ALL_SERVICES (STRUCT-014, v53)
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels_all_services (
    id               BIGSERIAL    NOT NULL,
    hotel_id         UUID         NOT NULL,
    url_id           UUID         NOT NULL,
    language         VARCHAR(10)  NOT NULL,
    service          VARCHAR(512) NOT NULL,
    -- BUILD-82-FIX (GAP-API-001): categoría del grupo de servicios de Booking.com.
    -- Extraída del heading (h3/div) del bloque facility-group.
    -- Ejemplos: "Internet", "Parking", "Outdoor swimming pool", "Pets".
    -- NULL cuando la estrategia de extracción no proporciona contexto de grupo
    -- (Apollo JSON cache, popular-wrapper fallback).
    service_category VARCHAR(128) NULL,
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_all_services PRIMARY KEY (id),
    CONSTRAINT fk_hallsvc_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hallsvc_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hallsvc_hotel_lang_service UNIQUE (hotel_id, language, service)
);

CREATE INDEX IF NOT EXISTS ix_hallsvc_hotel_id ON hotels_all_services (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hallsvc_language  ON hotels_all_services (language);
CREATE INDEX IF NOT EXISTS ix_hallsvc_service   ON hotels_all_services (service);

COMMENT ON TABLE  hotels_all_services IS
    'Todos los servicios/instalaciones del hotel — una fila por servicio (STRUCT-014, v53 / BUILD-82-FIX)';
COMMENT ON COLUMN hotels_all_services.service IS
    'Texto del servicio o instalación (e.g. ''Piscina al aire libre'', ''WiFi gratis'')';
COMMENT ON COLUMN hotels_all_services.service_category IS
    'Grupo de servicios de Booking.com (e.g. ''Internet'', ''Parking'', ''Pool''). NULL si la estrategia no aporta categoría.';


-- =============================================================================
-- 14. HOTELS_FAQS (STRUCT-015, v53)
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels_faqs (
    id          BIGSERIAL   NOT NULL,
    hotel_id    UUID        NOT NULL,
    url_id      UUID        NOT NULL,
    language    VARCHAR(10) NOT NULL,
    ask         TEXT        NOT NULL,
    -- BUG-FAQ-ANSWERS (v56): respuesta extraída del accordion de Booking.com
    answer      TEXT        NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_faqs PRIMARY KEY (id),
    CONSTRAINT fk_hfaq_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hfaq_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hfaq_hotel_lang_ask UNIQUE (hotel_id, language, ask)
);

CREATE INDEX IF NOT EXISTS ix_hfaq_hotel_id ON hotels_faqs (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hfaq_language  ON hotels_faqs (language);

COMMENT ON TABLE  hotels_faqs IS
    'Preguntas frecuentes del hotel — una fila por pregunta (STRUCT-015, v53). BUG-FAQ-ANSWERS (v56): columna answer añadida.';
COMMENT ON COLUMN hotels_faqs.ask IS
    'Texto de la pregunta frecuente (e.g. ''¿Cuál es el horario de check-in?'')';
COMMENT ON COLUMN hotels_faqs.answer IS
    'Texto de la respuesta (extraído del accordion. NULL si no disponible en DOM)';


-- =============================================================================
-- 15. HOTELS_GUEST_REVIEWS (STRUCT-016, v53)
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels_guest_reviews (
    id                  BIGSERIAL    NOT NULL,
    hotel_id            UUID         NOT NULL,
    url_id              UUID         NOT NULL,
    language            VARCHAR(10)  NOT NULL,
    reviews_categories  VARCHAR(256) NOT NULL,
    reviews_score       TEXT         NULL,
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_guest_reviews PRIMARY KEY (id),
    CONSTRAINT fk_hgrev_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hgrev_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hgrev_hotel_lang_cat UNIQUE (hotel_id, language, reviews_categories)
);

CREATE INDEX IF NOT EXISTS ix_hgrev_hotel_id   ON hotels_guest_reviews (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hgrev_language    ON hotels_guest_reviews (language);
CREATE INDEX IF NOT EXISTS ix_hgrev_categories  ON hotels_guest_reviews (reviews_categories);

COMMENT ON TABLE  hotels_guest_reviews IS
    'Categorías de valoración de huéspedes con puntuación — una fila por categoría (STRUCT-016, v53)';
COMMENT ON COLUMN hotels_guest_reviews.reviews_categories IS
    'Categoría de valoración (e.g. ''Limpieza'', ''Confort'', ''Ubicación'', ''Personal'')';
COMMENT ON COLUMN hotels_guest_reviews.reviews_score IS
    'Puntuación de la categoría (valor textual, e.g. ''9.5'', ''8.8'')';


-- =============================================================================
-- 16. HOTELS_PROPERTY_HIGHLIGHTS (STRUCT-017, v53)
-- =============================================================================
-- Estructura categoría/detalle desde FIX-PH-STRUCTURE-001 (v59):
--   highlight_category — nombre del grupo (e.g. "Ideal para tu estancia")
--   highlight_detail   — ítem individual del grupo (e.g. "Baño privado")

CREATE TABLE IF NOT EXISTS hotels_property_highlights (
    id                 BIGSERIAL    NOT NULL,
    hotel_id           UUID         NOT NULL,
    url_id             UUID         NOT NULL,
    language           VARCHAR(10)  NOT NULL,
    highlight_category VARCHAR(256) NOT NULL DEFAULT '',
    highlight_detail   VARCHAR(512) NOT NULL,
    created_at         TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_property_highlights PRIMARY KEY (id),
    CONSTRAINT fk_hph_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hph_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hph_hotel_lang_cat_detail
        UNIQUE (hotel_id, language, highlight_category, highlight_detail)
);

CREATE INDEX IF NOT EXISTS ix_hph_hotel_id  ON hotels_property_highlights (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hph_language   ON hotels_property_highlights (language);
CREATE INDEX IF NOT EXISTS ix_hph_url_id     ON hotels_property_highlights (url_id);
CREATE INDEX IF NOT EXISTS ix_hph_category   ON hotels_property_highlights (highlight_category);

COMMENT ON TABLE  hotels_property_highlights IS
    'Highlights de propiedad con estructura categoría/detalle: 1 registro por par (categoría, ítem) por hotel/idioma (FIX-PH-STRUCTURE-001, v59)';
COMMENT ON COLUMN hotels_property_highlights.highlight_category IS
    'Nombre del grupo de highlight (e.g. "Ideal para tu estancia")';
COMMENT ON COLUMN hotels_property_highlights.highlight_detail IS
    'Ítem individual del grupo (e.g. "Baño privado", "Parking", "WiFi gratis")';




-- =============================================================================
-- 17. HOTELS_EXTRA_INFO (STRUCT-021, v76)
-- =============================================================================
-- Información importante del alojamiento ("Good to know" / "Información importante").
-- Distinta del bloque Fine Print (hotels_fine_print): este es el bloque
-- data-testid="property-important-info" que aparece antes del Fine Print.

CREATE TABLE IF NOT EXISTS hotels_extra_info (
    id          UUID        NOT NULL DEFAULT gen_random_uuid(),
    hotel_id    UUID        NOT NULL,
    url_id      UUID        NOT NULL,
    language    VARCHAR(10) NOT NULL,
    extra_info  TEXT        NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_extra_info PRIMARY KEY (id),
    CONSTRAINT fk_hei_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hei_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hei_url_lang UNIQUE (url_id, language)
);

CREATE INDEX IF NOT EXISTS ix_hei_hotel_id ON hotels_extra_info (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hei_language  ON hotels_extra_info (language);

COMMENT ON TABLE  hotels_extra_info IS
    'Información importante del alojamiento — bloque property-important-info de Booking.com (STRUCT-021, v76)';
COMMENT ON COLUMN hotels_extra_info.extra_info IS
    'Texto del bloque "Good to know" / "Información importante". Distinto de Fine Print.';


-- =============================================================================
-- 18. HOTELS_NEARBY_PLACES (STRUCT-022, v76)
-- =============================================================================
-- Lugares de interés cercanos al hotel — bloque location-highlight de Booking.com.
-- Incluye: nombre del lugar, distancia aproximada y categoría del ícono.

CREATE TABLE IF NOT EXISTS hotels_nearby_places (
    id            BIGSERIAL    NOT NULL,
    hotel_id      UUID         NOT NULL,
    url_id        UUID         NOT NULL,
    language      VARCHAR(10)  NOT NULL,
    place_name    VARCHAR(256) NOT NULL,
    distance      VARCHAR(64)  NULL,
    category      VARCHAR(128) NULL,
    -- BUILD-82-FIX (GAP-SCHEMA-003): código numérico de categoría requerido por la API.
    -- La API destino espera category como INTEGER, no como texto.
    -- Mapa de conversión: 1=airport 2=restaurant 3=beach 4=transport 5=nature 6=attraction
    -- NULL si la categoría de texto no tiene correspondencia en el mapa.
    category_code SMALLINT     NULL,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_nearby_places PRIMARY KEY (id),
    CONSTRAINT fk_hnp_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hnp_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hnp_hotel_lang_place UNIQUE (hotel_id, language, place_name),
    CONSTRAINT chk_hnp_category_code CHECK (
        category_code IS NULL OR category_code BETWEEN 1 AND 99
    )
);

CREATE INDEX IF NOT EXISTS ix_hnp_hotel_id  ON hotels_nearby_places (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hnp_language   ON hotels_nearby_places (language);
CREATE INDEX IF NOT EXISTS ix_hnp_place_name ON hotels_nearby_places (place_name);

COMMENT ON TABLE  hotels_nearby_places IS
    'Lugares de interés cercanos — bloque location-highlight de Booking.com (STRUCT-022, v76 / BUILD-82-FIX)';
COMMENT ON COLUMN hotels_nearby_places.place_name IS
    'Nombre del lugar (e.g. "Aeropuerto Internacional", "Centro histórico")';
COMMENT ON COLUMN hotels_nearby_places.distance IS
    'Distancia textual tal como aparece en Booking.com (e.g. "2.1 km", "500 m")';
COMMENT ON COLUMN hotels_nearby_places.category IS
    'Categoría del ícono de Booking.com — texto (e.g. "airport", "restaurant", "beach")';
COMMENT ON COLUMN hotels_nearby_places.category_code IS
    'Código numérico de categoría para la API destino: 1=airport 2=restaurant 3=beach 4=transport 5=nature 6=attraction';


-- =============================================================================
-- 19. HOTELS_ROOM_TYPES (STRUCT-023, v76)
-- =============================================================================
-- Tabla normalizada de tipos de habitación — complemento a hotels.room_types (JSONB).
-- Permite queries SQL directas sobre room_name, description, facilities.
-- La columna JSONB hotels.room_types se mantiene para compatibilidad y acceso rápido.

CREATE TABLE IF NOT EXISTS hotels_room_types (
    id          BIGSERIAL    NOT NULL,
    hotel_id    UUID         NOT NULL,
    url_id      UUID         NOT NULL,
    language    VARCHAR(10)  NOT NULL,
    room_name   VARCHAR(256) NOT NULL,
    description TEXT         NULL,
    facilities  JSONB        NULL DEFAULT '[]'::jsonb,
    -- GAP-SCHEMA-002-FIX (Build 80): columnas requeridas por _API_.md rooms[]:
    --   adults   — ocupacion maxima adultos (NULL si DOM no cargó tabla de disponibilidad)
    --   children — ocupacion maxima niños (NULL si DOM no cargó tabla de disponibilidad)
    --   images   — URLs de imagenes de la habitacion (JSONB array de strings)
    --   info     — informacion adicional (nullable en _API_.md)
    adults      SMALLINT     NULL,
    children    SMALLINT     NULL,
    images      JSONB        NULL DEFAULT '[]'::jsonb,
    info        TEXT         NULL,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_room_types PRIMARY KEY (id),
    CONSTRAINT fk_hrt_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hrt_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hrt_hotel_lang_name UNIQUE (hotel_id, language, room_name)
);

CREATE INDEX IF NOT EXISTS ix_hrt_hotel_id  ON hotels_room_types (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hrt_language   ON hotels_room_types (language);
CREATE INDEX IF NOT EXISTS ix_hrt_room_name  ON hotels_room_types (room_name);
CREATE INDEX IF NOT EXISTS ix_hrt_facilities ON hotels_room_types USING GIN (facilities);
CREATE INDEX IF NOT EXISTS ix_hrt_images     ON hotels_room_types USING GIN (images);

COMMENT ON TABLE  hotels_room_types IS
    'Tipos de habitacion normalizados — complemento a hotels.room_types JSONB (STRUCT-023, v76 / GAP-SCHEMA-002-FIX Build 80)';
COMMENT ON COLUMN hotels_room_types.room_name IS
    'Nombre del tipo de habitacion (e.g. Deluxe Double Room, Superior Suite)';
COMMENT ON COLUMN hotels_room_types.facilities IS
    'Lista JSON de facilidades de la habitacion (e.g. [WiFi gratis, TV])';
COMMENT ON COLUMN hotels_room_types.adults IS
    'Ocupacion maxima adultos segun icono SVG de Booking.com. NULL si la tabla de disponibilidad no cargo.';
COMMENT ON COLUMN hotels_room_types.children IS
    'Ocupacion maxima ninos segun icono SVG de Booking.com. NULL si la tabla de disponibilidad no cargo.';
COMMENT ON COLUMN hotels_room_types.images IS
    'URLs de imagenes de la habitacion — JSONB array de strings (campo images de _API_.md rooms[])';
COMMENT ON COLUMN hotels_room_types.info IS
    'Informacion adicional de la habitacion, nullable en _API_.md';


-- =============================================================================
-- 20. HOTELS_SEO (STRUCT-024, v76)
-- =============================================================================
-- Meta tags SEO extraídos del <head> de la página de Booking.com.
-- Incluye meta description y meta keywords por idioma.

CREATE TABLE IF NOT EXISTS hotels_seo (
    id              UUID        NOT NULL DEFAULT gen_random_uuid(),
    hotel_id        UUID        NOT NULL,
    url_id          UUID        NOT NULL,
    language        VARCHAR(10) NOT NULL,
    seo_description TEXT        NULL,
    keywords        TEXT        NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_seo PRIMARY KEY (id),
    CONSTRAINT fk_hseo_hotel FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hseo_url   FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_hseo_url_lang UNIQUE (url_id, language)
);

CREATE INDEX IF NOT EXISTS ix_hseo_hotel_id ON hotels_seo (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hseo_language  ON hotels_seo (language);

COMMENT ON TABLE  hotels_seo IS
    'Meta tags SEO de la página del hotel — description y keywords por idioma (STRUCT-024, v76)';
COMMENT ON COLUMN hotels_seo.seo_description IS
    'Contenido de <meta name="description"> o <meta property="og:description">';
COMMENT ON COLUMN hotels_seo.keywords IS
    'Contenido de <meta name="keywords"> o <meta property="og:keywords">';


-- =============================================================================
-- 21. HOTELS_INDIVIDUAL_REVIEWS (BUG-SCHEMA-001-FIX, v77 / Build 78)
-- =============================================================================
-- Reseñas textuales individuales de huéspedes.
--
-- DIFERENCIA CON hotels_guest_reviews:
--   hotels_guest_reviews   → puntuaciones por categoría (Limpieza: 9.3, etc.)
--   hotels_individual_reviews → texto completo de cada reseña individual
--                               (nombre, país, título, comentario +/-, score propio)
--
-- BUG-SCHEMA-001-FIX (v77):
--   El modelo SQLAlchemy HotelIndividualReview existía en models.py
--   (STRUCT-025, etiquetado como v76 patch 2026-04-04) pero esta tabla
--   NUNCA fue incluida en el archivo schema SQL correspondiente.
--   Al recrear la BD desde el SQL en cada arranque, la tabla no se creaba
--   → desincronización modelo/schema → error potencial si el persister
--   intentase escribir en ella.
--   Fix: tabla añadida aquí con estructura idéntica al modelo ORM.
--
-- NOTA DE IMPLEMENTACIÓN (IMPL-001):
--   A la fecha del Build 78, no existe _extract_individual_reviews() en
--   extractor.py ni _upsert_hotel_individual_reviews() en scraper_service.py.
--   Las reseñas individuales requieren navegación Selenium separada a la URL
--   de reseñas (/reviews/hotel/...) o apertura del modal "Read all reviews".
--   La tabla se crea aquí para garantizar la consistencia schema/modelo;
--   la implementación del extractor es trabajo pendiente (Build 79+).
-- =============================================================================

CREATE TABLE IF NOT EXISTS hotels_individual_reviews (
    id              BIGSERIAL   NOT NULL,
    hotel_id        UUID        NOT NULL,
    url_id          UUID        NOT NULL,
    language        VARCHAR(10) NOT NULL,
    reviewer_name   VARCHAR(128) NULL,
    score           FLOAT       NULL,
    title           TEXT        NULL,
    positive_comment TEXT       NULL,
    negative_comment TEXT       NULL,
    reviewer_country VARCHAR(128) NULL,
    booking_id      VARCHAR(64) NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_hotels_individual_reviews PRIMARY KEY (id),
    CONSTRAINT fk_hir_hotel  FOREIGN KEY (hotel_id)
        REFERENCES hotels (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hir_url    FOREIGN KEY (url_id)
        REFERENCES url_queue (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_hir_score CHECK (score IS NULL OR score BETWEEN 0 AND 10)
);

CREATE INDEX IF NOT EXISTS ix_hir_hotel_id ON hotels_individual_reviews (hotel_id);
CREATE INDEX IF NOT EXISTS ix_hir_language  ON hotels_individual_reviews (language);
CREATE INDEX IF NOT EXISTS ix_hir_score     ON hotels_individual_reviews (score);

COMMENT ON TABLE  hotels_individual_reviews IS
    'Reseñas textuales individuales de huéspedes — distinto de hotels_guest_reviews (puntuaciones por categoría). BUG-SCHEMA-001-FIX v77.';
COMMENT ON COLUMN hotels_individual_reviews.reviewer_name IS
    'Nombre público del huésped según Booking.com';
COMMENT ON COLUMN hotels_individual_reviews.score IS
    'Puntuación individual de la reseña en escala 0-10';
COMMENT ON COLUMN hotels_individual_reviews.positive_comment IS
    'Texto positivo (campo "Liked" de Booking.com)';
COMMENT ON COLUMN hotels_individual_reviews.negative_comment IS
    'Texto negativo (campo "Disliked" de Booking.com)';
COMMENT ON COLUMN hotels_individual_reviews.booking_id IS
    'ID interno de Booking.com para la reseña, si está disponible en el DOM';


-- =============================================================================
-- TRIGGERS: updated_at automático
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

CREATE OR REPLACE TRIGGER trg_hotels_fine_print_updated_at
    BEFORE UPDATE ON hotels_fine_print
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE OR REPLACE TRIGGER trg_hotels_extra_info_updated_at
    BEFORE UPDATE ON hotels_extra_info
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

CREATE OR REPLACE TRIGGER trg_hotels_seo_updated_at
    BEFORE UPDATE ON hotels_seo
    FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at();

-- hotels_property_highlights no tiene updated_at (filas inmutables).
-- BUG-PH-NORMALIZATION-001 FIX (v57): trigger updated_at eliminado para esa tabla.


-- =============================================================================
-- VISTAS
-- =============================================================================

-- Vista principal: hotel completo con datos denormalizados de todas las tablas satélite
CREATE OR REPLACE VIEW v_hotels_full AS
SELECT
    h.id,
    h.url_id,
    h.url,
    h.language,
    h.hotel_name,
    h.hotel_id_booking,
    h.address_city,
    h.city_name,
    h.dest_ufi,
    h.atnm_en,
    h.dest_id,
    h.region_name,
    h.district_name,
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
    uq.external_ref,
    uq.external_url,
    -- Descripción larga
    hd.description,
    -- Fine print HTML (STRUCT-013, v53)
    hfp.fp,
    -- Property highlights como JSONB array con pares {category, detail} (FIX-PH-STRUCTURE-001, v59)
    COALESCE(
        (SELECT jsonb_agg(
            jsonb_build_object(
                'category', hph2.highlight_category,
                'detail',   hph2.highlight_detail
            ) ORDER BY hph2.id
         )
         FROM hotels_property_highlights hph2
         WHERE hph2.hotel_id = h.id AND hph2.language = h.language),
        '[]'::jsonb
    ) AS highlights,
    -- Servicios populares como array (fuente canónica desde Build 65)
    COALESCE(
        (SELECT array_agg(p.popular_service ORDER BY p.id)
         FROM hotels_popular_services p
         WHERE p.hotel_id = h.id AND p.language = h.language),
        ARRAY[]::TEXT[]
    ) AS popular_services,
    -- Todos los servicios como array (STRUCT-014, v53)
    COALESCE(
        (SELECT array_agg(s.service ORDER BY s.id)
         FROM hotels_all_services s
         WHERE s.hotel_id = h.id AND s.language = h.language),
        ARRAY[]::TEXT[]
    ) AS all_services,
    -- FAQs como array de preguntas (STRUCT-015, v53)
    COALESCE(
        (SELECT array_agg(f.ask ORDER BY f.id)
         FROM hotels_faqs f
         WHERE f.hotel_id = h.id AND f.language = h.language),
        ARRAY[]::TEXT[]
    ) AS faqs,
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
    -- Reseñas de huéspedes como JSON array (STRUCT-016, v53)
    COALESCE(
        (SELECT jsonb_agg(
            jsonb_build_object(
                'reviews_categories', gr.reviews_categories,
                'reviews_score',      gr.reviews_score
            ) ORDER BY gr.id
        )
         FROM hotels_guest_reviews gr
         WHERE gr.hotel_id = h.id AND gr.language = h.language),
        '[]'::jsonb
    ) AS guest_reviews,
    -- Legal con campo diagnóstico has_legal_content (BUG-DB-002-FIX v60)
    jsonb_build_object(
        'legal',             hl.legal,
        'legal_info',        hl.legal_info,
        'legal_details',     hl.legal_details,
        'has_legal_content', hl.has_legal_content
    ) AS legal,
    -- price_range, rooms_quantity, accommodation_type (STRUCT-019/020/GAP-EXTRACT-001-FIX, v76/v77)
    h.price_range,
    h.rooms_quantity,
    h.accommodation_type,
    -- Extra info (STRUCT-021, v76)
    hei.extra_info,
    -- SEO (STRUCT-024, v76)
    hseo.seo_description,
    hseo.keywords,
    -- Nearby places como JSON array (STRUCT-022, v76)
    COALESCE(
        (SELECT jsonb_agg(
            jsonb_build_object(
                'place_name',    hnp.place_name,
                'distance',      hnp.distance,
                'category',      hnp.category,
                -- BUG-VIEW-004-FIX (Build 86): category_code was missing from the view.
                -- The column exists in hotels_nearby_places and is populated by the scraper
                -- but was omitted here, making it invisible to v_hotels_full consumers.
                'category_code', hnp.category_code
            ) ORDER BY hnp.id
         )
         FROM hotels_nearby_places hnp
         WHERE hnp.hotel_id = h.id AND hnp.language = h.language),
        '[]'::jsonb
    ) AS nearby_places,
    -- Room types normalizados como JSON array (STRUCT-023, v76)
    COALESCE(
        (SELECT jsonb_agg(
            jsonb_build_object(
                'room_name',   hrt.room_name,
                'description', hrt.description,
                'facilities',  hrt.facilities,
                -- BUG-VIEW-004-FIX (Build 86): adults/children/images/info were missing
                -- from the view despite being in the schema since GAP-SCHEMA-002-FIX
                -- (Build 80). These fields are required by _API_.md rooms[] format.
                'adults',      hrt.adults,
                'children',    hrt.children,
                'images',      hrt.images,
                'info',        hrt.info
            ) ORDER BY hrt.id
         )
         FROM hotels_room_types hrt
         WHERE hrt.hotel_id = h.id AND hrt.language = h.language),
        '[]'::jsonb
    ) AS room_types_detail
FROM hotels h
LEFT JOIN url_queue uq
       ON uq.id = h.url_id
LEFT JOIN hotels_description hd
       ON hd.hotel_id = h.id AND hd.language = h.language
LEFT JOIN hotels_fine_print hfp
       ON hfp.hotel_id = h.id AND hfp.language = h.language
LEFT JOIN hotels_extra_info hei
       ON hei.hotel_id = h.id AND hei.language = h.language
LEFT JOIN hotels_seo hseo
       ON hseo.hotel_id = h.id AND hseo.language = h.language
LEFT JOIN hotels_legal hl
       ON hl.hotel_id = h.id AND hl.language = h.language;

COMMENT ON VIEW v_hotels_full IS
    'Vista denormalizada de hotel con description, fine_print, highlights, all_services, faqs, '
    'popular_services, policies, guest_reviews, legal, extra_info, seo, nearby_places, room_types_detail, accommodation_type — v76';


-- Vista: resumen de completitud de scraping por URL
CREATE OR REPLACE VIEW v_scraping_summary AS
SELECT
    uq.id               AS url_id,
    uq.url,
    uq.external_ref,
    uq.external_url,
    uq.status           AS queue_status,
    uq.retry_count,
    uq.scraped_at,
    COUNT(uls.id)                                               AS languages_tracked,
    SUM(CASE WHEN uls.status = 'done'  THEN 1 ELSE 0 END)      AS languages_done,
    SUM(CASE WHEN uls.status = 'error' THEN 1 ELSE 0 END)      AS languages_error,
    MAX(uls.attempts)                                           AS max_attempts
FROM url_queue uq
LEFT JOIN url_language_status uls ON uls.url_id = uq.id
GROUP BY uq.id, uq.url, uq.external_ref, uq.external_url,
         uq.status, uq.retry_count, uq.scraped_at;

COMMENT ON VIEW v_scraping_summary IS
    'Resumen de completitud de scraping por URL';


-- =============================================================================
-- CONSULTAS DE VALIDACIÓN POST-INSTALACIÓN (comentadas — ejecutar manualmente)
-- =============================================================================

/*
-- 1. Verificar que existen exactamente 22 tablas (v77: +1 tabla nueva hotels_individual_reviews)
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
      'url_queue','hotels','hotels_description',
      'hotels_policies','hotels_legal',
      'hotels_popular_services','url_language_status',
      'scraping_logs','image_downloads','image_data','system_metrics',
      'hotels_fine_print','hotels_all_services','hotels_faqs',
      'hotels_guest_reviews','hotels_property_highlights',
      'hotels_extra_info','hotels_nearby_places',
      'hotels_room_types','hotels_seo',
      'hotels_individual_reviews'
  )
ORDER BY table_name;
-- Esperado: 21 filas (scraping_logs es particionada, cuenta separado)

-- 2. Confirmar que hotels_amenities NO existe
SELECT COUNT(*) AS debe_ser_cero
FROM information_schema.tables
WHERE table_schema = 'public' AND table_name = 'hotels_amenities';
-- Esperado: 0

-- 3. Verificar campo has_legal_content en hotels_legal
SELECT column_name, data_type, column_default, is_nullable
FROM information_schema.columns
WHERE table_name = 'hotels_legal'
  AND column_name = 'has_legal_content';
-- Esperado: boolean, DEFAULT false, NOT NULL

-- 4. Verificar triggers updated_at
SELECT trigger_name, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public'
  AND trigger_name LIKE 'trg_%updated_at'
ORDER BY event_object_table;
-- Esperado: url_queue, hotels, hotels_description, url_language_status, hotels_fine_print

-- 5. Verificar columnas de v_hotels_full (sin columna amenities)
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'v_hotels_full'
ORDER BY ordinal_position;
-- amenities NO debe aparecer

-- 6. Conteo global post-scraping (referencia: 13 URLs x 6 idiomas = 78 filas esperadas)
SELECT 'hotels'                     AS tabla, COUNT(*) AS filas FROM hotels
UNION ALL SELECT 'hotels_description',        COUNT(*) FROM hotels_description
UNION ALL SELECT 'hotels_policies',           COUNT(*) FROM hotels_policies
UNION ALL SELECT 'hotels_legal',              COUNT(*) FROM hotels_legal
UNION ALL SELECT 'hotels_fine_print',         COUNT(*) FROM hotels_fine_print
UNION ALL SELECT 'hotels_all_services',       COUNT(*) FROM hotels_all_services
UNION ALL SELECT 'hotels_popular_services',   COUNT(*) FROM hotels_popular_services
UNION ALL SELECT 'hotels_faqs',               COUNT(*) FROM hotels_faqs
UNION ALL SELECT 'hotels_guest_reviews',      COUNT(*) FROM hotels_guest_reviews
UNION ALL SELECT 'hotels_property_highlights',COUNT(*) FROM hotels_property_highlights
UNION ALL SELECT 'image_data',                COUNT(*) FROM image_data
UNION ALL SELECT 'image_downloads',           COUNT(*) FROM image_downloads
UNION ALL SELECT 'url_language_status',       COUNT(*) FROM url_language_status
UNION ALL SELECT 'scraping_logs',             COUNT(*) FROM scraping_logs
UNION ALL SELECT 'url_queue',                 COUNT(*) FROM url_queue
UNION ALL SELECT 'hotels_extra_info',          COUNT(*) FROM hotels_extra_info
UNION ALL SELECT 'hotels_nearby_places',       COUNT(*) FROM hotels_nearby_places
UNION ALL SELECT 'hotels_room_types',          COUNT(*) FROM hotels_room_types
UNION ALL SELECT 'hotels_seo',                 COUNT(*) FROM hotels_seo
UNION ALL SELECT 'hotels_individual_reviews',  COUNT(*) FROM hotels_individual_reviews
ORDER BY tabla;
*/

-- =============================================================================
-- FIN DEL SCHEMA v77  (Build 78)
-- =============================================================================
