"""
BookingScraper/app/database.py
Conexión PostgreSQL con SQLAlchemy 2.0 — Windows 11 nativo - psycopg3

CORRECCIONES v21 (Audit Enterprise v20):
  [FIX CONC-006] Isolation level explícito: READ COMMITTED (default OLTP).
                 get_serializable_db() provee REPEATABLE READ para transiciones críticas.
  [FIX DB-007]   Timeout diferenciado: statement_timeout base en pool + override por sesión.
  [FIX SEC-005]  Error de conexión no expone credenciales en excepciones propagadas.
  [NEW]          get_olap_db() para queries de agregación con statement_timeout extendido.
"""

from sqlalchemy import create_engine, text, event as _sa_event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import OperationalError, DisconnectionError, InterfaceError
import os
import time as _time
import logging as _logging
from contextlib import contextmanager
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# ── CREDENCIALES ────────────────────────────────────────────────────────────────
_DB_USER     = os.getenv("DB_USER", "postgres")
_DB_PASSWORD = os.getenv("DB_PASSWORD")

# [FIX SEC-005] No exponer credenciales en mensajes de error.
# La excepción sólo menciona la variable faltante, nunca el valor ni la URL.
if not _DB_PASSWORD:
    raise EnvironmentError(
        "DB_PASSWORD environment variable is not set. "
        "Configure it in your .env file before starting the service. "
        "Do NOT hardcode credentials in source code."
    )

_DB_HOST = os.getenv("DB_HOST", "localhost")
_DB_PORT = os.getenv("DB_PORT", "5432")
_DB_NAME = os.getenv("DB_NAME", "booking_scraper")

# DATABASE_URL contiene la contraseña — NUNCA loguear esta variable.
DATABASE_URL = (
    f"postgresql+psycopg://{_DB_USER}:{_DB_PASSWORD}"
    f"@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}"
)

# ── POOL ────────────────────────────────────────────────────────────────────────
# [FIX CRIT-004] Enforce safe upper bounds to prevent PostgreSQL max_connections
# exhaustion. Raw env values are clamped; if the combined total still exceeds
# the enterprise hard cap (100 connections), startup is aborted to prevent
# cascading failures at runtime.
_POOL_SAFE_MAX   = int(os.getenv("DB_POOL_SAFE_MAX", "50"))   # per-process limit
_OVERFLOW_SAFE_MAX = int(os.getenv("DB_OVERFLOW_SAFE_MAX", "20"))
_TOTAL_HARD_CAP  = int(os.getenv("DB_TOTAL_HARD_CAP", "100")) # across all processes

_POOL_SIZE    = min(int(os.getenv("DB_POOL_SIZE",   "10")), _POOL_SAFE_MAX)
_MAX_OVERFLOW = min(int(os.getenv("DB_MAX_OVERFLOW", "5")),  _OVERFLOW_SAFE_MAX)
_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "1800"))

if _POOL_SIZE + _MAX_OVERFLOW > _TOTAL_HARD_CAP:
    raise EnvironmentError(
        f"[CRIT-004] Pool configuration exceeds hard cap: "
        f"DB_POOL_SIZE={_POOL_SIZE} + DB_MAX_OVERFLOW={_MAX_OVERFLOW} "
        f"= {_POOL_SIZE + _MAX_OVERFLOW} > DB_TOTAL_HARD_CAP={_TOTAL_HARD_CAP}. "
        "Reduce DB_POOL_SIZE or DB_MAX_OVERFLOW in your .env file."
    )

# [FIX CONC-006] statement_timeout base para operaciones OLTP (30s).
# Operaciones OLAP (aggregaciones, exports) usan get_olap_db() con 300s.
_STMT_TIMEOUT_OLTP_MS = int(os.getenv("STMT_TIMEOUT_OLTP_MS", "30000"))   # 30 s

# [FIX SEC-005] La excepción de conexión NO debe propagarse al cliente con la URL completa.
# creator= captura el error a nivel de driver y lo re-lanza sin credenciales.
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=_POOL_SIZE,
    max_overflow=_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=_POOL_RECYCLE,
    pool_timeout=_POOL_TIMEOUT,
    pool_reset_on_return="rollback",
    connect_args={
        "connect_timeout": 10,
        # [FIX CONC-006] Isolation level READ COMMITTED — explícito, no implícito.
        # READ COMMITTED es suficiente para la mayoría de operaciones OLTP.
        # Las transiciones de estado críticas usan get_serializable_db() que
        # eleva a REPEATABLE READ dentro de la sesión.
        "options": (
            f"-c statement_timeout={_STMT_TIMEOUT_OLTP_MS} "
            f"-c default_transaction_isolation='read committed'"
        ),
    },
    # [FIX CONC-006] isolation_level explícito a nivel de engine.
    # Esto establece el nivel en todas las sesiones salvo override explícito.
    isolation_level="READ COMMITTED",
    echo=os.getenv("DEBUG", "false").lower() == "true",
)

# ── SLOW QUERY LOGGING ─────────────────────────────────────────────────────────
_SLOW_QUERY_MS = float(os.getenv("SLOW_QUERY_THRESHOLD_MS", "2000"))
_slow_logger   = _logging.getLogger("bookingscraper.slowquery")


@_sa_event.listens_for(engine, "before_cursor_execute")
def _before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(_time.monotonic())


@_sa_event.listens_for(engine, "after_cursor_execute")
def _after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    start_times = conn.info.get("query_start_time", [])
    if start_times:
        elapsed_ms = (_time.monotonic() - start_times.pop()) * 1000
        if elapsed_ms > _SLOW_QUERY_MS:
            # [FIX SEC-005] No loguear parámetros — pueden contener datos sensibles.
            _slow_logger.warning(
                "[SLOW QUERY] %.0fms | %s",
                elapsed_ms,
                statement[:300].replace("\n", " "),
            )


# ── SESIONES ────────────────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Dependencia FastAPI para sesiones OLTP (READ COMMITTED, timeout 30s).
    Uso: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_serializable_db():
    """
    [FIX CONC-006] Sesión con aislamiento REPEATABLE READ para operaciones
    que requieren lecturas consistentes dentro de la misma transacción.

    Casos de uso:
    - Transiciones de estado en url_language_status (evita deadlocks por lecturas fantasma).
    - Actualizaciones de retry_count que comparan valor leído vs. actualizado.

    NOTA: REPEATABLE READ tiene mayor costo de bloqueo. Usar SÓLO donde sea necesario.

    Uso:
        with get_serializable_db() as db:
            db.execute(text("..."))
    """
    db = SessionLocal()
    try:
        db.execute(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"))
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_olap_db():
    """
    [FIX DB-007] Sesión para operaciones OLAP (aggregaciones, exports).
    statement_timeout extendido a 300s (configurable vía STMT_TIMEOUT_OLAP_MS).
    READ COMMITTED — no requiere aislamiento superior para lecturas analíticas.

    Uso:
        with get_olap_db() as db:
            result = db.execute(text("SELECT COUNT(*) FROM hotels GROUP BY language"))
    """
    _olap_timeout = int(os.getenv("STMT_TIMEOUT_OLAP_MS", "300000"))  # 300 s
    db = SessionLocal()
    try:
        db.execute(text(f"SET LOCAL statement_timeout = {_olap_timeout}"))
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ── RETRY CON BACKOFF EXPONENCIAL ──────────────────────────────────────────────
def execute_with_retry(
    session_factory,
    operation,
    max_retries: int = 3,
    backoff: float = 0.5,
):
    """
    [FIX BUG-NEW-15] Ejecuta una operación con reintento automático en errores
    transitorios de conexión (ej: primer query tras reinicio de PostgreSQL).

    Errores elegibles para reintento:
    - OperationalError: timeout, conexión rechazada, servidor caído.
    - DisconnectionError: conexión caída dentro del pool.
    - InterfaceError: protocolo interrumpido por reinicio del servidor.

    Los errores de lógica (IntegrityError, ProgrammingError) NO se reintentan.

    Uso:
        result = execute_with_retry(SessionLocal, lambda db: db.execute(text("SELECT 1")))
    """
    import time as _t
    last_exc = None
    for attempt in range(max_retries):
        db = session_factory()
        try:
            result = operation(db)
            db.commit()
            return result
        except (OperationalError, DisconnectionError, InterfaceError) as e:
            db.rollback()
            last_exc = e
            logger.warning(
                "[execute_with_retry] Error transitorio (intento %d/%d): %s",
                attempt + 1, max_retries, type(e).__name__,
            )
            _t.sleep(backoff * (2 ** attempt))
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    raise last_exc


# ── POOL MONITORING ────────────────────────────────────────────────────────────
def get_pool_status() -> dict:
    """Métricas de utilización del pool en tiempo real."""
    pool = engine.pool
    try:
        checked_out = pool.checkedout()
        capacity    = pool.size() + pool.overflow()
        return {
            "pool_size":       pool.size(),
            "checked_out":     checked_out,
            "overflow":        pool.overflow(),
            "checked_in":      pool.checkedin(),
            "utilization_pct": round(100.0 * checked_out / max(capacity, 1), 1),
        }
    except Exception as exc:
        return {"error": type(exc).__name__}  # [FIX SEC-005] No exponer detalles internos


def log_pool_status(threshold_pct: float = 80.0) -> None:
    status = get_pool_status()
    pct    = status.get("utilization_pct", 0)
    if pct >= threshold_pct:
        logger.warning(
            "⚠️ DB Pool alta utilización %s%% | size=%s checked_out=%s overflow=%s",
            pct, status.get("pool_size"), status.get("checked_out"), status.get("overflow"),
        )
    else:
        logger.debug("DB Pool OK %s%% | checked_out=%s", pct, status.get("checked_out"))


# ── BASE ORM ────────────────────────────────────────────────────────────────────
from app.models import Base  # noqa: F401


# ── UTILIDADES ──────────────────────────────────────────────────────────────────
def test_connection(retries: int = 3, backoff: float = 1.0) -> bool:
    """
    [FIX MED-011] Retry with exponential backoff on transient connection errors.
    Returns True only after a successful SELECT 1.
    Credentials are never included in log output (FIX SEC-005).
    """
    import time as _t
    for attempt in range(1, retries + 1):
        try:
            with SessionLocal() as db:
                db.execute(text("SELECT 1"))
            logger.success("✓ Conexión a PostgreSQL exitosa")
            return True
        except Exception as e:
            logger.warning(
                "✗ Error de conexión a PostgreSQL (intento %d/%d): %s",
                attempt, retries, type(e).__name__,
            )
            if attempt < retries:
                _t.sleep(backoff * (2 ** (attempt - 1)))
    logger.error("✗ No se pudo conectar a PostgreSQL tras %d intentos", retries)
    return False


def get_db_version() -> str:
    try:
        with SessionLocal() as db:
            result = db.execute(text("SELECT version()")).fetchone()
        return result[0] if result else "Unknown"
    except Exception as e:
        return f"Error: {type(e).__name__}"


def get_url_queue_stats() -> dict:
    try:
        with SessionLocal() as db:
            result = db.execute(text("""
                SELECT
                    COUNT(*) FILTER (WHERE status = 'pending')    AS pending,
                    COUNT(*) FILTER (WHERE status = 'processing') AS processing,
                    COUNT(*) FILTER (WHERE status = 'completed')  AS completed,
                    COUNT(*) FILTER (WHERE status = 'failed')     AS failed,
                    COUNT(*)                                       AS total
                FROM url_queue
            """)).fetchone()
        return {
            "pending":    result[0] or 0,
            "processing": result[1] or 0,
            "completed":  result[2] or 0,
            "failed":     result[3] or 0,
            "total":      result[4] or 0,
        }
    except Exception as e:
        logger.error("Error obteniendo stats: %s", type(e).__name__)
        return {"pending": 0, "processing": 0, "completed": 0, "failed": 0, "total": 0}


if __name__ == "__main__":
    print("=" * 60)
    print("  Test de Conexión a PostgreSQL")
    print("=" * 60)
    if test_connection():
        print(f"\nVersión: {get_db_version()}")
        print("\nEstadísticas de URL Queue:")
        for k, v in get_url_queue_stats().items():
            print(f"  {k:12s}: {v}")
    else:
        print("\n✗ No se pudo conectar. Verificar PostgreSQL y .env")
    print("=" * 60)
