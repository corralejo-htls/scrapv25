"""
load_urls.py — BookingScraper Pro v6.0.0 build 52
==================================================
Carga URLs desde CSV sin cabecera. Nuevo formato de 3 columnas:
    external_ref, url, external_url

    external_ref  — ID numérico del CSV origen (e.g. 1001)
    url           — URL de Booking.com del hotel
    external_url  — URL alternativa/externa del hotel (puede estar vacía)

Formato nuevo (3 columnas, sin cabecera, separador coma):
    1001,https://www.booking.com/hotel/br/manaus-hoteis-millennium.html,https://www.otrawebS01.com/
    1002,https://www.booking.com/hotel/br/colonna-park.html,

Formato legacy aún soportado (2 columnas — external_url queda NULL):
    1001,https://www.booking.com/hotel/br/manaus-hoteis-millennium.html

Uso:
    python scripts/load_urls.py urls.csv
    python scripts/load_urls.py urls.csv --dry-run

Cambios v52:
  STRUCT-009 (FIX-LOAD-010): _Row ahora incluye external_url (puede ser None/vacío).
    _parse_csv() acepta 2 o 3 columnas:
      - 3 columnas: external_ref, url, external_url
      - 2 columnas: external_ref, url (legacy — external_url = None)
    load_csv() persiste external_url en url_queue cuando la columna existe.
    La 3ª columna es opcional: si está vacía o ausente → NULL en DB.

BUG-LOAD-001 (v50): external_ref nunca se grababa porque el INSERT usaba
  ON CONFLICT DO NOTHING — si la URL ya existía (de una carga anterior sin
  external_ref), la columna quedaba NULL permanentemente.

  FIX: ON CONFLICT (url) DO UPDATE SET external_ref = EXCLUDED.external_ref,
                                        external_url = EXCLUDED.external_url
       WHERE url_queue.external_ref IS NULL
  Esto garantiza:
    a) Primera carga: INSERT normal con external_ref y external_url.
    b) Re-carga de mismo CSV: UPDATE solo si external_ref era NULL.
    c) URLs duplicadas con distinto id: NO sobrescriben (WHERE IS NULL protege).

Notas:
    - Soporta saltos de linea Windows (CRLF) y Unix (LF).
    - El id_externo_hotel se guarda en url_queue.external_ref.
    - La URL alternativa se guarda en url_queue.external_url.
    - Duplicados por URL con external_ref ya grabado se omiten (no se sobreescribe).
    - Usa INSERT directo con SQL parametrizado — no depende del ORM.
    - external_url NO se valida como URL de Booking.com (puede ser cualquier dominio).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from loguru import logger
from sqlalchemy import inspect, text
from app.config import get_settings
from app.database import get_db

_cfg = get_settings()

# ── Constantes ────────────────────────────────────────────────────────────────
_BOOKING_PREFIX = "https://www.booking.com/hotel/"
_MAX_URL_LEN    = 2048
_MAX_FILE_MB    = getattr(_cfg, "CSV_MAX_FILE_MB", 10)


class _Row(NamedTuple):
    ext_id:       str
    url:          str
    external_url: Optional[str]   # STRUCT-009 (v52): 3ª columna, puede ser None


# ── Validación ────────────────────────────────────────────────────────────────

def _is_valid_url(url: str) -> bool:
    return (
        bool(url)
        and url.startswith(_BOOKING_PREFIX)
        and len(url) <= _MAX_URL_LEN
    )


def _is_valid_id(raw: str) -> bool:
    return bool(raw) and raw.isdigit()


def _sanitize_external_url(raw: str) -> Optional[str]:
    """
    Limpia y valida la URL externa (3ª columna).
    - Acepta cualquier dominio (no solo Booking.com).
    - Requiere esquema http:// o https://.
    - Longitud máxima 2048 chars.
    - Retorna None si está vacía o inválida.
    """
    if not raw:
        return None
    url = raw.strip()
    if not url:
        return None
    if not (url.startswith("http://") or url.startswith("https://")):
        return None
    if len(url) > _MAX_URL_LEN:
        return None
    return url


# ── Parseo CSV ────────────────────────────────────────────────────────────────

def _parse_csv(filepath: Path) -> List[_Row]:
    """
    Lee CSV sin cabecera con formato: external_ref,url[,external_url]

    STRUCT-009 (v52): acepta 2 o 3 columnas:
      - 2 cols: external_ref, url           → external_url = None
      - 3 cols: external_ref, url, ext_url  → external_url validado o None

    Maneja CRLF y LF. Devuelve solo filas validas.
    """
    size_mb = filepath.stat().st_size / (1024 * 1024)
    if size_mb > _MAX_FILE_MB:
        logger.error("Archivo demasiado grande: {:.1f} MB (max {} MB).", size_mb, _MAX_FILE_MB)
        return []

    rows: List[_Row] = []
    total   = 0
    invalid = 0

    with open(filepath, encoding="utf-8", newline="") as f:
        for lineno, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue
            total += 1

            # Parsear columnas respetando comas dentro de comillas (básico)
            parts = [p.strip().strip('"').strip("'") for p in line.split(",")]

            if len(parts) < 2:
                logger.warning("Linea {}: menos de 2 columnas — omitida: {!r}", lineno, line)
                invalid += 1
                continue

            raw_id  = parts[0].strip()
            raw_url = parts[1].strip()

            # 3ª columna opcional
            raw_ext_url = parts[2].strip() if len(parts) >= 3 else ""

            if not _is_valid_id(raw_id):
                logger.warning("Linea {}: id {!r} no es numerico — omitida.", lineno, raw_id)
                invalid += 1
                continue

            if not _is_valid_url(raw_url):
                logger.warning("Linea {}: URL invalida — omitida: {!r}", lineno, raw_url)
                invalid += 1
                continue

            external_url = _sanitize_external_url(raw_ext_url)

            rows.append(_Row(ext_id=raw_id, url=raw_url, external_url=external_url))

    logger.info(
        "CSV leido: {} lineas, {} validas, {} invalidas.",
        total, len(rows), invalid,
    )
    return rows


# ── Deteccion de columnas en url_queue ───────────────────────────────────────

def _get_url_queue_columns() -> set:
    """
    Retorna el conjunto de columnas existentes en url_queue.
    Usado para compatibilidad entre versiones de schema.
    """
    try:
        from app.database import _get_engine
        engine = _get_engine()
        insp = inspect(engine)
        return {c["name"] for c in insp.get_columns("url_queue")}
    except Exception as exc:
        logger.warning("No se pudo inspeccionar url_queue: {} — usando fallback vacío.", exc)
        return set()


# ── Carga a DB ────────────────────────────────────────────────────────────────

def load_csv(filepath: Path, dry_run: bool = False) -> int:
    """
    Inserta las URLs en url_queue usando SQL parametrizado.

    STRUCT-009 (v52): incluye external_url en el INSERT cuando la columna existe.

    BUG-LOAD-001 FIX: ON CONFLICT (url) DO UPDATE SET
        external_ref = EXCLUDED.external_ref,
        external_url = EXCLUDED.external_url
    WHERE url_queue.external_ref IS NULL

    Comportamiento:
      - URL nueva              → INSERT con external_ref y external_url
      - URL existente sin ref  → UPDATE external_ref y external_url
      - URL existente con ref  → no modifica (WHERE IS NULL protege)

    Returns:
        Número de filas insertadas o actualizadas efectivamente.
    """
    rows = _parse_csv(filepath)
    if not rows:
        logger.warning("Ninguna URL valida en {}.", filepath)
        return 0

    if dry_run:
        logger.info("[DRY-RUN] Se cargarian {} URLs:", len(rows))
        for r in rows:
            ext_url_info = f"  ext_url={r.external_url}" if r.external_url else ""
            logger.info("  id={:>6}  {}{}", r.ext_id, r.url, ext_url_info)
        return 0

    existing_cols = _get_url_queue_columns()
    has_ext_ref = "external_ref" in existing_cols
    has_ext_url = "external_url" in existing_cols  # STRUCT-009

    if has_ext_ref:
        logger.info("Columna external_ref detectada — se guardara el id externo.")
    else:
        logger.warning(
            "Columna external_ref NO existe en url_queue — "
            "se insertara solo url/base_url. "
            "Aplica schema_v52_complete.sql para habilitar esta columna."
        )

    if has_ext_url:
        logger.info("Columna external_url detectada — se guardara la URL externa.")
    else:
        logger.warning(
            "Columna external_url NO existe en url_queue — "
            "3a columna del CSV sera ignorada. "
            "Aplica schema_v52_complete.sql para habilitar esta columna."
        )

    # Construir SQL según columnas disponibles
    if has_ext_ref and has_ext_url:
        sql = text("""
            INSERT INTO url_queue (url, base_url, external_ref, external_url)
            VALUES (:url, :url, :ext_id, :external_url)
            ON CONFLICT (url) DO UPDATE
                SET external_ref = EXCLUDED.external_ref,
                    external_url = EXCLUDED.external_url
            WHERE url_queue.external_ref IS NULL
        """)
    elif has_ext_ref:
        # Schema v50/v51: solo external_ref, sin external_url
        sql = text("""
            INSERT INTO url_queue (url, base_url, external_ref)
            VALUES (:url, :url, :ext_id)
            ON CONFLICT (url) DO UPDATE
                SET external_ref = EXCLUDED.external_ref
            WHERE url_queue.external_ref IS NULL
        """)
    else:
        # Schema antiguo: sin ninguna de las columnas
        sql = text("""
            INSERT INTO url_queue (url, base_url)
            VALUES (:url, :url)
            ON CONFLICT (url) DO NOTHING
        """)

    inserted = 0
    updated  = 0
    errors   = 0

    with get_db() as session:
        for row in rows:
            try:
                if has_ext_ref and has_ext_url:
                    params = {
                        "url":          row.url,
                        "ext_id":       row.ext_id,
                        "external_url": row.external_url,   # puede ser None
                    }
                elif has_ext_ref:
                    params = {"url": row.url, "ext_id": row.ext_id}
                else:
                    params = {"url": row.url}

                result = session.execute(sql, params)
                if result.rowcount == 1:
                    # rowcount=1 cubre tanto INSERT como UPDATE exitoso
                    inserted += 1

            except Exception as exc:
                logger.error("Error en id={} url={}: {}", row.ext_id, row.url, exc)
                errors += 1

    skipped = len(rows) - inserted - errors
    logger.info(
        "Carga completada — insertadas/actualizadas: {}  sin cambios: {}  errores: {}",
        inserted, skipped, errors,
    )
    return inserted


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Carga URLs de Booking.com desde CSV sin cabecera.\n"
            "Formato: external_ref,url[,external_url]\n"
            "Ejemplo: 1001,https://www.booking.com/hotel/es/melia.html,https://otraweb.com/hotel/melia"
        )
    )
    parser.add_argument("csv_file", help="Ruta al archivo CSV")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo muestra las URLs que se insertarian sin modificar la DB",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        logger.error("Archivo no encontrado: {}", csv_path)
        sys.exit(1)

    count = load_csv(csv_path, dry_run=args.dry_run)
    sys.exit(0)
