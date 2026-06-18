"""
language_config.py — Build 103
Carga y valida languages.json.

Secciones activas (Build 103):
  lang_url_codes      → LANG_URL_MAP en scraper.py
  lang_accept_headers → LANG_TO_ACCEPT_LANGUAGE en scraper.py
  category_labels     → etiquetas API en api_payload_builder.py
  see_all_patterns    → detección de ruido en extractor.py

Secciones ELIMINADAS en Build 103 (extraer4.py v4.5 — DOM verbatim):
  room_level_category_labels  — categorías de habitación por idioma
  category_key_map            — normalización de reseñas por idioma
  facility_group_map          — groupId → etiqueta de categoría
  service_category_rules      — inferencia de categoría por keywords

El servicio service_category ahora se importa verbatim desde el DOM de Booking.com.
No se realizan traducciones ni mapeos de categorías de instalaciones.

Para añadir un nuevo idioma:
  1. Añadir código en lang_url_codes y lang_accept_headers.
  2. Añadir etiquetas de reseñas en category_labels para ese idioma.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, FrozenSet, List, Optional, Tuple

logger = logging.getLogger(__name__)

_API_KEYS = frozenset([
    "hotel_services", "hotel_clean", "hotel_comfort",
    "hotel_value", "hotel_location", "hotel_wifi",
])

# Secciones que DEBEN tener cobertura para todos los idiomas habilitados
_REQUIRED_SECTIONS = (
    "lang_url_codes",
    "lang_accept_headers",
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
    Contenedor tipado de los diccionarios dependientes de idioma.
    Se construye desde languages.json y se valida antes de ser devuelto.

    Build 103: facility_group_map, service_category_rules,
    room_level_category_labels y category_key_map eliminados.
    El service_category se importa verbatim desde el DOM de Booking.com.
    """
    _config_file: str

    # ── Secciones activas (Build 103) ──────────────────────────────────────
    lang_url_codes:     Dict[str, str]              # lang → url_code
    lang_accept_headers: Dict[str, str]             # lang → Accept-Language
    category_labels:    Dict[str, Dict[str, str]]  # api_key → {lang: label}
    see_all_pattern:    re.Pattern                  # compiled regex

    def get_category_label(self, api_key: str, lang: str) -> Optional[str]:
        """Devuelve la etiqueta canónica para api_key y lang. None si no existe."""
        return self.category_labels.get(api_key, {}).get(lang)

    def get_url_code(self, lang: str) -> str:
        """Devuelve el código URL de Booking.com para lang. Fallback → lang."""
        return self.lang_url_codes.get(lang, lang)

    def get_accept_header(self, lang: str) -> str:
        """Devuelve el header Accept-Language para lang. Fallback → 'lang;q=0.9'."""
        return self.lang_accept_headers.get(lang, f"{lang};q=0.9")


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

        lang_url_codes      = self._section_flat(raw, "lang_url_codes")
        lang_accept_headers = self._section_flat(raw, "lang_accept_headers")
        category_labels     = self._section_nested(raw, "category_labels")
        see_all_pat         = self._build_see_all_pattern(raw)

        lc = LanguageConfig(
            _config_file=str(path),
            lang_url_codes=lang_url_codes,
            lang_accept_headers=lang_accept_headers,
            category_labels=category_labels,
            see_all_pattern=see_all_pat,
        )

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

    def _build_see_all_pattern(self, raw: dict) -> re.Pattern:
        section = raw.get("see_all_patterns", {})
        patterns = section.get("patterns", [])
        if not patterns:
            return re.compile(r"^$")
        alternation = "|".join(f"(?:{p})" for p in patterns)
        return re.compile(f"^({alternation})", re.IGNORECASE | re.VERBOSE)

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

        # 1. lang_url_codes, lang_accept_headers
        flat_checks = {
            "lang_url_codes":      lc.lang_url_codes,
            "lang_accept_headers": lc.lang_accept_headers,
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

        # 2. category_labels — todos los api_keys por idioma
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

        # 3. 'en' debe estar en enabled_langs y ser el primero
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
