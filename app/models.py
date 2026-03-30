"""
models.py — BookingScraper Pro v6.0.0 build 60
===============================================
Cambios v60:

  MODEL-002 : HotelLegal.has_legal_content — nuevo campo diagnóstico BOOLEAN.
              BUG-DB-002-FIX: distingue entre "no legal section found" (FALSE)
              y "legal section found with content" (TRUE).
              Antes, la ausencia de sección legal producía 0 registros en
              hotels_legal para hoteles de BR/UY — fallo silencioso sin traza.
              Ahora siempre existe 1 registro por hotel/idioma con has_legal_content
              indicando si Booking.com publicó o no esa sección para ese hotel.

Cambios estructurales v53:

  STRUCT-013 : HotelFinePrint — nueva tabla v53.
               Almacena el bloque "Fine Print" / "Letra pequeña" de Booking.com
               como HTML sanitizado preservando etiquetas <p> para saltos de línea.
               Campo principal: fp (TEXT).
               Clave primaria UUID (1 registro por hotel/idioma, como HotelDescription).

  STRUCT-014 : HotelAllService — nueva tabla v53.
               Almacena TODOS los servicios/instalaciones del hotel.
               Campo: service (VARCHAR 512). Una fila por servicio.
               BIGSERIAL pk (muchas filas por hotel/idioma, como HotelPopularService).

  STRUCT-015 : HotelFAQ — nueva tabla v53.
               Almacena las preguntas frecuentes del hotel.
               Campos: ask (TEXT) + answer (TEXT NULL). Una pregunta/respuesta por fila.
               BIGSERIAL pk (como HotelPopularService).
               BUG-FAQ-ANSWERS (v56): columna answer añadida — extracción completa del acordeón.

  STRUCT-016 : HotelGuestReview — nueva tabla v53.
               Almacena categorías de valoración de huéspedes con puntuación.
               Campos: reviews_categories (VARCHAR 256), reviews_score (TEXT).
               BIGSERIAL pk (como HotelPolicy, par categoría/puntuación).

  STRUCT-017 : HotelPropertyHighlights — nueva tabla v53.
               Almacena el bloque "Property Highlights" como HTML sanitizado.
               SVG e imágenes eliminados. Todos los atributos HTML eliminados.
               Campo: highlights (TEXT).
               UUID pk (1 registro por hotel/idioma, como HotelDescription).

Cambios estructurales v52:

  STRUCT-009 : URLQueue.external_url — nueva columna.
               Tercer campo del CSV de carga (external_ref, url, external_url).
               Almacena la URL alternativa/externa asociada al hotel.

  STRUCT-010 : URLQueue.hotel_id_booking — ELIMINADO.
               Campo redundante: su valor se persiste correctamente en
               hotels.hotel_id_booking durante el scraping. Eliminados también
               los índices asociados.

  STRUCT-011 : hotels.city RENOMBRADO a hotels.address_city.
               Alineación con la convención de nomenclatura de los demás campos
               de dirección: address_locality, address_country.
               Índice renombrado: ix_hotels_city_country → ix_hotels_address_city.

  STRUCT-012 : hotels.country — ELIMINADO.
               Duplicado de hotels.address_country (ambos provienen de
               addressCountry del JSON-LD de schema.org). Eliminados también
               los índices que lo referenciaban.

Fixes heredados:
  STRUCT-001 : HotelDescription — nueva tabla v50.
  STRUCT-002 : hotels.photos eliminado — image_downloads es fuente única.
  STRUCT-003 : hotels.review_count renombrado desde review_count_schema.
  STRUCT-004 : hotels.address eliminado — campo muerto.
  STRUCT-005 : HotelAmenity — nueva tabla v51.
  STRUCT-006 : HotelPolicy — nueva tabla v51.
  STRUCT-007 : HotelLegal — nueva tabla v51.
  STRUCT-008 : HotelPopularService — nueva tabla v51.
  BUG-003/103: FK de ScrapingLog via trigger.
  BUG-007/012: version_id — optimistic locking.
  BUG-016    : URLLanguageStatus check incluye todos los estados válidos.
  BUG-019    : SystemMetrics time-series indexes.
  Platform   : Windows 11 / PostgreSQL 15+ / psycopg v3.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, Column, DateTime, Float,
    Index, Integer, SmallInteger, String, Text, UniqueConstraint,
    event, text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

class Base(DeclarativeBase):
    """Common base for all ORM models."""
    pass


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# URLQueue
# ---------------------------------------------------------------------------

class URLQueue(Base):
    """
    Cola de tareas de scraping.

    external_ref    : ID numérico del CSV origen (e.g. 1001, 1002...).
    external_url    : URL alternativa/externa del hotel (3ª columna del CSV).
                      STRUCT-009 (v52): nuevo campo para el formato de 3 columnas.

    BUG-LOAD-001: load_urls.py ahora usa ON CONFLICT DO UPDATE para garantizar
                  que external_ref se guarda incluso en re-cargas de CSV.

    STRUCT-010 (v52): hotel_id_booking ELIMINADO — redundante con hotels.hotel_id_booking.
    """
    __tablename__ = "url_queue"
    __mapper_args__ = {
        "version_id_col": None,
    }

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    url: Mapped[str] = mapped_column(String(2048), nullable=False, unique=True)
    base_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    external_ref: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, index=True,
        comment="ID numerico del CSV origen (e.g. 1001)"
    )
    # STRUCT-009 (v52): URL externa/alternativa del hotel
    external_url: Mapped[Optional[str]] = mapped_column(
        String(2048), nullable=True,
        comment="URL alternativa/externa del hotel (3a columna del CSV)"
    )
    # STRUCT-010 (v52): hotel_id_booking ELIMINADO — ver hotels.hotel_id_booking
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending", index=True
    )
    priority: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=5)
    retry_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    max_retries: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=3)
    last_error: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    # STRATEGY-E (v58): Track per-language outcome for partial retry
    languages_completed: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, default="",
        comment="Comma-separated list of successfully scraped languages (e.g. 'es,it')"
    )
    languages_failed: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, default="",
        comment="Comma-separated list of failed languages (e.g. 'en,de')"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow
    )
    scraped_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    version_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','processing','done','error','skipped','incomplete')",
            name="chk_url_queue_status",
        ),
        CheckConstraint("priority BETWEEN 1 AND 10", name="chk_url_queue_priority"),
        Index("ix_url_queue_status_priority", "status", "priority"),
        Index("ix_url_queue_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<URLQueue id={self.id} status={self.status} ext={self.external_ref}>"


# ---------------------------------------------------------------------------
# Hotel
# ---------------------------------------------------------------------------

class Hotel(Base):
    """
    Datos principales del hotel por idioma.

    v52 — cambios estructurales:
      - city          : RENOMBRADO a address_city (STRUCT-011)
                        Alineación con address_locality, address_country.
      - country       : ELIMINADO — duplicado de address_country (STRUCT-012)

    v51 — cambios estructurales:
      - amenities  : ELIMINADO → movido a HotelAmenity  (STRUCT-005)
      - policies   : ELIMINADO → movido a HotelPolicy   (STRUCT-006)

    v50 — cambios estructurales:
      - description    : ELIMINADO → movido a HotelDescription (STRUCT-001)
      - photos         : ELIMINADO → duplicado con image_downloads (STRUCT-002)
      - address        : ELIMINADO → campo muerto, usar street_address (STRUCT-004)
      - review_count   : RENOMBRADO desde review_count_schema (JSON-LD, fiable)

    Campos schema.org / JSON-LD (NEW-COLS-001, v49):
      main_image_url    — Hotel.image
      short_description — Hotel.description (resumen corto)
      rating_value      — aggregateRating.ratingValue
      best_rating       — aggregateRating.bestRating
      review_count      — aggregateRating.reviewCount (JSON-LD)
      street_address    — address.streetAddress
      address_city      — address.addressRegion / breadcrumb (STRUCT-011, v52)
      address_locality  — address.addressLocality
      address_country   — address.addressCountry
      postal_code       — address.postalCode
    """
    __tablename__ = "hotels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="FK to url_queue.id (enforced via FK constraint in SQL)",
    )
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    hotel_name: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    hotel_id_booking: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    # STRUCT-011 (v52): renombrado desde 'city' → 'address_city'
    address_city: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, index=True,
        comment="Ciudad/región del hotel — antes 'city'. Fuente: addressRegion JSON-LD o breadcrumb"
    )
    # STRUCT-012 (v52): country ELIMINADO — usar address_country
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    star_rating: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True,
        comment="Estrellas normalizadas 0-5 (valor raw Booking ÷ 2)"
    )
    review_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # STRUCT-003: review_count = reviewCount de JSON-LD (antes review_count_schema)
    review_count: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True,
        comment="aggregateRating.reviewCount de JSON-LD (language-independent)"
    )

    # schema.org / JSON-LD enrichment fields (NEW-COLS-001)
    main_image_url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True,
        comment="Hotel primary image URL from schema.org JSON-LD 'image' field")
    short_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True,
        comment="Short description from schema.org JSON-LD 'description' field")
    rating_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True,
        comment="aggregateRating.ratingValue from schema.org")
    best_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True,
        comment="aggregateRating.bestRating from schema.org (usually 10)")
    street_address: Mapped[Optional[str]] = mapped_column(String(512), nullable=True,
        comment="address.streetAddress from schema.org")
    address_locality: Mapped[Optional[str]] = mapped_column(String(256), nullable=True,
        comment="address.addressLocality from schema.org")
    address_country: Mapped[Optional[str]] = mapped_column(String(128), nullable=True,
        comment="address.addressCountry from schema.org")
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True,
        comment="address.postalCode from schema.org")

    # STRUCT-005: amenities ELIMINADO — ver tabla hotels_amenities
    # STRUCT-006: policies  ELIMINADO — ver tabla hotels_policies

    room_types: Mapped[Optional[List]] = mapped_column(JSONB, nullable=True, default=list)
    raw_data: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True, default=dict)
    scrape_duration_s: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    scrape_engine: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow
    )
    version_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    __table_args__ = (
        UniqueConstraint("url_id", "language", name="uq_hotels_url_lang"),
        CheckConstraint(
            "star_rating IS NULL OR (star_rating >= 0 AND star_rating <= 5)",
            name="chk_hotels_star_rating",
        ),
        CheckConstraint(
            "review_score IS NULL OR review_score BETWEEN 0 AND 10",
            name="chk_hotels_review_score",
        ),
        CheckConstraint(
            "review_count IS NULL OR review_count >= 0",
            name="chk_hotels_review_count",
        ),
        # STRUCT-011 (v52): índice sobre address_city (renombrado desde ix_hotels_city_country)
        Index("ix_hotels_address_city", "address_city"),
        Index("ix_hotels_created_at", "created_at"),
        # STRUCT-005: ix_hotels_amenities_gin ELIMINADO — amenities removido de hotels
        # STRUCT-012 (v52): ix_hotels_city_country ELIMINADO — country eliminado
    )

    def __repr__(self) -> str:
        return f"<Hotel id={self.id} name={self.hotel_name!r} lang={self.language}>"


# ---------------------------------------------------------------------------
# HotelDescription  (STRUCT-001 — nueva tabla v50)
# ---------------------------------------------------------------------------

class HotelDescription(Base):
    """
    Descripción larga del hotel por idioma.

    STRUCT-001: Separada de hotels para:
      - Reducir tamaño de la tabla principal hotels (TEXT de ~500-2000 chars por fila).
      - Permitir queries sobre hotels sin cargar descripciones.
      - Facilitar indexado GIN full-text sobre descriptions de forma independiente.
    """
    __tablename__ = "hotels_description"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id"
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a url_queue.id — redundante pero útil para queries directas"
    )
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow
    )

    __table_args__ = (
        UniqueConstraint("url_id", "language", name="uq_hdesc_url_lang"),
        Index("ix_hdesc_hotel_id", "hotel_id"),
        Index("ix_hdesc_language", "language"),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelDescription hotel_id={self.hotel_id} lang={self.language} "
            f"len={len(self.description or '')}>"
        )


# ---------------------------------------------------------------------------
# HotelAmenity  (STRUCT-005 — nueva tabla v51)
# ---------------------------------------------------------------------------

class HotelAmenity(Base):
    """
    Amenidades del hotel — una fila por amenidad.

    STRUCT-005: Reemplaza hotels.amenities (JSONB array) con tabla normalizada.
    Permite:
      - Filtrado exacto por amenidad sin operadores JSONB.
      - Joins eficientes con índice B-Tree en amenity.
      - Queries multiidioma sobre instalaciones.

    Estructura:
      hotel_id  — FK a hotels.id
      url_id    — FK a url_queue.id (redundante, facilita queries sin JOIN)
      language  — código ISO 639-1 del idioma
      amenity   — texto de la amenidad (e.g. 'Piscina al aire libre')
    """
    __tablename__ = "hotels_amenities"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True,
        comment="Surrogate key BIGSERIAL — compatible con volúmenes altos"
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id"
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a url_queue.id"
    )
    language: Mapped[str] = mapped_column(
        String(10), nullable=False, index=True,
        comment="Código ISO 639-1 del idioma de la amenidad"
    )
    amenity: Mapped[str] = mapped_column(
        String(512), nullable=False,
        comment="Texto de la amenidad extraído del bloque de instalaciones del hotel"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    __table_args__ = (
        # Evita duplicados por re-scrape del mismo hotel/idioma/amenidad
        UniqueConstraint("hotel_id", "language", "amenity", name="uq_hamenity_hotel_lang_amenity"),
        Index("ix_hamenity_hotel_id", "hotel_id"),
        Index("ix_hamenity_language", "language"),
        Index("ix_hamenity_amenity", "amenity"),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelAmenity hotel_id={self.hotel_id} lang={self.language} "
            f"amenity={self.amenity!r}>"
        )


# ---------------------------------------------------------------------------
# HotelPolicy  (STRUCT-006 — nueva tabla v51)
# ---------------------------------------------------------------------------

class HotelPolicy(Base):
    """
    Políticas del hotel — una fila por política.

    STRUCT-006: Reemplaza hotels.policies (JSONB dict) con tabla normalizada.
    Permite:
      - Consultas directas sobre política específica (e.g. 'Check-in').
      - Filtrado por idioma sin deserializar JSONB.
      - Almacenamiento de detalles largos (TEXT) sin límite de JSONB.

    Estructura:
      hotel_id       — FK a hotels.id
      url_id         — FK a url_queue.id
      language       — código ISO 639-1
      policy_name    — nombre de la política (e.g. 'Check-in', 'Mascotas')
      policy_details — texto completo de la política
    """
    __tablename__ = "hotels_policies"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True,
        comment="Surrogate key BIGSERIAL"
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id"
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a url_queue.id"
    )
    language: Mapped[str] = mapped_column(
        String(10), nullable=False, index=True,
        comment="Código ISO 639-1"
    )
    policy_name: Mapped[str] = mapped_column(
        String(256), nullable=False,
        comment="Nombre de la política (e.g. 'Check-in', 'Cancelación / prepago')"
    )
    policy_details: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        comment="Texto completo de la política"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "hotel_id", "language", "policy_name",
            name="uq_hpolicy_hotel_lang_name",
        ),
        Index("ix_hpolicy_hotel_id", "hotel_id"),
        Index("ix_hpolicy_language", "language"),
        Index("ix_hpolicy_policy_name", "policy_name"),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelPolicy hotel_id={self.hotel_id} lang={self.language} "
            f"policy={self.policy_name!r}>"
        )


# ---------------------------------------------------------------------------
# HotelLegal  (STRUCT-007 — nueva tabla v51)
# ---------------------------------------------------------------------------

class HotelLegal(Base):
    """
    Texto legal del hotel por idioma.

    STRUCT-007: Almacena información legal extraída del pie de página de Booking.com.

    Estructura:
      hotel_id          — FK a hotels.id
      url_id            — FK a url_queue.id
      language          — código ISO 639-1
      legal             — título del bloque legal (e.g. 'Información legal')
      legal_info        — texto introductorio del bloque legal
      legal_details     — texto adicional / detalles extendidos (puede ser vacío)
      has_legal_content — TRUE si Booking.com publicó sección legal para este hotel/idioma
                          FALSE si la página fue procesada pero no tiene sección legal

    BUG-DB-002-FIX (v60): has_legal_content añadido para registrar la ausencia de
      sección legal de forma explícita y auditable. Antes de v60, la ausencia
      producía 0 registros en hotels_legal (inconsistencia silenciosa). Ahora
      siempre existe 1 registro por hotel/idioma.

    FIX-LEGAL-001 (v52): _extract_legal() corregido en extractor.py para detectar
      correctamente el título en múltiples idiomas (ES, JA, AR, FR y otros).
      Registros ES con IDs 1-22 tenían el título en legal_info por error.
    """
    __tablename__ = "hotels_legal"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True,
        comment="Surrogate key BIGSERIAL"
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id"
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a url_queue.id"
    )
    language: Mapped[str] = mapped_column(
        String(10), nullable=False, index=True,
        comment="Código ISO 639-1"
    )
    legal: Mapped[Optional[str]] = mapped_column(
        String(256), nullable=True,
        comment="Título del bloque legal (e.g. 'Información legal')"
    )
    legal_info: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        comment="Texto introductorio del bloque legal"
    )
    legal_details: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        comment="Detalles extendidos (normalmente vacío en Booking.com)"
    )
    has_legal_content: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False,
        comment="TRUE si Booking.com publicó sección legal para este hotel/idioma (BUG-DB-002-FIX v60)"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    __table_args__ = (
        # Un bloque legal por hotel/idioma (Booking.com tiene uno solo)
        UniqueConstraint("hotel_id", "language", name="uq_hlegal_hotel_lang"),
        Index("ix_hlegal_hotel_id", "hotel_id"),
        Index("ix_hlegal_language", "language"),
        # BUG-DB-002-FIX (v60): índice para consultas de auditoría de cobertura
        Index("ix_hlegal_has_content", "has_legal_content"),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelLegal hotel_id={self.hotel_id} lang={self.language} "
            f"has_content={self.has_legal_content} legal={self.legal!r}>"
        )


# ---------------------------------------------------------------------------
# HotelPopularService  (STRUCT-008 — nueva tabla v51)
# ---------------------------------------------------------------------------

class HotelPopularService(Base):
    """
    Servicios más populares del hotel — una fila por servicio.

    STRUCT-008: Curated subset de instalaciones que Booking.com destaca en el
    bloque 'Most popular facilities' / 'Servicios más populares'.
    Difiere de hotels_amenities en que es una selección editorial del proveedor
    (normalmente 8-12 ítems) mientras que hotels_amenities es la lista completa.

    Estructura:
      hotel_id        — FK a hotels.id
      url_id          — FK a url_queue.id
      language        — código ISO 639-1
      popular_service — texto del servicio popular
    """
    __tablename__ = "hotels_popular_services"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True,
        comment="Surrogate key BIGSERIAL"
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id"
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a url_queue.id"
    )
    language: Mapped[str] = mapped_column(
        String(10), nullable=False, index=True,
        comment="Código ISO 639-1"
    )
    popular_service: Mapped[str] = mapped_column(
        String(512), nullable=False,
        comment="Nombre del servicio popular (e.g. 'WiFi gratis', 'Piscina al aire libre')"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "hotel_id", "language", "popular_service",
            name="uq_hpopservice_hotel_lang_service",
        ),
        Index("ix_hpopservice_hotel_id", "hotel_id"),
        Index("ix_hpopservice_language", "language"),
        Index("ix_hpopservice_service", "popular_service"),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelPopularService hotel_id={self.hotel_id} lang={self.language} "
            f"service={self.popular_service!r}>"
        )


# ---------------------------------------------------------------------------
# URLLanguageStatus
# ---------------------------------------------------------------------------

class URLLanguageStatus(Base):
    """
    Tracking de completitud de scraping por URL y lenguaje.
    BUG-016: check constraint incluye TODOS los estados válidos.
    """
    __tablename__ = "url_language_status"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    attempts: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    last_error: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (
        UniqueConstraint("url_id", "language", name="uq_uls_url_lang"),
        CheckConstraint(
            "status IN ('pending','processing','done','error','skipped','incomplete')",
            name="chk_uls_status_valid",
        ),
        Index("ix_uls_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<URLLanguageStatus url_id={self.url_id} lang={self.language} status={self.status}>"


# ---------------------------------------------------------------------------
# ScrapingLog  (PARTITIONED TABLE)
# ---------------------------------------------------------------------------

class ScrapingLog(Base):
    """
    Log de eventos de scraping — tabla particionada por mes (RANGE on scraped_at).

    ⚠️  BUG-003 / BUG-103: PostgreSQL NO soporta FK constraints en tablas particionadas.
    La integridad referencial para url_id / hotel_id se garantiza via trigger:
        trg_scraping_logs_fk_check  (BEFORE INSERT / UPDATE)
    """
    __tablename__ = "scraping_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    url_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    hotel_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    worker_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    extra_data: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True, default=dict)
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, primary_key=True
    )

    __table_args__ = (
        {"postgresql_partition_by": "RANGE (scraped_at)"},
    )

    def __repr__(self) -> str:
        return f"<ScrapingLog url_id={self.url_id} event={self.event_type} status={self.status}>"


# ---------------------------------------------------------------------------
# ImageDownload
# ---------------------------------------------------------------------------

class ImageDownload(Base):
    """
    Tracking de descargas individuales de imágenes por hotel y categoría de tamaño.

    BUG-IMG-SCHEMA (v49): Columnas id_photo y category añadidas.
    STRUCT-002 (v50): hotels.photos eliminado — image_downloads es la fuente única de verdad.
    """
    __tablename__ = "image_downloads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    id_photo: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, index=True,
        comment="Booking.com photo ID (e.g. '49312038')")
    category: Mapped[Optional[str]] = mapped_column(String(16), nullable=True,
        comment="Variante de tamaño: thumb_url | large_url | highres_url")
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    local_path: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    error_message: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utcnow)
    downloaded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','downloading','done','error','skipped')",
            name="chk_imgdl_status",
        ),
        CheckConstraint(
            "category IS NULL OR category IN ('thumb_url','large_url','highres_url')",
            name="chk_imgdl_category",
        ),
        UniqueConstraint("hotel_id", "url", name="uq_imgdl_hotel_url"),
        Index("ix_imgdl_status", "status"),
        Index("ix_imgdl_id_photo", "id_photo"),
    )


# ---------------------------------------------------------------------------
# ImageData
# ---------------------------------------------------------------------------

class ImageData(Base):
    """
    Metadatos completos de fotos desde el JS hotelPhotos de Booking.com.

    Una fila por foto única (id_photo es globalmente único en Booking.com).
    """
    __tablename__ = "image_data"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_photo: Mapped[str] = mapped_column(String(32), nullable=False, unique=True,
        comment="Booking.com photo ID — globalmente único")
    hotel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id")
    orientation: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    photo_width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    photo_height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    alt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at_photo: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True,
        comment="Timestamp de creación de la foto en Booking.com")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    __table_args__ = (
        CheckConstraint(
            "orientation IS NULL OR orientation IN ('landscape','portrait','square')",
            name="chk_imgdata_orientation",
        ),
        CheckConstraint("photo_width IS NULL OR photo_width > 0", name="chk_imgdata_width_positive"),
        CheckConstraint("photo_height IS NULL OR photo_height > 0", name="chk_imgdata_height_positive"),
        Index("ix_imgdata_hotel_id", "hotel_id"),
    )

    def __repr__(self) -> str:
        return f"<ImageData id_photo={self.id_photo} hotel_id={self.hotel_id} orient={self.orientation}>"


# ---------------------------------------------------------------------------
# SystemMetrics
# ---------------------------------------------------------------------------

class SystemMetrics(Base):
    """
    Snapshots periódicos de salud del sistema.
    BUG-019: índices en columnas de series temporales.
    """
    __tablename__ = "system_metrics"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, index=True
    )
    cpu_usage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    memory_usage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    active_workers: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    db_pool_checked_out: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    redis_connected: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    urls_pending: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    urls_done: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    extra_data: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True, default=dict)

    __table_args__ = (
        Index("ix_sysmetrics_recorded_cpu", "recorded_at", "cpu_usage"),
        Index("ix_sysmetrics_recorded_mem", "recorded_at", "memory_usage"),
    )

    def __repr__(self) -> str:
        return f"<SystemMetrics recorded_at={self.recorded_at} cpu={self.cpu_usage}>"


# ---------------------------------------------------------------------------
# HotelFinePrint  (STRUCT-013 — nueva tabla v53)
# ---------------------------------------------------------------------------

class HotelFinePrint(Base):
    """
    Bloque "Fine Print" / "Letra pequeña" del hotel por idioma.

    STRUCT-013 (v53): Almacena el contenido HTML sanitizado del bloque
    Fine Print de Booking.com:
      - Etiquetas <p> preservadas para mantener saltos de línea.
      - SVG e imágenes (<img>, <picture>, <source>) eliminados completamente.
      - Atributos HTML eliminados de todas las etiquetas restantes.

    Estructura: 1 registro por hotel/idioma (como HotelDescription).
      hotel_id — FK a hotels.id
      url_id   — FK a url_queue.id
      language — código ISO 639-1
      fp       — HTML sanitizado del bloque Fine Print
    """
    __tablename__ = "hotels_fine_print"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
        comment="Surrogate key UUID"
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id"
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a url_queue.id"
    )
    language: Mapped[str] = mapped_column(
        String(10), nullable=False,
        comment="Código ISO 639-1"
    )
    fp: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        comment="HTML sanitizado del bloque Fine Print. <p> preservados, SVG/img eliminados, atributos eliminados"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow
    )

    __table_args__ = (
        UniqueConstraint("url_id", "language", name="uq_hfp_url_lang"),
        Index("ix_hfp_hotel_id", "hotel_id"),
        Index("ix_hfp_language", "language"),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelFinePrint hotel_id={self.hotel_id} lang={self.language} "
            f"len={len(self.fp or '')}>"
        )


# ---------------------------------------------------------------------------
# HotelAllService  (STRUCT-014 — nueva tabla v53)
# ---------------------------------------------------------------------------

class HotelAllService(Base):
    """
    Todos los servicios/instalaciones del hotel — una fila por servicio.

    STRUCT-014 (v53): Complementa hotels_amenities con la extracción
    completa de servicios desde la sección de instalaciones de Booking.com.
    Mientras hotels_amenities captura spans del bloque principal,
    hotels_all_services captura los ítems completos de la lista expandida.

    Estructura (como HotelPopularService — BIGSERIAL, muchas filas por hotel/lang):
      hotel_id — FK a hotels.id
      url_id   — FK a url_queue.id
      language — código ISO 639-1
      service  — texto del servicio/instalación
    """
    __tablename__ = "hotels_all_services"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True,
        comment="Surrogate key BIGSERIAL"
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id"
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a url_queue.id"
    )
    language: Mapped[str] = mapped_column(
        String(10), nullable=False, index=True,
        comment="Código ISO 639-1"
    )
    service: Mapped[str] = mapped_column(
        String(512), nullable=False,
        comment="Texto del servicio/instalación (e.g. 'Piscina al aire libre', 'Parking gratuito')"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "hotel_id", "language", "service",
            name="uq_hallsvc_hotel_lang_service",
        ),
        Index("ix_hallsvc_hotel_id", "hotel_id"),
        Index("ix_hallsvc_language", "language"),
        Index("ix_hallsvc_service", "service"),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelAllService hotel_id={self.hotel_id} lang={self.language} "
            f"service={self.service!r}>"
        )


# ---------------------------------------------------------------------------
# HotelFAQ  (STRUCT-015 — nueva tabla v53)
# ---------------------------------------------------------------------------

class HotelFAQ(Base):
    """
    Preguntas frecuentes del hotel — una pregunta (ask) + respuesta (answer) por fila.

    STRUCT-015 (v53): Extrae el bloque de preguntas frecuentes (FAQ)
    de la página de Booking.com.

    BUG-FAQ-ANSWERS (v56): columna answer añadida — extracción completa del acordeón
    (botón de pregunta + div hermano de respuesta).

    Estructura (como HotelPopularService — BIGSERIAL):
      hotel_id — FK a hotels.id
      url_id   — FK a url_queue.id
      language — código ISO 639-1
      ask      — texto de la pregunta frecuente
      answer   — texto de la respuesta (puede ser NULL si no está disponible en el DOM)
    """
    __tablename__ = "hotels_faqs"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True,
        comment="Surrogate key BIGSERIAL"
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id"
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a url_queue.id"
    )
    language: Mapped[str] = mapped_column(
        String(10), nullable=False, index=True,
        comment="Código ISO 639-1"
    )
    ask: Mapped[str] = mapped_column(
        Text, nullable=False,
        comment="Texto de la pregunta frecuente (e.g. '¿Cuál es el horario de check-in?')"
    )
    # BUG-FAQ-ANSWERS (v56): columna answer añadida
    answer: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        comment="Texto de la respuesta a la pregunta frecuente (extraído del accordion de Booking.com)"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "hotel_id", "language", "ask",
            name="uq_hfaq_hotel_lang_ask",
        ),
        Index("ix_hfaq_hotel_id", "hotel_id"),
        Index("ix_hfaq_language", "language"),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelFAQ hotel_id={self.hotel_id} lang={self.language} "
            f"ask={str(self.ask)[:60]!r}>"
        )


# ---------------------------------------------------------------------------
# HotelGuestReview  (STRUCT-016 — nueva tabla v53)
# ---------------------------------------------------------------------------

class HotelGuestReview(Base):
    """
    Categorías de valoración de huéspedes con puntuación — una fila por categoría.

    STRUCT-016 (v53): Extrae las puntuaciones por categoría del bloque
    de reseñas de Booking.com (Cleanliness, Comfort, Location, etc.).

    Estructura (como HotelPolicy — BIGSERIAL, par categoría/puntuación):
      hotel_id            — FK a hotels.id
      url_id              — FK a url_queue.id
      language            — código ISO 639-1
      reviews_categories  — nombre de la categoría de valoración
      reviews_score       — puntuación de la categoría (valor textual)
    """
    __tablename__ = "hotels_guest_reviews"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True,
        comment="Surrogate key BIGSERIAL"
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id"
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a url_queue.id"
    )
    language: Mapped[str] = mapped_column(
        String(10), nullable=False, index=True,
        comment="Código ISO 639-1"
    )
    reviews_categories: Mapped[str] = mapped_column(
        String(256), nullable=False,
        comment="Categoría de valoración (e.g. 'Limpieza', 'Confort', 'Ubicación', 'Personal')"
    )
    reviews_score: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        comment="Puntuación de la categoría (valor textual, e.g. '9.5', '8.8')"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "hotel_id", "language", "reviews_categories",
            name="uq_hgrev_hotel_lang_cat",
        ),
        Index("ix_hgrev_hotel_id", "hotel_id"),
        Index("ix_hgrev_language", "language"),
        Index("ix_hgrev_categories", "reviews_categories"),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelGuestReview hotel_id={self.hotel_id} lang={self.language} "
            f"cat={self.reviews_categories!r} score={self.reviews_score!r}>"
        )


# ---------------------------------------------------------------------------
# HotelPropertyHighlights  (STRUCT-017 — nueva tabla v53)
# BUG-PH-NORMALIZATION-001 FIX (v56): Estructura normalizada — un registro
# ---------------------------------------------------------------------------
# FIX-PH-STRUCTURE-001 (v59): HotelPropertyHighlights reestructurada.
# ANTES (v57-v58): 1 columna 'highlight' (texto plano, sin jerarquía).
# AHORA (v59): 2 columnas 'highlight_category' + 'highlight_detail'.
# Estructura: 1 fila por par (categoría, ítem) por hotel/idioma.
# Ejemplo:
#   highlight_category = "Ideal para tu estancia"
#   highlight_detail   = "Baño privado"
# UniqueConstraint actualizado: (hotel_id, language, highlight_category, highlight_detail)
# ---------------------------------------------------------------------------

class HotelPropertyHighlights(Base):
    """
    Highlights de propiedad con estructura categoría/detalle.

    FIX-PH-STRUCTURE-001 (v59): Estructura rediseñada de 1 columna 'highlight'
    a 2 columnas 'highlight_category' + 'highlight_detail', capturando la
    jerarquía real que muestra Booking.com en el DOM.

    Estructura: 1 fila por par (categoría, ítem) por hotel/idioma:
      highlight_category — nombre del grupo (e.g. "Ideal para tu estancia")
      highlight_detail   — ítem individual  (e.g. "Baño privado", "Parking")
    """
    __tablename__ = "hotels_property_highlights"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True,
        comment="Surrogate key BIGSERIAL"
    )
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a hotels.id"
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
        comment="FK a url_queue.id"
    )
    language: Mapped[str] = mapped_column(
        String(10), nullable=False,
        comment="Código ISO 639-1"
    )
    highlight_category: Mapped[str] = mapped_column(
        String(256), nullable=False,
        comment="Nombre del grupo de highlight (e.g. 'Ideal para tu estancia', 'Baño')"
    )
    highlight_detail: Mapped[str] = mapped_column(
        String(512), nullable=False,
        comment="Ítem individual del grupo (e.g. 'Baño privado', 'Parking', 'WiFi gratis')"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )

    __table_args__ = (
        # Un registro por combinación hotel/idioma/categoría/detalle
        UniqueConstraint(
            "hotel_id", "language", "highlight_category", "highlight_detail",
            name="uq_hph_hotel_lang_cat_detail"
        ),
        Index("ix_hph_hotel_id", "hotel_id"),
        Index("ix_hph_language", "language"),
        Index("ix_hph_url_id", "url_id"),
        Index("ix_hph_category", "highlight_category"),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelPropertyHighlights hotel_id={self.hotel_id} lang={self.language} "
            f"cat={self.highlight_category!r} detail={self.highlight_detail!r}>"
        )


# ---------------------------------------------------------------------------
# Compatibility aliases
# ---------------------------------------------------------------------------
# BUG-IMPORT-001 (Build 63-fix):
#   scraper_service.py imports 'ScrapingLogs' (plural).
#   The ORM class is defined as 'ScrapingLog' (singular).
#   This alias resolves the ImportError without renaming the class or altering
#   any schema definition.  Both names now reference the same ORM class.
ScrapingLogs = ScrapingLog
