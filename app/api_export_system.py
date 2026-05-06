"""
api_export_system.py — BookingScraper Pro v6.0.0 Build 98
==========================================================

GAP-EXPORT-001-FIX (Build 98):
    _send_hotel(): el bucle de reintentos no distinguía HTTP 429 (Too Many
    Requests / rate limiting) de otros errores HTTP 4xx/5xx. En caso de
    rate limiting, el backoff exponencial estándar (2s, 4s, 8s) es
    insuficiente — los servidores de API suelen requerir 30–120 s de espera.

    Fix:
    1. Detectar HTTP 429 explícitamente.
    2. Leer el header Retry-After (segundos o fecha HTTP) si está presente.
    3. Aplicar max(Retry-After, API_EXPORT_RATE_LIMIT_WAIT_S) como backoff.
    4. Añadir campo de config API_EXPORT_RATE_LIMIT_WAIT_S (default 60 s).
    5. Si el Retry-After supera API_EXPORT_MAX_RETRY_AFTER_S (default 300 s),
       abortar los reintentos para ese hotel (no bloquear la cola indefinidamente).

    Impacto: evita fallos silenciosos al exportar múltiples hoteles en lotes
    cuando la API externa aplica rate limiting (HTTP 429).

Implementa el sistema completo de exportación de datos hacia la API externa
definida en _API_.md.

Componentes:
    APIField        — Enum con todos los campos exportables del payload.
    ExportTemplate  — Configuración de una exportación (campos + idiomas + args).
    TemplateManager — Carga/guarda plantillas desde disco.
    ExportSelection — Lista de url_ids a exportar (desde archivo o manual).
    APIConfig       — Parámetros de conexión a la API externa.
    APIExporter     — Motor principal: genera payloads y los envía o guarda.

Reglas de la API (_API_.md):
    - Idioma 'en' OBLIGATORIO en cada payload; siempre en primer lugar.
    - Método HTTP: PATCH.
    - Saltos de línea con \\n, no con <p>.
    - Cualquier campo puede omitirse si no se desea actualizar.
    - El campo 'locales' en args refleja los idiomas incluidos (en primero).

URL de la API:
    {base_url}/{language}/{api_key}/update/{hotel_id}.json

Platform: Windows 11 / Python 3.14 / PostgreSQL 14+
"""

from __future__ import annotations

import json
import logging
import re
import time
import uuid
from email.utils import parsedate_to_datetime  # GAP-EXPORT-001-FIX: parse HTTP-date Retry-After
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

import requests
from sqlalchemy.orm import Session

from app.api_payload_builder import ApiPayloadBuilder
from app.models import Hotel, URLLanguageStatus, URLQueue

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# APIField — campos exportables
# ---------------------------------------------------------------------------

class APIField(str, Enum):
    """Campos del payload definidos en _API_.md."""
    NAME                  = "name"
    RATING                = "rating"
    ADDRESS               = "address"
    GEO_POSITION          = "geoPosition"
    SERVICES              = "services"
    CONDITIONS            = "conditions"
    TO_CONSIDER           = "toConsider"
    IMAGES                = "images"
    SCORE_REVIEW          = "scoreReview"
    SCORE_REVIEW_BASED_ON = "scoreReviewBasedOn"
    ROOMS_QUANTITY        = "roomsQuantity"
    ACCOMMODATION_TYPE    = "accommodationType"
    PRICE_RANGE           = "priceRange"
    EXTRA_INFO            = "extraInfo"
    LONG_DESCRIPTION      = "longDescription"
    REVIEWS               = "reviews"
    CATEGORY_SCORE_REVIEW = "categoryScoreReview"
    ROOMS                 = "rooms"
    NEARBY_PLACES         = "nearbyPlaces"
    GUEST_VALUES          = "guestValues"
    SEO_DESCRIPTION       = "seoDescription"
    KEYWORDS              = "keywords"

    @classmethod
    def recommended(cls) -> List["APIField"]:
        """Campos recomendados para una exportación estándar."""
        return [
            cls.NAME, cls.ADDRESS, cls.GEO_POSITION, cls.SERVICES,
            cls.CONDITIONS, cls.TO_CONSIDER, cls.IMAGES, cls.SCORE_REVIEW,
            cls.ACCOMMODATION_TYPE, cls.LONG_DESCRIPTION,
            cls.CATEGORY_SCORE_REVIEW, cls.ROOMS, cls.NEARBY_PLACES,
            cls.SEO_DESCRIPTION, cls.KEYWORDS,
        ]

    @classmethod
    def all_fields(cls) -> List["APIField"]:
        return list(cls)

    @classmethod
    def mandatory(cls) -> List["APIField"]:
        return [cls.NAME, cls.SCORE_REVIEW, cls.CATEGORY_SCORE_REVIEW]


# ---------------------------------------------------------------------------
# ExportTemplate
# ---------------------------------------------------------------------------

SUPPORTED_LANGUAGES = ["en", "es", "de", "fr", "it", "pt"]


@dataclass
class ExportTemplate:
    """
    Configuración completa de una exportación.

    Garantías:
      - 'en' siempre incluido en locales (regla _API_.md).
      - 'en' siempre en primer lugar de la lista locales.
    """
    name: str = "default"
    description: str = ""
    fields: List[APIField] = field(default_factory=APIField.recommended)
    languages: List[str] = field(default_factory=lambda: ["en"])
    include_args: bool = True
    args_config: Dict[str, Any] = field(default_factory=lambda: {
        "seoFormatKey": "",
        "onlyTitle": True,
        "regenerateSeo": True,
        "append": False,
        "cache": True,
    })
    validate_before_export: bool = True
    required_fields_for_validation: List[APIField] = field(
        default_factory=lambda: [APIField.NAME, APIField.SCORE_REVIEW]
    )
    skip_incomplete: bool = False

    def __post_init__(self) -> None:
        # Normalize: ensure 'en' is always present and first
        langs: List[str] = [ln for ln in self.languages if ln != "en"]
        self.languages = ["en"] + langs

    @property
    def locales(self) -> List[str]:
        return self.languages

    @classmethod
    def default_template(cls) -> "ExportTemplate":
        return cls(
            name="default",
            description="Exportación estándar — campos recomendados, idioma en",
            fields=APIField.recommended(),
            languages=["en"],
        )

    @classmethod
    def full_template(cls) -> "ExportTemplate":
        return cls(
            name="full",
            description="Exportación completa — todos los campos, todos los idiomas",
            fields=APIField.all_fields(),
            languages=["en", "es", "de", "fr", "it", "pt"],
        )

    @classmethod
    def minimal_template(cls) -> "ExportTemplate":
        return cls(
            name="minimal",
            description="Exportación mínima — solo campos obligatorios",
            fields=APIField.mandatory(),
            languages=["en"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "fields": [f.value for f in self.fields],
            "languages": self.languages,
            "include_args": self.include_args,
            "args_config": self.args_config,
            "validate_before_export": self.validate_before_export,
            "required_fields_for_validation": [
                f.value for f in self.required_fields_for_validation
            ],
            "skip_incomplete": self.skip_incomplete,
        }

    def to_file(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ExportTemplate":
        return cls(
            name=d.get("name", "custom"),
            description=d.get("description", ""),
            fields=[APIField(f) for f in d.get("fields", [])],
            languages=d.get("languages", ["en"]),
            include_args=d.get("include_args", True),
            args_config=d.get("args_config", {}),
            validate_before_export=d.get("validate_before_export", True),
            required_fields_for_validation=[
                APIField(f) for f in d.get("required_fields_for_validation", [])
            ],
            skip_incomplete=d.get("skip_incomplete", False),
        )

    @classmethod
    def from_file(cls, path: str | Path) -> "ExportTemplate":
        return cls.from_dict(
            json.loads(Path(path).read_text(encoding="utf-8"))
        )


# ---------------------------------------------------------------------------
# TemplateManager
# ---------------------------------------------------------------------------

class TemplateManager:
    """Gestión de plantillas en disco."""

    BUILTIN: Dict[str, ExportTemplate] = {
        "default": ExportTemplate.default_template(),
        "full":    ExportTemplate.full_template(),
        "minimal": ExportTemplate.minimal_template(),
    }

    def __init__(self, templates_dir: str | Path = "templates") -> None:
        self.templates_dir = Path(templates_dir)

    def load_template(self, name: str) -> ExportTemplate:
        if name in self.BUILTIN:
            return self.BUILTIN[name]
        path = self.templates_dir / f"{name}.json"
        if path.exists():
            return ExportTemplate.from_file(path)
        raise FileNotFoundError(f"Template '{name}' not found in {self.templates_dir}")

    def save_template(self, template: ExportTemplate) -> None:
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        template.to_file(self.templates_dir / f"{template.name}.json")

    def list_templates(self) -> List[str]:
        names = list(self.BUILTIN.keys())
        if self.templates_dir.exists():
            names += [p.stem for p in self.templates_dir.glob("*.json")]
        return sorted(set(names))


# ---------------------------------------------------------------------------
# ExportSelection
# ---------------------------------------------------------------------------

@dataclass
class ExportSelection:
    """Lista de url_ids a exportar."""

    url_ids: List[UUID] = field(default_factory=list)
    description: str = ""
    source_file: str = ""

    def add_url_id(self, uid: str | UUID) -> None:
        self.url_ids.append(UUID(str(uid)))

    def __len__(self) -> int:
        return len(self.url_ids)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url_ids": [str(u) for u in self.url_ids],
            "description": self.description,
            "source_file": self.source_file,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }

    def to_file(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @classmethod
    def from_file(cls, path: str | Path) -> "ExportSelection":
        p = Path(path)
        text = p.read_text(encoding="utf-8").strip()
        sel = cls(source_file=str(p))

        # JSON format
        if text.startswith("{"):
            d = json.loads(text)
            for uid in d.get("url_ids", []):
                sel.add_url_id(uid)
            sel.description = d.get("description", "")
            return sel

        # Plain text / CSV: one UUID per line (skip comments)
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            uid = line.split(",")[0].strip().strip('"').strip("'")
            if _is_valid_uuid(uid):
                sel.add_url_id(uid)

        return sel

    @classmethod
    def from_db_all_pending(
        cls,
        db: Session,
        required_languages: Optional[List[str]] = None,
    ) -> "ExportSelection":
        """
        BUG-EXPORT-003-FIX (Build 96): Verifica completitud por idioma.
        Antes seleccionaba TODOS los url_queue con status='done' sin importar
        si todos los idiomas habilitados fueron scrapeados. Ahora solo incluye
        URLs donde TODOS los idiomas requeridos tienen status='done' en
        url_language_status. Las URLs con idiomas pendientes/fallidos son
        excluidas del payload de exportación para evitar datos incompletos.
        """
        from app.config import get_settings
        cfg = get_settings()
        if required_languages is None:
            required_languages = [
                ln.strip()
                for ln in cfg.ENABLED_LANGUAGES.split(",")
                if ln.strip()
            ]

        done_urls = db.query(URLQueue).filter(URLQueue.status == "done").all()
        sel = cls(description="All done URLs from database (language-verified)")
        skipped = 0

        for url_row in done_urls:
            # Count languages with status='done' for this URL
            done_langs = (
                db.query(URLLanguageStatus.language)
                .filter(
                    URLLanguageStatus.url_id == url_row.id,
                    URLLanguageStatus.status == "done",
                )
                .all()
            )
            done_lang_set = {r.language for r in done_langs}
            missing = [ln for ln in required_languages if ln not in done_lang_set]
            if missing:
                import logging as _log
                _log.getLogger(__name__).warning(
                    "ExportSelection: url_id=%s skipped — missing languages: %s",
                    url_row.id, missing,
                )
                skipped += 1
                continue
            sel.add_url_id(url_row.id)

        if skipped:
            import logging as _log
            _log.getLogger(__name__).warning(
                "ExportSelection: %d URL(s) excluded — incomplete language scraping",
                skipped,
            )
        return sel


def _is_valid_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
        return True
    except (ValueError, AttributeError):
        return False


# ---------------------------------------------------------------------------
# APIConfig
# ---------------------------------------------------------------------------

@dataclass
class APIConfig:
    """Configuración de conexión a la API externa."""

    base_url: str = "https://web.com/api"
    api_key: str = ""
    endpoint_template: str = "/{language}/{api_key}/update/{hotel_id}.json"
    http_method: str = "PATCH"
    headers: Dict[str, str] = field(
        default_factory=lambda: {"Content-Type": "application/json"}
    )
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 2.0
    # GAP-EXPORT-001-FIX (Build 98): campos para manejo de HTTP 429
    rate_limit_wait_s: float = 60.0    # backoff mínimo al recibir HTTP 429
    max_retry_after_s: float = 300.0   # Retry-After máximo aceptable; si supera este valor, aborta

    def build_url(self, language: str, hotel_id: str) -> str:
        path = self.endpoint_template.format(
            language=language,
            api_key=self.api_key,
            hotel_id=hotel_id,
        )
        return self.base_url.rstrip("/") + path

    def to_dict(self) -> Dict[str, Any]:
        return {
            "base_url": self.base_url,
            "api_key": self.api_key,
            "endpoint_template": self.endpoint_template,
            "http_method": self.http_method,
            "headers": self.headers,
            "timeout": self.timeout,
            "retry_attempts": self.retry_attempts,
            "retry_delay": self.retry_delay,
            # GAP-EXPORT-001-FIX (Build 98)
            "rate_limit_wait_s": self.rate_limit_wait_s,
            "max_retry_after_s": self.max_retry_after_s,
        }

    def to_file(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "APIConfig":
        return cls(
            base_url=d.get("base_url", "https://web.com/api"),
            api_key=d.get("api_key", ""),
            endpoint_template=d.get(
                "endpoint_template",
                "/{language}/{api_key}/update/{hotel_id}.json",
            ),
            http_method=d.get("http_method", "PATCH"),
            headers=d.get("headers", {"Content-Type": "application/json"}),
            timeout=d.get("timeout", 30),
            retry_attempts=d.get("retry_attempts", 3),
            retry_delay=d.get("retry_delay", 2.0),
            # GAP-EXPORT-001-FIX (Build 98): backwards-compatible defaults
            rate_limit_wait_s=d.get("rate_limit_wait_s", 60.0),
            max_retry_after_s=d.get("max_retry_after_s", 300.0),
        )

    @classmethod
    def from_file(cls, path: str | Path) -> "APIConfig":
        return cls.from_dict(
            json.loads(Path(path).read_text(encoding="utf-8"))
        )


# ---------------------------------------------------------------------------
# APIExporter
# ---------------------------------------------------------------------------

class APIExporter:
    """
    Motor de exportación.

    Flujo:
      1. Para cada url_id en selection:
         a. Llama ApiPayloadBuilder.build_payload(url_id) → payload completo.
         b. Filtra solo los campos pedidos por el template.
         c. Ajusta locales según template.languages (en siempre primero).
         d. Valida si template.validate_before_export.
         e. En dry_run=False: envía PATCH a la API; en dry_run=True: solo retorna payload.

    Hotel ID usado en la URL:
      Se usa hotel_id_booking (dest_id de Booking.com) del primer registro Hotel
      para el url_id. Si no está disponible se usa el UUID de url_id.
    """

    def __init__(
        self,
        db: Session,
        config: APIConfig,
        template: ExportTemplate,
        selection: ExportSelection,
    ) -> None:
        self.db = db
        self.config = config
        self.template = template
        self.selection = selection
        self._builder = ApiPayloadBuilder(db)
        # BUG-EXPORT-001-FIX (Build 96): requests.Session() para reutilización
        # de conexiones HTTP. Antes cada _send() abría una nueva conexión TCP
        # vía requests.request(). Con Session() las conexiones se mantienen
        # vivas (Keep-Alive) entre hoteles del mismo batch.
        self._http_session = requests.Session()
        self._http_session.headers.update(self.config.headers)

    # ── public ────────────────────────────────────────────────────────────

    def export_single(
        self,
        url_id: UUID,
        dry_run: bool = True,
    ) -> Dict[str, Any]:
        """
        Exporta un único hotel.

        Returns dict con:
          url_id, hotel_id, payload, validation_errors, sent, response_status
        """
        result: Dict[str, Any] = {
            "url_id": str(url_id),
            "hotel_id": None,
            "payload": None,
            "validation_errors": [],
            "sent": False,
            "response_status": None,
            "error": None,
        }

        try:
            # Build full payload
            full_payload = self._builder.build_payload(url_id)

            # Get hotel_id_booking for URL construction
            hotel_row = (
                self.db.query(Hotel)
                .filter(Hotel.url_id == url_id, Hotel.language == "en")
                .first()
            )
            hotel_id_booking = (
                hotel_row.hotel_id_booking if hotel_row else None
            ) or str(url_id)
            result["hotel_id"] = hotel_id_booking

            # Filter fields + languages
            filtered = self._filter_payload(full_payload)
            result["payload"] = filtered

            # Validate
            if self.template.validate_before_export:
                errors = self._validate(filtered)
                result["validation_errors"] = errors
                if errors and self.template.skip_incomplete:
                    result["error"] = "Validation failed — skipped"
                    return result

            # Send
            if not dry_run:
                status = self._send(hotel_id_booking, filtered)
                result["sent"] = True
                result["response_status"] = status

        except Exception as exc:
            logger.error("export_single url_id=%s: %s", url_id, exc, exc_info=True)
            result["error"] = str(exc)[:500]

        return result

    def export_batch(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        Exporta todos los url_ids de selection.

        Returns summary dict: total, success, failed, skipped, errors.
        """
        summary: Dict[str, Any] = {
            "total": len(self.selection),
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "errors": [],
            "dry_run": dry_run,
        }

        for uid in self.selection.url_ids:
            res = self.export_single(uid, dry_run=dry_run)
            if res.get("error"):
                summary["failed"] += 1
                summary["errors"].append(
                    {"url_id": str(uid), "error": res["error"]}
                )
            elif res.get("validation_errors") and self.template.skip_incomplete:
                summary["skipped"] += 1
            else:
                summary["success"] += 1

        logger.info(
            "export_batch done — total=%d success=%d failed=%d skipped=%d dry_run=%s",
            summary["total"], summary["success"],
            summary["failed"], summary["skipped"], dry_run,
        )
        return summary

    def export_to_json_files(
        self,
        output_dir: str | Path = "output/export",
        dry_run: bool = True,
    ) -> Dict[str, Any]:
        """
        Exporta todos los hoteles como archivos JSON individuales para revisión.

        Cada archivo: {output_dir}/{hotel_id_booking}.json
        """
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        summary = {"total": len(self.selection), "success": 0, "failed": 0}

        for uid in self.selection.url_ids:
            res = self.export_single(uid, dry_run=True)
            hotel_id = res.get("hotel_id") or str(uid)
            file_path = out / f"{hotel_id}.json"
            try:
                file_path.write_text(
                    json.dumps(res["payload"], indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                summary["success"] += 1
            except Exception as exc:
                logger.error("export_to_json_files: %s — %s", hotel_id, exc)
                summary["failed"] += 1

        return summary

    # ── private ───────────────────────────────────────────────────────────

    def _filter_payload(self, full_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filtra el payload completo:
          1. Conserva solo los campos solicitados por template.fields.
          2. Dentro de cada campo multilingüe, conserva solo template.languages.
          3. Garantiza que 'en' sea siempre el primer idioma.
          4. Actualiza args.locales con los idiomas efectivamente presentes.
        """
        target_fields: Set[str] = {f.value for f in self.template.fields}
        target_langs: List[str] = self.template.locales  # en siempre primero

        full_data: Dict[str, Any] = full_payload.get("data", {})
        filtered_data: Dict[str, Any] = {}

        # Language-independent scalar fields
        scalar_fields = {
            "rating", "geoPosition", "scoreReview", "scoreReviewBasedOn",
            "roomsQuantity", "accommodationType", "priceRange", "images",
        }

        for field_name in target_fields:
            if field_name not in full_data:
                continue
            val = full_data[field_name]
            if field_name in scalar_fields:
                filtered_data[field_name] = val
            elif isinstance(val, dict):
                # Multilingual dict — filter to requested languages, en first
                filtered_lang: Dict[str, Any] = {}
                for lang in target_langs:
                    if lang in val:
                        filtered_lang[lang] = val[lang]
                filtered_data[field_name] = filtered_lang
            else:
                filtered_data[field_name] = val

        # Build args — locales = languages actually present in payload
        present_langs: List[str] = []
        for lang in target_langs:
            for v in filtered_data.values():
                if isinstance(v, dict) and lang in v:
                    if lang not in present_langs:
                        present_langs.append(lang)
                    break
        if not present_langs:
            present_langs = target_langs

        args: Dict[str, Any] = {}
        if self.template.include_args:
            args = dict(self.template.args_config)
            args["locales"] = present_langs

        return {"data": filtered_data, "args": args}

    def _validate(self, payload: Dict[str, Any]) -> List[str]:
        """Returns list of validation error strings (empty = valid)."""
        errors: List[str] = []
        data = payload.get("data", {})

        for req_field in self.template.required_fields_for_validation:
            fn = req_field.value
            if fn not in data:
                errors.append(f"Missing required field: {fn}")
                continue
            val = data[fn]
            if val is None:
                errors.append(f"Field '{fn}' is None")
            elif isinstance(val, dict):
                if not val:
                    errors.append(f"Field '{fn}' is empty dict")
                elif "en" not in val:
                    errors.append(f"Field '{fn}' missing 'en' locale")

        return errors

    def _send(self, hotel_id: str, payload: Dict[str, Any]) -> int:
        """
        BUG-EXPORT-001-FIX + BUG-EXPORT-002-FIX (Build 96):
          - Usa self._http_session (requests.Session) en lugar de requests.request()
            directo. La sesión reutiliza conexiones TCP entre hoteles del mismo batch.
          - Añade X-Idempotency-Key único por hotel. La misma clave se reutiliza
            en todos los reintentos del mismo hotel para que el servidor destino
            pueda deduplicar sin requerirlo en peticiones nuevas.

        Envía el payload a la API via PATCH.
        Reintentos con backoff exponencial.
        Retorna el HTTP status code del último intento.
        """
        # Primary language for URL: always 'en' per _API_.md
        url = self.config.build_url(language="en", hotel_id=hotel_id)
        body = json.dumps(payload, ensure_ascii=False)
        last_status = 0

        # BUG-EXPORT-002-FIX: clave de idempotencia única por hotel, estable
        # en todos los reintentos del mismo intento de exportación.
        idempotency_key = str(uuid.uuid4())

        for attempt in range(1, self.config.retry_attempts + 1):
            try:
                # BUG-EXPORT-002-FIX: X-Idempotency-Key en cada request
                request_headers = {"X-Idempotency-Key": idempotency_key}
                # BUG-EXPORT-001-FIX: usa Session() en lugar de requests.request()
                resp = self._http_session.request(
                    method=self.config.http_method,
                    url=url,
                    data=body.encode("utf-8"),
                    headers=request_headers,
                    timeout=self.config.timeout,
                )
                last_status = resp.status_code
                if resp.ok:
                    logger.info(
                        "API PATCH hotel_id=%s → %d (attempt %d, idempotency_key=%s)",
                        hotel_id, last_status, attempt, idempotency_key,
                    )
                    return last_status

                # GAP-EXPORT-001-FIX (Build 98): tratamiento especial HTTP 429
                if last_status == 429:
                    wait_s = self.config.rate_limit_wait_s
                    retry_after_header = resp.headers.get("Retry-After", "")
                    if retry_after_header:
                        try:
                            # Formato numérico: "Retry-After: 90"
                            wait_s = max(float(retry_after_header), wait_s)
                        except ValueError:
                            # Formato HTTP-date: "Retry-After: Wed, 21 Oct 2025 07:28:00 GMT"
                            try:
                                import datetime
                                ra_dt = parsedate_to_datetime(retry_after_header)
                                delta = (ra_dt - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
                                if delta > 0:
                                    wait_s = max(delta, wait_s)
                            except Exception:
                                pass  # header malformado — usar rate_limit_wait_s por defecto

                    if wait_s > self.config.max_retry_after_s:
                        logger.error(
                            "GAP-EXPORT-001-FIX: API 429 hotel_id=%s — "
                            "Retry-After=%.0f s supera max_retry_after_s=%.0f s. "
                            "Abortando reintentos para este hotel.",
                            hotel_id, wait_s, self.config.max_retry_after_s,
                        )
                        return last_status

                    logger.warning(
                        "GAP-EXPORT-001-FIX: API 429 hotel_id=%s — "
                        "rate limited. Esperando %.0f s antes de reintento %d/%d.",
                        hotel_id, wait_s, attempt, self.config.retry_attempts,
                    )
                    time.sleep(wait_s)
                    continue  # ir directamente al siguiente intento sin el backoff estándar

                logger.warning(
                    "API PATCH hotel_id=%s → %d body=%s (attempt %d/%d)",
                    hotel_id, last_status,
                    resp.text[:200], attempt, self.config.retry_attempts,
                )
            except requests.RequestException as exc:
                logger.error(
                    "API PATCH hotel_id=%s attempt %d/%d: %s",
                    hotel_id, attempt, self.config.retry_attempts, exc,
                )

            if attempt < self.config.retry_attempts:
                time.sleep(self.config.retry_delay * (2 ** (attempt - 1)))

        return last_status


# ---------------------------------------------------------------------------
# CLI panel (opcional — para uso interactivo)
# ---------------------------------------------------------------------------

def user_panel_cli(db: Session) -> None:
    """
    Panel interactivo de exportación en línea de comandos.

    Uso:
        from app.api_export_system import user_panel_cli
        from app.database import get_db
        with get_db() as db:
            user_panel_cli(db)
    """
    manager = TemplateManager()
    config = APIConfig()
    selection = ExportSelection()

    while True:
        print("\n" + "=" * 60)
        print("PANEL DE EXPORTACIÓN API — BookingScraper Pro")
        print("=" * 60)
        print(f"  Selección actual : {len(selection)} hotel(es)")
        print(f"  Plantilla activa : {getattr(manager, '_active', 'default')}")
        print()
        print("  [1] Cargar IDs desde archivo")
        print("  [2] Seleccionar todos los hoteles completados (status=done)")
        print("  [3] Listar plantillas disponibles")
        print("  [4] Cambiar plantilla")
        print("  [5] Configurar conexión API (base_url / api_key)")
        print("  [6] Previsualizar primer hotel (dry run)")
        print("  [7] Exportar a archivos JSON")
        print("  [8] Exportar a la API")
        print("  [0] Salir")

        choice = input("\nOpción: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            path = input("Ruta del archivo (JSON o TXT): ").strip()
            try:
                selection = ExportSelection.from_file(path)
                print(f"  ✓ Cargados {len(selection)} IDs desde {path}")
            except Exception as exc:
                print(f"  ✗ Error: {exc}")

        elif choice == "2":
            selection = ExportSelection.from_db_all_pending(db)
            print(f"  ✓ {len(selection)} hoteles completados seleccionados")

        elif choice == "3":
            templates = manager.list_templates()
            print(f"  Plantillas disponibles: {', '.join(templates)}")

        elif choice == "4":
            name = input("Nombre de plantilla: ").strip()
            try:
                tmpl = manager.load_template(name)
                manager._active = name  # type: ignore[attr-defined]
                print(f"  ✓ Plantilla '{name}' cargada — {len(tmpl.fields)} campos, idiomas: {tmpl.locales}")
            except Exception as exc:
                print(f"  ✗ Error: {exc}")

        elif choice == "5":
            config.base_url = input(f"  base_url [{config.base_url}]: ").strip() or config.base_url
            config.api_key  = input(f"  api_key  [{config.api_key}]: ").strip()  or config.api_key
            print(f"  ✓ Configuración actualizada")

        elif choice in ("6", "7", "8"):
            if not selection.url_ids:
                print("  ✗ No hay IDs seleccionados. Usa opciones [1] o [2] primero.")
                continue

            tmpl_name = getattr(manager, "_active", "default")
            try:
                template = manager.load_template(tmpl_name)
            except Exception:
                template = ExportTemplate.default_template()

            exporter = APIExporter(db, config, template, selection)

            if choice == "6":
                res = exporter.export_single(selection.url_ids[0], dry_run=True)
                print(json.dumps(res["payload"], indent=2, ensure_ascii=False)[:2000])

            elif choice == "7":
                out_dir = input("  Carpeta de salida [output/export]: ").strip() or "output/export"
                result = exporter.export_to_json_files(out_dir)
                print(f"  ✓ JSON exportados: {result['success']}/{result['total']}")

            elif choice == "8":
                confirm = input(f"  Enviar {len(selection)} hoteles a la API? (s/N): ").strip().lower()
                if confirm == "s":
                    result = exporter.export_batch(dry_run=False)
                    print(f"  ✓ Enviados: {result['success']}  Fallidos: {result['failed']}  Saltados: {result['skipped']}")
                else:
                    print("  Cancelado.")

        else:
            print("  Opción no reconocida.")
