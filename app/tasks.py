"""
BookingScraper/app/tasks.py
Tareas Celery — BookingScraper Pro
Windows 11 + Python 3.14.3

[FIX BUG-NEW-03] Archivo creado: celery_app.py referenciaba 'app.tasks' pero
  el archivo no existía en el repositorio, causando ImportError al iniciar
  el worker Celery y dejando el dispatcher programado completamente inoperativo.

[FIX BUG-15] disk_usage ahora usa plataforma dinámica (sys.platform) con
  fallback a raíz '/' en Linux/Mac — evita FileNotFoundError en entornos
  no-Windows. El check con __doc__ era siempre True y el fallback nunca ejecutaba.

[FIX ERR-CONC-001] Nueva tarea reset_stale_urls:
  URLs en status='processing' durante más de STALE_PROCESSING_MINUTES son reseteadas
  a 'pending' automáticamente. Resuelve el problema de URLs bloqueadas después de
  un crash del proceso sin reinicio manual.

ARRANQUE:
  Worker:  celery -A app.celery_app worker --pool=solo --loglevel=info
  Beat:    celery -A app.celery_app beat --loglevel=info
"""

from __future__ import annotations

import logging
import os
import platform
import sys
from datetime import datetime, timezone
from typing import Any, Dict

import psutil

from app.celery_app import celery_app
from app.config import settings
from app.database import SessionLocal

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _get_db():
    """Devuelve una sesión de BD sin dejarla abierta si falla."""
    return SessionLocal()


def _disk_usage_percent() -> float:
    """
    [FIX BUG-15] Devuelve el porcentaje de uso de disco de forma cross-platform.

    Lógica:
    - Windows → usa la unidad configurada en settings.BASE_DATA_PATH (normalmente C:\\)
    - Linux/Mac/Docker → usa '/' (raíz del sistema de archivos)
    - Fallback → 0.0 si la ruta no existe o psutil falla
    """
    try:
        if sys.platform.startswith("win"):
            # Extraer letra de unidad de la ruta de datos configurada
            import os
            data_path = settings.BASE_DATA_PATH
            drive = os.path.splitdrive(data_path)[0] or "C:\\"
            if not drive.endswith("\\"):
                drive += "\\"
            disk_path = drive
        else:
            # Linux, macOS, Docker
            disk_path = "/"
        return psutil.disk_usage(disk_path).percent
    except (FileNotFoundError, PermissionError, OSError) as e:
        logger.warning(f"[BUG-15] No se pudo obtener uso de disco para '{disk_path}': {e}")
        return 0.0


# ─────────────────────────────────────────────────────────────────────────────
# TAREA 1 — Despachar URLs pendientes (sustituye al asyncio loop cuando USE_CELERY=True)
# ─────────────────────────────────────────────────────────────────────────────

@celery_app.task(
    name="app.tasks.process_pending_urls",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    # [FIX HIGH-013] Reduced from time_limit=600 (10 min) / soft_time_limit=540.
    # A single hotel scrape (1 URL × 5 languages) should complete in <3 min on
    # a local Windows machine with Brave. The previous 10-minute limit allowed
    # a hung task to exhaust all worker capacity until forced termination.
    # New limits: soft=150s (warning + graceful abort), hard=180s (SIGKILL).
    # If profiling shows legitimate tasks exceeding 150s (e.g., gallery image
    # extraction with many languages), raise via CELERY_TASK_SOFT_TIME_LIMIT
    # and CELERY_TASK_TIME_LIMIT env vars rather than modifying code.
    soft_time_limit=int(os.getenv("CELERY_TASK_SOFT_TIME_LIMIT", "150")),
    time_limit=int(os.getenv("CELERY_TASK_TIME_LIMIT", "180")),
    acks_late=True,
)
def process_pending_urls(self, batch_size: int = 5) -> Dict[str, Any]:
    """
    Despacha un batch de URLs pendientes hacia el scraper_service.

    Invocada cada 30 segundos por Celery Beat (beat_schedule en celery_app.py).
    También puede invocarse manualmente:
      celery -A app.celery_app call app.tasks.process_pending_urls --args='[10]'
    """
    try:
        from app.scraper_service import process_batch
        result = process_batch(batch_size)
        logger.info(f"[Task: process_pending_urls] batch={batch_size} result={result}")
        return result
    except Exception as exc:
        logger.error(
            f"[Task: process_pending_urls] Error inesperado: {exc}",
            exc_info=True,
        )
        # [FIX-018 / CRIT-007] Exponential backoff: 60s, 120s, 240s, ... (max 3600s).
        # Prevents hammering a temporarily unavailable dependency (DB, Redis) on
        # every retry. The ceiling (3600s = 1 hour) bounds the delay for long outages.
        _backoff = min(60 * (2 ** self.request.retries), 3600)
        raise self.retry(exc=exc, countdown=_backoff)


# ─────────────────────────────────────────────────────────────────────────────
# TAREA 2 — Limpieza de logs antiguos (diaria a las 03:00 UTC)
# ─────────────────────────────────────────────────────────────────────────────

@celery_app.task(
    name="app.tasks.cleanup_old_logs",
    bind=True,
    max_retries=2,
    default_retry_delay=300,
    soft_time_limit=120,
    time_limit=180,
)
def cleanup_old_logs(self, days_to_keep: int = 30) -> Dict[str, Any]:
    """
    Elimina registros de scraping_logs anteriores a `days_to_keep` días.

    Invocada cada día a las 03:00 UTC por Celery Beat.
    """
    from sqlalchemy import text as sa_text

    db = _get_db()
    deleted = 0
    try:
        # [FIX BUG-V5-003] Patrón SQL seguro para PostgreSQL INTERVAL con parámetro numérico.
        # INTERVAL ':days days' con .bindparams() NO funciona en PostgreSQL — el driver
        # no puede sustituir un named param dentro de un literal de string INTERVAL.
        # Patrón correcto: multiplicar INTERVAL '1 day' por el parámetro numérico.
        # ELIMINADO: comentario f-string — ese fallback era vulnerabilidad de SQL injection.
        result = db.execute(
            sa_text(
                "DELETE FROM scraping_logs "
                "WHERE timestamp < NOW() - INTERVAL '1 day' * :days"
            ),
            {"days": days_to_keep}
        )
        deleted = result.rowcount
        db.commit()
        logger.info(f"[Task: cleanup_old_logs] Eliminados {deleted} registros de logs > {days_to_keep} días")
        return {"deleted_rows": deleted, "days_kept": days_to_keep}
    except Exception as exc:
        db.rollback()
        logger.error(f"[Task: cleanup_old_logs] Error: {exc}", exc_info=True)
        # [FIX-018] Exponential backoff: 300s, 600s ceiling at 3 retries
        _backoff = min(300 * (2 ** self.request.retries), 3600)
        raise self.retry(exc=exc, countdown=_backoff)
    finally:
        db.close()


# ─────────────────────────────────────────────────────────────────────────────
# TAREA 3 — Guardar métricas del sistema (cada 5 minutos)
# ─────────────────────────────────────────────────────────────────────────────

@celery_app.task(
    name="app.tasks.save_system_metrics",
    bind=True,
    max_retries=1,
    default_retry_delay=60,
    soft_time_limit=30,
    time_limit=60,
)
def save_system_metrics(self) -> Dict[str, Any]:
    """
    Captura métricas de CPU, RAM y disco y las almacena en system_metrics.

    [FIX BUG-15] Uso de disco calculado con _disk_usage_percent() cross-platform.
    Invocada cada 5 minutos por Celery Beat.
    """
    from sqlalchemy import text as sa_text

    # Recopilar métricas del sistema
    cpu_pct    = psutil.cpu_percent(interval=1)
    ram        = psutil.virtual_memory()
    ram_pct    = ram.percent
    ram_mb     = round(ram.used / 1_048_576, 1)
    disk_pct   = _disk_usage_percent()          # [FIX BUG-15]
    os_name    = platform.system()
    py_version = platform.python_version()

    metrics = {
        "cpu_pct":    cpu_pct,
        "ram_pct":    ram_pct,
        "ram_mb":     ram_mb,
        "disk_pct":   disk_pct,
        "os":         os_name,
        "python":     py_version,
        "timestamp":  datetime.now(timezone.utc).isoformat(),
    }

    db = _get_db()
    try:
        # [FIX BUG-A-01] Column names cpu_percent/ram_percent/disk_percent did NOT match
        # the SQLAlchemy model SystemMetrics which defines cpu_usage/memory_usage/disk_usage.
        # The INSERT silently failed with "column cpu_percent does not exist" on every run,
        # meaning system_metrics table was always empty regardless of how long the system ran.
        db.execute(
            sa_text(
                "INSERT INTO system_metrics "
                "(cpu_usage, memory_usage, disk_usage, recorded_at) "
                "VALUES (:cpu, :ram, :disk, NOW())"
            ),
            {"cpu": cpu_pct, "ram": ram_pct, "disk": disk_pct},
        )
        db.commit()
        logger.debug(f"[Task: save_system_metrics] CPU={cpu_pct}% RAM={ram_pct}% Disk={disk_pct}%")
    except Exception as exc:
        db.rollback()
        logger.error(f"[Task: save_system_metrics] Error al guardar métricas: {exc}", exc_info=True)
        # No reintentamos — las métricas son best-effort
    finally:
        db.close()

    return metrics


# ─────────────────────────────────────────────────────────────────────────────
# TAREA 4 — Resetear URLs bloqueadas en 'processing' (ERR-CONC-001)
# ─────────────────────────────────────────────────────────────────────────────

@celery_app.task(
    name="app.tasks.reset_stale_urls",
    bind=True,
    max_retries=2,
    default_retry_delay=60,
    soft_time_limit=30,
    time_limit=60,
)
def reset_stale_urls(self, stale_minutes: int = None) -> Dict[str, Any]:
    """
    [FIX ERR-CONC-001] Resetea URLs atascadas en status='processing'.

    PROBLEMA: El estado 'processing' se asigna ANTES de iniciar el scraping.
    Si el proceso crashea o es terminado brutalmente (SIGKILL, apagado Windows),
    las URLs quedan en 'processing' indefinidamente. Sin esta tarea, el sistema
    las ignora para siempre (la query de dispatch filtra WHERE status='pending').

    SOLUCIÓN: Cada 5 minutos, detectar URLs en 'processing' con updated_at
    anterior a STALE_PROCESSING_MINUTES (default: 30 min) y resetearlas a
    'pending' para que el próximo ciclo las reintente.

    INVARIANTE: Solo resetea si updated_at < NOW() - interval, no si el scraper
    está activamente procesando la URL (las URLs activas tienen updated_at reciente).

    CONFIGURABLE: STALE_PROCESSING_MINUTES en .env (default: 30).
    """
    from sqlalchemy import text as sa_text

    _stale_minutes = stale_minutes or int(os.getenv("STALE_PROCESSING_MINUTES", "30"))

    db = _get_db()
    reset_count = 0
    reset_ids   = []
    try:
        # Reset url_queue rows stuck in 'processing'
        result = db.execute(
            sa_text("""
                UPDATE url_queue
                SET
                    status     = 'pending',
                    updated_at = NOW()
                WHERE
                    status     = 'processing'
                    AND updated_at < NOW() - INTERVAL '1 minute' * :minutes
                RETURNING id
            """),
            {"minutes": _stale_minutes}
        )
        reset_ids  = [row[0] for row in result]
        reset_count = len(reset_ids)

        # Also reset corresponding url_language_status rows
        if reset_ids:
            db.execute(
                sa_text("""
                    UPDATE url_language_status
                    SET
                        status     = 'pending',
                        updated_at = NOW()
                    WHERE
                        url_id IN :ids
                        AND status = 'processing'
                """),
                {"ids": tuple(reset_ids)}
            )

        db.commit()

        if reset_count > 0:
            logger.warning(
                "[ERR-CONC-001] reset_stale_urls: %d URLs reseteadas de 'processing' a 'pending' "
                "(atascadas > %d min). IDs: %s",
                reset_count, _stale_minutes, reset_ids[:20]
            )
        else:
            logger.debug(
                "[ERR-CONC-001] reset_stale_urls: sin URLs atascadas (threshold=%d min)",
                _stale_minutes
            )

        return {
            "reset_count": reset_count,
            "stale_minutes": _stale_minutes,
            "reset_ids": reset_ids[:50],  # Truncar para evitar payload enorme en respuesta
        }

    except Exception as exc:
        db.rollback()
        logger.error("[ERR-CONC-001] reset_stale_urls error: %s", exc, exc_info=True)
        _backoff = min(60 * (2 ** self.request.retries), 600)
        raise self.retry(exc=exc, countdown=_backoff)
    finally:
        db.close()


# ─────────────────────────────────────────────────────────────────────────────
# TAREA 5 — Crear partición de scraping_logs del mes siguiente (mensual)
# ─────────────────────────────────────────────────────────────────────────────

@celery_app.task(
    name="app.tasks.create_next_partition",
    bind=True,
    max_retries=2,
    default_retry_delay=300,
    soft_time_limit=30,
    time_limit=60,
)
def create_next_partition(self) -> Dict[str, Any]:
    """
    [FIX MED-004] Crea la partición de scraping_logs para el mes siguiente.

    La función create_scraping_logs_partition() está definida en el SQL de
    instalación. Esta tarea la invoca el primer día de cada mes a las 01:00 UTC
    para asegurar que la partición del mes entrante exista antes de que comiencen
    a insertarse registros.

    Sin esta tarea, los INSERTs del mes siguiente fallarían con:
        ERROR: no partition of relation "scraping_logs" found for row
    """
    from sqlalchemy import text as sa_text
    from datetime import datetime, timezone, timedelta

    db = _get_db()
    try:
        next_month = datetime.now(timezone.utc) + timedelta(days=32)
        year  = next_month.year
        month = next_month.month

        db.execute(
            sa_text("SELECT create_scraping_logs_partition(:year, :month)"),
            {"year": year, "month": month}
        )
        db.commit()
        logger.info("[MED-004] Partición creada: scraping_logs_%04d_%02d", year, month)
        return {"partition": f"scraping_logs_{year:04d}_{month:02d}", "status": "ok"}
    except Exception as exc:
        db.rollback()
        logger.error("[MED-004] Error creando partición: %s", exc, exc_info=True)
        raise self.retry(exc=exc)
    finally:
        db.close()
