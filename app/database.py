"""
database.py — BookingScraper Pro v6.0.0 Build 127
VERSION-RECONCILE-001 (Build 127): cabecera sincronizada con el BUILD_VERSION canonico (app/__init__.py = 127). Sin cambios funcionales.
Fixes applied:
  SCRAP-BUG-004 / BUG-001: Lazy engine creation — no module-level URL construction.
  BUG-006               : SET LOCAL uses parameterised-safe integer cast.
  BUG-010               : execute_with_retry logs underlying exception details.
  BUG-015               : get_pool_status preserves full exception context.
  SCRAP-BUG-005         : get_readonly_db — intento de fix con BEGIN READ ONLY.
  BUG-DB-READONLY-001   : (Build 120) get_readonly_db usaba "BEGIN READ ONLY", que
                           es incorrecto en SQLAlchemy 2.0 + psycopg3. El autobegin
                           de SQLAlchemy emite BEGIN antes del primer execute(), por
                           lo que "BEGIN READ ONLY" llega como segundo statement y
                           PostgreSQL responde "WARNING: there is already a transaction
                           in progress" — ignorando el modo read-only. Fix: sustituir
                           por "SET TRANSACTION READ ONLY", que es válido dentro de
                           una transacción activa antes de cualquier operación de datos.
  Platform              : Windows 11 connection pool limits respected.
"""

from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from typing import Any, Dict, Generator, Iterator, Optional

from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import InterfaceError, OperationalError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool, NullPool

from app.config import get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Engine singleton — lazy, thread-safe via GIL for assignment
# ---------------------------------------------------------------------------
_engine: Optional[Any] = None
_SessionFactory: Optional[Any] = None


def _get_engine() -> Any:
    """
    Return (or create) the SQLAlchemy engine.
    Lazy creation prevents import-time failures — SCRAP-BUG-004 fix.
    """
    global _engine, _SessionFactory
    if _engine is None:
        cfg = get_settings()
        # Windows 11: effective_io_concurrency=1, conservative pool sizing
        _engine = create_engine(
            cfg.database_url,
            poolclass=QueuePool,
            pool_size=cfg.DB_POOL_SIZE,
            max_overflow=cfg.DB_MAX_OVERFLOW,
            pool_timeout=cfg.DB_POOL_TIMEOUT,
            pool_recycle=cfg.DB_POOL_RECYCLE,
            pool_pre_ping=True,           # detect stale connections
            echo=cfg.DEBUG,
            connect_args={
                "connect_timeout": 10,
                "application_name": f"BookingScraper_{cfg.BUILD_VERSION}",
            },
        )

        @event.listens_for(_engine, "connect")
        def _on_connect(dbapi_conn: Any, connection_record: Any) -> None:
            """Set session-level options on new connections."""
            pass  # Placeholder for future per-connection setup

        _SessionFactory = sessionmaker(bind=_engine, expire_on_commit=False)
        logger.info(
            "Database engine created: host=%s db=%s pool_size=%d max_overflow=%d",
            cfg.DB_HOST, cfg.DB_NAME, cfg.DB_POOL_SIZE, cfg.DB_MAX_OVERFLOW,
        )
    return _engine


def get_session_factory() -> Any:
    """Return the session factory (creates engine on first call)."""
    _get_engine()
    return _SessionFactory


# ---------------------------------------------------------------------------
# Session context managers
# ---------------------------------------------------------------------------

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Standard read-write session with autocommit=False."""
    factory = get_session_factory()
    session: Session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def get_readonly_db() -> Generator[Session, None, None]:
    """
    Read-only session.

    BUG-DB-READONLY-001-FIX (Build 120):
    El fix anterior (SCRAP-BUG-005) usaba 'BEGIN READ ONLY' como primer statement.
    Sin embargo, SQLAlchemy 2.0 con psycopg3 activa autobegin: al llamar
    session.execute() por primera vez, SQLAlchemy emite BEGIN implícitamente.
    Esto hace que 'BEGIN READ ONLY' llegue a PostgreSQL como segundo statement,
    desencadenando:
        WARNING: there is already a transaction in progress
    PostgreSQL ignora el segundo BEGIN, dejando la transacción en modo read-write.

    Fix correcto: usar 'SET TRANSACTION READ ONLY', que es válido dentro de una
    transacción activa (después del BEGIN implícito) siempre que se ejecute ANTES
    de cualquier operación de datos (SELECT/DML). PostgreSQL acepta SET TRANSACTION
    como primer statement post-BEGIN y aplica el modo read-only correctamente.

    Nota: get_readonly_db no está importada en ningún módulo activo (verificado
    Build 120). El bug tenía impacto en producción = 0. Fix incluido por
    corrección arquitectónica y para uso futuro seguro.
    """
    factory = get_session_factory()
    session: Session = factory()
    try:
        # BUG-DB-READONLY-001-FIX (Build 120):
        # SET TRANSACTION READ ONLY — ejecutado DESPUÉS del BEGIN implícito de autobegin,
        # ANTES de cualquier operación de datos. Válido en PostgreSQL 9.1+.
        # Reemplaza 'BEGIN READ ONLY' que causaba "already in transaction" warning.
        session.execute(text("SET TRANSACTION READ ONLY"))
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def get_serializable_db() -> Generator[Session, None, None]:
    """SERIALIZABLE isolation for critical consistency operations."""
    factory = get_session_factory()
    session: Session = factory()
    try:
        session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def get_olap_db(timeout_ms: Optional[int] = None) -> Generator[Session, None, None]:
    """
    Session optimised for long-running OLAP queries.
    BUG-006 fix: timeout cast to int prevents any injection via f-string.
    Uses SET LOCAL so the timeout applies only to this transaction.
    """
    factory = get_session_factory()
    cfg = get_settings()
    timeout = int(timeout_ms if timeout_ms is not None else cfg.STMT_TIMEOUT_OLAP_MS)
    session: Session = factory()
    try:
        # SET LOCAL is transaction-scoped; safe because timeout is int-cast
        session.execute(text(f"SET LOCAL statement_timeout = {timeout}"))
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ---------------------------------------------------------------------------
# Retry helper
# ---------------------------------------------------------------------------

def execute_with_retry(
    session: Session,
    stmt: Any,
    params: Optional[Dict[str, Any]] = None,
    max_retries: int = 3,
    base_delay: float = 0.5,
) -> Any:
    """
    Execute a statement with exponential-backoff retry for transient errors.
    BUG-010 fix: logs full exception details including type and message.
    """
    params = params or {}
    last_exc: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            result = session.execute(stmt, params)
            return result
        except (OperationalError, InterfaceError) as exc:
            last_exc = exc
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning(
                "DB execute attempt %d/%d failed [%s: %s]. Retrying in %.1fs.",
                attempt, max_retries,
                type(exc).__name__,   # BUG-010: include exception type
                str(exc),             # BUG-010: include exception message
                delay,
            )
            session.rollback()
            time.sleep(delay)

    logger.error(
        "All %d DB execute attempts failed. Last error: [%s] %s",
        max_retries, type(last_exc).__name__, str(last_exc),
    )
    raise last_exc


# ---------------------------------------------------------------------------
# Health / diagnostics
# ---------------------------------------------------------------------------

def test_connection() -> bool:
    """Verify database connectivity. Returns True if reachable."""
    try:
        engine = _get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.error("Database connectivity test failed: [%s] %s", type(exc).__name__, exc)
        return False


def get_pool_status() -> Dict[str, Any]:
    """
    Return connection pool statistics.
    BUG-015 fix: preserves full exception context, not just type name.
    """
    try:
        engine = _get_engine()
        pool = engine.pool
        return {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "invalid": pool.status(),
        }
    except Exception as exc:
        # BUG-015 fix: include message, not just type name
        return {
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }


def log_pool_status() -> None:
    """Log current pool status at INFO level (utility for monitoring scripts)."""
    status = get_pool_status()
    if "error_type" in status:
        logger.error("Pool status unavailable: [%s] %s", status["error_type"], status.get("error_message"))
    else:
        logger.info(
            "Pool status — size: %s, checked_in: %s, checked_out: %s, overflow: %s",
            status.get("size"), status.get("checked_in"),
            status.get("checked_out"), status.get("overflow"),
        )


# ---------------------------------------------------------------------------
# Teardown
# ---------------------------------------------------------------------------

def dispose_engine() -> None:
    """Dispose engine and reset singleton (use on application shutdown)."""
    global _engine, _SessionFactory
    if _engine is not None:
        _engine.dispose()
        _engine = None
        _SessionFactory = None
        logger.info("Database engine disposed.")
