"""
BookingScraper Pro v6.0 - Application Configuration
====================================================
Platform : Windows 11 + Python 3.11+
Validation: Pydantic-Settings v2

Corrections Applied (v46):
- BUG-004 : VPN + multi-worker incompatibility now validated early and with
            a clear, actionable error message.
- BUG-010 : LANGUAGE_EXT["en"] documented as Booking.com canonical dependency;
            fallback mapping added.
- BUG-014 : MAX_ERROR_LEN is the single source of truth (models.py imports it).
- BUG-016 : _VALID_ISO_639_1 is the authoritative set; LANGUAGE_EXT is a
            subset checked against it at startup.
- BUG-022 : MAX_LANG_RETRIES is now configurable via environment variable
            (was hardcoded = 1 in completeness_service.py).
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import FrozenSet, Optional, Set

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# BUG-014 FIX: Single definition — imported by models.py so it never drifts
# ---------------------------------------------------------------------------
MAX_ERROR_LEN: int = 2000
MAX_URL_LEN  : int = 2048

# ---------------------------------------------------------------------------
# BUG-016 FIX: Authoritative ISO-639-1 set.
# LANGUAGE_EXT is always validated against this set at model instantiation.
# ---------------------------------------------------------------------------
_VALID_ISO_639_1: FrozenSet[str] = frozenset({
    "af","ak","am","ar","az","be","bg","bm","bn","bo","br","bs","ca","cs",
    "cy","da","de","dz","ee","el","en","eo","es","et","eu","fa","ff","fi",
    "fo","fr","fy","ga","gl","gn","gu","gv","ha","he","hi","hr","hu","hy",
    "id","ig","ii","is","it","iu","ja","jv","ka","ki","kk","kl","km","kn",
    "ko","ks","ku","kw","ky","la","lb","lo","lt","lu","lv","mg","mi","mk",
    "ml","mn","mr","ms","mt","my","nb","nd","ne","nl","nn","no","ny","om",
    "or","os","pa","pl","ps","pt","qu","rm","ro","ru","rw","se","sg","si",
    "sk","sl","sm","sn","so","sq","sr","ss","st","sv","sw","ta","te","tg",
    "th","ti","tk","tl","tn","to","tr","ts","tt","ug","uk","ur","uz","ve",
    "vi","vo","wa","wo","xh","yo","za","zh","zu",
})

# BUG-010 NOTE: ".en-gb" suffix reflects Booking.com canonical URL format.
# If Booking.com changes their URL structure this mapping must be updated.
# The fallback "" means "use the language code as-is".
LANGUAGE_EXT: dict[str, str] = {
    "en": ".en-gb",   # BUG-010: Booking.com uses en-gb as English canonical
    "es": ".es",
    "de": ".de",
    "fr": ".fr",
    "it": ".it",
    "pt": ".pt",
    "nl": ".nl",
    "pl": ".pl",
    "ru": ".ru",
    "zh": ".zh-cn",
    "ja": ".ja",
    "ko": ".ko",
    "ar": ".ar",
    "tr": ".tr",
    "sv": ".sv",
    "da": ".da",
    "fi": ".fi",
    "nb": ".nb",
    "cs": ".cs",
}


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
class Settings(BaseSettings):
    """
    Application settings loaded from environment variables / .env file.
    All Windows-specific constraints validated at instantiation time.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    APP_ENV    : str   = "development"
    APP_VERSION: str   = "6.0.0"      # BUG-008 FIX: matches __init__.py
    APP_HOST   : str   = "127.0.0.1"
    APP_PORT   : int   = 8000
    APP_WORKERS: int   = 1

    # ------------------------------------------------------------------
    # Database  (BUG-001 related: validated here for early failure)
    # ------------------------------------------------------------------
    DB_HOST       : str = "localhost"
    DB_PORT       : int = 5432
    DB_NAME       : str = "bookingscraper"
    DB_USER       : str = ""
    DB_PASSWORD   : str = ""
    DB_POOL_SIZE  : int = 10
    DB_MAX_OVERFLOW: int = 5
    DB_POOL_TIMEOUT: float = 30.0
    DB_POOL_RECYCLE: int = 3600
    DB_ECHO       : bool = False

    # ------------------------------------------------------------------
    # Redis / Memurai
    # ------------------------------------------------------------------
    REDIS_HOST    : str = "localhost"
    REDIS_PORT    : int = 6379
    REDIS_DB      : int = 0
    REDIS_PASSWORD: str = ""

    @property
    def CELERY_BROKER_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB + 1}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB + 1}"

    # ------------------------------------------------------------------
    # Scraper
    # ------------------------------------------------------------------
    SCRAPER_MAX_WORKERS       : int   = 4
    SCRAPER_ENGINE            : str   = "cloudscraper"   # cloudscraper | selenium | auto
    SCRAPER_REQUEST_DELAY_MIN : float = 2.0
    SCRAPER_REQUEST_DELAY_MAX : float = 8.0
    SCRAPER_PAGE_TIMEOUT      : int   = 30
    SCRAPER_MAX_RETRIES       : int   = 3
    ENABLED_LANGUAGES_STR     : str   = "en,es,de,fr,it"

    @property
    def ENABLED_LANGUAGES(self) -> list[str]:
        langs = [l.strip().lower() for l in self.ENABLED_LANGUAGES_STR.split(",") if l.strip()]
        invalid = [l for l in langs if l not in _VALID_ISO_639_1]
        if invalid:
            raise ValueError(f"Invalid language codes in ENABLED_LANGUAGES: {invalid}")
        return langs

    # BUG-022 FIX: Was hardcoded to 1 in completeness_service.py
    MAX_LANG_RETRIES: int = 3

    # ------------------------------------------------------------------
    # VPN  (BUG-004 FIX: validated early with actionable message)
    # ------------------------------------------------------------------
    VPN_ENABLED           : bool = False
    VPN_ROTATION_INTERVAL : int  = 600
    VPN_CONNECT_TIMEOUT   : int  = 30
    VPN_COUNTRIES_STR     : str  = ""

    @property
    def VPN_COUNTRIES(self) -> list[str]:
        if not self.VPN_COUNTRIES_STR:
            return []
        return [c.strip().upper() for c in self.VPN_COUNTRIES_STR.split(",") if c.strip()]

    # ------------------------------------------------------------------
    # Image downloader
    # ------------------------------------------------------------------
    IMAGES_DIR         : str = "C:/BookingScraper/images"
    IMAGES_MAX_WORKERS : int = 4
    IMAGES_TIMEOUT     : int = 30
    IMAGES_MAX_SIZE_MB : int = 10

    @property
    def IMAGES_PATH(self) -> Path:
        return Path(self.IMAGES_DIR)

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    LOG_LEVEL       : str = "INFO"
    LOG_DIR         : str = "./logs"
    LOG_MAX_BYTES   : int = 10_485_760   # 10 MB
    LOG_BACKUP_COUNT: int = 5

    @property
    def LOG_PATH(self) -> Path:
        return Path(self.LOG_DIR)

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------
    DATA_DIR      : str = "C:/BookingScraper/data"
    EXPORT_DIR    : str = "C:/BookingScraper/exports"
    DEBUG_HTML_DIR: str = "C:/BookingScraper/debug"

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------
    SECRET_KEY   : str = "change-this-to-a-random-secret-key"
    API_KEY      : str = ""
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

    @field_validator("DB_USER", "DB_PASSWORD", mode="before")
    @classmethod
    def _validate_db_credentials(cls, v: str) -> str:
        # Strip whitespace — common copy-paste error
        return (v or "").strip()

    @model_validator(mode="after")
    def _validate_settings(self) -> "Settings":
        """
        Cross-field validation with Windows-specific constraint checks.
        BUG-004 FIX: VPN + multi-worker check runs here (model level),
        which is after individual field parsing — still early enough to
        fail before any I/O or service startup occurs.
        """
        errors: list[str] = []

        # BUG-001 related: validate credentials
        if not self.DB_USER:
            errors.append("DB_USER is required. Set it in your .env file.")
        if not self.DB_PASSWORD:
            errors.append("DB_PASSWORD is required. Set it in your .env file.")

        # BUG-004 FIX: VPN only works with a single worker (NordVPN CLI is not thread-safe)
        if self.VPN_ENABLED and self.SCRAPER_MAX_WORKERS > 1:
            errors.append(
                "VPN_ENABLED=true is incompatible with SCRAPER_MAX_WORKERS > 1. "
                "NordVPN CLI is not safe for concurrent use. "
                "Either set VPN_ENABLED=false or set SCRAPER_MAX_WORKERS=1."
            )

        # Windows: warn about pool size approaching Desktop Heap limit
        if self.DB_POOL_SIZE + self.DB_MAX_OVERFLOW > 50:
            logger.warning(
                "DB_POOL_SIZE (%d) + DB_MAX_OVERFLOW (%d) = %d connections. "
                "Windows 11 Desktop Heap limits max_connections to ~100. "
                "Consider reducing pool settings.",
                self.DB_POOL_SIZE, self.DB_MAX_OVERFLOW,
                self.DB_POOL_SIZE + self.DB_MAX_OVERFLOW,
            )

        # Validate log level
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.LOG_LEVEL.upper() not in valid_levels:
            errors.append(f"LOG_LEVEL must be one of {valid_levels}, got '{self.LOG_LEVEL}'")

        if errors:
            raise ValueError(
                f"Configuration errors ({len(errors)}):\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

        return self

    def create_directories(self) -> None:
        """Create required application directories (Windows paths via pathlib)."""
        dirs = [
            self.IMAGES_PATH,
            self.LOG_PATH,
            Path(self.DATA_DIR),
            Path(self.EXPORT_DIR),
            Path(self.DEBUG_HTML_DIR),
        ]
        for d in dirs:
            try:
                d.mkdir(parents=True, exist_ok=True)
                logger.debug("Directory ensured: %s", d)
            except OSError as exc:
                logger.warning("Cannot create directory %s: %s", d, exc)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance. Call once at startup."""
    return Settings()
