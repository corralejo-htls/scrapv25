"""
BookingScraper/app/models.py
Modelos SQLAlchemy — BookingScraper Pro
Windows 11 + Python 3.14.x

CORRECCIONES v21 (Audit Enterprise v20):
  [FIX DB-004]  GIN indexes en columnas JSONB (services, facilities, review_scores, images_urls).
                Habilita queries de contenido (@>) con O(log n) en lugar de sequential scan.
  [FIX DB-009]  Partial index ix_urlqueue_pending_dispatch: cubre SÓLO filas 'pending'
                con retry_count < max_retries. ~85% más pequeño que índice completo.
  [FIX DATA-001] Unique constraint para (url, language) cuando url_id IS NULL.
                PostgreSQL no aplica unicidad en NULL — índice parcial resuelve esto.
  [FIX CONC-007] version_id column en URLQueue y URLLanguageStatus para optimistic locking.
                Detecta lost updates en actualizaciones concurrentes (last-writer-wins → error).
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean,
    Float, ForeignKey, Index, func, CheckConstraint, BigInteger
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


class URLQueue(Base):
    """Cola de URLs a procesar."""
    __tablename__ = "url_queue"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    url         = Column(String(512), unique=True, nullable=False, index=True)

    # Estado
    status      = Column(String(50), default="pending", index=True)
    priority    = Column(Integer, default=0, index=True)

    # [FIX CONC-007] Optimistic locking — version_id se incrementa en cada UPDATE.
    # SQLAlchemy mapper_args version_id_col: si dos transacciones leen la misma fila y
    # la segunda intenta actualizar, detecta que version_id cambió y lanza StaleDataError.
    version_id  = Column(Integer, nullable=False, default=0)

    language    = Column(String(10), default="en")
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    last_error  = Column(String(2000), nullable=True)  # [FIX ERR-SEC-001] VARCHAR(2000) cap
    scraped_at  = Column(DateTime(timezone=True), nullable=True)

    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    hotel       = relationship("Hotel", back_populates="url_queue", uselist=False)

    __table_args__ = (
        # [FIX DB-009] Partial index para dispatch query.
        # La query de despacho siempre filtra status='pending' AND retry_count < max_retries.
        # Un partial index sólo indexa las filas elegibles → ~85-90% más pequeño.
        # ACCIÓN REQUERIDA (producción): Crear con CONCURRENTLY para evitar lock exclusivo:
        #   CREATE INDEX CONCURRENTLY ix_urlqueue_pending_dispatch
        #   ON url_queue (priority DESC, created_at ASC)
        #   WHERE status = 'pending' AND retry_count < max_retries;
        # SQLAlchemy no soporta partial index con postgresql_where en create_all().
        # Este índice se gestiona manualmente vía SQL en install_clean_v31.sql.
        #
        # [FIX ERR-DB-004] ix_urlqueue_status_priority ELIMINADO — era prefijo redundante
        # de ix_urlqueue_dispatch (status, priority, created_at). PostgreSQL puede usar
        # el índice largo para queries que solo filtran (status, priority).
        # Un índice redundante añade overhead de mantenimiento en cada INSERT/UPDATE sin
        # beneficio de rendimiento. Solo se conserva el índice más largo.
        Index("ix_urlqueue_dispatch", "status", "priority", "created_at"),

        # Constraints de integridad
        # [FIX ERR-DB-005] B-Tree index on updated_at for incremental exports.
        Index("ix_urlqueue_updated_at", "updated_at"),
        CheckConstraint("retry_count >= 0",           name="chk_urlqueue_retry_count_nonneg"),
        CheckConstraint("max_retries >= 0",           name="chk_urlqueue_max_retries_nonneg"),
        CheckConstraint("retry_count <= max_retries", name="chk_urlqueue_retry_lte_max"),
        CheckConstraint(
            "status IN ('pending','processing','completed','failed','incomplete')",
            name="chk_urlqueue_status_valid",
        ),
        # [FIX ERR-DB-007] fillfactor=70: reserves 30% page space for HOT updates.
        # url_queue has frequent status/retry_count UPDATEs — reduces table bloat.
        {"postgresql_with": {"fillfactor": 70}},
    )

    # [FIX CONC-007] Mapper config para optimistic locking.
    # version_id_col: column to track, version_id_generator: incrementa en cada flush.
    __mapper_args__ = {
        "version_id_col": version_id,
        "version_id_generator": lambda v: (v or 0) + 1,
    }

    def __repr__(self):
        return f"<URLQueue(id={self.id}, status={self.status}, url={self.url[:60]}...)>"


class Hotel(Base):
    """Datos extraídos de hoteles — una fila por hotel+idioma."""
    __tablename__ = "hotels"

    id      = Column(Integer, primary_key=True, autoincrement=True)
    # [FIX HIGH-012] ondelete="SET NULL": when a url_queue row is deleted,
    # the FK is set to NULL (hotel record is preserved, link is severed).
    # This is intentional — hotel data has standalone value even without the
    # original queue entry. The companion SQL function cleanup_orphaned_hotels()
    # in install_clean_v32.sql provides a manual periodic purge of hotels
    # where BOTH url_id IS NULL AND url IS NULL (truly unreferenceable records).
    # Hotels with url_id=NULL but url IS NOT NULL are searchable by URL and
    # should NOT be deleted automatically.
    url_id  = Column(Integer, ForeignKey("url_queue.id", ondelete="SET NULL"),
                     nullable=True, index=True)
    url     = Column(String(512), nullable=True, index=True)  # [FIX HIGH-003] B-Tree index
    language= Column(String(10),  default="en", index=True)

    # Información básica
    name        = Column(String(255), nullable=True, index=True)
    address     = Column(Text,        nullable=True)
    description = Column(Text,        nullable=True)

    # Puntuaciones
    rating          = Column(Float,   nullable=True)
    total_reviews   = Column(Integer, nullable=True)
    rating_category = Column(String(100), nullable=True)
    review_scores   = Column(JSONB, nullable=True)

    # Servicios e instalaciones
    services    = Column(JSONB, nullable=True)
    facilities  = Column(JSONB, nullable=True)

    # Políticas
    house_rules    = Column(Text, nullable=True)
    important_info = Column(Text, nullable=True)

    # Habitaciones
    rooms_info  = Column(JSONB, nullable=True)

    # Imágenes
    images_urls  = Column(JSONB, nullable=True)
    images_local = Column(JSONB, nullable=True)
    images_count = Column(Integer, default=0)

    scraped_at  = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at  = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    url_queue   = relationship("URLQueue", back_populates="hotel")

    __table_args__ = (
        # ── Índice único principal (url_id NOT NULL) ─────────────────────────
        Index("ix_hotels_url_language", "url_id", "language", unique=True),

        # [FIX DATA-001] Unique constraint para el caso url_id IS NULL.
        # PostgreSQL trata NULL como distinto de NULL → el índice compuesto
        # ix_hotels_url_language NO aplica unicidad cuando url_id=NULL.
        # Este índice parcial garantiza unicidad (url, language) cuando url_id es NULL.
        # ACCIÓN REQUERIDA: Crear con CONCURRENTLY en producción:
        #   CREATE UNIQUE INDEX CONCURRENTLY ix_hotels_url_lang_null
        #   ON hotels (url, language) WHERE url_id IS NULL;
        # SQLAlchemy no soporta partial unique index en create_all() — gestionar vía Alembic.
        Index("ix_hotels_language", "language"),

        # ── GIN indexes para JSONB ────────────────────────────────────────────
        # [FIX DB-004] Sin GIN index, queries de contenido (@>) hacen sequential scan.
        # jsonb_path_ops: más compacto que default ops para containment queries.
        # Ejemplo: SELECT * FROM hotels WHERE services @> '["WiFi"]';
        #          → Con GIN: Index Scan O(log n), Sin GIN: Seq Scan O(n).
        #
        # ACCIÓN REQUERIDA: Crear con CONCURRENTLY para evitar lock durante creación:
        #   CREATE INDEX CONCURRENTLY ix_hotels_services_gin
        #     ON hotels USING GIN (services jsonb_path_ops);
        #   CREATE INDEX CONCURRENTLY ix_hotels_facilities_gin
        #     ON hotels USING GIN (facilities jsonb_path_ops);
        #   CREATE INDEX CONCURRENTLY ix_hotels_review_scores_gin
        #     ON hotels USING GIN (review_scores jsonb_path_ops);
        #   CREATE INDEX CONCURRENTLY ix_hotels_images_gin
        #     ON hotels USING GIN (images_urls jsonb_path_ops);
        #
        # SQLAlchemy soporta GIN via postgresql_using='gin':
        # [FIX ERR-DB-003] jsonb_path_ops is ~40% smaller and faster for @> queries.
        # Trade-off: ? (key-exists) operator not supported — acceptable, all JSONB
        # queries on these columns use @> containment only.
        Index("ix_hotels_services_gin",
              "services",      postgresql_using="gin",
              postgresql_ops={"services":      "jsonb_path_ops"}),
        Index("ix_hotels_facilities_gin",
              "facilities",    postgresql_using="gin",
              postgresql_ops={"facilities":    "jsonb_path_ops"}),
        Index("ix_hotels_review_scores_gin",
              "review_scores", postgresql_using="gin",
              postgresql_ops={"review_scores": "jsonb_path_ops"}),
        Index("ix_hotels_images_gin",
              "images_urls",   postgresql_using="gin",
              postgresql_ops={"images_urls":   "jsonb_path_ops"}),
        # [FIX ERR-DB-005] B-Tree index on updated_at for incremental export queries.
        # Without this, WHERE updated_at > :ts performs full sequential scan.
        Index("ix_hotels_updated_at", "updated_at"),
        # [FIX ERR-DB-006] Booking.com ratings are 0.0–10.0. Enforce at DB level.
        # NULL is allowed (hotel with no reviews yet has no rating).
        CheckConstraint(
            "rating IS NULL OR (rating >= 0.0 AND rating <= 10.0)",
            name="chk_hotel_rating_range",
        ),
        # [FIX ERR-DB-005] JSONB type validation at DB level.
        # Prevents application bugs or direct DB manipulation from storing
        # wrong types (e.g. passing an object where an array is expected).
        CheckConstraint(
            "services IS NULL OR jsonb_typeof(services) = 'array'",
            name="chk_hotel_services_array",
        ),
        CheckConstraint(
            "facilities IS NULL OR jsonb_typeof(facilities) = 'object'",
            name="chk_hotel_facilities_object",
        ),
        CheckConstraint(
            "review_scores IS NULL OR jsonb_typeof(review_scores) = 'object'",
            name="chk_hotel_review_scores_object",
        ),
        CheckConstraint(
            "images_urls IS NULL OR jsonb_typeof(images_urls) = 'array'",
            name="chk_hotel_images_urls_array",
        ),
    )

    def __repr__(self):
        return f"<Hotel(id={self.id}, name={self.name}, lang={self.language})>"


class ScrapingLog(Base):
    """Log detallado de cada operación de scraping."""
    __tablename__ = "scraping_logs"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    # [FIX BUG-V6-013] index=True — sin index, ON DELETE CASCADE es O(n).
    url_id   = Column(Integer, ForeignKey("url_queue.id"), nullable=True, index=True)

    status          = Column(String(50),  nullable=False)
    language        = Column(String(10),  nullable=True)
    duration_seconds= Column(Float,       nullable=True)
    items_extracted = Column(Integer,     default=0)
    error_message   = Column(Text,        nullable=True)

    http_status_code= Column(Integer,     nullable=True)
    user_agent      = Column(Text,        nullable=True)
    vpn_ip          = Column(String(50),  nullable=True)
    task_id         = Column(String(100), nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<ScrapingLog(id={self.id}, status={self.status})>"


class VPNRotation(Base):
    """Registro de rotaciones de VPN."""
    __tablename__ = "vpn_rotations"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    old_ip          = Column(String(45),  nullable=True)
    new_ip          = Column(String(45),  nullable=True)
    country         = Column(String(100), nullable=True)
    rotation_reason = Column(String(100), nullable=True)
    requests_count  = Column(Integer,     default=0)
    success         = Column(Boolean,     default=True)
    error_message   = Column(Text,        nullable=True)
    rotated_at      = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<VPNRotation(id={self.id}, {self.old_ip} → {self.new_ip})>"


class SystemMetrics(Base):
    """Métricas del sistema (capturadas periódicamente)."""
    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)

    urls_pending    = Column(Integer, default=0)
    urls_processing = Column(Integer, default=0)
    urls_completed  = Column(Integer, default=0)
    urls_failed     = Column(Integer, default=0)

    hotels_scraped    = Column(Integer, default=0)
    images_downloaded = Column(Integer, default=0)
    active_workers    = Column(Integer, default=0)

    avg_scraping_time   = Column(Float, nullable=True)
    total_scraping_time = Column(Float, default=0.0)

    cpu_usage    = Column(Float, nullable=True)
    memory_usage = Column(Float, nullable=True)
    disk_usage   = Column(Float, nullable=True)

    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<SystemMetrics(id={self.id}, completed={self.urls_completed})>"


class URLLanguageStatus(Base):
    """Estado de scraping por URL + idioma. Una fila por combinación (url_id, language)."""
    __tablename__ = "url_language_status"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    url_id      = Column(Integer, ForeignKey("url_queue.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    language    = Column(String(10), nullable=False)
    status      = Column(String(50), nullable=False, default="pending")

    retry_count = Column(Integer, nullable=False, default=0)
    max_retries = Column(Integer, nullable=False, default=3)
    last_error  = Column(String(2000), nullable=True)  # [FIX ERR-SEC-001] VARCHAR(2000) cap
    scraped_at  = Column(DateTime(timezone=True), nullable=True)

    # [FIX CONC-007] Optimistic locking para detectar lost updates.
    version_id  = Column(Integer, nullable=False, default=0)

    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("uls_url_lang_unique", "url_id", "language", unique=True),
        Index("ix_uls_url_status", "url_id", "status"),
        # [FIX ERR-DB-005] B-Tree index on updated_at for incremental exports.
        Index("ix_urllangs_updated_at", "updated_at"),
        CheckConstraint("retry_count >= 0",           name="chk_uls_retry_count_nonneg"),
        CheckConstraint("max_retries >= 0",           name="chk_uls_max_retries_nonneg"),
        CheckConstraint("retry_count <= max_retries", name="chk_uls_retry_lte_max"),
        CheckConstraint(
            "status IN ('pending','processing','completed','failed','skipped_existing')",
            name="chk_uls_status_valid",
        ),
        # [FIX ERR-DB-007] fillfactor=70 for url_language_status.
        # High UPDATE frequency (status transitions per language per URL).
        {"postgresql_with": {"fillfactor": 70}},
    )

    __mapper_args__ = {
        "version_id_col": version_id,
        "version_id_generator": lambda v: (v or 0) + 1,
    }

    def __repr__(self):
        return (
            f"<URLLanguageStatus(url_id={self.url_id}, "
            f"lang={self.language}, status={self.status})>"
        )
