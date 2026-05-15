"""
language_config.py — BookingScraper Pro v6.0.0 Build 98
========================================================

Single source of truth loader for ALL language-dependent dictionaries.

Architecture:
    languages.json  →  LanguageConfig (singleton)  →  todos los módulos
         ↑                      ↑
    .env / config.py      Validado en startup
    LANGUAGES_CONFIG_FILE  con LanguageConfigValidator

Responsabilidades:
    - Cargar languages.json desde la ruta configurada en LANGUAGES_CONFIG_FILE.
    - Exponer diccionarios tipados para uso en extractor.py,
      api_payload_builder.py y scraper.py.
    - Validar cobertura de TODOS los idiomas de ENABLED_LANGUAGES contra
      TODAS las secciones obligatorias del JSON.
    - BLOQUEAR el arranque del sistema si la validación falla
      (raise LanguageConfigError con informe completo).

Secciones obligatorias de languages.json (deben cubrir todos los idiomas):
    lang_url_codes           → LANG_URL_MAP en scraper.py
    lang_accept_headers      → LANG_TO_ACCEPT_LANGUAGE en scraper.py
    room_level_category_labels → filtro groupId=15 en api_payload_builder.py
    category_key_map         → normalización reseñas en api_payload_builder.py
    category_labels          → etiquetas API en api_payload_builder.py
    facility_group_map       → categorías de servicios en extractor.py
    service_category_rules   → inferencia de categoría en extractor.py
    see_all_patterns         → detección de ruido en extractor.py

Claves con valor '__EXCLUDED__' se tratan como exclusiones intencionales
(no como faltantes). Ejemplo: FR en room_level_category_labels.

Uso:
    from app.language_config import get_language_config
    lc = get_language_config()
    url_code = lc.lang_url_codes["es"]         # → "es"
    labels   = lc.category_labels["hotel_clean"]["de"]  # → "Sauberkeit"

Platform: Windows 11 / Python 3.14 / PostgreSQL 14+
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)

# Constantes
_EXCLUDED_MARKER = "__EXCLUDED__"
_API_KEYS: Tuple[str, ...] = (
    "hotel_services", "hotel_clean", "hotel_comfort",
    "hotel_value", "hotel_location", "hotel_wifi", "total",
)

# Secciones que DEBEN tener cobertura para todos los idiomas habilitados
_REQUIRED_SECTIONS = (
    "lang_url_codes",
    "lang_accept_headers",
    "room_level_category_labels",
    "category_labels",
)
# Secciones con estructura interna que requieren validación específica
_REQUIRED_DEEP_SECTIONS = (
    "category_key_map",   # {api_key: {lang: [variants]}}
    "facility_group_map", # {group_id: {lang: label}}
)


# ---------------------------------------------------------------------------
# Excepción de configuración de idioma
# ---------------------------------------------------------------------------

class LanguageConfigError(RuntimeError):
    """
    Lanzada cuando languages.json no cubre todos los idiomas habilitados.
    El mensaje incluye el informe completo de issues para facilitar la corrección.
    Causa que el arranque del sistema falle de forma controlada.
    """


# ---------------------------------------------------------------------------
# Dataclasses de resultado de validación
# ---------------------------------------------------------------------------

@dataclass
class LangConfigIssue:
    section:  str
    lang:     str
    detail:   str
    severity: str = "ERROR"   # "ERROR" bloquea arranque; "WARNING" no


@dataclass
class LangConfigReport:
    enabled_langs: List[str]
    config_file:   str
    issues:        List[LangConfigIssue] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(i.severity == "ERROR" for i in self.issues)

    @property
    def has_warnings(self) -> bool:
        return any(i.severity == "WARNING" for i in self.issues)

    def summary(self) -> str:
        errors   = [i for i in self.issues if i.severity == "ERROR"]
        warnings = [i for i in self.issues if i.severity == "WARNING"]
        if not self.issues:
            return (
                f"✅ LanguageConfig OK — {len(self.enabled_langs)} langs validated "
                f"against {self.config_file}"
            )
        lines = [
            f"{'❌' if errors else '⚠️'} LanguageConfig — "
            f"{len(errors)} error(s), {len(warnings)} warning(s) "
            f"| langs={self.enabled_langs} | file={self.config_file}"
        ]
        for iss in self.issues:
            tag = "❌ ERROR" if iss.severity == "ERROR" else "⚠️  WARN "
            lines.append(f"  [{tag}] [{iss.section}] lang={iss.lang!r}: {iss.detail}")
        if errors:
            lines.append("")
            lines.append(
                "ACTION REQUIRED: update languages.json to add missing entries "
                "before restarting the system."
            )
        return "\n".join(lines)

    def raise_if_errors(self) -> None:
        if self.has_errors:
            raise LanguageConfigError(
                f"Language configuration incomplete — system cannot start.\n"
                f"{self.summary()}"
            )


# ---------------------------------------------------------------------------
# LanguageConfig — el objeto central
# ---------------------------------------------------------------------------

@dataclass
class LanguageConfig:
    """
    Contenedor tipado de todos los diccionarios dependientes de idioma.
    Se construye desde languages.json y se valida antes de ser devuelto.
    """
    _config_file: str

    # ── Secciones expuestas ────────────────────────────────────────────────
    lang_url_codes:             Dict[str, str]              # lang → url_code
    lang_accept_headers:        Dict[str, str]              # lang → Accept-Language
    room_level_category_labels: Dict[str, str]              # lang → label | __EXCLUDED__
    category_labels:            Dict[str, Dict[str, str]]   # api_key → {lang: label}
    facility_group_map:         Dict[int, Dict[str, str]]   # group_id → {lang: label}
    service_category_rules:     List[Tuple[Tuple[str, ...], int]]  # [(keywords, group_id)]
    see_all_pattern:            re.Pattern                  # compiled regex

    # Derivados en tiempo de carga
    category_key_map:           Dict[str, str]              # text_lower → api_key (flat)
    room_level_filter:          FrozenSet[str]              # valores lowercased (sin __EXCLUDED__)

    def get_facility_label(self, group_id: int, lang: str) -> str:
        """Devuelve la etiqueta de grupo para group_id y lang. Fallback → EN → str(group_id)."""
        group = self.facility_group_map.get(group_id, {})
        return (
            group.get(lang)
            or group.get("en")
            or str(group_id)
        )

    def get_category_label(self, api_key: str, lang: str) -> Optional[str]:
        """Devuelve la etiqueta canónica para api_key y lang. None si no existe."""
        return self.category_labels.get(api_key, {}).get(lang)

    def get_url_code(self, lang: str) -> str:
        """Devuelve el código URL de Booking.com para lang. Fallback → lang."""
        return self.lang_url_codes.get(lang, lang)

    def get_accept_header(self, lang: str) -> str:
        """Devuelve el header Accept-Language para lang. Fallback → 'lang;q=0.9'."""
        return self.lang_accept_headers.get(lang, f"{lang};q=0.9")

    def is_room_level_category(self, category: str, lang: str) -> bool:
        """
        Devuelve True si category es una categoría de amenidades de habitación
        (groupId=15) para el idioma dado. Tiene en cuenta __EXCLUDED__ (FR).
        """
        raw = self.room_level_category_labels.get(lang)
        if raw is None or raw == _EXCLUDED_MARKER:
            return False
        return category.strip().lower() == raw.lower()

    def is_room_level_category_by_value(self, category_lower: str) -> bool:
        """Devuelve True si category_lower está en el filtro room_level_filter."""
        return category_lower in self.room_level_filter


# ---------------------------------------------------------------------------
# LanguageConfigLoader — carga y construye LanguageConfig desde JSON
# ---------------------------------------------------------------------------

class LanguageConfigLoader:
    """Carga languages.json y construye un LanguageConfig validado."""

    def load(self, config_file: str, enabled_langs: List[str]) -> LanguageConfig:
        """
        Carga, valida y devuelve un LanguageConfig.
        Lanza LanguageConfigError si algún idioma obligatorio falta.
        """
        path = Path(config_file)
        if not path.is_absolute():
            # Buscar relativo al directorio raíz del proyecto
            for candidate in [
                Path(config_file),
                Path(__file__).parent.parent / config_file,
                Path(__file__).parent / config_file,
            ]:
                if candidate.exists():
                    path = candidate
                    break

        if not path.exists():
            raise LanguageConfigError(
                f"languages.json not found at '{config_file}'. "
                f"Copy languages.json to the project root or set "
                f"LANGUAGES_CONFIG_FILE in .env."
            )

        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise LanguageConfigError(
                f"languages.json is not valid JSON: {e}"
            ) from e

        # Construir los dicts internos
        lang_url_codes      = self._section_flat(raw, "lang_url_codes")
        lang_accept_headers = self._section_flat(raw, "lang_accept_headers")
        room_level_labels   = self._section_flat(raw, "room_level_category_labels")
        category_labels     = self._section_nested(raw, "category_labels")
        facility_group_map  = self._build_facility_group_map(raw)
        service_rules       = self._build_service_rules(raw, facility_group_map)
        see_all_pat         = self._build_see_all_pattern(raw)
        category_key_map    = self._flatten_category_key_map(raw)

        room_level_filter = frozenset(
            v.lower() for v in room_level_labels.values()
            if v and v != _EXCLUDED_MARKER
        )

        lc = LanguageConfig(
            _config_file=str(path),
            lang_url_codes=lang_url_codes,
            lang_accept_headers=lang_accept_headers,
            room_level_category_labels=room_level_labels,
            category_labels=category_labels,
            facility_group_map=facility_group_map,
            service_category_rules=service_rules,
            see_all_pattern=see_all_pat,
            category_key_map=category_key_map,
            room_level_filter=room_level_filter,
        )

        # Validar cobertura → bloquea arranque si hay errores
        report = self._validate(lc, raw, enabled_langs, str(path))
        logger.info(report.summary())
        report.raise_if_errors()

        return lc

    # ── Helpers de construcción ─────────────────────────────────────────────

    def _section_flat(self, raw: dict, key: str) -> Dict[str, str]:
        section = raw.get(key, {})
        return {k: v for k, v in section.items() if not k.startswith("_")}

    def _section_nested(self, raw: dict, key: str) -> Dict[str, Dict[str, str]]:
        section = raw.get(key, {})
        return {
            api_k: {lang: label for lang, label in lang_map.items()
                    if not lang.startswith("_")}
            for api_k, lang_map in section.items()
            if not api_k.startswith("_")
        }

    def _build_facility_group_map(self, raw: dict) -> Dict[int, Dict[str, str]]:
        section = raw.get("facility_group_map", {})
        result: Dict[int, Dict[str, str]] = {}
        for gid_str, lang_map in section.items():
            if gid_str.startswith("_"):
                continue
            try:
                gid = int(gid_str)
            except ValueError:
                logger.warning("facility_group_map: non-integer key %r — skipped", gid_str)
                continue
            result[gid] = {k: v for k, v in lang_map.items() if not k.startswith("_")}
        return result

    def _build_service_rules(
        self, raw: dict, facility_map: Dict[int, Dict[str, str]]
    ) -> List[Tuple[Tuple[str, ...], int]]:
        section = raw.get("service_category_rules", {})
        rules_raw = section.get("rules", [])
        result: List[Tuple[Tuple[str, ...], int]] = []
        for rule in rules_raw:
            keywords = tuple(str(k).lower() for k in rule.get("keywords", []))
            try:
                gid = int(rule.get("group_id", 0))
            except (ValueError, TypeError):
                logger.warning("service_category_rules: invalid group_id %r — skipped",
                               rule.get("group_id"))
                continue
            if keywords and gid in facility_map:
                result.append((keywords, gid))
            elif gid not in facility_map:
                logger.warning(
                    "service_category_rules: group_id=%d not in facility_group_map — skipped", gid
                )
        return result

    def _build_see_all_pattern(self, raw: dict) -> re.Pattern:
        section = raw.get("see_all_patterns", {})
        patterns = section.get("patterns", [])
        if not patterns:
            return re.compile(r"^$")  # match nothing
        alternation = "|".join(f"(?:{p})" for p in patterns)
        return re.compile(f"^({alternation})", re.IGNORECASE | re.VERBOSE)

    def _flatten_category_key_map(self, raw: dict) -> Dict[str, str]:
        """
        Convierte category_key_map de {api_key: {lang: [variants]}}
        al dict plano {text_lower: api_key} usado en runtime.
        """
        section = raw.get("category_key_map", {})
        result: Dict[str, str] = {}
        for api_key, lang_variants in section.items():
            if api_key.startswith("_"):
                continue
            if api_key not in _API_KEYS:
                logger.warning("category_key_map: unknown api_key %r — skipped", api_key)
                continue
            for lang, variants in lang_variants.items():
                if lang.startswith("_"):
                    continue
                for text in (variants if isinstance(variants, list) else [variants]):
                    text_lower = str(text).strip().lower()
                    if text_lower:
                        result[text_lower] = api_key
        return result

    # ── Validador ──────────────────────────────────────────────────────────

    def _validate(
        self,
        lc: LanguageConfig,
        raw: dict,
        enabled_langs: List[str],
        config_file: str,
    ) -> LangConfigReport:
        report = LangConfigReport(
            enabled_langs=list(enabled_langs),
            config_file=config_file,
        )

        # 1. Secciones planas: lang_url_codes, lang_accept_headers, room_level
        flat_checks = {
            "lang_url_codes":             lc.lang_url_codes,
            "lang_accept_headers":        lc.lang_accept_headers,
        }
        for section_name, mapping in flat_checks.items():
            for lang in enabled_langs:
                if lang not in mapping:
                    report.issues.append(LangConfigIssue(
                        section=section_name,
                        lang=lang,
                        detail=(
                            f"Missing entry. Add \"{lang}\": \"<value>\" "
                            f"to section '{section_name}' in languages.json."
                        ),
                    ))

        # 2. room_level_category_labels (permite __EXCLUDED__)
        for lang in enabled_langs:
            val = lc.room_level_category_labels.get(lang)
            if val is None:
                report.issues.append(LangConfigIssue(
                    section="room_level_category_labels",
                    lang=lang,
                    detail=(
                        f"Missing entry. Add \"{lang}\": \"<groupId=15 label>\" "
                        f"(or \"{lang}\": \"{_EXCLUDED_MARKER}\" if label collides "
                        f"with hotel-level facilities like FR 'Équipements')."
                    ),
                ))

        # 3. category_labels — todos los api_keys por idioma
        for lang in enabled_langs:
            missing_keys = [
                api_key for api_key in _API_KEYS
                if lang not in lc.category_labels.get(api_key, {})
            ]
            if missing_keys:
                report.issues.append(LangConfigIssue(
                    section="category_labels",
                    lang=lang,
                    detail=(
                        f"Missing api_keys: {missing_keys}. "
                        f"Add \"{lang}\": \"<label>\" under each missing key "
                        f"in 'category_labels' in languages.json."
                    ),
                ))

        # 4. category_key_map — al menos una variante por api_key por idioma
        cat_key_section = raw.get("category_key_map", {})
        for lang in enabled_langs:
            missing_keys = []
            for api_key in _API_KEYS:
                variants = cat_key_section.get(api_key, {}).get(lang)
                if not variants:
                    missing_keys.append(api_key)
            if missing_keys:
                report.issues.append(LangConfigIssue(
                    section="category_key_map",
                    lang=lang,
                    detail=(
                        f"Missing text variants for api_keys: {missing_keys}. "
                        f"Add \"{lang}\": [\"<booking_text>\"] under each missing "
                        f"key in 'category_key_map' in languages.json."
                    ),
                ))

        # 5. facility_group_map — todos los group_ids por idioma
        for lang in enabled_langs:
            missing_gids = [
                gid for gid, lang_map in lc.facility_group_map.items()
                if lang not in lang_map
            ]
            if missing_gids:
                report.issues.append(LangConfigIssue(
                    section="facility_group_map",
                    lang=lang,
                    detail=(
                        f"Missing labels for group_ids: {missing_gids}. "
                        f"Add \"{lang}\": \"<label>\" under each missing "
                        f"group_id in 'facility_group_map' in languages.json."
                    ),
                ))

        # 6. 'en' debe estar en enabled_langs y ser el primero
        if "en" not in enabled_langs:
            report.issues.append(LangConfigIssue(
                section="ENABLED_LANGUAGES",
                lang="en",
                detail=(
                    "'en' is mandatory and must always be in ENABLED_LANGUAGES. "
                    "API contract (_API_.md) requires English data in all payloads."
                ),
            ))
        elif enabled_langs[0] != "en":
            report.issues.append(LangConfigIssue(
                section="ENABLED_LANGUAGES",
                lang="en",
                severity="WARNING",
                detail=(
                    f"'en' is not first in ENABLED_LANGUAGES={enabled_langs}. "
                    f"It will be reordered automatically, but .env should list 'en' first."
                ),
            ))

        return report


# ---------------------------------------------------------------------------
# Singleton — único punto de acceso
# ---------------------------------------------------------------------------

_instance: Optional[LanguageConfig] = None


def get_language_config() -> LanguageConfig:
    """
    Devuelve el singleton LanguageConfig.
    Debe haber sido inicializado con init_language_config() antes de llamar.
    Lanza RuntimeError si no se ha inicializado.
    """
    if _instance is None:
        raise RuntimeError(
            "LanguageConfig not initialized. "
            "Call init_language_config() in the application lifespan."
        )
    return _instance


def init_language_config(
    config_file: str,
    enabled_langs: List[str],
) -> LanguageConfig:
    """
    Inicializa el singleton LanguageConfig.
    Debe llamarse UNA VEZ en el arranque (lifespan de FastAPI).
    Lanza LanguageConfigError si la validación falla.
    """
    global _instance
    loader = LanguageConfigLoader()
    _instance = loader.load(config_file, enabled_langs)
    return _instance


def reset_language_config() -> None:
    """Resetea el singleton (útil en tests unitarios)."""
    global _instance
    _instance = None
