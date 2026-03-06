"""
BookingScraper/app/scraper_service.py  v6.0  [COMPLETENESS TRACKING + LANGUAGE SNAPSHOT]
Servicio de scraping directo - BookingScraper Pro

CAMBIOS v6.0 [COMPLETENESS TRACKING + LANGUAGE SNAPSHOT]:

  PROBLEMA RESUELTO:
  - El sistema marcaba una URL como 'completed' si scraped_count > 0.
    1/5 idiomas era indistinguible de 5/5 idiomas.
  - Si LANGUAGES_ENABLED cambiaba con el scraper activo, las URLs ya
    inicializadas podian recibir idiomas nuevos (violacion de regla de negocio).

  [NUEVO] completeness_service: tracking por idioma en url_language_status.
  [NUEVO] _get_languages_for_url(): Lee idiomas desde SNAPSHOT en url_language_status,
    NO desde settings.ENABLED_LANGUAGES. Si LANGUAGES_ENABLED cambia mientras el
    scraper corre, las URLs ya inicializadas procesan sus idiomas originales.
  [NUEVO] Retry por idioma: hasta MAX_LANG_RETRIES intentos antes de 'failed'.
  [NUEVO] url_queue.status 'incomplete': URLs con algun idioma fallido tras reintentos.
  [NUEVO] process_batch() limita a MAX_BATCH_SIZE=10 URLs por ciclo.

CAMBIOS v5.1 [FIX NO-OVERWRITE + images_count]:
  [FIX #36] _save_hotel(): ON CONFLICT DO NOTHING
  [FIX #37] _save_hotel(): images_count=0 explicito en INSERT.

CAMBIOS v5.0: VPN UK-first para en-gb.
CAMBIOS v4.0: Bloquear guardado en idioma incorrecto.
CAMBIOS v3.1: imagenes del primer idioma exitoso.
CAMBIOS v2.x: mejoras incrementales.
"""

import json
import os  # [FIX BUG-V6-006] CRITICAL: os was missing — os.getenv() in _VPN_LOCK_TIMEOUT caused NameError at import time
import re  # [FIX ERR-RUN-001] re.sub() used at line ~95 to sanitize Redis URL before logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Set
from loguru import logger

from sqlalchemy import text

from app.database import SessionLocal
from app.config import settings
from app.completeness_service import completeness_service, MAX_LANG_RETRIES


# Pool de threads
# [BUG-006 FIX] max_workers leído desde settings.SCRAPER_MAX_WORKERS (configurable en .env).
# Default=1 (secuencial seguro). Aumentar requiere VPN_ROTATE_EVERY_N más bajo.
_executor = ThreadPoolExecutor(
    max_workers=settings.SCRAPER_MAX_WORKERS,
    thread_name_prefix="scraper",
)

# [FIX BUG-NEW-05] atexit ensures executor is shut down even on abnormal termination.
import atexit as _atexit
_atexit.register(lambda: _executor.shutdown(wait=False, cancel_futures=True))

# ─────────────────────────────────────────────────────────────────────────────
# [FIX CRIT-004] BoundedSemaphore as backpressure for ThreadPoolExecutor.
#
# PROBLEM: ThreadPoolExecutor has an unbounded internal queue (SimpleQueue).
# When process_batch() submits faster than workers complete (e.g., 10 URLs/30s
# but each URL takes 60s+ due to VPN rotation), tasks accumulate indefinitely,
# causing memory exhaustion proportional to accumulated pending futures.
#
# SOLUTION: BoundedSemaphore limits pending submissions to max_workers * 2.
# If the semaphore is full, _submit_with_backpressure() rejects new submissions
# immediately (non-blocking try), releasing the URL back to 'pending' state so
# the next process_batch() cycle can re-claim it.
#
# WHY max_workers * 2: allows one full "wave" of submissions to queue while
# the current wave executes. Higher values increase memory risk; lower values
# (max_workers * 1) would cause immediate rejection when all workers are busy.
# ─────────────────────────────────────────────────────────────────────────────
_dispatch_semaphore = threading.BoundedSemaphore(
    max(1, settings.SCRAPER_MAX_WORKERS * 2)
)


def _submit_with_backpressure(url_id: int) -> bool:
    """
    [FIX CRIT-004] Submit url_id to thread pool with backpressure protection.

    Acquires the BoundedSemaphore before submitting. If the semaphore is
    exhausted (all slots occupied by queued/running tasks), logs a warning
    and returns False without submitting. The caller must release the URL
    back to 'pending' state when this returns False.

    Args:
        url_id: The URL ID to submit for scraping.

    Returns:
        True if submitted successfully, False if backpressure limit reached.
    """
    acquired = _dispatch_semaphore.acquire(blocking=False)
    if not acquired:
        logger.warning(
            "[CRIT-004] Backpressure: dispatch queue full "
            "(max=%d). Skipping url_id=%d — will retry next cycle.",
            settings.SCRAPER_MAX_WORKERS * 2,
            url_id,
        )
        return False

    def _wrapped_task():
        try:
            _run_safe(url_id)
        finally:
            _dispatch_semaphore.release()

    _executor.submit(_wrapped_task)
    return True

_lock = threading.Lock()

# ─────────────────────────────────────────────────────────────────────────────
# [FIX ARCH-002] _active_ids respaldado por Redis para despliegue multi-worker.
# Con set() en memoria, cada proceso tiene su propio estado:
#   → doble despacho de URLs, bypass del rate limiter, estado VPN incoherente.
# Con Redis SET atómico (NX + TTL), todos los workers comparten el registro.
# PREREQUISITO: REDIS_URL en .env (ej: REDIS_URL=redis://localhost:6379/0)
# FALLBACK: Si Redis no está disponible, usa set local (single-process only).
# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
# [FIX ERR-ARCH-001] Explicit ConnectionPool — prevents file-descriptor exhaustion.
# [FIX ERR-CONC-002] socket_timeout on all operations — prevents indefinite thread hang.
# [FIX ERR-RUN-001]  Use settings.REDIS_URL — _REDIS_URL was undefined, causing NameError.
# [FIX ERR-ARCH-002] Health-check + auto-reconnect on every Redis operation.
# ─────────────────────────────────────────────────────────────────────────────
_REDIS_SOCKET_TIMEOUT   = float(os.getenv("REDIS_SOCKET_TIMEOUT_S",  "2.0"))

# [FIX ERR-SEC-006] Sanitize Booking.com URLs before logging.
# Strips query parameters that may contain session tokens, affiliate IDs,
# or pricing tokens (e.g. ?sid=, ?aid=, ?token=). Only the path is retained.
_URL_SENSITIVE_PARAMS = frozenset({
    "sid", "aid", "token", "session", "auth", "key", "label", "lang",
    "req_adults", "req_nights", "checkin", "checkout", "ucfs", "group_adults",
})

def _sanitize_url_log(url: str) -> str:
    """Return url with sensitive query params replaced by *** for safe logging."""
    try:
        from urllib.parse import urlparse as _up, urlencode as _ue, parse_qs as _pq
        p = _up(url)
        if not p.query:
            return url
        qs = _pq(p.query, keep_blank_values=True)
        sanitized = {
            k: (["***"] if k.lower() in _URL_SENSITIVE_PARAMS else v)
            for k, v in qs.items()
        }
        clean_qs = _ue(sanitized, doseq=True)
        return p._replace(query=clean_qs).geturl()
    except Exception:
        return url  # never break logging
_REDIS_SOCKET_CONN_TO   = float(os.getenv("REDIS_CONN_TIMEOUT_S",    "2.0"))
_REDIS_MAX_CONNECTIONS  = int(os.getenv("REDIS_MAX_CONNECTIONS",      "10"))

try:
    import redis as _redis_lib
    from redis.connection import ConnectionPool as _RedisConnectionPool

    _redis_pool = _RedisConnectionPool.from_url(
        settings.REDIS_URL,
        max_connections=_REDIS_MAX_CONNECTIONS,
        socket_timeout=_REDIS_SOCKET_TIMEOUT,          # [FIX ERR-CONC-002] all ops
        socket_connect_timeout=_REDIS_SOCKET_CONN_TO,  # [FIX ERR-CONC-002] connect
        socket_keepalive=True,
        retry_on_timeout=False,   # fail fast, let caller use local fallback
    )
    _redis_client = _redis_lib.Redis(connection_pool=_redis_pool)
    _redis_client.ping()
    # [FIX ERR-RUN-001] Was: _REDIS_URL.split("@")[-1] → NameError.
    # Now: sanitize settings.REDIS_URL to strip credentials before logging.
    _redis_safe_url = re.sub(r':([^@/]+)@', ':***@', settings.REDIS_URL)
    logger.info(
        "[ARCH-001/002] Redis/Memurai conectado (%s) pool_size=%d timeout=%.1fs",
        _redis_safe_url, _REDIS_MAX_CONNECTIONS, _REDIS_SOCKET_TIMEOUT,
    )
except Exception as _redis_init_err:
    _redis_pool   = None
    _redis_client = None
    logger.warning(
        "[ARCH-001/002] Redis/Memurai no disponible (%s:%s) — "
        "_active_ids en memoria local (modo normal Windows SCRAPER_MAX_WORKERS=1).",
        type(_redis_init_err).__name__, _redis_init_err,
    )


def _get_redis() -> "Optional[_redis_lib.Redis]":
    """
    [FIX HIGH-002] Return a healthy Redis client, or None.

    Incorporates a circuit breaker to prevent repeated reconnection attempts
    from adding blocking latency to every scraping operation after Redis goes
    down. The circuit opens after _REDIS_CB_THRESHOLD consecutive failures and
    stays open for _REDIS_CB_COOLDOWN seconds.

    States:
      CLOSED  — Redis healthy, normal operation.
      OPEN    — Redis down; return None immediately (zero latency fallback).
      HALF-OPEN — Cooldown expired; allow one probe. Close on success.
    """
    global _redis_client, _redis_pool, _redis_cb_failures, _redis_cb_open_until

    if _redis_client is None:
        return None

    with _redis_cb_lock:
        now = time.monotonic()

        # OPEN: circuit tripped — check if cooldown expired
        if _redis_cb_open_until > 0:
            if now < _redis_cb_open_until:
                return None  # Still in cooldown — return immediately
            # Cooldown expired → HALF-OPEN: allow one probe attempt
            logger.debug("[HIGH-002] Redis CB half-open — probing...")
            _redis_cb_open_until = 0.0  # tentatively clear; re-set if probe fails

    try:
        _redis_client.ping()
        with _redis_cb_lock:
            was_recovering = _redis_cb_failures > 0
            _redis_cb_failures = 0
        if was_recovering:
            logger.info("[HIGH-002] Redis CB closed — connection restored.")
            # [FIX Recovery-003] Re-sync in-memory _active_ids from Redis after
            # circuit recovers. During the outage, _claim_active_url() fell back
            # to _active_ids (local set). Any URLs still held in Redis (from
            # before the outage) but absent from _active_ids could be double-claimed.
            # Scan all bsp:active:* keys and populate the local set as a safety net.
            # TTL on Redis keys (_ACTIVE_ID_TTL) bounds the scan to live entries only.
            try:
                keys = _redis_client.keys("bsp:active:*")
                if keys:
                    recovered_ids = set()
                    for k in keys:
                        try:
                            uid = int(k.decode().split(":")[-1])
                            recovered_ids.add(uid)
                        except (ValueError, AttributeError):
                            pass
                    with _active_ids_local_lock:
                        _active_ids.update(recovered_ids)
                    logger.info(
                        "[Recovery-003] Re-synced %d active URL IDs from Redis "
                        "into local _active_ids after circuit recovery.",
                        len(recovered_ids),
                    )
            except Exception as sync_err:
                logger.warning("[Recovery-003] _active_ids re-sync skipped: %s", sync_err)
        return _redis_client
    except Exception as hc_err:
        with _redis_cb_lock:
            _redis_cb_failures += 1
            if _redis_cb_failures >= _REDIS_CB_THRESHOLD:
                _redis_cb_open_until = time.monotonic() + _REDIS_CB_COOLDOWN
                logger.warning(
                    "[HIGH-002] Redis CB OPEN after %d failures — "
                    "fallback to local set for %ds. Error: %s",
                    _redis_cb_failures, _REDIS_CB_COOLDOWN, hc_err,
                )
                _redis_client = None
                return None
        # Below threshold — attempt reconnect once
        logger.warning("[HIGH-002] Redis ping failed (%s) — attempting reconnect...", hc_err)
        try:
            _redis_client = _redis_lib.Redis(connection_pool=_redis_pool)
            _redis_client.ping()
            with _redis_cb_lock:
                _redis_cb_failures = 0
            logger.info("[HIGH-002] Redis reconnected successfully.")
            return _redis_client
        except Exception as reconn_err:
            logger.error("[HIGH-002] Redis reconnect failed (%s).", reconn_err)
            _redis_client = None
            return None

_ACTIVE_ID_TTL = int(os.getenv("ACTIVE_ID_TTL_SECONDS", "3600"))

# ── [FIX HIGH-002] Redis Circuit Breaker ──────────────────────────────────────
# Without a circuit breaker, every call to _get_redis() after a Redis failure
# performs a reconnection attempt + ping, adding 2–3s of blocking latency to
# every scraping operation until Redis recovers.
#
# Pattern: after _REDIS_CB_THRESHOLD consecutive ping failures, the circuit
# opens for _REDIS_CB_COOLDOWN seconds. During that period, _get_redis()
# returns None immediately without retrying (zero latency fallback to local set).
# After the cooldown, the circuit enters HALF-OPEN: allows one probe. On
# success, the circuit closes and normal operation resumes.
_redis_cb_failures:    int   = 0
_redis_cb_open_until:  float = 0.0
_redis_cb_lock = threading.Lock()
_REDIS_CB_THRESHOLD = int(os.getenv("REDIS_FAILURE_THRESHOLD", "5"))
_REDIS_CB_COOLDOWN  = int(os.getenv("REDIS_COOLDOWN_SECONDS",  "60"))

# [FIX ERR-CONC-005] Validate USE_CELERY_DISPATCHER requires Redis.
# When Celery is enabled, FastAPI and the Celery worker are separate processes.
# Stats, _active_ids, and job state MUST be shared via Redis — not in-memory.
if settings.USE_CELERY_DISPATCHER and _redis_client is None:
    logger.error(
        "[CONC-005] USE_CELERY_DISPATCHER=True requires Redis for inter-process state sharing. "
        "Stats at GET /stats will only reflect the FastAPI process, NOT the Celery worker. "
        "Start Redis/Memurai and set REDIS_HOST/REDIS_PORT in .env for correct operation."
    )

# [FIX-023 / MED-006] Explicit Redis unavailability alert at startup.
# When Redis is not reachable, the system silently falls back to in-memory _active_ids.
# This degraded mode is safe for single-process deployment (SCRAPER_MAX_WORKERS=1)
# but can cause duplicate URL processing if multiple processes run simultaneously.
# The warning is emitted once at startup so it appears clearly in the log.
if _redis_client is None:
    logger.warning(
        "[MED-006] Redis unavailable at startup — DEGRADED MODE active.\n"
        "  _active_ids is LOCAL ONLY (in-memory set, not shared across processes).\n"
        "  Metrics aggregation may be incomplete.\n"
        "  For single-process Windows 11 deployment, this is SAFE.\n"
        "  To restore full operation: start Memurai/Redis and verify REDIS_HOST "
        "and REDIS_PORT in your .env file, then restart the application."
    )
_active_ids: Set[int] = set()       # fallback local
_active_ids_local_lock = threading.Lock()


# ─────────────────────────────────────────────────────────────────────────────
# [FIX-024 / MED-014] Error classification: transient vs fatal
# ─────────────────────────────────────────────────────────────────────────────
# Previously all exceptions were treated equally — logged at the same level with
# the same retry logic. This made alert logs noisy (transient network blips at
# ERROR level) and prevented smart retry decisions (fatal errors retried uselessly).
#
# Classification rules:
#  TRANSIENT — network/timeout/connection errors: safe to retry with backoff
#  FATAL     — programming errors, data validation failures: retrying won't help
#
# Usage in scraping loop:
#   if _is_transient_error(e):
#       schedule_retry()
#   else:
#       mark_failed_permanently()
# ─────────────────────────────────────────────────────────────────────────────

_TRANSIENT_EXCEPTION_TYPES = (
    ConnectionError,
    TimeoutError,
    OSError,
    IOError,
)

_TRANSIENT_MESSAGE_KEYWORDS = (
    "timeout", "timed out",
    "connection", "connect",
    "network", "unreachable",
    "reset by peer", "reset", "eof",
    "ssl", "handshake",
    "proxy", "socks",
    "name resolution", "dns",
    "refused", "refused connection",
    "broken pipe",
    "temporarily unavailable",
    "too many requests", "429",          # HTTP rate-limit
    "service unavailable", "503",        # HTTP temporary
    "bad gateway", "502",
    "gateway timeout", "504",
)

_FATAL_EXCEPTION_TYPES = (
    ValueError,
    TypeError,
    AttributeError,
    KeyError,
    NotImplementedError,
    PermissionError,                     # filesystem permission — not transient
)


def _is_transient_error(exc: Exception) -> bool:
    """
    [FIX-024] Returns True if the exception is likely transient (safe to retry).
    Returns False if the error is fatal (retrying will not help).

    Conservative by default: unknown exception types → True (assume transient
    so they get retried rather than silently dropped). Override by adding
    exception types to _FATAL_EXCEPTION_TYPES when the failure mode is known.
    """
    if isinstance(exc, _FATAL_EXCEPTION_TYPES):
        return False
    if isinstance(exc, _TRANSIENT_EXCEPTION_TYPES):
        return True
    # Heuristic: check message text for known transient keywords
    msg = str(exc).lower()
    return any(kw in msg for kw in _TRANSIENT_MESSAGE_KEYWORDS)


def _log_scrape_error(url_id: int, language: str, exc: Exception, context: str = "") -> None:
    """
    [FIX-024] Structured error logging with transient/fatal classification.
    - Transient errors: WARNING level (expected, will retry)
    - Fatal errors:     ERROR level (unexpected, needs investigation)
    """
    is_transient = _is_transient_error(exc)
    prefix = f"[{'TRANSIENT' if is_transient else 'FATAL'}] url_id={url_id} lang={language}"
    if context:
        prefix = f"{prefix} [{context}]"
    if is_transient:
        logger.warning("{}: {} — {}", prefix, type(exc).__name__, exc)
    else:
        logger.opt(exception=True).error("{}: {} — {}", prefix, type(exc).__name__, exc)


def _claim_active_url(url_id: int) -> bool:
    """
    [FIX ARCH-002] Reclama url_id de forma atómica.
    [FIX ERR-CONC-002] Usa _get_redis() que aplica socket_timeout en cada operación.
    [FIX ERR-ARCH-002] Usa _get_redis() que verifica salud antes de operar.
    Retorna True si el claim fue exitoso. Retorna False si ya está activo.
    """
    r = _get_redis()
    if r is not None:
        try:
            return bool(r.set(
                f"bsp:active:{url_id}", "1", nx=True, ex=_ACTIVE_ID_TTL
            ))
        except (ConnectionError, TimeoutError, OSError) as e:
            # [FIX ERR-PY-001] Specific exception types instead of bare Exception.
            # redis.ConnectionError/TimeoutError are subclasses of these builtins.
            logger.warning("[ARCH-002] Redis claim error (network/timeout, fallback local): %s", type(e).__name__)
        except Exception as e:
            # Unexpected error (programming bug, not transient) — log at ERROR
            logger.error("[ARCH-002] Redis claim unexpected error: %s — %s", type(e).__name__, e)
    with _active_ids_local_lock:
        if url_id in _active_ids:
            return False
        _active_ids.add(url_id)
        return True


def _release_active_url(url_id: int) -> None:
    """
    [FIX ARCH-002] Libera el claim de url_id al completar o fallar.
    [FIX ERR-CONC-002] socket_timeout aplicado vía _get_redis().
    """
    r = _get_redis()
    if r is not None:
        try:
            r.delete(f"bsp:active:{url_id}")
            return
        except (ConnectionError, TimeoutError, OSError) as e:
            # [FIX ERR-PY-001] Specific exception types for Redis release.
            logger.warning("[ARCH-002] Redis release network error: %s", type(e).__name__)
        except Exception as e:
            logger.error("[ARCH-002] Redis release unexpected error: %s — %s", type(e).__name__, e)
    with _active_ids_local_lock:
        _active_ids.discard(url_id)


# ─────────────────────────────────────────────────────────────────────────────
# [FIX CONC-002] Circuit breaker para operaciones VPN.
# Tras VPN_FAILURE_THRESHOLD fallos consecutivos, el circuit abre por
# VPN_COOLDOWN_SECONDS. Durante el cooldown, scraping continúa sin VPN
# (modo degradado) en lugar de bloquear el thread pool esperando reconexiones.
# ─────────────────────────────────────────────────────────────────────────────
_VPN_FAILURE_THRESHOLD  = int(os.getenv("VPN_FAILURE_THRESHOLD",  "5"))
_VPN_COOLDOWN_SECONDS   = int(os.getenv("VPN_COOLDOWN_SECONDS",   "300"))
_vpn_consecutive_fails: int   = 0
_vpn_circuit_open_until: float = 0.0
_vpn_circuit_lock = threading.Lock()


def _vpn_circuit_is_open() -> bool:
    """True si el circuit breaker está abierto — operar sin VPN temporalmente."""
    global _vpn_circuit_open_until, _vpn_consecutive_fails
    with _vpn_circuit_lock:
        now = time.monotonic()
        if _vpn_circuit_open_until > 0 and now >= _vpn_circuit_open_until:
            # Cooldown expirado → auto-reset (half-open state)
            logger.info("[CONC-002] VPN circuit breaker RESET — intentando reconexión")
            _vpn_circuit_open_until = 0.0
            _vpn_consecutive_fails = 0
        return time.monotonic() < _vpn_circuit_open_until


def _record_vpn_failure(reason: str = "") -> None:
    """Registra fallo VPN. Abre el circuit si se supera el umbral."""
    global _vpn_consecutive_fails, _vpn_circuit_open_until
    with _vpn_circuit_lock:
        _vpn_consecutive_fails += 1
        logger.warning(
            "[CONC-002] VPN fallo %d/%d: %s",
            _vpn_consecutive_fails, _VPN_FAILURE_THRESHOLD, reason,
        )
        if _vpn_consecutive_fails >= _VPN_FAILURE_THRESHOLD:
            _vpn_circuit_open_until = time.monotonic() + _VPN_COOLDOWN_SECONDS
            logger.error(
                "[CONC-002] VPN circuit ABIERTO por %ds — modo degradado sin VPN",
                _VPN_COOLDOWN_SECONDS,
            )


def _record_vpn_success() -> None:
    """Resetea el circuito tras una operación VPN exitosa."""
    global _vpn_consecutive_fails, _vpn_circuit_open_until
    with _vpn_circuit_lock:
        if _vpn_consecutive_fails > 0:
            logger.info("[CONC-002] VPN operación exitosa — reseteando contador de fallos")
        _vpn_consecutive_fails = 0
        _vpn_circuit_open_until = 0.0


def get_vpn_circuit_status() -> dict:
    """Estado del circuit breaker para el endpoint /vpn/status."""
    with _vpn_circuit_lock:
        now = time.monotonic()
        is_open = now < _vpn_circuit_open_until
        return {
            "circuit_open":             is_open,
            "consecutive_failures":     _vpn_consecutive_fails,
            "cooldown_remaining_seconds": max(0, int(_vpn_circuit_open_until - now)) if is_open else 0,
            "failure_threshold":        _VPN_FAILURE_THRESHOLD,
            "cooldown_seconds":         _VPN_COOLDOWN_SECONDS,
        }


_stats = {
    "total_dispatched":           0,
    "total_completed":            0,
    "total_failed":               0,
    "currently_processing":       0,
    "consecutive_failures":       0,
    "hotels_since_vpn_rotate":    0,
    "lang_mismatch_count":        0,
    "lang_mismatch_blocked":      0,
    # [FIX Recovery-001] Backoff deadline (monotonic). scrape_one() checks this
    # before each attempt to avoid hammering a flagged IP after rotation failure.
    # Value 0.0 = no active backoff.
    "vpn_rotation_backoff_until": 0.0,
}
_MAX_LANG_RETRY = 2
_stats_lock = threading.Lock()

# [v6.0] Limite maximo de URLs por batch (regla de negocio)
MAX_BATCH_SIZE: int = 10

_vpn_manager = None
_vpn_lock = threading.Lock()

# [FIX BUG-NEW-08] Context manager that acquires _vpn_lock with a timeout.
# Prevents indefinite deadlock when VPN operations hang (e.g. network timeout during connect).
# All callers use `with _vpn_lock_ctx():` instead of bare `with _vpn_lock_ctx():`.
from contextlib import contextmanager as _contextmanager

_VPN_LOCK_TIMEOUT = float(os.getenv("VPN_LOCK_TIMEOUT_SECONDS", "30"))

@_contextmanager
def _vpn_lock_ctx():
    """Acquire _vpn_lock with timeout. Raises RuntimeError if timed out."""
    acquired = _vpn_lock.acquire(timeout=_VPN_LOCK_TIMEOUT)
    if not acquired:
        raise RuntimeError(
            f"[BUG-NEW-08] _vpn_lock not acquired within {_VPN_LOCK_TIMEOUT}s — "
            "possible VPN operation hang. Aborting to avoid thread pool exhaustion."
        )
    try:
        yield
    finally:
        _vpn_lock.release()



def _get_vpn_manager():
    """
    Return the VPN manager singleton (thread-safe).

    Returns:
        NordVPNManagerWindows instance, or None if VPN is disabled or
        the lock cannot be acquired (lock timeout → returns None gracefully
        instead of propagating RuntimeError to the caller).

    Note:
        [FIX BUG-V9-008] _vpn_lock_ctx() raises RuntimeError when the lock
        cannot be acquired within VPN_LOCK_TIMEOUT seconds. Callers of
        _get_vpn_manager() did not catch RuntimeError, causing unhandled
        exceptions that crashed threads. Wrapped here so the function always
        returns None on lock timeout (degraded mode: no VPN).
    """
    global _vpn_manager
    # [FIX CONC-002] Verificar circuit breaker antes de intentar cualquier operación VPN.
    # Si está abierto, retornar None → el caller opera en modo degradado sin VPN.
    if _vpn_circuit_is_open():
        logger.debug("[CONC-002] VPN circuit abierto — retornando None (modo degradado)")
        return None
    if not settings.VPN_ENABLED:
        return None
    try:
        with _vpn_lock_ctx():
            if _vpn_manager is None:
                try:
                    from app.vpn_manager import vpn_manager_factory
                    _vpn_manager = vpn_manager_factory(interactive=False)
                    logger.info("VPN Manager iniciado (singleton)")
                except Exception as e:
                    logger.error(f"Error iniciando VPN Manager: {e}")
                    _vpn_manager = None
        return _vpn_manager
    except RuntimeError as lock_err:
        # [FIX BUG-V9-008] Lock timeout — degrade gracefully, do not crash caller
        logger.warning(f"[_get_vpn_manager] Lock timeout — VPN no disponible: {lock_err}")
        return None


def rotate_vpn_now() -> Dict:
    """
    [FIX BUG-NEW-17] Rotate VPN to a new server immediately.

    Returns:
        Dict with keys: success (bool), reason (str on failure),
        new_ip (str), country (str), server (str).
    Raises:
        RuntimeError: if _vpn_lock cannot be acquired within timeout.
    """
    vpn = _get_vpn_manager()
    if not vpn:
        return {"success": False, "reason": "VPN_ENABLED=False o VPN no disponible"}
    with _vpn_lock_ctx():
        try:
            logger.info("Rotacion VPN manual solicitada...")
            success = vpn.rotate(reason="manual")
            _log_vpn_rotation_to_db(vpn, reason="manual")  # [BUG-001 FIX]
            with _stats_lock:
                _stats["consecutive_failures"] = 0
                _stats["hotels_since_vpn_rotate"] = 0
            _record_vpn_success()  # [FIX CONC-002] reset circuit breaker
            return {"success": success, "new_ip": vpn.current_ip, "server": vpn.current_server}
        except Exception as e:
            logger.error(f"Error rotando VPN: {e}")
            _record_vpn_failure(str(e))  # [FIX CONC-002] track para circuit breaker
            return {"success": False, "error": str(e)}


def _log_vpn_rotation_to_db(vpn, reason: str = "periodica"):
    """
    [BUG-001 FIX] Persiste el evento de rotación VPN en la tabla vpn_rotations.

    Desacoplamiento: vpn_manager_windows.py NO tiene dependencia de BD.
    En su lugar, expone last_rotation_info y este helper lo persiste.
    Se llama DESPUÉS de cada rotate() exitoso o fallido.

    Arquitectura:
      NordVPNManagerWindows.rotate() → popula last_rotation_info
      _log_vpn_rotation_to_db()     → lee ese dict y hace INSERT en vpn_rotations
    """
    if vpn is None:
        return
    info = getattr(vpn, "last_rotation_info", None)
    if not info:
        return
    db = SessionLocal()
    try:
        db.execute(
            text("""
                INSERT INTO vpn_rotations
                    (old_ip, new_ip, country, rotation_reason, requests_count, success, error_message)
                VALUES
                    (:old_ip, :new_ip, :country, :rotation_reason, :requests_count, :success, :error_message)
            """),
            {
                "old_ip":          info.get("old_ip"),
                "new_ip":          info.get("new_ip"),
                "country":         info.get("country"),
                "rotation_reason": reason or info.get("rotation_reason", "desconocida"),
                "requests_count":  info.get("requests_count", 0),
                "success":         info.get("success", False),
                "error_message":   info.get("error_message"),
            }
        )
        db.commit()
        logger.debug(
            f"[BUG-001] VPN rotation registrada: {info.get('old_ip')} → {info.get('new_ip')} "
            f"({info.get('country')}, success={info.get('success')})"
        )
    except Exception as e:
        logger.error(f"[BUG-001] Error persistiendo vpn_rotation: {e}")
        try:
            db.rollback()
        except Exception:
            pass
    finally:
        db.close()


def get_vpn_status() -> Dict:
    """
    [BUG-005 FIX / BUG-V7-012] Returns current VPN status and cumulative rotation metrics.

    Called from GET /vpn/status. Exposes in-memory stats accumulated since process start.

    Returns:
        dict with keys:
          - enabled (bool): whether VPN_ENABLED=True in .env
          - reason (str): only present when enabled=False
          - hotels_since_rotate (int): hotels scraped since last VPN rotation
          - consecutive_failures (int): consecutive scraping failures triggering rotation
          - lang_mismatch_count (int): times wrong-language content was detected
          - lang_mismatch_blocked (int): times URL was blocked due to language mismatch
          - total_dispatched (int): total URLs dispatched since process start
          - total_completed (int): total URLs completed (all languages) since process start
          - Plus all fields from vpn.get_status() (country, ip, rotations, etc.)

    Raises:
        No exceptions raised — errors are caught and logged internally.
    """
    vpn = _get_vpn_manager()
    if not vpn:
        return {"enabled": False, "reason": "VPN_ENABLED=False en .env"}
    try:
        return {
            "enabled": True,
            **vpn.get_status(),
            "hotels_since_rotate":   _stats.get("hotels_since_vpn_rotate", 0),
            "consecutive_failures":  _stats.get("consecutive_failures", 0),
            "lang_mismatch_count":   _stats.get("lang_mismatch_count", 0),
            "lang_mismatch_blocked": _stats.get("lang_mismatch_blocked", 0),
            "total_dispatched":      _stats.get("total_dispatched", 0),
            "total_completed":       _stats.get("total_completed", 0),
            "total_failed":          _stats.get("total_failed", 0),
            "currently_processing":  _stats.get("currently_processing", 0),
        }
    except Exception as e:
        return {"enabled": True, "error": str(e)}


def _maybe_rotate_vpn(force: bool = False, reason: str = "") -> None:
    """
    Rota la VPN si se supero el limite o hay demasiados fallos.
    [BUG-001 FIX] Persiste el evento en vpn_rotations via _log_vpn_rotation_to_db.
    [FIX Recovery-001] When rotation fails and IP is already flagged (consecutive
    failures >= threshold), applies exponential backoff before the next scraping
    attempt to avoid hammering Booking.com with a known-blocked IP.
    """
    vpn = _get_vpn_manager()
    if not vpn:
        return
    with _stats_lock:
        consec = _stats["consecutive_failures"]
        since_rotate = _stats["hotels_since_vpn_rotate"]
    rotate_every = getattr(settings, "VPN_ROTATE_EVERY_N", 10)
    too_many_failures = consec >= 3
    if not (force or since_rotate >= rotate_every or too_many_failures):
        return
    auto_reason = "manual" if force else ("bloqueo_ip" if too_many_failures else "periodica")
    effective_reason = reason or auto_reason
    logger.info(f"Rotando VPN (motivo={effective_reason}, fallos={consec}, hoteles={since_rotate})...")
    with _vpn_lock_ctx():
        try:
            success = vpn.rotate(reason=effective_reason)
            _log_vpn_rotation_to_db(vpn, reason=effective_reason)  # [BUG-001 FIX]
            if success:
                with _stats_lock:
                    _stats["consecutive_failures"] = 0
                    _stats["hotels_since_vpn_rotate"] = 0
                    _stats["vpn_rotation_backoff_until"] = 0.0
                logger.success(f"VPN rotada -> IP: {vpn.current_ip}")
            else:
                # [FIX BUG-16-009] Reset consecutive_failures even on failed rotate.
                with _stats_lock:
                    _stats["consecutive_failures"] = 1
                    _stats["hotels_since_vpn_rotate"] = 0
                # [FIX Recovery-001] When the old IP is likely flagged (we rotated
                # because of consecutive failures) and rotation itself failed, the
                # next scraping attempt with the same IP is very likely to be blocked
                # again. Apply exponential backoff (base 30s, max 300s) so we don't
                # hammer Booking.com with a known-blocked IP.
                if too_many_failures:
                    # Backoff duration doubles with each consecutive failure cluster.
                    # Stored in _stats so scrape_one() can check before dispatching.
                    backoff_secs = min(30 * (2 ** max(consec - 3, 0)), 300)
                    backoff_until = time.monotonic() + backoff_secs
                    with _stats_lock:
                        _stats["vpn_rotation_backoff_until"] = backoff_until
                    logger.warning(
                        "[Recovery-001] VPN rotation failed on flagged IP "
                        "(consec_failures=%d). Applying %ds backoff before next attempt.",
                        consec, backoff_secs,
                    )
                else:
                    logger.warning("Rotacion VPN fallo - continuando con IP actual (failures reset a 1)")
        except Exception as e:
            logger.opt(exception=True).error(f"[BUG-16-008] Error en rotacion VPN: {e}")


# =============================================================================
# [v6.0] HELPER: LEER IDIOMAS DESDE SNAPSHOT EN url_language_status
# =============================================================================

def _get_languages_for_url(db, url_id: int) -> List[str]:
    """
    Lee los idiomas a procesar para una URL desde url_language_status.

    FUENTE DE VERDAD: El snapshot registrado por initialize_url_processing()
    al momento de la carga. Garantiza que si LANGUAGES_ENABLED cambia
    mientras el scraper corre, las URLs ya inicializadas no se ven afectadas.

    ORDENAMIENTO: settings.DEFAULT_LANGUAGE siempre primero, resto alfabético.

    [FIX BUG-V9-015] NOTA DE COMPORTAMIENTO: La lógica de ordenamiento coloca
    DEFAULT_LANGUAGE al inicio tanto en la consulta SQL (CASE WHEN language =
    :default_lang THEN 0 ELSE 1) como en el fallback Python. Si DEFAULT_LANGUAGE
    se cambia en la configuración, los URLs ya inicializados respetan el idioma
    que tenían al snapshot (correcto), pero los fallback URLs de pre-migración
    usarán el nuevo DEFAULT como primer idioma (comportamiento esperado).
    Este es el diseño intencionado documentado explícitamente aquí.

    FALLBACK: Si no hay snapshot (URL pre-migración), usa settings.ENABLED_LANGUAGES.

    Args:
        db:     SQLAlchemy session.
        url_id: Primary key from url_queue.

    Returns:
        List[str]: Language codes ordered with DEFAULT_LANGUAGE first.
    """
    DEFAULT = settings.DEFAULT_LANGUAGE  # "en"
    try:
        rows = db.execute(
            text("""
                SELECT language
                FROM   url_language_status
                WHERE  url_id = :url_id
                ORDER BY
                    CASE WHEN language = :default_lang THEN 0 ELSE 1 END,
                    language
            """),
            {"url_id": url_id, "default_lang": DEFAULT}
        ).fetchall()

        if rows:
            languages = [r[0] for r in rows]
            logger.debug(f"  [{url_id}] Idiomas desde snapshot: {languages}")
            return languages

        # Fallback: URL sin snapshot (pre-migracion)
        logger.warning(
            f"  [{url_id}] Sin snapshot en url_language_status. "
            f"Usando settings.ENABLED_LANGUAGES como fallback."
        )
        fallback = list(settings.ENABLED_LANGUAGES)
        if DEFAULT in fallback:
            return [DEFAULT] + [l for l in fallback if l != DEFAULT]
        return [DEFAULT] + fallback

    except Exception as e:
        logger.error(f"  [{url_id}] Error leyendo idiomas desde snapshot: {e}. Fallback.")
        fallback = list(settings.ENABLED_LANGUAGES)
        if DEFAULT in fallback:
            return [DEFAULT] + [l for l in fallback if l != DEFAULT]
        return [DEFAULT] + fallback


# =============================================================================
# PUNTO DE ENTRADA: PROCESAR BATCH
# =============================================================================

def process_batch(batch_size: int = 5) -> Dict:
    """
    Obtiene URLs pendientes de la BD y las envia al thread pool.
    Thread-safe. Puede llamarse desde asyncio (via run_in_executor).

    [v6.0] Hard cap: batch_size no puede superar MAX_BATCH_SIZE (10).
    """
    # [FIX HIGH-001] Reject invalid batch_size instead of silently capping.
    # Silent capping hid misconfiguration from callers; explicit rejection
    # forces the caller to fix the value, preventing repeated misconfigured calls.
    if batch_size < 1:
        raise ValueError(f"batch_size must be >= 1, got {batch_size}")
    if batch_size > MAX_BATCH_SIZE:
        raise ValueError(
            f"batch_size={batch_size} exceeds MAX_BATCH_SIZE={MAX_BATCH_SIZE}. "
            "Reduce the requested batch size."
        )

    # [FIX v5.0] VPN al iniciar: preferir UK para en-gb
    # [BUG-004 FIX] Timeout máximo para todo el bloque de failover VPN.
    vpn = _get_vpn_manager()
    if vpn and settings.VPN_ENABLED:
        _failover_start = time.time()
        _failover_timeout = getattr(settings, "VPN_FAILOVER_TIMEOUT_SECS", 90)
        try:
            if not vpn.verify_vpn_active():
                logger.warning("VPN inactiva al procesar batch - conectando a UK...")
                success = vpn.connect("UK")
                if not success:
                    if (time.time() - _failover_start) >= _failover_timeout:
                        logger.error(
                            f"[BUG-004] Timeout de failover VPN ({_failover_timeout}s). "
                            f"Continuando en modo degradado (sin VPN)."
                        )
                    else:
                        logger.warning("Conexion a UK fallo - intentando cualquier pais...")
                        vpn.connect()
                        if (time.time() - _failover_start) >= _failover_timeout:
                            logger.error(
                                f"[BUG-004] Timeout de failover VPN tras segundo intento. "
                                f"Modo degradado activado."
                            )
        except Exception as e:
            logger.warning(f"Error verificando VPN: {e}")

    db = SessionLocal()
    try:
        # [FIX CRIT-003] Atomic CTE dispatch: SELECT + UPDATE in a single SQL statement.
        # The previous two-step approach (SELECT ... FOR UPDATE SKIP LOCKED, then
        # separate UPDATE) still had a small window where:
        #   - Locks were held on ALL selected rows, but
        #   - _claim_active_url() could filter some out before the UPDATE ran, leaving
        #     those rows locked-but-not-updated until commit, blocking other workers.
        #
        # The CTE eliminates this by atomically locking AND updating only the rows
        # that will actually be dispatched, returning their IDs in one round-trip.
        # RETURNING id removes the need for a subsequent SELECT entirely.
        #
        # FOR UPDATE SKIP LOCKED inside the CTE still provides cross-process safety.
        # _claim_active_url() is retained as a same-process secondary guard only.
        rows = db.execute(
            text("""
                WITH selected AS (
                    SELECT id FROM url_queue
                    WHERE  status = 'pending'
                      AND  retry_count < max_retries
                    ORDER BY priority DESC, created_at ASC
                    LIMIT  :limit
                    FOR UPDATE SKIP LOCKED
                )
                UPDATE url_queue
                   SET status     = 'processing',
                       updated_at = NOW()
                 WHERE id IN (SELECT id FROM selected)
                RETURNING id
            """),
            {"limit": batch_size}
        ).fetchall()

        url_ids = [r[0] for r in rows]

        if not url_ids:
            logger.debug("No hay URLs pendientes para despachar")
            db.rollback()
            return {"dispatched": 0, "message": "No hay URLs pendientes"}

        # [FIX ARCH-002] Secondary same-process guard via Redis/local set.
        # The CTE already guarantees cross-process correctness; this guard
        # prevents duplicate work only within the same process.
        new_ids = [uid for uid in url_ids if _claim_active_url(uid)]

        if not new_ids:
            # Rows were updated to 'processing' by the CTE but all were already
            # claimed in-process — roll back to return them to 'pending'.
            db.rollback()
            return {"dispatched": 0, "message": "Todas las URLs ya estan en proceso"}

        db.commit()

        dispatched_ids = []
        for uid in new_ids:
            submitted = _submit_with_backpressure(uid)
            if submitted:
                dispatched_ids.append(uid)
            else:
                # Backpressure: release URL back to pending
                _release_active_url(uid)
                with SessionLocal() as _rollback_db:
                    try:
                        _rollback_db.execute(
                            text("UPDATE url_queue SET status='pending', updated_at=NOW() WHERE id=:id AND status='processing'"),
                            {"id": uid}
                        )
                        _rollback_db.commit()
                    except Exception as _rb_err:
                        _rollback_db.rollback()
                        logger.warning("[CRIT-004] Could not reset url_id=%d to pending: %s", uid, _rb_err)
        new_ids = dispatched_ids

        with _stats_lock:
            _stats["total_dispatched"] += len(new_ids)
            _stats["currently_processing"] += len(new_ids)

        logger.info(f"Despachadas {len(new_ids)} URLs al thread pool")
        return {"dispatched": len(new_ids), "url_ids": new_ids}

    except Exception as e:
        logger.opt(exception=True).error(f"Error en process_batch: {e}")
        return {"dispatched": 0, "error": str(e)}
    finally:
        db.close()


# =============================================================================
# SCRAPING DE UN HOTEL INDIVIDUAL
# =============================================================================

def _run_safe(url_id: int) -> None:
    """
    Thread-pool worker wrapper: scrape one URL and release its active-ID slot.

    [FIX BUG-V11-009] Full parameter, return and exception documentation added.

    Ensures `url_id` is always removed from `_active_ids` even if `scrape_one()`
    raises an unexpected exception, preventing the thread pool from leaking
    active-ID reservations that would block the same URL from being re-queued.

    Args:
        url_id (int): Primary key from url_queue to process.

    Returns:
        None

    Raises:
        Never — all exceptions from scrape_one() are caught and logged at ERROR.
    """
    try:
        scrape_one(url_id)
    except Exception as e:
        logger.opt(exception=True).error(f"[BUG-16-008] Error inesperado en _run_safe({url_id}): {e}")
    finally:
        _release_active_url(url_id)  # [FIX ARCH-002] atomic release via Redis or local
        with _stats_lock:
            _stats["currently_processing"] = max(0, _stats["currently_processing"] - 1)


def scrape_one(url_id: int) -> Dict:
    """
    Scrapea un hotel completo en todos los idiomas del snapshot.

    [v6.0] CAMBIOS CRITICOS:
    - initialize_url_processing(): registra snapshot de idiomas en url_language_status.
    - _get_languages_for_url(): lee idiomas desde snapshot, no desde settings.
    - Retry loop por idioma: hasta MAX_LANG_RETRIES intentos adicionales.
    - record_language_success/skipped/failure(): tracking granular por idioma.
    - finalize_url(): determina completed (todos OK) o incomplete (algun fallo).

    [v2.1] Con Selenium: crea UN SOLO driver por hotel.
    """
    db = SessionLocal()
    start_time = time.time()
    DEFAULT = settings.DEFAULT_LANGUAGE  # "en"

    try:
        row = db.execute(
            text("SELECT url, language FROM url_queue WHERE id = :id"),
            {"id": url_id}
        ).fetchone()

        if not row:
            logger.error(f"URL ID {url_id} no encontrada en url_queue")
            return {"error": "URL no encontrada"}

        base_url   = row[0]
        queue_lang = row[1] or "en"
        logger.info(f"\n{chr(8212)*60}")
        logger.info(f"Iniciando scraping | ID={url_id} | lang_queue={queue_lang} | {base_url}")
        logger.info(f"{chr(8212)*60}")

        # [FIX Recovery-001] Respect VPN rotation backoff before attempting scrape.
        # If _maybe_rotate_vpn() set a backoff window (rotation failed on flagged IP),
        # sleep here so the next attempt doesn't immediately hammer the same blocked IP.
        with _stats_lock:
            backoff_until = _stats.get("vpn_rotation_backoff_until", 0.0)
        remaining = backoff_until - time.monotonic()
        if remaining > 0:
            logger.info(
                "[Recovery-001] VPN backoff active — sleeping {:.1f}s before scraping url_id={}",
                remaining, url_id,
            )
            time.sleep(min(remaining, 300))  # cap at 5 min; remaining should already be ≤300

        # VPN check
        vpn = _get_vpn_manager()
        if vpn and settings.VPN_ENABLED:
            try:
                with _vpn_lock_ctx():
                    vpn.reconnect_if_disconnected()
            except Exception as vpn_err:
                logger.warning(f"VPN check error: {vpn_err}")

        from app.scraper import BookingScraper, build_language_url, purge_debug_html

        # [v6.0] Snapshot de idiomas en url_language_status (idempotente)
        completeness_service.initialize_url_processing(url_id, db)
        db.commit()

        # [v6.0] Leer idiomas desde snapshot -- NO desde settings.ENABLED_LANGUAGES
        languages = _get_languages_for_url(db, url_id)
        # [FIX DB-003] Orden de procesamiento de idiomas consistente entre todos los workers.
        # Sin orden fijo: Worker A bloquea lang='de', Worker B bloquea lang='en',
        # luego cada uno espera al otro → deadlock garantizado con FOR UPDATE.
        # Ordenar alfabéticamente garantiza que todos los workers intentan los locks
        # en el mismo orden → elimina el ciclo de espera circular (ANSI SQL lock ordering).
        languages = sorted(languages)

        scraped_count     = 0
        hotel_name        = None
        lang_failures     = 0
        images_downloaded = False

        if settings.USE_SELENIUM:
            scraper_instance = BookingScraper()
        else:
            scraper_instance = None

        try:
            for lang in languages:
                lang_url = build_language_url(base_url, lang)
                logger.info("  -> [%s] Idioma [%s]: %s", url_id, lang, _sanitize_url_log(lang_url))  # [FIX ERR-SEC-006]

                lang_succeeded = False

                # [v6.0] Retry loop por idioma
                # range(1, MAX_LANG_RETRIES+2) = [1,2] con MAX_LANG_RETRIES=1
                for attempt in range(1, MAX_LANG_RETRIES + 2):
                    try:
                        if settings.USE_SELENIUM:
                            data = scraper_instance.scrape_hotel(lang_url, language=lang)
                        else:
                            with BookingScraper() as scraper:
                                data = scraper.scrape_hotel(lang_url, language=lang)

                        # Sin datos
                        if not data or not data.get("name"):
                            logger.warning(f"  [{url_id}][{lang}] Sin datos (attempt={attempt})")
                            _log(db, url_id, lang, "no_data",
                                 time.time() - start_time, 0, "Sin datos extraidos")
                            has_retry = completeness_service.record_language_failure(
                                url_id, lang, "Sin datos extraidos", db
                            )
                            db.commit()
                            if has_retry and attempt <= MAX_LANG_RETRIES:
                                logger.info(f"  [{url_id}][{lang}] Reintentando (attempt {attempt+1})...")
                                continue
                            else:
                                lang_failures += 1
                                break

                        if hotel_name is None:
                            hotel_name = data["name"]

                        # Verificacion de idioma detectado
                        detected = data.get("detected_lang")
                        if detected and detected != lang:
                            logger.error(
                                f"  [{url_id}][{lang}] IDIOMA INCORRECTO - NO SE GUARDA: "
                                f"solicitado='{lang}', pagina en '{detected}'"
                            )
                            with _stats_lock:
                                _stats["lang_mismatch_count"] = _stats.get("lang_mismatch_count", 0) + 1
                                _stats["lang_mismatch_blocked"] = _stats.get("lang_mismatch_blocked", 0) + 1

                            _log(db, url_id, lang, "lang_mismatch",
                                 time.time() - start_time, 0,
                                 f"Pagina en '{detected}', solicitado '{lang}'. NO guardado.")

                            has_retry = completeness_service.record_language_failure(
                                url_id, lang,
                                f"lang_mismatch: solicitado={lang} detectado={detected}", db
                            )
                            db.commit()

                            if lang == DEFAULT and _stats.get("lang_mismatch_count", 0) >= 3:
                                logger.warning(f"  [{url_id}] Mismatches acumulados - rotando VPN...")
                                _maybe_rotate_vpn(force=True, reason="lang_mismatch_acumulado")
                                with _stats_lock:
                                    _stats["lang_mismatch_count"] = 0

                            if has_retry and attempt <= MAX_LANG_RETRIES:
                                # [BUG-003 FIX] Rotar VPN antes de reintentar idioma incorrecto.
                                # El reintento con la misma IP recibirá el mismo contenido geo-cacheado.
                                # Con nueva IP, Booking.com sirve el idioma correcto para la cookie.
                                logger.info(
                                    f"  [{url_id}][{lang}] Rotando VPN antes de reintento "
                                    f"(mismatch: solicitado={lang} detectado={detected})..."
                                )
                                _maybe_rotate_vpn(force=True, reason=f"lang_mismatch_{lang}_retry_{attempt}")
                                time.sleep(3)  # breve pausa para estabilizar nueva IP
                                logger.info(
                                    f"  [{url_id}][{lang}] Reintentando por mismatch "
                                    f"(attempt {attempt+1})..."
                                )
                                continue
                            else:
                                lang_failures += 1
                                break
                        else:
                            with _stats_lock:
                                _stats["lang_mismatch_count"] = 0

                        # Guardar en BD
                        saved = _save_hotel(db, url_id, lang_url, lang, data)

                        if saved:
                            scraped_count += 1
                            lang_failures  = 0
                            completeness_service.record_language_success(url_id, lang, db)
                            db.commit()
                        else:
                            logger.debug(
                                f"  [{url_id}][{lang}] Registro ya existe - "
                                f"preservando (ON CONFLICT DO NOTHING)"
                            )
                            scraped_count += 1
                            completeness_service.record_language_skipped(url_id, lang, db)
                            db.commit()

                        duration   = time.time() - start_time
                        imgs_count = len(data.get("images_urls") or [])
                        _log(db, url_id, lang, "completed", duration, 1)

                        logger.success(
                            f"  [{url_id}][{lang}] '{hotel_name}' "
                            f"| rating={data.get('rating')} | imgs={imgs_count}"
                        )

                        # Descarga de imagenes: solo lang=DEFAULT confirmado
                        if lang == DEFAULT and not images_downloaded and settings.DOWNLOAD_IMAGES:
                            imgs = data.get("images_urls") or []
                            if imgs:
                                driver = scraper_instance.driver if settings.USE_SELENIUM else None
                                n_downloaded = _download_images(url_id, imgs, DEFAULT, driver=driver)
                                if n_downloaded and n_downloaded > 0:
                                    try:
                                        db.execute(
                                            text("""
                                                UPDATE hotels
                                                SET images_count = :count, updated_at = NOW()
                                                WHERE url_id = :url_id AND language = :lang
                                            """),
                                            {"count": n_downloaded, "url_id": url_id, "lang": DEFAULT}
                                        )
                                        db.commit()
                                    except Exception as upd_err:
                                        logger.debug(f"  No se pudo actualizar images_count: {upd_err}")
                            images_downloaded = True

                        lang_succeeded = True
                        break  # exito -> salir del retry loop

                    except Exception as lang_err:
                        err_str = str(lang_err)
                        # [FIX BUG-V7-011] [:200] here is intentional — this is a console log line for operator readability.
                        # Storage path uses _log() which applies _MAX_ERROR_LEN=2000.
                        logger.opt(exception=True).error(
                        f"  [{url_id}][{lang}] attempt={attempt}: {err_str[:500]}")
                        try:
                            db.rollback()
                        except Exception:
                            pass

                        # Brave crasheo -> recrear driver y reintentar
                        if settings.USE_SELENIUM and "invalid session id" in err_str.lower():
                            logger.warning(f"  [{url_id}][{lang}] Brave crasheo - recreando driver...")
                            try:
                                scraper_instance.close()
                            except Exception:
                                pass
                            try:
                                scraper_instance = BookingScraper()
                                data = scraper_instance.scrape_hotel(lang_url, language=lang)
                                if data and data.get("name"):
                                    if hotel_name is None:
                                        hotel_name = data["name"]
                                    saved = _save_hotel(db, url_id, lang_url, lang, data)
                                    scraped_count += 1
                                    lang_failures  = 0
                                    duration = time.time() - start_time
                                    _log(db, url_id, lang, "completed", duration,
                                         len(data.get("images_urls") or []))
                                    if saved:
                                        completeness_service.record_language_success(url_id, lang, db)
                                    else:
                                        completeness_service.record_language_skipped(url_id, lang, db)
                                    db.commit()
                                    logger.success(f"  [{url_id}][{lang}] '{hotel_name}' (recuperado)")
                                    if not images_downloaded and settings.DOWNLOAD_IMAGES:
                                        imgs = data.get("images_urls") or []
                                        if imgs:
                                            drv = scraper_instance.driver if settings.USE_SELENIUM else None
                                            n_dl = _download_images(url_id, imgs, DEFAULT, driver=drv)
                                            if n_dl and n_dl > 0:
                                                try:
                                                    # [FIX BUG-B-04] Missing AND language=:lang filter.
                                                    # Without it, the UPDATE affects ALL language rows
                                                    # for this url_id (en, es, de, fr, it), incorrectly
                                                    # overwriting images_count for languages not yet scraped.
                                                    # This is the crash-recovery path; it must use the
                                                    # same scoped UPDATE as the normal path (lines 617-623).
                                                    db.execute(
                                                        text("UPDATE hotels SET images_count=:c, updated_at=NOW() WHERE url_id=:u AND language=:lang"),
                                                        {"c": n_dl, "u": url_id, "lang": DEFAULT}
                                                    )
                                                    db.commit()
                                                except Exception:
                                                    pass
                                        images_downloaded = True
                                    lang_succeeded = True
                                    break
                            except Exception as retry_err:
                                logger.error(f"  [{url_id}][{lang}] Reintento tras crash fallido: {retry_err}")
                                try:
                                    db.rollback()
                                except Exception:
                                    pass

                        # [FIX BUG-V7-006] Removed redundant [:500] slice — _log() truncates to 2000 chars
                        _log(db, url_id, lang, "error", time.time() - start_time, 0, err_str)
                        has_retry = completeness_service.record_language_failure(
                            url_id, lang, err_str, db
                        )
                        try:
                            db.commit()
                        except Exception:
                            pass

                        if has_retry and attempt <= MAX_LANG_RETRIES:
                            logger.info(
                                f"  [{url_id}][{lang}] Reintentando tras error "
                                f"(attempt {attempt+1})..."
                            )
                            continue
                        else:
                            lang_failures += 1
                            if lang_failures >= 3:
                                logger.warning(f"  [{url_id}] {lang_failures} fallos - posible bloqueo IP")
                                with _stats_lock:
                                    _stats["consecutive_failures"] += 1
                                _maybe_rotate_vpn()
                            break

                if not lang_succeeded:
                    logger.warning(f"  [{url_id}][{lang}] Idioma fallido definitivamente.")

        finally:
            if settings.USE_SELENIUM and scraper_instance is not None:
                try:
                    scraper_instance.close()
                    logger.debug(f"  Driver Selenium cerrado para hotel {url_id}")
                except Exception:
                    pass

        # [v6.0] Finalizacion via completeness_service
        # Evalua completitud -> actualiza url_queue a 'completed' o 'incomplete'
        try:
            report       = completeness_service.finalize_url(url_id, db)
            final_status = "completed" if report.is_complete else "incomplete"
        except Exception as finalize_err:
            logger.opt(exception=True).error(f"[{url_id}] Error en finalize_url: {finalize_err}")
            final_status = "completed" if scraped_count > 0 else "failed"
            db.execute(
                text("""
                    UPDATE url_queue
                    SET status = :status, scraped_at = NOW(), updated_at = NOW()
                    WHERE id = :id
                """),
                {"status": final_status, "id": url_id}
            )
            db.commit()

        total_dur = time.time() - start_time

        if scraped_count > 0:
            with _stats_lock:
                _stats["total_completed"] += 1
                _stats["consecutive_failures"] = 0
                _stats["hotels_since_vpn_rotate"] += 1
            _maybe_rotate_vpn()
            logger.success(
                f"[{url_id}] {final_status.upper()} | '{hotel_name}' "
                f"| {scraped_count}/{len(languages)} idiomas | {total_dur:.1f}s"
            )
        else:
            with _stats_lock:
                _stats["total_failed"] += 1
                _stats["consecutive_failures"] += 1
            _maybe_rotate_vpn()
            logger.error(f"[{url_id}] FALLIDO | {total_dur:.1f}s")

        return {
            "success":    scraped_count > 0,
            "hotel_name": hotel_name,
            "languages":  scraped_count,
            "duration":   round(total_dur, 2),
            "status":     final_status,
        }

    except Exception as e:
        logger.error(f"Error fatal URL {url_id}: {e}", exc_info=True)
        db.rollback()
        with _stats_lock:
            _stats["total_failed"] += 1
            _stats["consecutive_failures"] += 1
        _maybe_rotate_vpn()
        try:
            db.execute(
                text("""
                    UPDATE url_queue
                    SET status = CASE
                            WHEN retry_count + 1 >= max_retries THEN 'failed'
                            ELSE 'pending'
                        END,
                        retry_count = retry_count + 1,
                        last_error  = :error,
                        updated_at  = NOW()
                    WHERE id = :id
                """),
                {"id": url_id, "error": str(e)[:settings.MAX_ERROR_LEN]}
            )
            db.commit()
        except Exception:
            pass
        return {"error": str(e)}

    finally:
        db.close()


# =============================================================================
# HELPERS INTERNOS
# =============================================================================

def _save_hotel(db, url_id: int, url: str, lang: str, data: Dict) -> bool:
    """
    Inserta un hotel. ON CONFLICT DO NOTHING preserva datos existentes.
    Returns True si se inserto nuevo registro, False si ya existia.
    """
    # [FIX CRIT-008] Validate extractor output with Pydantic schema before INSERT.
    # Prevents malformed JSONB from reaching the database (e.g. dict where array expected).
    from app.extractor import validate_hotel_data
    try:
        data = validate_hotel_data(data)
    except (ValueError, TypeError) as _val_err:
        logger.error(
            "[CRIT-008] JSONB validation failed for url_id=%s lang=%s: %s. "
            "Skipping INSERT to prevent DB constraint violation.",
            url_id, lang, _val_err,
        )
        raise ValueError(f"Hotel data validation failed: {_val_err}") from _val_err

    result = db.execute(
        text("""
            INSERT INTO hotels (
                url_id, url, language,
                name, address, description,
                rating, total_reviews, rating_category,
                review_scores, services, facilities,
                house_rules, important_info,
                rooms_info, images_urls, images_count,
                scraped_at, updated_at
            ) VALUES (
                :url_id, :url, :language,
                :name, :address, :description,
                :rating, :total_reviews, :rating_category,
                CAST(:review_scores AS jsonb), CAST(:services AS jsonb), CAST(:facilities AS jsonb),
                :house_rules, :important_info,
                CAST(:rooms_info AS jsonb), CAST(:images_urls AS jsonb), 0,
                NOW(), NOW()
            )
            ON CONFLICT (url_id, language) DO NOTHING
        """),
        {
            "url_id":           url_id,
            "url":              url,
            "language":         lang,
            "name":             data.get("name"),
            "address":          data.get("address"),
            "description":      data.get("description"),
            "rating":           data.get("rating"),
            "total_reviews":    data.get("total_reviews"),
            "rating_category":  data.get("rating_category"),
            "review_scores":    json.dumps(data.get("review_scores") or {}),
            "services":         json.dumps(data.get("services")      or []),
            "facilities":       json.dumps(data.get("facilities")    or {}),
            "house_rules":      data.get("house_rules"),
            "important_info":   data.get("important_info"),
            "rooms_info":       json.dumps(data.get("rooms")         or []),
            "images_urls":      json.dumps(data.get("images_urls")   or []),
        }
    )
    db.commit()
    return result.rowcount > 0


def _download_images(url_id: int, img_urls: List[str], lang: str, driver=None) -> int:
    """
    Download hotel images and persist them to disk via ImageDownloader.

    [FIX BUG-V11-009] Full parameter and return documentation added.

    Args:
        url_id (int):       Primary key from url_queue — determines storage path.
        img_urls (List[str]): List of HTTP/HTTPS image URLs to download.
        lang (str):         ISO 639-1 language code for the storage subdirectory.
        driver:             Optional Selenium WebDriver instance. If provided,
                            its cookies are injected into the download session to
                            bypass CDN authentication that requires browser state.
                            Pass None when calling from the CloudScraper backend.

    Returns:
        int: Number of images successfully saved to disk.
             Returns 0 if img_urls is empty or all downloads fail.

    Raises:
        Never — all errors are caught internally and logged at WARNING level.
    """
    if not img_urls:
        return 0
    try:
        from app.image_downloader import ImageDownloader
        import requests as _req
        session = _req.Session()
        session.headers.update({
            "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer":         "https://www.booking.com/",
            "Accept":          "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,*;q=0.5",
            "sec-fetch-dest":  "image",
            "sec-fetch-mode":  "no-cors",
            "sec-fetch-site":  "cross-site",
        })
        if driver:
            try:
                browser_cookies = driver.get_cookies()
                for c in browser_cookies:
                    session.cookies.set(c["name"], c["value"], domain=c.get("domain", ".booking.com"))
            except Exception as ce:
                logger.debug(f"  [{url_id}] No se pudieron extraer cookies: {ce}")
        dl = ImageDownloader()
        results = dl.download_images(url_id, img_urls, language=lang, session=session)
        ok = len(results)
        logger.info(f"  [{url_id}] {ok}/{len(img_urls)} imagenes descargadas")
        return ok
    except Exception as e:
        logger.warning(f"  Error descargando imagenes [{url_id}]: {e}")
        return 0


def _log(db, url_id: int, language: str, status: str,
         duration: float, items: int, error: str = None):
    """Inserta una linea en scraping_logs."""
    # [FIX HIGH-005] Use settings.MAX_ERROR_LEN (centralized constant) instead of
    # a local hardcoded value. This ensures consistent truncation across all paths.
    _max_err = settings.MAX_ERROR_LEN
    if error and len(error) > _max_err:
        error = error[:_max_err] + f"... [truncated {len(error) - _max_err} chars]"
    try:
        db.execute(
            text("""
                INSERT INTO scraping_logs
                    (url_id, language, status, duration_seconds,
                     items_extracted, error_message, timestamp)
                VALUES
                    (:url_id, :lang, :status, :dur, :items, :error, NOW())
            """),
            {"url_id": url_id, "lang": language, "status": status,
             "dur": round(duration, 2), "items": items, "error": error}
        )
        db.commit()
    except Exception as e:
        logger.debug(f"No se pudo insertar log: {e}")


# =============================================================================
# ESTADO DEL SERVICIO
# =============================================================================

def get_service_stats() -> Dict:
    """
    [FIX BUG-NEW-17] Return real-time scraping service statistics.

    Returns:
        Dict containing: active_ids (list[int]), stats snapshot (counters),
        currently_processing (int), pool_utilization.
    Thread-safe: reads from _active_ids under _lock, stats under _stats_lock.
    """
    with _lock:
        active = list(_active_ids)
    with _stats_lock:
        s = _stats.copy()
    s["active_ids"]   = active
    s["active_count"] = len(active)
    return s
