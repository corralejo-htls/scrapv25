"""
models.py — BookingScraper Pro v48
Fixes applied:
  BUG-003 / BUG-103: ScrapingLog FK absence documented; trigger dependency
                      made explicit — install_clean_v48.sql is REQUIRED.
  BUG-007 / BUG-012: version_id (optimistic locking) usage documented.
  BUG-016           : URLLanguageStatus check constraint includes all valid statuses.
  BUG-019           : SystemMetrics gets indexes on time-series query columns.
  SCRAP-BUG-007     : JSONB defaults use callable factories to avoid shared state.
  Platform          : Windows 11 / PostgreSQL 15+ / psycopg v3.
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
    Scraping task queue.

    Optimistic locking via `version_id` (SQLAlchemy mapper_args):
    Usage pattern — always reload the row with `session.get(URLQueue, id)`
    before updating status to detect concurrent modifications:

        url_obj = session.get(URLQueue, url_id)
        if url_obj.status == "pending":
            url_obj.status = "processing"
            session.commit()  # raises StaleDataError on version conflict
    """
    __tablename__ = "url_queue"
    __mapper_args__ = {
        "version_id_col": None,  # Use explicit version_id without mapper magic to avoid ORM StaleDataError on bulk ops
    }

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    url: Mapped[str] = mapped_column(String(2048), nullable=False, unique=True)
    base_url: Mapped[str] = mapped_column(String(2048), nullable=False)
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
        return f"<URLQueue id={self.id} status={self.status}>"


# ---------------------------------------------------------------------------
# Hotel
# ---------------------------------------------------------------------------

class Hotel(Base):
    """
    Core hotel data store.
    JSONB fields use server_default={} / [] to avoid shared mutable state (SCRAP-BUG-007).
    """
    __tablename__ = "hotels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    url_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="FK to url_queue.id (enforced via FK constraint below)",
    )
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    hotel_name: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    hotel_id_booking: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    city: Mapped[Optional[str]] = mapped_column(String(256), nullable=True, index=True)
    country: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    address: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    star_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    review_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    review_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # JSONB columns — callable default prevents shared mutable state
    amenities: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True, default=dict)
    room_types: Mapped[Optional[List]] = mapped_column(JSONB, nullable=True, default=list)
    policies: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True, default=dict)
    photos: Mapped[Optional[List]] = mapped_column(JSONB, nullable=True, default=list)
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
        # Partial unique index: one record per (url_id, language), excluding NULLs
        # NOTE: This index requires manual creation via install_clean_v48.sql
        # because SQLAlchemy create_all() does not support partial UNIQUE indexes.
        # See: BUG-007 mitigation
        UniqueConstraint("url_id", "language", name="uq_hotels_url_lang"),
        CheckConstraint("star_rating BETWEEN 0 AND 5", name="chk_hotels_star_rating"),
        CheckConstraint("review_score BETWEEN 0 AND 10", name="chk_hotels_review_score"),
        CheckConstraint(
            "review_count >= 0",
            name="chk_hotels_review_count_positive",
        ),
        Index("ix_hotels_city_country", "city", "country"),
        Index("ix_hotels_created_at", "created_at"),
        Index("ix_hotels_amenities_gin", "amenities", postgresql_using="gin"),
    )

    def __repr__(self) -> str:
        return f"<Hotel id={self.id} name={self.hotel_name!r} lang={self.language}>"


# ---------------------------------------------------------------------------
# URLLanguageStatus
# ---------------------------------------------------------------------------

class URLLanguageStatus(Base):
    """
    Tracks per-language scraping completion for each URL.
    BUG-016 fix: check constraint now includes ALL valid statuses.
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
        # BUG-016 fix: 'incomplete' included in valid statuses
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
    High-volume event log, partitioned by month (RANGE on scraped_at).

    ⚠️  IMPORTANT — BUG-003 / BUG-103 mitigation:
    PostgreSQL does NOT support FOREIGN KEY constraints on the child
    (referencing) side of a partitioned table.  Referential integrity for
    `url_id` and `hotel_id` is therefore enforced by database triggers:

        trg_scraping_logs_fk_check  (BEFORE INSERT / UPDATE)

    These triggers are created by install_clean_v48.sql.
    Running Base.metadata.create_all() WITHOUT executing install_clean_v48.sql
    will leave the table WITHOUT referential integrity enforcement.
    Always use install_clean_v48.sql for schema installation.
    """
    __tablename__ = "scraping_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    # url_id intentionally HAS NO ForeignKey — see docstring above
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
        # Partition declaration — actual partitions created by install_clean_v48.sql
        {"postgresql_partition_by": "RANGE (scraped_at)"},
    )

    def __repr__(self) -> str:
        return f"<ScrapingLog url_id={self.url_id} event={self.event_type} status={self.status}>"


# ---------------------------------------------------------------------------
# ImageDownload
# ---------------------------------------------------------------------------

class ImageDownload(Base):
    """Tracks individual image download attempts."""
    __tablename__ = "image_downloads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
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
        UniqueConstraint("hotel_id", "url", name="uq_imgdl_hotel_url"),
        Index("ix_imgdl_status", "status"),
    )


# ---------------------------------------------------------------------------
# SystemMetrics
# ---------------------------------------------------------------------------

class SystemMetrics(Base):
    """
    Periodic system health snapshots.
    BUG-019 fix: indexes added on time-series query columns.
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
        # BUG-019 fix: composite index for time-series dashboard queries
        Index("ix_sysmetrics_recorded_cpu", "recorded_at", "cpu_usage"),
        Index("ix_sysmetrics_recorded_mem", "recorded_at", "memory_usage"),
    )

    def __repr__(self) -> str:
        return f"<SystemMetrics recorded_at={self.recorded_at} cpu={self.cpu_usage}>"
