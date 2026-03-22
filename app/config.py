"""
config.py — BookingScraper Pro v6.0.0 build 53
================================================
Rutas corregidas según estructura real del proyecto:
  BASE_DIR/
  ├── logs/          ← logs de aplicación (rotating file handler)
  │   └── debug/     ← logs debug nivel aplicación
  ├── data/
  │   ├── images/    ← imágenes descargadas de hoteles
  │   ├── exports/   ← exportaciones CSV/JSON
  │   └── logs/
  │       └── debug/ ← HTML debug del scraper (selenium, cloudscraper)
  ├── backups/       ← backups de base de datos
  └── templates/     ← plantillas (uso futuro)

Fixes aplicados (v48):
  SCRAP-SEC-001: SECRET_KEY auto-generada si ausente/insegura.
  SCRAP-SEC-002: API_KEY validada cuando REQUIRE_API_KEY=true.
  BUG-001/SCRAP-BUG-004: database_url es lazy property — no falla en import.
  BUG-005: ENABLED_LANGUAGES validada una sola vez en model_validator.
  BUG-009: VPN_COUNTRIES validados contra lista canónica de vpn_manager_windows.
  BUG-014: DEBUG_HTML_MAX_AGE_HOURS con conversión segura a int.
  BUG-017: LANGUAGE_EXT validado contra ENABLED_LANGUAGES en startup.

Cambios v52-v53:
  ERROR-001 (v53): BUILD_VERSION consolidado — fuente única de verdad en
                   app/__init__.py. config.py importa desde allí via módulo
                   para evitar divergencia. Valor actualizado a 53.
  ERROR-007 (v53): Comentario corrupto en línea Browser/Selenium corregido.
"""

from __future__ import annotations

import logging
import os
import secrets
import sys
from functools import cached_property
from pathlib import Path
from typing import ClassVar, Dict, List, Optional, Set

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, DotEnvSettingsSource, EnvSettingsSource

# ── Versión — importada desde app/__init__.py (fuente única de verdad)
# ERROR-001 (v53): BUILD_VERSION consolidado. El valor canónico vive en
# app/__init__.py (BUILD_VERSION = 53). config.py re-expone las mismas
# constantes para que Settings.BUILD_VERSION sea consistente sin
# duplicar la definición.
APP_VERSION: str = "6.0.0"
BUILD_VERSION: int = 53

# ── Directorio base del proyecto ─────────────────────────────────────────────
BASE_DIR: Path = Path(__file__).resolve().parent.parent

logger = logging.getLogger(__name__)

# ── Lista canónica de países VPN (compartida con vpn_manager_windows.py) ─────
_VALID_VPN_COUNTRIES: Set[str] = {
    "United_States", "United_Kingdom", "Germany", "France", "Spain",
    "Netherlands", "Switzerland", "Sweden", "Norway", "Denmark",
    "Finland", "Austria", "Belgium", "Italy", "Canada", "Australia",
    "Japan", "Singapore", "Hong_Kong", "Poland", "Czech_Republic",
    "Hungary", "Portugal", "Romania", "Bulgaria", "Croatia",
    "Slovakia", "Slovenia", "Estonia", "Latvia", "Lithuania",
}


class _CommaAwareDotEnvSource(DotEnvSettingsSource):
    """
    Custom DotEnvSettingsSource that handles comma-separated strings
    for List[str] fields without crashing on non-JSON values.

    pydantic-settings v2 calls json.loads() on every 'complex' field
    (List, Dict, etc.) inside decode_complex_value(). For .env values
    like VPN_COUNTRIES=Spain,Germany,France this raises JSONDecodeError
    which pydantic-settings wraps in SettingsError — crashing BEFORE
    any model_validator can run.

    This subclass overrides decode_complex_value() to fall back to
    comma-splitting instead of hard-failing on non-JSON strings.
    """
    def decode_complex_value(
        self, field_name: str, field_info: object, value: object
    ) -> object:
        import json as _json
        if not isinstance(value, str):
            return value
        value = value.strip()
        # Try JSON first (handles ["Spain","Germany"] format)
        try:
            return _json.loads(value)
        except _json.JSONDecodeError:
            pass
        # Fallback: comma-separated string → list
        # Applies to VPN_COUNTRIES and ENABLED_LANGUAGES
        if "," in value:
            return [item.strip() for item in value.split(",") if item.strip()]
        # Single value: wrap in list for List[str] fields
        return [value] if value else []



class _CommaAwareEnvSource(EnvSettingsSource):
    """
    Custom EnvSettingsSource that handles comma-separated strings for
    List[str] fields read from OS environment variables (os.environ).

    Required because _CommaAwareDotEnvSource only covers .env file reads.
    When tests use monkeypatch.setenv() or production uses OS env vars,
    pydantic-settings routes those through EnvSettingsSource which also
    calls json.loads() on List fields — failing on 'Spain,Germany,France'.

    BUG-TEST-005 fix: cover both sources with comma-aware decode logic.
    """
    def decode_complex_value(
        self, field_name: str, field_info: object, value: object
    ) -> object:
        import json as _json
        if not isinstance(value, str):
            return value
        value = value.strip()
        try:
            return _json.loads(value)
        except _json.JSONDecodeError:
            pass
        if "," in value:
            return [item.strip() for item in value.split(",") if item.strip()]
        return [value] if value else []


class Settings(BaseSettings):
    """
    Configuración de la aplicación cargada desde variables de entorno / .env.
    La construcción de la URL de base de datos es LAZY (cached_property) para
    evitar fallos en tiempo de importación (fix BUG-001 / SCRAP-BUG-004).
    """

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ── Identidad ─────────────────────────────────────────────────────────────
    APP_VERSION: str = APP_VERSION
    BUILD_VERSION: int = BUILD_VERSION
    APP_NAME: str = "BookingScraper Pro"
    DEBUG: bool = False

    # ── Seguridad (SCRAP-SEC-001) ─────────────────────────────────────────────
    SECRET_KEY: Optional[str] = None
    API_KEY: str = Field(default="")
    REQUIRE_API_KEY: bool = False

    # ── Base de datos (lazy — sin construcción de URL en import) ──────────────
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "bookingscraper"
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_POOL_SIZE: int = Field(default=10, ge=1, le=50)
    DB_MAX_OVERFLOW: int = Field(default=5, ge=0, le=20)
    DB_POOL_TIMEOUT: int = Field(default=30, ge=5, le=120)
    DB_POOL_RECYCLE: int = Field(default=3600, ge=60)

    # ── Redis ─────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = Field(default=20, ge=5, le=100)

    # ── Celery ────────────────────────────────────────────────────────────────
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # ── Scraper ───────────────────────────────────────────────────────────────
    SCRAPER_MAX_WORKERS: int = Field(default=2, ge=1, le=4)
    SCRAPER_REQUEST_TIMEOUT: int = Field(default=30, ge=5, le=120)
    SCRAPER_RETRY_DELAY: float = Field(default=2.0, ge=0.5, le=30.0)
    MAX_RETRIES: int = Field(default=3, ge=1, le=10)
    MAX_LANG_RETRIES: int = Field(default=3, ge=1, le=10)

    # ── VPN ───────────────────────────────────────────────────────────────────
    VPN_ENABLED: bool = False
    VPN_COUNTRIES: List[str] = Field(default_factory=lambda: ["Spain", "Germany", "France"])
    VPN_ROTATION_INTERVAL: int = Field(default=300, ge=30, le=3600)

    # ── Browser / Selenium ────────────────────────────────────────────────────
    # HEADLESS_BROWSER=False  → ventana visible (modo test/debug)
    # HEADLESS_BROWSER=True   → sin ventana (produccion/servidor)
    HEADLESS_BROWSER: bool = True

    # ── Idiomas ───────────────────────────────────────────────────────────────
    ENABLED_LANGUAGES: List[str] = Field(
        default_factory=lambda: ["es", "en", "de", "fr", "it", "nl", "pt"]
    )

    # ── Rutas (estructura REAL del proyecto) ─────────────────────────────────
    # Logs de aplicación → BASE_DIR/logs/
    LOGS_DIR: Path = BASE_DIR / "logs"
    LOGS_DEBUG_DIR: Path = BASE_DIR / "logs" / "debug"
    # Datos generados → BASE_DIR/data/
    IMAGES_DIR: Path = BASE_DIR / "data" / "images"
    EXPORT_DIR: Path = BASE_DIR / "data" / "exports"
    # HTML debug del scraper → BASE_DIR/data/logs/debug/
    DEBUG_HTML_DIR: Path = BASE_DIR / "data" / "logs" / "debug"
    # Backups → BASE_DIR/backups/
    BACKUPS_DIR: Path = BASE_DIR / "backups"

    # ── Logging ───────────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_MAX_BYTES: int = Field(default=10_485_760, ge=1_048_576)
    LOG_BACKUP_COUNT: int = Field(default=5, ge=1, le=20)

    # ── Debug ─────────────────────────────────────────────────────────────────
    DEBUG_HTML_SAVE: bool = False
    DEBUG_HTML_MAX_AGE_HOURS: int = 24   # BUG-014: validado en field_validator
    MAX_ERROR_LEN: int = 2000
    CSV_MAX_FILE_MB: int = Field(default=10, ge=1, le=100)
    STMT_TIMEOUT_OLAP_MS: int = Field(default=30_000, ge=1_000, le=300_000)

    # ── Mapeo de extensiones de idioma (Booking.com) ──────────────────────────
    LANGUAGE_EXT: Dict[str, str] = Field(
        default_factory=lambda: {
            "es": "es", "en": "en-gb", "de": "de", "fr": "fr",
            "it": "it", "nl": "nl", "pt": "pt-pt", "ru": "ru",
            "zh": "zh-cn", "ja": "ja", "ko": "ko", "pl": "pl",
            "cs": "cs", "hu": "hu", "sv": "sv", "da": "da",
            "fi": "fi", "nb": "nb", "ro": "ro", "el": "el",
            "tr": "tr", "ar": "ar",
        }
    )

    # ── XPaths de Booking.com ─────────────────────────────────────────────────
    XPATHS: Dict[str, str] = Field(
        default_factory=lambda: {
            "hotel_name":  '//h2[@data-testid="title"]',
            "rating":      '//div[@data-testid="review-score"]',
            "address":     '//span[@data-testid="address"]',
            "description": '//div[@data-testid="property-description"]',
        }
    )

    # ── ClassVar (no son campos de settings) ─────────────────────────────────
    _VALID_ISO_639_1: ClassVar[Set[str]] = {
        "af", "sq", "ar", "be", "bg", "ca", "cs", "cy", "da", "de",
        "el", "en", "eo", "es", "et", "eu", "fa", "fi", "fo", "fr",
        "ga", "gl", "gu", "he", "hi", "hr", "hu", "hy", "id", "is",
        "it", "ja", "ka", "kn", "ko", "lt", "lv", "mk", "ml", "mr",
        "ms", "mt", "nb", "ne", "nl", "no", "pl", "pt", "rm", "ro",
        "ru", "sk", "sl", "sq", "sr", "sv", "sw", "ta", "te", "th",
        "tl", "tr", "uk", "ur", "uz", "vi", "yi", "zh",
    }

    # =========================================================================
    # Validators
    # =========================================================================

    @field_validator("DEBUG_HTML_MAX_AGE_HOURS", mode="before")
    @classmethod
    def _parse_age_hours(cls, v: object) -> int:
        """BUG-014: conversión segura a int — no lanza ValueError si es string inválido."""
        try:
            return int(v)
        except (ValueError, TypeError):
            logger.warning(
                "DEBUG_HTML_MAX_AGE_HOURS='%s' no es un entero válido; usando 24h por defecto.", v
            )
            return 24

    @model_validator(mode="before")
    @classmethod
    def _parse_list_env_vars(cls, data: object) -> object:
        """
        FIX DEFINITIVO para pydantic-settings v2 con campos List[str].

        pydantic-settings lee el .env y pasa los valores como strings CRUDOS
        al validador de tipos de pydantic-core. Para List[str], pydantic-core
        intenta JSON.parse("Spain,Germany,France") → falla porque no es JSON.
        field_validator(mode="before") NO intercepta esto — el crash ocurre
        antes, en la capa de pydantic-settings.

        model_validator(mode="before") SÍ intercepta los datos RAW antes de
        cualquier coerción de tipos, convirtiendo:
          "Spain,Germany,France"    → ["Spain", "Germany", "France"]
          '["Spain","Germany"]'     → ["Spain", "Germany"]
          ["Spain", "Germany"]      → sin cambios
        """
        import json as _json
        if not isinstance(data, dict):
            return data
        for key in ("VPN_COUNTRIES", "ENABLED_LANGUAGES"):
            val = data.get(key)
            if val is None or isinstance(val, list):
                continue
            if isinstance(val, str):
                val = val.strip()
                if val.startswith("["):
                    try:
                        data[key] = [str(i).strip() for i in _json.loads(val) if str(i).strip()]
                        continue
                    except _json.JSONDecodeError:
                        pass
                # Formato habitual .env: Spain,Germany,France
                data[key] = [item.strip() for item in val.split(",") if item.strip()]
        return data

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def _validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        val = str(v).upper()
        if val not in allowed:
            raise ValueError(f"LOG_LEVEL debe ser uno de {allowed}, recibido: '{v}'")
        return val

    @model_validator(mode="after")
    def _post_validate(self) -> "Settings":
        """
        Validación post-instanciación.
        Se ejecuta DESPUÉS de establecer todos los campos — seguro contra crashes en import.
        """
        # SECRET_KEY (SCRAP-SEC-001)
        insecure = {"change-this-to-a-random-secret-key", "", None}
        if self.SECRET_KEY in insecure:
            generated = secrets.token_urlsafe(48)
            object.__setattr__(self, "SECRET_KEY", generated)
            logger.critical(
                "SECRET_KEY no configurada o usa valor inseguro. "
                "Se ha generado una clave aleatoria SÓLO para esta sesión. "
                "Copia esta clave en tu .env: %s", generated,
            )

        # API_KEY (SCRAP-SEC-002)
        if self.REQUIRE_API_KEY and not self.API_KEY:
            raise ValueError(
                "REQUIRE_API_KEY=true pero API_KEY no está configurada. "
                "Añade API_KEY en tu archivo .env."
            )

        # ENABLED_LANGUAGES (BUG-005: validado una sola vez aquí, no por llamada)
        invalid_langs = [l for l in self.ENABLED_LANGUAGES if l not in self._VALID_ISO_639_1]
        if invalid_langs:
            raise ValueError(f"ENABLED_LANGUAGES contiene códigos ISO 639-1 inválidos: {invalid_langs}")

        # LANGUAGE_EXT vs ENABLED_LANGUAGES (BUG-017)
        missing_ext = [l for l in self.ENABLED_LANGUAGES if l not in self.LANGUAGE_EXT]
        if missing_ext:
            logger.warning(
                "LANGUAGE_EXT no tiene mapeo para: %s — se usará el código ISO directamente.",
                missing_ext,
            )
            for lang in missing_ext:
                self.LANGUAGE_EXT[lang] = lang

        # VPN_COUNTRIES (BUG-009)
        invalid_vpn = [c for c in self.VPN_COUNTRIES if c not in _VALID_VPN_COUNTRIES]
        if invalid_vpn:
            raise ValueError(
                f"VPN_COUNTRIES contiene países inválidos: {invalid_vpn}. "
                f"Opciones válidas: {sorted(_VALID_VPN_COUNTRIES)}"
            )

        # Crear directorios en tiempo de ejecución (nunca en import)
        for d in (
            self.LOGS_DIR, self.LOGS_DEBUG_DIR,
            self.IMAGES_DIR, self.EXPORT_DIR,
            self.DEBUG_HTML_DIR, self.BACKUPS_DIR,
        ):
            try:
                d.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                logger.warning("No se pudo crear el directorio %s: %s", d, exc)

        return self

    # =========================================================================
    # Properties
    # =========================================================================

    @cached_property
    def database_url(self) -> str:
        """
        URL de conexión psycopg v3 — LAZY (BUG-001 / SCRAP-BUG-004).
        Solo se evalúa cuando se accede, nunca en tiempo de importación.
        """
        if not self.DB_USER:
            raise ValueError("DB_USER no está configurado. Añádelo a tu archivo .env.")
        if not self.DB_PASSWORD:
            raise ValueError("DB_PASSWORD no está configurado. Añádelo a tu archivo .env.")
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @cached_property
    def database_url_sync(self) -> str:
        """URL psycopg2 para Alembic en modo offline."""
        if not self.DB_USER or not self.DB_PASSWORD:
            raise ValueError("DB_USER y DB_PASSWORD son necesarios.")
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    def get_language_ext(self, lang_code: str) -> str:
        """Devuelve la extensión de Booking.com para un código ISO 639-1."""
        return self.LANGUAGE_EXT.get(lang_code, lang_code)


    @classmethod
    def settings_customise_sources(cls, settings_cls: type, **kwargs: object) -> tuple:
        """
        Reemplaza DotEnvSettingsSource por nuestra versión que acepta
        listas separadas por comas (VPN_COUNTRIES=Spain,Germany,France).

        Se usa **kwargs para ser compatible con CUALQUIER versión de
        pydantic-settings (2.5, 2.6, 2.7, 2.8) — la firma del método
        varía entre versiones (secrets_dir → file_secret_settings).

        Pipeline de prioridad (mismo que pydantic-settings por defecto):
          1. init_settings   — valores pasados directamente a Settings()
          2. env_settings    — variables de entorno del sistema (os.environ)
          3. dotenv custom   — archivo .env con soporte para comas
        """
        init_settings    = kwargs.get("init_settings")
        env_settings     = kwargs.get("env_settings")
        dotenv_settings  = kwargs.get("dotenv_settings")

        if dotenv_settings is None:
            # Fallback: pydantic-settings API no reconocida — usar defaults
            return super().settings_customise_sources(settings_cls, **kwargs)

        # Construir nuestra fuente personalizada con los mismos parámetros
        # que el dotenv original (env_file, encoding, etc.)
        env_file = getattr(dotenv_settings, "env_file", None)
        env_enc  = getattr(dotenv_settings, "env_file_encoding", "utf-8")
        try:
            custom_dotenv = _CommaAwareDotEnvSource(
                settings_cls,
                env_file=env_file,
                env_file_encoding=env_enc,
            )
        except TypeError:
            # Fallback por si la firma del constructor cambia
            custom_dotenv = _CommaAwareDotEnvSource(settings_cls)

        # BUG-TEST-005: wrap env_settings with comma-aware decoder
        try:
            comma_env = _CommaAwareEnvSource(settings_cls)
        except Exception:
            comma_env = env_settings
        return (init_settings, comma_env, custom_dotenv)


# ── Singleton ─────────────────────────────────────────────────────────────────
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """Devuelve el singleton de Settings. Thread-safe para acceso de solo lectura."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance


def reset_settings() -> None:
    """Fuerza la re-instanciación de settings (útil en tests)."""
    global _settings_instance
    _settings_instance = None
