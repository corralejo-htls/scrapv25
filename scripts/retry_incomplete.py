#!/usr/bin/env python3
"""
retry_incomplete.py — BookingScraper Pro v6.0.0 build 59
=========================================================
STRATEGY-E: Script de reintento parcial inteligente.

Detecta URLs con fallo parcial (algunos idiomas exitosos, otros fallidos)
y re-scrapeea SOLO los idiomas que fallaron, preservando los datos existentes.

Uso (Windows 11 — desde el directorio raíz del proyecto):
    python scripts/retry_incomplete.py --summary
    python scripts/retry_incomplete.py --dry-run
    python scripts/retry_incomplete.py --dry-run --limit 10
    python scripts/retry_incomplete.py --limit 5
    python scripts/retry_incomplete.py --reset-total-failures
    python scripts/retry_incomplete.py --fix-legacy
    python scripts/retry_incomplete.py --url-id <UUID>

Opciones:
    --summary             Muestra resumen de estado sin ejecutar nada.
    --dry-run             Muestra qué se reintentaría sin ejecutar.
    --limit N             Procesa máximo N URLs en esta ejecución.
    --reset-total-failures Resetea a 'pending' las URLs con fallo total (sin datos).
    --fix-legacy          Corrige URLs 'done' con datos incompletos (pre-v58).
    --url-id UUID         Reintenta un URL específico por su UUID.

CAMBIOS v59 (BUG-NUEVO-001 — Auditoría 2026-03-27):
    - Eliminado patrón set(cfg.ENABLED_LANGUAGES) + add("en") como fuente
      global de idiomas esperados. Era incorrecto: asumía un número fijo de
      idiomas independiente de la configuración real de cada despliegue.
    - Nuevo helper _get_expected_langs_for_url(): obtiene los idiomas esperados
      POR URL desde url_language_status (la misma fuente de verdad dinámica
      que usa el schema v59 y los nuevos SQL diagnósticos).
    - Fallback a cfg.ENABLED_LANGUAGES solo cuando url_language_status está vacía
      (URL recién insertada antes del primer scrape).
    - fix_legacy_incomplete_done() ahora evalúa cada URL individualmente contra
      su propio url_language_status, no contra un expected_count global.
    - Banners y textos actualizados a build 59.

Notas Windows 11:
    - Usar siempre: if __name__ == '__main__': (spawn-safe)
    - Rutas con pathlib.Path para compatibilidad con drive letters
    - ThreadPoolExecutor (no ProcessPoolExecutor) para tareas I/O

Platform: Windows 11 / Single-node PostgreSQL
"""
from __future__ import annotations

import argparse
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Windows 11: garantiza que el módulo app sea localizable desde este script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import Hotel, URLLanguageStatus, URLQueue

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("retry_incomplete")


# ─────────────────────────────────────────────────────────────────────────────
# FIX-BUG-NUEVO-001 (v59): Helper dinámico — sin hardcoding de idiomas
# ─────────────────────────────────────────────────────────────────────────────

def _get_expected_langs_for_url(session: Session, url_id: uuid.UUID) -> Set[str]:
    """
    Retorna el conjunto de idiomas esperados para un URL específico.

    FIX-BUG-NUEVO-001 (v59): usa url_language_status como fuente de verdad
    dinámica, igual que el trigger fn_check_url_done_integrity() en schema v59
    y la vista v_integrity_check.

    Si url_language_status está vacía (URL recién creada antes del primer
    scrape), cae en el fallback de cfg.ENABLED_LANGUAGES como estimación.

    Args:
        session: sesión SQLAlchemy activa.
        url_id:  UUID de la URL a consultar.

    Returns:
        Set de códigos de idioma (e.g. {'en', 'es', 'de', 'it'}).
    """
    rows = (
        session.query(URLLanguageStatus.language)
        .filter(URLLanguageStatus.url_id == url_id)
        .distinct()
        .all()
    )
    langs = {r[0] for r in rows}

    if not langs:
        # Fallback: URL aún sin url_language_status (recién insertada).
        # Usar ENABLED_LANGUAGES de config como estimación.
        cfg = get_settings()
        langs = set(cfg.ENABLED_LANGUAGES)
        logger.debug(
            "url_id=%s sin url_language_status — usando ENABLED_LANGUAGES como fallback: %s",
            url_id, sorted(langs),
        )

    return langs


def _get_global_expected_langs() -> Set[str]:
    """
    Retorna los idiomas configurados globalmente en ENABLED_LANGUAGES.
    Usado solo para el resumen global de integridad, donde no hay un
    url_id específico de referencia.

    FIX-BUG-NUEVO-001 (v59): este valor es una ESTIMACIÓN para el resumen.
    Las evaluaciones per-URL siempre usan _get_expected_langs_for_url().
    """
    cfg = get_settings()
    return set(cfg.ENABLED_LANGUAGES)


# ─────────────────────────────────────────────────────────────────────────────
# Queries de diagnóstico
# ─────────────────────────────────────────────────────────────────────────────

def get_partial_failure_urls(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Retorna URLs con fallo PARCIAL: al menos 1 idioma OK y al menos 1 fallido.
    Estas son candidatas a partial retry (sólo re-scrapeear los fallidos).

    FIX-BUG-NUEVO-001 (v59): los idiomas esperados se obtienen POR URL
    desde url_language_status, no desde cfg.ENABLED_LANGUAGES global.

    Returns:
        Lista de dicts: {url_id, url, external_ref, completed, missing, ...}
    """
    results: List[Dict[str, Any]] = []

    with get_db() as session:
        query = session.query(URLQueue).filter(URLQueue.status == "error")
        if limit:
            query = query.limit(limit * 5)  # oversample — filtramos abajo
        error_urls = query.all()

        for url_row in error_urls:
            # Idiomas realmente scrapeados (fuente de verdad: tabla hotels)
            completed_rows = (
                session.query(Hotel.language)
                .filter(Hotel.url_id == url_row.id)
                .distinct()
                .all()
            )
            completed = {r[0] for r in completed_rows}

            # FIX-BUG-NUEVO-001: idiomas esperados POR URL (dinámico)
            expected_langs = _get_expected_langs_for_url(session, url_row.id)
            missing = expected_langs - completed

            if completed and missing:          # parcial: algunos OK, algunos faltantes
                results.append({
                    "url_id":           str(url_row.id),
                    "url":              url_row.url,
                    "external_ref":     url_row.external_ref,
                    "completed":        sorted(completed),
                    "missing":          sorted(missing),
                    "expected":         sorted(expected_langs),
                    "retry_count":      url_row.retry_count,
                    "max_retries":      url_row.max_retries,
                    "last_error":       url_row.last_error or "",
                    "scraped_at":       str(url_row.scraped_at) if url_row.scraped_at else "—",
                })

            if limit and len(results) >= limit:
                break

    return results


def get_total_failure_urls(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Retorna URLs con fallo TOTAL: status='error' y ningún registro en hotels.
    Estas necesitan un retry completo (todos los idiomas).
    """
    results: List[Dict[str, Any]] = []

    with get_db() as session:
        query = session.query(URLQueue).filter(URLQueue.status == "error")
        if limit:
            query = query.limit(limit * 5)
        error_urls = query.all()

        for url_row in error_urls:
            count = (
                session.query(func.count(Hotel.id))
                .filter(Hotel.url_id == url_row.id)
                .scalar()
            ) or 0

            if count == 0:
                results.append({
                    "url_id":       str(url_row.id),
                    "url":          url_row.url,
                    "external_ref": url_row.external_ref,
                    "retry_count":  url_row.retry_count,
                    "max_retries":  url_row.max_retries,
                    "last_error":   url_row.last_error or "",
                    "scraped_at":   str(url_row.scraped_at) if url_row.scraped_at else "—",
                })

            if limit and len(results) >= limit:
                break

    return results


def get_integrity_summary() -> Dict[str, Any]:
    """
    Resumen completo del estado de integridad de datos.

    FIX-BUG-NUEVO-001 (v59):
    - legacy_incomplete ahora evalúa cada URL contra su propio
      url_language_status (dinámico), no contra un expected_count global.
    - expected_languages en el resumen refleja cfg.ENABLED_LANGUAGES como
      referencia de configuración activa, claramente marcado como estimación.
    """
    global_expected = _get_global_expected_langs()

    with get_db() as session:
        total_urls   = session.query(func.count(URLQueue.id)).scalar() or 0
        done_urls    = (session.query(func.count(URLQueue.id))
                        .filter(URLQueue.status == "done").scalar() or 0)
        error_urls   = (session.query(func.count(URLQueue.id))
                        .filter(URLQueue.status == "error").scalar() or 0)
        pending_urls = (session.query(func.count(URLQueue.id))
                        .filter(URLQueue.status == "pending").scalar() or 0)

        # FIX-BUG-NUEVO-001: evaluación per-URL con expected dinámico
        legacy_incomplete = 0
        done_rows = session.query(URLQueue).filter(URLQueue.status == "done").all()
        for row in done_rows:
            scraped_count = (
                session.query(func.count(Hotel.id))
                .filter(Hotel.url_id == row.id)
                .scalar()
            ) or 0
            expected_for_url = _get_expected_langs_for_url(session, row.id)
            if scraped_count < len(expected_for_url):
                legacy_incomplete += 1

    partial = get_partial_failure_urls()
    total_f = get_total_failure_urls()

    return {
        "timestamp":              datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "configured_languages":   sorted(global_expected),          # cfg.ENABLED_LANGUAGES activo
        "configured_count":       len(global_expected),
        "note_dynamic":           "Los idiomas esperados por URL se leen de url_language_status (dinámico)",
        "total_urls":             total_urls,
        "done":                   done_urls,
        "error":                  error_urls,
        "pending":                pending_urls,
        "partial_failures":       len(partial),
        "total_failures":         len(total_f),
        "legacy_incomplete":      legacy_incomplete,
        "integrity_ok":           legacy_incomplete == 0 and len(partial) == 0,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Acciones de corrección
# ─────────────────────────────────────────────────────────────────────────────

def reset_partial_for_retry(url_ids: List[str]) -> int:
    """
    Resetea URLs con fallo parcial a 'pending' para que el scraper las
    reintente. Los datos existentes se PRESERVAN; sólo se resetean los
    url_language_status de los idiomas fallidos.

    FIX-BUG-NUEVO-001 (v59): idiomas esperados obtenidos por URL desde
    url_language_status, no desde cfg.ENABLED_LANGUAGES global.

    Returns:
        Número de URLs reseteadas.
    """
    reset_count = 0

    with get_db() as session:
        for uid_str in url_ids:
            try:
                uid = uuid.UUID(uid_str)
            except ValueError:
                logger.warning("UUID inválido ignorado: %s", uid_str)
                continue

            url_row = session.get(URLQueue, uid)
            if not url_row:
                logger.warning("URL no encontrada: %s", uid_str)
                continue

            # Idiomas realmente en DB
            completed_rows = (
                session.query(Hotel.language)
                .filter(Hotel.url_id == uid)
                .distinct()
                .all()
            )
            completed = {r[0] for r in completed_rows}

            # FIX-BUG-NUEVO-001: expected dinámico per-URL
            expected_langs = _get_expected_langs_for_url(session, uid)
            missing = expected_langs - completed

            if not missing:
                logger.info("URL %s ya completa — sin cambios.", uid_str)
                continue

            # Resetear url_language_status de los fallidos a 'pending'
            for lang in missing:
                uls = (
                    session.query(URLLanguageStatus)
                    .filter_by(url_id=uid, language=lang)
                    .first()
                )
                if uls:
                    uls.status     = "pending"
                    uls.last_error = None
                    uls.attempts   = 0
                else:
                    session.add(URLLanguageStatus(
                        url_id=uid, language=lang, status="pending"
                    ))

            # Resetear url_queue a 'pending' para que el scraper la recoja
            url_row.status              = "pending"
            url_row.last_error          = f"Partial retry: re-queued for {sorted(missing)}"
            url_row.retry_count         = max(0, url_row.retry_count - 1)
            url_row.languages_failed    = ",".join(sorted(missing))
            url_row.languages_completed = ",".join(sorted(completed))
            url_row.updated_at          = datetime.now(timezone.utc)
            reset_count += 1
            logger.info(
                "URL %s re-encolada — expected=%s completed=%s missing=%s",
                uid_str, sorted(expected_langs), sorted(completed), sorted(missing),
            )

        session.commit()

    return reset_count


def reset_total_failures_for_retry(limit: Optional[int] = None) -> int:
    """
    Resetea URLs con fallo total a 'pending'.
    Limpia cualquier registro residual en url_language_status.
    """
    total_failures = get_total_failure_urls(limit=limit)
    if not total_failures:
        logger.info("No hay fallos totales que resetear.")
        return 0

    reset_count = 0
    with get_db() as session:
        for item in total_failures:
            uid = uuid.UUID(item["url_id"])
            url_row = session.get(URLQueue, uid)
            if not url_row:
                continue
            # Limpiar url_language_status para que el scraper recree el tracking
            session.query(URLLanguageStatus).filter_by(url_id=uid).delete(
                synchronize_session=False
            )
            url_row.status              = "pending"
            url_row.last_error          = "Total failure reset — full retry"
            url_row.retry_count         = 0
            url_row.languages_completed = ""
            url_row.languages_failed    = ""
            url_row.scraped_at          = None
            url_row.updated_at          = datetime.now(timezone.utc)
            reset_count += 1

        session.commit()

    logger.info("Total failures reseteados: %d", reset_count)
    return reset_count


def fix_legacy_incomplete_done(dry_run: bool = False) -> int:
    """
    Corrige URLs marcadas 'done' pero con datos incompletos (bug pre-v58).
    Las marca como 'error' para que sean recogidas por partial retry.

    FIX-BUG-NUEVO-001 (v59): evaluación per-URL con expected dinámico
    desde url_language_status. Cada URL puede tener diferente número de
    idiomas configurados dependiendo de cuándo fue insertada en la cola.

    Args:
        dry_run: si True, sólo cuenta sin modificar.
    Returns:
        Número de URLs corregidas (o que se corregirían en dry_run).
    """
    fixed = 0

    with get_db() as session:
        done_rows = session.query(URLQueue).filter(URLQueue.status == "done").all()
        for row in done_rows:
            # FIX-BUG-NUEVO-001: expected dinámico per-URL
            expected_langs = _get_expected_langs_for_url(session, row.id)
            expected_count = len(expected_langs)

            completed_rows = (
                session.query(Hotel.language)
                .filter(Hotel.url_id == row.id)
                .distinct()
                .all()
            )
            completed = {r[0] for r in completed_rows}
            missing   = expected_langs - completed

            if missing:
                fixed += 1
                if not dry_run:
                    row.status              = "error"
                    row.last_error          = (
                        f"Legacy fix v59: incomplete "
                        f"({len(completed)}/{expected_count}) "
                        f"missing={sorted(missing)}"
                    )
                    row.languages_completed = ",".join(sorted(completed))
                    row.languages_failed    = ",".join(sorted(missing))
                    row.updated_at          = datetime.now(timezone.utc)
                    logger.info(
                        "Legacy fix: url_id=%s expected=%d scraped=%d missing=%s",
                        row.id, expected_count, len(completed), sorted(missing),
                    )

        if not dry_run:
            session.commit()

    return fixed


# ─────────────────────────────────────────────────────────────────────────────
# CLI output helpers
# ─────────────────────────────────────────────────────────────────────────────

SEP = "=" * 72


def print_summary() -> None:
    print(f"\n{SEP}")
    print("BOOKINGSCRAPER PRO v6.0.0 build 59 — INTEGRITY SUMMARY")
    print(SEP)
    s = get_integrity_summary()
    print(f"  Timestamp                : {s['timestamp']}")
    print(f"  Configured languages     : {s['configured_languages']} ({s['configured_count']} langs)")
    print(f"  Note                     : {s['note_dynamic']}")
    print(f"\n  URL Queue")
    print(f"    Total                  : {s['total_urls']}")
    print(f"    Done                   : {s['done']}")
    print(f"    Error                  : {s['error']}")
    print(f"    Pending                : {s['pending']}")
    print(f"\n  Integrity Findings")
    print(f"    Partial failures (data preserved)    : {s['partial_failures']}")
    print(f"    Total  failures  (no data)           : {s['total_failures']}")
    print(f"    Legacy 'done' but incomplete (pre-v58): {s['legacy_incomplete']}")
    status = "✓ OK" if s["integrity_ok"] else "✗ ISSUES FOUND"
    print(f"\n  Overall Status           : {status}")
    print(SEP)

    partial = get_partial_failure_urls(limit=10)
    if partial:
        print(f"\n  Partial failures (first {min(10, len(partial))}):")
        for item in partial[:10]:
            ref = item["external_ref"] or "—"
            print(f"    [{ref:>6}] {item['url'][:60]}")
            print(f"             expected={item['expected']}")
            print(f"             OK={item['completed']}  MISSING={item['missing']}")
        print()


def print_dry_run(partial: List[Dict], total_f: List[Dict]) -> None:
    print(f"\n{SEP}")
    print("DRY RUN — No se realizarán cambios")
    print(SEP)
    if partial:
        print(f"\n  Partial retries pendientes ({len(partial)}):")
        for i, item in enumerate(partial, 1):
            print(f"  [{i:3}] {item['url'][:65]}")
            print(f"        Re-scrapeear: {item['missing']}  (expected: {item['expected']})")
    else:
        print("\n  Sin fallos parciales que reintentar.")
    if total_f:
        print(f"\n  Fallos totales (requieren retry completo): {len(total_f)}")
        print("  → Usa --reset-total-failures para resetear a 'pending'")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Main — Windows 11 spawn-safe guard obligatorio
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Strategy E — Partial retry for BookingScraper Pro v59",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python scripts/retry_incomplete.py --summary\n"
            "  python scripts/retry_incomplete.py --dry-run\n"
            "  python scripts/retry_incomplete.py --limit 5\n"
            "  python scripts/retry_incomplete.py --reset-total-failures\n"
            "  python scripts/retry_incomplete.py --fix-legacy\n"
            "  python scripts/retry_incomplete.py --fix-legacy --dry-run\n"
            "  python scripts/retry_incomplete.py --url-id <UUID>\n"
        )
    )
    parser.add_argument("--summary",
                        action="store_true",
                        help="Muestra resumen de integridad.")
    parser.add_argument("--dry-run",
                        action="store_true",
                        help="Muestra qué se haría sin ejecutar.")
    parser.add_argument("--limit",
                        type=int, default=None,
                        help="Máximo de URLs a procesar.")
    parser.add_argument("--reset-total-failures",
                        action="store_true",
                        help="Resetea URLs con fallo total a 'pending'.")
    parser.add_argument("--fix-legacy",
                        action="store_true",
                        help="Corrige URLs 'done' con datos incompletos (pre-v58).")
    parser.add_argument("--url-id",
                        type=str, default=None,
                        help="Reintenta un URL específico por UUID.")
    args = parser.parse_args()

    if args.summary:
        print_summary()
        return

    if args.fix_legacy:
        fixed = fix_legacy_incomplete_done(dry_run=args.dry_run)
        tag = "(dry-run)" if args.dry_run else ""
        print(f"\n  Legacy fix {tag}: {fixed} URLs corregidas/detectadas.")
        return

    if args.reset_total_failures:
        if args.dry_run:
            failures = get_total_failure_urls(limit=args.limit)
            print(f"\n  [DRY RUN] Se resetearían {len(failures)} fallos totales.")
        else:
            n = reset_total_failures_for_retry(limit=args.limit)
            print(f"\n  Fallos totales reseteados: {n}")
        return

    if args.url_id:
        if args.dry_run:
            print(f"\n  [DRY RUN] Se reintentaría: {args.url_id}")
        else:
            n = reset_partial_for_retry([args.url_id])
            print(f"\n  URL reseteada para retry: {n}")
        return

    # Default: partial retry
    partial = get_partial_failure_urls(limit=args.limit)
    total_f = get_total_failure_urls()

    if args.dry_run:
        print_dry_run(partial, total_f)
        return

    if not partial:
        print("\n  ✓ Sin fallos parciales que reintentar.")
        if total_f:
            print(f"  {len(total_f)} fallos totales — usa --reset-total-failures")
        return

    url_ids = [item["url_id"] for item in partial]
    n = reset_partial_for_retry(url_ids)
    print(f"\n  ✓ {n} URLs re-encoladas para partial retry.")
    print("  Reinicia el scraper para procesar la cola.\n")


if __name__ == "__main__":
    main()
