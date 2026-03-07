"""
BookingScraper Pro v6.0 - Database Connection Module
====================================================
Platform : Windows 11 + PostgreSQL 15-18 + psycopg (v3)
Driver   : psycopg  (NOT psycopg2 — note the difference)

Corrections Applied (v46):
- BUG-001 : Credential validation at module import time, not deferred to engine creation.
- BUG-006 : get_serializable_db() sets isolation level on the connection object
            BEFORE the transaction starts, not via bare SET TRANSACTION.
- BUG-011 : execute_with_retry() distinguishes transient (retryable) vs programming
            errors (non-retryable) so IntegrityError/ProgrammingError are not masked.
- BUG-017 : get_pool_status() has defensive null-handling when pool is uninitialised.
"""

from __future__ import annotations

import logging
import os
import time
from contextlib import contextmanager
from typing import Any, Callable, Generator, Optional, TypeVar

from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import (
    DisconnectionError,
    IntegrityError,
    InterfaceError,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

logger = logging.getLogger(__name__)
T = TypeVar("T")

# ---------------------------------------------------------------------------
# BUG-001 FIX: Validate credentials at IMPORT TIME
# ---------------------------------------------------------------------------

def _get_required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise EnvironmentError(
            f"Required environment variable '{name}' is not set or is empty. "
            f"Ensure your .env file is loaded before importing app.database."
        )
    return value


def _build_database_url() -> str:
    host     = os.environ.get("DB_HOST", "localhost")
    port     = os.environ.get("DB_PORT", "5432")
    name     = os.environ.get("DB_NAME", "bookingscraper")
    user     = _get_required_env("DB_USER")
    password = _get_required_env("DB_PASSWORD")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"


try:
    DATABASE_URL: str = _build_database_url()
except EnvironmentError as _e:
    raise EnvironmentError(
        f"Database configuration failed at module load: {_e}\n"
        "Load your .env file (via python-dotenv or os.environ) BEFORE importing app.database."
    ) from _e


# ---------------------------------------------------------------------------
# Engine — Windows 11 tuned
# ---------------------------------------------------------------------------

def _create_engine_windows():
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size      =int(os.environ.get("DB_POOL_SIZE",    "10")),
        max_overflow   =int(os.environ.get("DB_MAX_OVERFLOW",  "5")),
        pool_timeout   =float(os.environ.get("DB_POOL_TIMEOUT","30")),
        pool_recycle   =int(os.environ.get("DB_POOL_RECYCLE","3600")),
        pool_pre_ping  =True,
        echo           =os.environ.get("DB_ECHO", "false").lower() == "true",
        connect_args   ={"connect_timeout": 10, "options": "-c statement_timeout=30000"},
    )

    @event.listens_for(engine, "connect")
    def _set_search_path(dbapi_conn, _rec):
        cur = dbapi_conn.cursor()
        cur.execute("SET search_path TO public")
        cur.close()

    return engine


engine       = _create_engine_windows()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------------------------
# Context managers
# ---------------------------------------------------------------------------

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Standard READ COMMITTED session."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def get_serializable_db() -> Generator[Session, None, None]:
    """
    REPEATABLE READ session.
    BUG-006 FIX: isolation level set via execution_options on the connection
    object BEFORE the transaction begins (not via bare SET TRANSACTION inside
    an already-active transaction).
    """
    session = SessionLocal()
    try:
        session.connection(execution_options={"isolation_level": "REPEATABLE READ"})
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def get_readonly_db() -> Generator[Session, None, None]:
    """Read-only session — always rolled back, prevents accidental writes."""
    session = SessionLocal()
    try:
        session.execute(text("SET TRANSACTION READ ONLY"))
        yield session
    finally:
        session.rollback()
        session.close()


# ---------------------------------------------------------------------------
# Retry utility
# BUG-011 FIX: separate transient vs fatal exception sets
# ---------------------------------------------------------------------------

_TRANSIENT = (OperationalError, DisconnectionError, InterfaceError)
_FATAL     = (IntegrityError, ProgrammingError)


def execute_with_retry(
    fn: Callable[..., T],
    *args: Any,
    max_retries: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 30.0,
    **kwargs: Any,
) -> T:
    """
    Execute fn(session, *args, **kwargs) with exponential-backoff retry.

    BUG-011 FIX:
    - Only _TRANSIENT errors are retried (OperationalError, DisconnectionError, InterfaceError).
    - _FATAL errors (IntegrityError, ProgrammingError) are raised immediately without retry,
      so programming bugs are never silently swallowed.
    - Re-raises the final exception wrapped in RuntimeError with retry context.
    """
    last_exc: Optional[Exception] = None

    for attempt in range(max_retries + 1):
        try:
            with get_db() as session:
                return fn(session, *args, **kwargs)

        except _FATAL as exc:
            logger.error("Non-retryable DB error (attempt %d): %s", attempt + 1, exc)
            raise

        except _TRANSIENT as exc:
            last_exc = exc
            if attempt >= max_retries:
                break
            delay = min(base_delay * (2 ** attempt), max_delay)
            logger.warning(
                "Transient DB error (attempt %d/%d), retrying in %.1fs: %s",
                attempt + 1, max_retries + 1, delay, exc,
            )
            time.sleep(delay)

    raise RuntimeError(
        f"DB operation failed after {max_retries + 1} attempts"
    ) from last_exc


# ---------------------------------------------------------------------------
# Connection testing
# ---------------------------------------------------------------------------

def test_connection(max_retries: int = 5, base_delay: float = 2.0) -> bool:
    """Verify DB connectivity; differentiate auth failure from timeout."""
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                row = conn.execute(text("SELECT current_database(), version()")).fetchone()
                logger.info("DB connection OK — database: %s", row[0])
                return True
        except OperationalError as exc:
            err = str(exc).lower()
            if any(k in err for k in ("password", "authentication", "pg_hba", "role")):
                logger.error("Auth failure (non-retryable): %s", exc)
                raise
            if attempt < max_retries - 1:
                delay = min(base_delay * (2 ** attempt), 60.0)
                logger.warning("DB connect attempt %d/%d failed, retry in %.1fs", attempt + 1, max_retries, delay)
                time.sleep(delay)
            else:
                logger.error("DB connection failed after %d attempts", max_retries)
                raise
    return False


# ---------------------------------------------------------------------------
# Pool status
# BUG-017 FIX: defensive null-handling
# ---------------------------------------------------------------------------

def get_pool_status() -> dict:
    """Return pool metrics; safe if pool is not yet initialised."""
    try:
        pool = getattr(engine, "pool", None)
        if pool is None:
            return {"status": "uninitialized"}
        if isinstance(pool, NullPool):
            return {"pool_type": "NullPool", "status": "ok"}
        return {
            "pool_type"  : type(pool).__name__,
            "pool_size"  : getattr(pool, "size",       lambda: 0)(),
            "checked_in" : getattr(pool, "checkedin",  lambda: 0)(),
            "checked_out": getattr(pool, "checkedout", lambda: 0)(),
            "overflow"   : getattr(pool, "overflow",   lambda: 0)(),
            "status"     : "ok",
        }
    except Exception as exc:
        logger.warning("Pool status unavailable: %s", exc)
        return {"status": "error", "error": str(exc)}


def log_pool_status() -> None:
    logger.info("Connection pool: %s", get_pool_status())
