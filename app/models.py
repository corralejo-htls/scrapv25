"""
BookingScraper Pro v6.0 - SQLAlchemy ORM Models
================================================
Platform : Windows 11 + PostgreSQL 15-18
ORM      : SQLAlchemy 2.x  |  Driver: psycopg (v3)

Corrections Applied (v46):
- BUG-002 : ix_hotels_url_lang_null declared as Index() with postgresql_where —
            will be created by create_all() and by install_clean_v46.sql.
- BUG-005 : version_id optimistic locking is now backed by DB trigger.
- BUG-012 : ScrapingLog FK gap fully documented; trigger enforces RI instead.
- BUG-014 : MAX_ERROR_LEN imported from config (single source of truth).
- BUG-021 : ScrapingLog partition FK absence explained in class docstring.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger, CheckConstraint, Column, DateTime, Index,
    Integer, Numeric, SmallInteger, String, Text, UniqueConstraint,
    func, text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase

# BUG-014 FIX: single source of truth
from app.config import MAX_ERROR_LEN, MAX_URL_LEN
MAX_NAME_LEN: int = 500


class Base(DeclarativeBase):
    pass


# ─────────────────────────────────────────────────────────────────────────────
class URLQueue(Base):
    """Scraping task queue — one row per (URL, language) job."""
    __tablename__ = "url_queue"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url           = Column(String(MAX_URL_LEN), nullable=False)
    language      = Column(String(10), nullable=False, default="en")
    status        = Column(String(30), nullable=False, default="pending")
    priority      = Column(SmallInteger, nullable=False, default=5)
    retry_count   = Column(SmallInteger, nullable=False, default=0)
    max_retries   = Column(SmallInteger, nullable=False, default=3)
    error_message = Column(String(MAX_ERROR_LEN))
    claimed_by    = Column(String(255))
    claimed_at    = Column(DateTime(timezone=True))
    completed_at  = Column(DateTime(timezone=True))
    created_at    = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    version_id    = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        CheckConstraint("status IN ('pending','processing','done','error','skipped')", name="ck_urlq_status"),
        CheckConstraint("priority BETWEEN 1 AND 10",  name="ck_urlq_priority"),
        CheckConstraint("retry_count >= 0",            name="ck_urlq_retry"),
        Index("ix_url_queue_status_priority", "status", "priority", "created_at",
              postgresql_where=text("status = 'pending'")),
        Index("ix_url_queue_url", "url"),
    )

    def __repr__(self) -> str:
        return f"<URLQueue {self.id} {self.url!r} lang={self.language} status={self.status}>"


# ─────────────────────────────────────────────────────────────────────────────
class URLLanguageStatus(Base):
    """Per-language completion tracking for each queued URL."""
    __tablename__ = "url_language_status"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url_id        = Column(UUID(as_uuid=True), nullable=False)
    language      = Column(String(10), nullable=False)
    status        = Column(String(30), nullable=False, default="pending")
    attempt_count = Column(SmallInteger, nullable=False, default=0)
    last_error    = Column(String(MAX_ERROR_LEN))
    completed_at  = Column(DateTime(timezone=True))
    created_at    = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    version_id    = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("url_id", "language", name="uq_url_lang_status"),
        CheckConstraint("status IN ('pending','processing','done','error','skipped')", name="ck_uls_status"),
        Index("ix_url_lang_pending", "url_id", "status",
              postgresql_where=text("status IN ('pending','error')")),
    )

    def __repr__(self) -> str:
        return f"<URLLanguageStatus url_id={self.url_id} lang={self.language} status={self.status}>"


# ─────────────────────────────────────────────────────────────────────────────
class Hotel(Base):
    """
    Core hotel data.

    Index notes (BUG-002 FIX):
    - ix_hotels_url_lang_null  : partial UNIQUE (url, language) WHERE url_id IS NULL
      Previously only in a comment — now declared as Index() so create_all() creates it.
    - ix_hotels_url_id_lang    : partial UNIQUE (url_id, language) WHERE url_id IS NOT NULL
    Both are also in install_clean_v46.sql for non-ORM deployments.
    """
    __tablename__ = "hotels"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url          = Column(String(MAX_URL_LEN))
    language     = Column(String(10), nullable=False, default="en")
    url_id       = Column(UUID(as_uuid=True))
    hotel_name   = Column(String(MAX_NAME_LEN))
    hotel_id_ext = Column(String(100))
    star_rating  = Column(Numeric(2, 1))
    review_score = Column(Numeric(3, 1))
    review_count = Column(Integer)
    address      = Column(String(1000))
    city         = Column(String(255))
    country      = Column(String(100))
    latitude     = Column(Numeric(10, 7))
    longitude    = Column(Numeric(10, 7))
    amenities    = Column(JSONB, nullable=False, default=list)
    room_types   = Column(JSONB, nullable=False, default=list)
    policies     = Column(JSONB, nullable=False, default=dict)
    photos       = Column(JSONB, nullable=False, default=list)
    raw_data     = Column(JSONB, nullable=False, default=dict)
    scrape_status  = Column(String(30), nullable=False, default="pending")
    scrape_engine  = Column(String(30))
    error_message  = Column(String(MAX_ERROR_LEN))
    scraped_at     = Column(DateTime(timezone=True))
    created_at     = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at     = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    version_id     = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        CheckConstraint("scrape_status IN ('pending','done','error','partial')", name="ck_hotels_status"),
        CheckConstraint("scrape_engine IS NULL OR scrape_engine IN ('cloudscraper','selenium','manual')", name="ck_hotels_engine"),
        CheckConstraint("star_rating  IS NULL OR star_rating  BETWEEN 0 AND 5",  name="ck_hotels_stars"),
        CheckConstraint("review_score IS NULL OR review_score BETWEEN 0 AND 10", name="ck_hotels_score"),
        # BUG-002 FIX: partial unique indexes as proper Index() objects
        Index("ix_hotels_url_lang_null", "url", "language", unique=True,
              postgresql_where=text("url_id IS NULL")),
        Index("ix_hotels_url_id_lang", "url_id", "language", unique=True,
              postgresql_where=text("url_id IS NOT NULL")),
        Index("ix_hotels_url", "url", postgresql_where=text("url IS NOT NULL")),
        Index("ix_hotels_city_country", "city", "country"),
        Index("ix_hotels_scrape_status", "scrape_status",
              postgresql_where=text("scrape_status != 'done'")),
        # GIN indexes for JSONB (BUG-007 FIX)
        Index("ix_hotels_amenities_gin",  "amenities",  postgresql_using="gin"),
        Index("ix_hotels_room_types_gin", "room_types", postgresql_using="gin"),
    )

    def __repr__(self) -> str:
        return f"<Hotel {self.id} {self.hotel_name!r} lang={self.language}>"


# ─────────────────────────────────────────────────────────────────────────────
class ScrapingLog(Base):
    """
    High-volume event log — physically stored in monthly partitions.

    BUG-012 / BUG-021 FIX:
    PostgreSQL does NOT support FOREIGN KEY constraints on partitioned tables
    (the referencing side).  scraping_logs is RANGE-partitioned by created_at,
    so url_id and hotel_id intentionally have no SQLAlchemy ForeignKey().
    Referential integrity is enforced by:
      • DB trigger : trg_scraping_logs_fk_check  (install_clean_v46.sql)
      • App layer  : ScraperService validates ids before inserting log rows.
    """
    __tablename__ = "scraping_logs"

    id          = Column(BigInteger, primary_key=True, autoincrement=True)
    url_id      = Column(UUID(as_uuid=True))   # no FK — see docstring
    hotel_id    = Column(UUID(as_uuid=True))   # no FK — see docstring
    event_type  = Column(String(50), nullable=False)
    engine      = Column(String(30))
    language    = Column(String(10))
    duration_ms = Column(Integer)
    http_status = Column(SmallInteger)
    message     = Column(Text)
    metadata_   = Column("metadata", JSONB, nullable=False, default=dict)
    worker_id   = Column(String(100))
    created_at  = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "event_type IN ("
            "'scrape_start','scrape_done','scrape_error',"
            "'vpn_rotate','vpn_error',"
            "'image_download','image_error',"
            "'queue_claim','queue_release',"
            "'health_check','system_event')",
            name="ck_scraping_logs_event_type",
        ),
        Index("ix_slog_url_id",    "url_id",    postgresql_where=text("url_id IS NOT NULL")),
        Index("ix_slog_hotel_id",  "hotel_id",  postgresql_where=text("hotel_id IS NOT NULL")),
        Index("ix_slog_event",     "event_type","created_at"),
        Index("ix_slog_worker",    "worker_id", "created_at", postgresql_where=text("worker_id IS NOT NULL")),
        {"postgresql_partition_by": "RANGE (created_at)"},
    )

    def __repr__(self) -> str:
        return f"<ScrapingLog id={self.id} event={self.event_type}>"


# ─────────────────────────────────────────────────────────────────────────────
class ImageDownload(Base):
    """Tracks per-hotel image download status to allow idempotent re-runs."""
    __tablename__ = "image_downloads"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id        = Column(UUID(as_uuid=True), nullable=False)
    url             = Column(Text, nullable=False)
    filename        = Column(String(500))
    file_size_bytes = Column(Integer)
    width           = Column(Integer)
    height          = Column(Integer)
    content_type    = Column(String(100))
    status          = Column(String(30), nullable=False, default="pending")
    error_message   = Column(String(MAX_ERROR_LEN))
    downloaded_at   = Column(DateTime(timezone=True))
    created_at      = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("hotel_id", "url", name="uq_img_hotel_url"),
        CheckConstraint("status IN ('pending','done','error','skipped')", name="ck_img_status"),
        Index("ix_img_hotel_status", "hotel_id", "status",
              postgresql_where=text("status != 'done'")),
    )

    def __repr__(self) -> str:
        return f"<ImageDownload hotel={self.hotel_id} status={self.status}>"


# ─────────────────────────────────────────────────────────────────────────────
class SystemConfig(Base):
    """Runtime key-value configuration — allows live tuning without restart."""
    __tablename__ = "system_config"

    key        = Column(String(100), primary_key=True)
    value      = Column(Text, nullable=False)
    description= Column(String(500))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<SystemConfig {self.key!r}={self.value!r}>"
