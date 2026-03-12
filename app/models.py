"""
models.py — BookingScraper Pro v6.0.0 build 50
===============================================
Cambios estructurales v50:

  STRUCT-001 : HotelDescription — nueva tabla para descriptions multiidioma.
               hotels.description eliminado y movido a hotels_description.
  STRUCT-002 : hotels.photos eliminado — datos duplicados con image_downloads.
  STRUCT-003 : hotels.review_count_schema renombrado a hotels.review_count
               (el campo review_count anterior era scraper-regex, siempre NULL).
  STRUCT-004 : hotels.address eliminado — campo muerto (siempre NULL);
               street_address (JSON-LD) cubre la misma información.
  BUG-EXTR-001: review_score ahora se asigna correctamente (antes siempre NULL).
  BUG-EXTR-002: amenities ahora usa el selector actualizado de Booking.com React.
  BUG-EXTR-003: review_count usa JSON-LD reviewCount (language-independent).
  BUG-EXTR-006: city/country usan JSON-LD en lugar del breadcrumb completo.
  BUG-EXTR-007: star_rating normalizado ÷2 (Booking.com usa escala 0-10).
  BUG-LOAD-001: load_urls.py ON CONFLICT ahora actualiza external_ref.

Fixes heredados (v49 y anteriores):
  BUG-DESC-001  : Cross-contamination de description — sesiones thread-safe.
  BUG-IMG-401   : URLs de imágenes preservan parámetro k= (auth token).
  BUG-IMG-SCHEMA: image_downloads incluye id_photo / category.
  NEW-TABLE-001 : image_data — metadatos completos de fotos.
  BUG-003/103   : FK de ScrapingLog via trigger (partitioned table).
  BUG-007/012   : version_id — optimistic locking.
  BUG-016       : URLLanguageStatus check incluye todos los estados válidos.
  BUG-019       : SystemMetrics time-series indexes.
  Platform      : Windows 11 / PostgreSQL 15+ / psycopg v3.
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

    external_ref: ID numérico del CSV origen (e.g. 1001, 1002...).
    BUG-LOAD-001: load_urls.py ahora usa ON CONFLICT DO UPDATE para garantizar
                  que external_ref se guarda incluso en re-cargas de CSV.
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
    hotel_id_booking: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending", index=True
    )
    priority: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=5)
    retry_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    max_retries: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=3)
    last_error: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
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
            "status IN ('pending','processing','done','error','skipped')",
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

    v50 — cambios estructurales:
      - description    : ELIMINADO → movido a HotelDescription (STRUCT-001)
      - photos         : ELIMINADO → duplicado con image_downloads (STRUCT-002)
      - address        : ELIMINADO → campo muerto, usar street_address (STRUCT-004)
      - review_count   : RENOMBRADO desde review_count_schema (JSON-LD, fiable)
                         El campo anterior review_count (regex, siempre NULL) se elimina.

    Campos schema.org / JSON-LD (NEW-COLS-001, v49):
      main_image_url    — Hotel.image
      short_description — Hotel.description (resumen corto)
      rating_value      — aggregateRating.ratingValue
      best_rating       — aggregateRating.bestRating
      review_count      — aggregateRating.reviewCount (JSON-LD, renombrado de review_count_schema)
      street_address    — address.streetAddress
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
    city: Mapped[Optional[str]] = mapped_column(Text, nullable=True, index=True)
    country: Mapped[Optional[str]] = mapped_column(Text, nullable=True, index=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    star_rating: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True,
        comment="Estrellas normalizadas 0-5 (valor raw Booking ÷ 2)"
    )
    review_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # STRUCT-003: review_count = reviewCount de JSON-LD (antes review_count_schema)
    # El antiguo campo review_count (regex scraper, siempre NULL) fue eliminado.
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

    # JSONB columns — callable default prevents shared mutable state (SCRAP-BUG-007)
    amenities: Mapped[Optional[List]] = mapped_column(JSONB, nullable=True, default=list,
        comment="Lista de servicios del hotel extraída del bloque de instalaciones")
    room_types: Mapped[Optional[List]] = mapped_column(JSONB, nullable=True, default=list)
    policies: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True, default=dict)
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
        # BUG-STARRATING-002: Booking.com usa escala 0-10, normalizado a 0-5 en extractor
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
        Index("ix_hotels_city_country", "city", "country"),
        Index("ix_hotels_created_at", "created_at"),
        Index("ix_hotels_amenities_gin", "amenities", postgresql_using="gin"),
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

    Estructura:
      hotel_id  — FK a hotels.id
      url_id    — FK a url_queue.id (redundante pero útil para queries sin JOIN a hotels)
      language  — código ISO 639-1 del idioma
      description — texto completo extraído del HTML
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
        # Índice GIN full-text (opcional, activar si se requiere búsqueda textual)
        # Index("ix_hdesc_desc_gin", "description", postgresql_using="gin",
        #       postgresql_ops={"description": "to_tsvector('simple', description)"}),
    )

    def __repr__(self) -> str:
        return (
            f"<HotelDescription hotel_id={self.hotel_id} lang={self.language} "
            f"len={len(self.description or '')}>"
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
    Creado por migration_v50.sql.
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
