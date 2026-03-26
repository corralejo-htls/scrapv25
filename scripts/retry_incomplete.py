#!/usr/bin/env python3
"""
retry_incomplete.py — BookingScraper Pro v6.0.0 build 58
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

Opciones:
    --summary             Muestra resumen de estado sin ejecutar nada.
    --dry-run             Muestra qué se reintentaría sin ejecutar.
    --limit N             Procesa máximo N URLs en esta ejecución.
    --reset-total-failures Resetea a 'pending' las URLs con fallo total (sin datos).
    --url-id UUID         Reintenta un URL específico por su UUID.

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
from typing import Any, Dict, List, Optional

# Windows 11: garantiza que el módulo app sea localizable desde este script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import func

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
# Queries de diagnóstico
# ─────────────────────────────────────────────────────────────────────────────

def get_partial_failure_urls(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Retorna URLs con fallo PARCIAL: al menos 1 idioma OK y al menos 1 fallido.
    Estas son candidatas a partial retry (sólo re-scrapeear los fallidos).

    Returns:
        Lista de dicts: {url_id, url, external_ref, completed, missing, last_error}
    """
    cfg = get_settings()
    expected_langs = set(cfg.ENABLED_LANGUAGES)
    # 'en' siempre presente (BUG-LANG-001)
    expected_langs.add("en")

    results: List[Dict[str, Any]] = []

    with get_db() as session:
        query = session.query(URLQueue).filter(URLQueue.status == "error")
        if limit:
            query = query.limit(limit * 5)  # oversample — filter below
        error_urls = query.all()

        for url_row in error_urls:
            completed_rows = (
                session.query(Hotel.language)
                .filter(Hotel.url_id == url_row.id)
                .distinct()
                .all()
            )
            completed = {r[0] for r in completed_rows}
            missing   = expected_langs - completed

            if completed and missing:          # partial: some OK, some missing
                results.append({
                    "url_id":       str(url_row.id),
                    "url":          url_row.url,
                    "external_ref": url_row.external_ref,
                    "completed":    sorted(completed),
                    "missing":      sorted(missing),
                    "retry_count":  url_row.retry_count,
                    "max_retries":  url_row.max_retries,
                    "last_error":   url_row.last_error or "",
                    "scraped_at":   str(url_row.scraped_at) if url_row.scraped_at else "—",
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
    Detecta también URLs marcadas 'done' pero con datos incompletos
    (legacy bug de builds anteriores a v58).
    """
    cfg = get_settings()
    expected_langs = set(cfg.ENABLED_LANGUAGES)
    expected_langs.add("en")
    expected_count = len(expected_langs)

    with get_db() as session:
        total_urls   = session.query(func.count(URLQueue.id)).scalar() or 0
        done_urls    = session.query(func.count(URLQueue.id)).filter(URLQueue.status == "done").scalar() or 0
        error_urls   = session.query(func.count(URLQueue.id)).filter(URLQueue.status == "error").scalar() or 0
        pending_urls = session.query(func.count(URLQueue.id)).filter(URLQueue.status == "pending").scalar() or 0

        # URLs 'done' pero con registros incompletos en hotels (legacy bug)
        legacy_incomplete = 0
        done_rows = session.query(URLQueue).filter(URLQueue.status == "done").all()
        for row in done_rows:
            cnt = (session.query(func.count(Hotel.id))
                   .filter(Hotel.url_id == row.id).scalar()) or 0
            if cnt < expected_count:
                legacy_incomplete += 1

    partial  = get_partial_failure_urls()
    total_f  = get_total_failure_urls()

    return {
        "timestamp":           datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "expected_languages":  sorted(expected_langs),
        "expected_count":      expected_count,
        "total_urls":          total_urls,
        "done":                done_urls,
        "error":               error_urls,
        "pending":             pending_urls,
        "partial_failures":    len(partial),
        "total_failures":      len(total_f),
        "legacy_incomplete":   legacy_incomplete,
        "integrity_ok":        legacy_incomplete == 0 and len(partial) == 0,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Acciones de corrección
# ─────────────────────────────────────────────────────────────────────────────

def reset_partial_for_retry(url_ids: List[str]) -> int:
    """
    Resetea URLs con fallo parcial a 'pending' para que el scraper las
    reintente. Los datos existentes se PRESERVAN; sólo se resetean los
    url_language_status de los idiomas fallidos.

    Returns:
        Número de URLs reseteadas.
    """
    cfg = get_settings()
    expected_langs = set(cfg.ENABLED_LANGUAGES)
    expected_langs.add("en")
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

            # Identificar idiomas faltantes
            completed_rows = (
                session.query(Hotel.language)
                .filter(Hotel.url_id == uid)
                .distinct()
                .all()
            )
            completed = {r[0] for r in completed_rows}
            missing   = expected_langs - completed

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
            logger.info("URL %s re-queued — missing langs: %s", uid_str, sorted(missing))

        session.commit()

    return reset_count


def reset_total_failures_for_retry(limit: Optional[int] = None) -> int:
    """
    Resetea URLs con fallo total a 'pending'.
    Limpia cualquier registro residual en hotels y tablas satellite.
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
            # Limpiar url_language_status
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

    Args:
        dry_run: si True, sólo cuenta sin modificar.
    Returns:
        Número de URLs corregidas (o que se corregirían en dry_run).
    """
    cfg = get_settings()
    expected_langs = set(cfg.ENABLED_LANGUAGES)
    expected_langs.add("en")
    expected_count = len(expected_langs)
    fixed = 0

    with get_db() as session:
        done_rows = session.query(URLQueue).filter(URLQueue.status == "done").all()
        for row in done_rows:
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
                    row.last_error          = f"Legacy fix v58: incomplete ({len(completed)}/{expected_count}) missing={sorted(missing)}"
                    row.languages_completed = ",".join(sorted(completed))
                    row.languages_failed    = ",".join(sorted(missing))
                    row.updated_at          = datetime.now(timezone.utc)
                    logger.info("Legacy fix: url_id=%s — missing %s", row.id, sorted(missing))

        if not dry_run:
            session.commit()

    return fixed


# ─────────────────────────────────────────────────────────────────────────────
# CLI output helpers
# ─────────────────────────────────────────────────────────────────────────────

SEP = "=" * 72

def print_summary() -> None:
    print(f"\n{SEP}")
    print("BOOKINGSCRAPER PRO v6.0.0 build 58 — INTEGRITY SUMMARY")
    print(SEP)
    s = get_integrity_summary()
    print(f"  Timestamp         : {s['timestamp']}")
    print(f"  Expected languages: {s['expected_languages']} ({s['expected_count']} langs)")
    print(f"\n  URL Queue")
    print(f"    Total           : {s['total_urls']}")
    print(f"    Done            : {s['done']}")
    print(f"    Error           : {s['error']}")
    print(f"    Pending         : {s['pending']}")
    print(f"\n  Integrity Findings")
    print(f"    Partial failures (data preserved)  : {s['partial_failures']}")
    print(f"    Total  failures  (no data)         : {s['total_failures']}")
    print(f"    Legacy 'done' but incomplete (pre-v58): {s['legacy_incomplete']}")
    status = "✓ OK" if s["integrity_ok"] else "✗ ISSUES FOUND"
    print(f"\n  Overall Status    : {status}")
    print(SEP)

    partial = get_partial_failure_urls(limit=10)
    if partial:
        print(f"\n  Partial failures (first {min(10, len(partial))}):")
        for item in partial[:10]:
            print(f"    [{item['external_ref'] or '—':>6}] {item['url'][:60]}")
            print(f"           OK={item['completed']}  MISSING={item['missing']}")
        print()


def print_dry_run(partial: List[Dict], total_f: List[Dict]) -> None:
    print(f"\n{SEP}")
    print("DRY RUN — No se realizarán cambios")
    print(SEP)
    if partial:
        print(f"\n  Partial retries pendientes ({len(partial)}):")
        for i, item in enumerate(partial, 1):
            print(f"  [{i:3}] {item['url'][:65]}")
            print(f"        Re-scrapeear: {item['missing']}")
    else:
        print("\n  Sin fallos parciales que reintentar.")
    if total_f:
        print(f"\n  Fallos totales (requieren retry completo): {len(total_f)}")
        print("  → Usa --reset-total-failures para resetear a 'pending'")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Strategy E — Partial retry for BookingScraper Pro v58",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python scripts/retry_incomplete.py --summary\n"
            "  python scripts/retry_incomplete.py --dry-run\n"
            "  python scripts/retry_incomplete.py --limit 5\n"
            "  python scripts/retry_incomplete.py --reset-total-failures\n"
            "  python scripts/retry_incomplete.py --fix-legacy\n"
        )
    )
    parser.add_argument("--summary",              action="store_true",
                        help="Muestra resumen de integridad.")
    parser.add_argument("--dry-run",              action="store_true",
                        help="Muestra qué se haría sin ejecutar.")
    parser.add_argument("--limit",                type=int, default=None,
                        help="Máximo de URLs a procesar.")
    parser.add_argument("--reset-total-failures", action="store_true",
                        help="Resetea URLs con fallo total a 'pending'.")
    parser.add_argument("--fix-legacy",           action="store_true",
                        help="Corrige URLs 'done' con datos incompletos (pre-v58).")
    parser.add_argument("--url-id",               type=str, default=None,
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
