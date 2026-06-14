# =============================================================================
# app/scraper.py — BookingScraper Pro v6.0.0 Build 123
# =============================================================================
# BUILD 123 — BUG-GALLERY-OPEN-ALL-LANGS-001-FIX
#   Root cause: _open_gallery() was called unconditionally for all 6 languages
#   inside _fetch_with_selenium(). The function clicks the gallery hero image,
#   triggering Cloudflare JS fingerprinting on every non-EN language pass.
#   Its return value was discarded for non-EN. No useful data was produced.
#   Evidence: 92/121 gallery challenge events in the 2026-06-12 session
#   (12h log) were from non-EN languages (es, de, it, fr, pt).
#   Fix: _open_gallery() moved inside the "if lang == 'en'" block alongside
#   _capture_gallery_modal(). _extract_hotel_photos_js() remains unconditional
#   — it reads the hotelPhotos JS variable at page load, independent of gallery
#   state, and discarding its call would lose photo count logging for non-EN.
#
# BUILD 123 — BUG-USER-AGENT-STALE-001-FIX
#   Root cause: User-Agent hardcoded to Chrome/131.0.0.0 while the actual
#   ChromeDriver in production is 149.0.7827.115 (confirmed in all 2026-06-12
#   log entries). The 18-major-version gap between the spoofed UA (131) and
#   the real CDP-reported version (149) is a strong Cloudflare bot signal.
#   Fix: Updated static UA string from Chrome/131 to Chrome/149.
#   Long-term improvement: read Brave version at runtime via webdriver_manager
#   and inject the correct UA dynamically.
#
# BUILD 117 — BUG-CHROMEDRIVER-001-FIX
#   Root cause: CHROMEDRIVER_PATH apuntaba a un binario fijo de ChromeDriver
#   mientras Brave Browser se auto-actualizaba a versiones más nuevas
#   (e.g. ChromeDriver 145 vs Brave 147). La desincronización causaba
#   SessionNotCreatedException en TODOS los intentos de apertura de browser.
#   El error se propagaba como "All scraping engines failed" bloqueando
#   el 100% de los scrapes.
#
#   Fix: _get_driver() ahora intenta 3 estrategias en orden:
#     1. CHROMEDRIVER_PATH en .env (comportamiento legacy — prioridad máxima,
#        permite uso offline).
#     2. webdriver-manager con ChromeType.BRAVE — detecta la versión instalada
#        de Brave y descarga el ChromeDriver compatible automáticamente.
#     3. webdriver.Chrome() sin service — fallback para entornos con ChromeDriver
#        en PATH del sistema.
#   La estrategia 2 requiere: pip install webdriver-manager>=4.0.0
#   (añadido a requirements.txt como dependencia OBLIGATORIA en Build 117).
#   NOTA: la primera ejecución con webdriver-manager requiere acceso a internet
#   para descargar el ChromeDriver. Las ejecuciones subsiguientes usan la caché
#   local (~/.wdm/).
# BUILD 116 — NAV-TIMEOUT-001-FIX
#   Root cause: driver.get(url) can block indefinitely when Booking.com/
#   Cloudflare serve a challenge page that loads instantly (bypassing the
#   TimeoutException path) but then enters an infinite JS loop. window.stop()
#   is called via execute_script() — which also blocks if Brave is frozen.
#   This was the mechanism behind INC-2026-0602-BROWSER-FREEZE-001: the gallery
#   click triggered a chal_t= redirect, and the subsequent navigation to
#   vidimo-se.en-gb.html froze in the 4-second gap between the last log entry
#   and the watchdog kill.
#   Fix: wrap driver.get(url) in a daemon threading.Thread with join(
#   NAVIGATION_TIMEOUT_S=45). On timeout, window.stop() is attempted (best-
#   effort) and None is returned so the language pass fails cleanly for retry.
#
# BUILD 106 — BUG-EN-LAZY-001-FIX
#   Root cause: 7 hotels show EN-only empty service_category values while all
#   other languages (es, de, fr, it, pt) extract 40-150 services with proper
#   categories.  IntersectionObserver lazy-loading for facility-group-container
#   did not fire within the original single 15-second wait for the English page.
#
#   Fix A — _expand_facilities() Strategy 4 (multi-scroll retry loop):
#     Replaced single 15-second WebDriverWait with a 3-attempt retry loop
#     (3 × 8 s = 24 s max).  Each retry:
#       (i)  Re-scrolls the facility container into view.
#       (ii) Re-dispatches the synthetic scroll event.
#       (iii) Waits 8 s for facility-group-container to appear.
#
#   Fix B — Pre-scroll in _fetch_with_selenium():
#     Added full-page bottom scroll BEFORE facility scroll.  This warms ALL
#     IntersectionObservers on the page simultaneously, improving the
#     probability that the facility observer fires on the first attempt.
#
# BUILD 98 — BUG-EXTRACT-IT-001-FIX
#   Root cause: _fetch_with_selenium() iteraba 4 selectores CSS secuencialmente,
#   cada uno con su propio WebDriverWait(content_wait_s). Si los 3 primeros
#   selectores no coincidían (caso habitual en páginas IT, DE, FR que usan
#   h1.pp-header__title), cada timeout acumulaba content_wait_s (default 10 s)
#   antes de probar el siguiente → latencia observada 15–75 s (outliers >120 s).
#
#   Fix: reemplazar el bucle for con un único WebDriverWait usando EC.any_of()
#   que dispara en paralelo todos los selectores. Si CUALQUIERA aparece antes
#   de content_wait_s, se resuelve inmediatamente.
#   Peor caso anterior: 4 × 10 s = 40 s
#   Peor caso nuevo:    1 × 10 s = 10 s  (reducción 75%)
#
#   EC.any_of() disponible desde selenium >= 4.0 (proyecto usa >= 4.27.0).
#
# BUILD 70 — BUG-VPN-006-FIX
#   Root cause: NordVPN GUI opens the system DEFAULT browser (Brave) for
#   OAuth re-auth or help pages. When Selenium also uses Brave, both share
#   the same user profile → NordVPN's browser tabs appear inside the Selenium-
#   controlled window, corrupting the scraping session.
#
#   Fix: Selenium Brave now uses a dedicated isolated profile at
#   SELENIUM_BRAVE_PROFILE_DIR (config field, default: data/brave_profile).
#   NordVPN opens the system Brave with its DEFAULT profile (different path)
#   → tabs opened by NordVPN go to a SEPARATE Brave process, never touching
#   the Selenium-controlled instance.
#
#   Additional flags to prevent the Selenium Brave from loading external content:
#     --no-default-browser-check  : prevents first-run browser prompt
#     --disable-default-apps      : disables preloaded app shortcuts
#     --no-first-run              : skips first-run setup
#
# BUILD 75 — BUG-URL-001-FIX: Correct Booking.com URL format
#   Root cause: build_language_url() generated .html?lang=en-gb
#   Correct format confirmed from canonical URLs in pruebas/ HTML files:
#     .en-gb.html?lang=en-gb  (language code embedded in filename)
#   Impact: Booking.com serves a 301 redirect from the old format to the
#   canonical URL. Selenium follows the redirect but loses the Accept-Language
#   header set via CDP, causing occasional language mismatches. Direct
#   canonical URL avoids the redirect entirely.
#   Fix: build_language_url() now embeds lang_code in .html filename.
#
# BUILD 74 — SIMPLIFICATION: remove isolated Brave profile
#   SELENIUM_BRAVE_PROFILE_DIR removed. Brave uses its default system profile.
#   This was the behaviour before Build 70 and it worked correctly.
#   Since Brave is used EXCLUSIVELY by this application:
#     - No conflict with NordVPN browser tabs (handled by _enforce_single_tab)
#     - No stale profile accumulation (system profile is stable)
#     - No DevToolsActivePort timeout (default profile = instant startup)
#   Removed: _prepare_fresh_profile(), --user-data-dir, --bwsi
#   Kept:    _enforce_single_tab(), anti-hang flags, pywin32 popup dismiss
#
# BUILD 73 — BUG-BRAVE-001-FIX (superseded by BUILD 74)
#   Root cause: --user-data-dir=data/brave_profile (Build 70 BUG-VPN-006-FIX)
#   causes Brave to accumulate profile state across sessions. On next startup,
#   Brave processes stale profile data (Preferences, Local State, cache) and
#   takes 60+ seconds to initialize → ChromeDriver DevTools timeout →
#   "DevToolsActivePort file doesn't exist" on 100% of attempts.
#   Fix: _prepare_fresh_profile() wipes data/brave_profile completely before
#   every webdriver.Chrome() call. Fresh empty profile = instant Brave startup.
#   Additional anti-hang flags added to _build_chrome_options().
#
# BUILD 72 — BUG-SCRAPER-OS-001-FIX (preserved)
# BUILD 71 — BUG-VPN-007-FIX
#   Root cause: reset_browser() calls driver.quit() during VPN rotation, which
#   kills the Brave process but leaves behind a Chromium SingletonLock file in
#   data/brave_profile/. The next _get_driver() call finds the lock and Brave
#   exits immediately → "session not created: DevToolsActivePort file doesn't
#   exist". Observed: 192 consecutive SessionNotCreatedException errors in the
#   Build 70 production log.
#   Fix: _clear_profile_singletons() removes SingletonLock, SingletonSocket,
#   and SingletonCookie from the profile dir before every webdriver.Chrome()
#   instantiation. Called from _get_driver() when self._driver is None.
#
# BUILD 67 — BUG-SCRAPER-001-FIX (preserved)
# BUILD 64 — BUG-PERF-001-FIX (preserved)
# BUILD 63 — CLOUDSCRAPER ELIMINATED (preserved)
# BUILD 62 — BUG-LANG-002-FIX (preserved)
# BUILD 61 — BUG-LANG-001-FIX (preserved)
# =============================================================================

from __future__ import annotations

import hashlib
import logging
import os
import re
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.config import get_settings

logger = logging.getLogger(__name__)

# =============================================================================
# CONSTANTS
# =============================================================================

# ISO 639-1 → Booking.com URL language suffix
LANG_URL_MAP: dict[str, str] = {
    "en": "en-gb",
    "es": "es",
    "de": "de",
    "fr": "fr",
    "it": "it",
    "pt": "pt-pt",
    "nl": "nl",
    "pl": "pl",
    "ru": "ru",
    "zh": "zh-cn",
    "ja": "ja",
    "ko": "ko",
}

# ISO 639-1 → Accept-Language header value (BUG-LANG-002 fix)
LANG_TO_ACCEPT_LANGUAGE: dict[str, str] = {
    "en": "en-GB,en;q=0.9,en-US;q=0.8",
    "es": "es-ES,es;q=0.9",
    "de": "de-DE,de;q=0.9",
    "fr": "fr-FR,fr;q=0.9",
    "it": "it-IT,it;q=0.9",
    "pt": "pt-PT,pt;q=0.9,pt-BR;q=0.8",
    "nl": "nl-NL,nl;q=0.9",
    "pl": "pl-PL,pl;q=0.9",
    "ru": "ru-RU,ru;q=0.9",
    "zh": "zh-CN,zh;q=0.9",
    "ja": "ja-JP,ja;q=0.9",
    "ko": "ko-KR,ko;q=0.9",
}

# Minimum bytes expected from a real Booking.com hotel page (150k–500k typical)
_SHORT_HTML_DEFAULT_THRESHOLD: int = 5_000

# Block page indicators detectable by Selenium (Cloudflare JS challenge
# and Booking.com anti-bot pages).
# BUG-SCRAPER-001-FIX (Build 67): Booking.com "Max challenge attempts exceeded"
# page was not in this list. driver.page_source after that page hangs 30+
# minutes because Booking.com JS keeps the browser in perpetual loading state.
_BLOCK_INDICATORS: tuple[str, ...] = (
    "just a moment",
    "checking your browser",
    "enable javascript and cookies",
    "ddos-guard",
    "access denied",
    "cf-browser-verification",
    "ray id",
    # Booking.com anti-bot challenge pages (BUG-SCRAPER-001-FIX)
    "max challenge attempts exceeded",
    "please refresh the page to try again",
    "security check to continue",
    "too many requests",
    # BUG-BLOCK-IND-002-FIX (Build 115): Cloudflare challenge variants that do
    # NOT use "just a moment" — appear on challenge pages with custom templates.
    "verifying your browser",
    "please wait while we verify",
    # "chal_t" may be embedded in the HTML source of challenge pages as a JS var
    # (distinct from the URL parameter — here it appears in page_source text).
    "chal_t",
)

# BUG-CHAL-DETECT-001-FIX (Build 114): parámetros de bot-detection en URL.
# Cuando Booking.com/Cloudflare detectan scraping, inyectan estos parámetros en
# la URL del redirect. La URL con chal_t= o force_referer= NO es cargable
# normalmente — genera una página de desafío o una carga indefinida.
# La URL del incidente INC-2026-0602-RADISSON-001:
#   radisson-graz.es.html?lang=es&chal_t=1780362976169&force_referer=#hp_facilities_box
# El parámetro force_referer indica redirección forzada; chal_t es el token
# de tiempo del desafío. Navegar a estas URLs con Selenium cuelga la carga.
_BOOKING_CHALLENGE_URL_PARAMS: tuple[str, ...] = (
    "chal_t=",
    "force_referer=",
    "challenged_by=",
)


def _url_has_challenge_params(url: str) -> bool:
    """
    BUG-CHAL-DETECT-001-FIX (Build 114):
    True si la URL contiene parámetros de bot-detection de Booking.com.
    Detecta chal_t=, force_referer=, challenged_by= que indican que
    Booking.com/Cloudflare ya ha marcado la sesión como bot.
    """
    url_lower = url.lower()
    return any(p in url_lower for p in _BOOKING_CHALLENGE_URL_PARAMS)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def build_language_url(base_url: str, lang: str) -> str:
    """
    Build a language-specific Booking.com URL.

    BUG-URL-001-FIX (Build 75): Booking.com canonical URL format embeds the
    language code directly in the HTML filename:
      Correct:  .../hotel-name.en-gb.html?lang=en-gb
      Previous: .../hotel-name.html?lang=en-gb   ← triggers 301 redirect

    Evidence: canonical URLs extracted from pruebas/ HTML files confirm the
    embedded format for all languages (de, en-gb, es, it, fr, pt-pt).

    The 301 redirect was causing Selenium to lose the CDP Accept-Language
    header set by BUG-LANG-002-FIX, occasionally producing language mismatches.

    Args:
        base_url: Base hotel URL (any format — with or without existing lang).
        lang:     ISO 639-1 language code (e.g. "de", "en").

    Returns:
        Canonical URL with lang code in filename + ?lang= query param.
    """
    lang_code = LANG_URL_MAP.get(lang, lang)
    url = base_url.rstrip("/")

    # Strip any existing query string
    if "?" in url:
        url = url.split("?")[0].rstrip("&")

    # Strip any existing embedded lang code: hotel.de.html → hotel.html
    # Pattern: .<lang_code>.html at end of path
    url = re.sub(r"\.[a-z]{2}(?:-[a-z]{2,4})?\.html$", ".html", url, flags=re.IGNORECASE)

    # Ensure base URL ends with .html (add if missing)
    if not url.lower().endswith(".html"):
        url = url + ".html"

    # Embed lang_code in filename: hotel.html → hotel.en-gb.html
    url = re.sub(r"\.html$", f".{lang_code}.html", url, flags=re.IGNORECASE)

    return f"{url}?lang={lang_code}"


def _is_blocked(html: str) -> bool:
    """Return True if HTML is a Cloudflare block/challenge page."""
    if not html:
        return True
    lower = html.lower()
    return any(indicator in lower for indicator in _BLOCK_INDICATORS)


def _is_hotel_page(html: str) -> bool:
    """Return True if HTML looks like a real Booking.com hotel page."""
    if not html or len(html) < 10_000:
        return False
    required = ("booking.com", "aggregateRating")
    return all(marker in html for marker in required)


def _detect_page_language(html: str) -> Optional[str]:
    """
    Extract the page language from Booking.com HTML.

    Checks (in order):
      1. <html lang="XX"> attribute
      2. <meta property="og:locale"> tag

    Returns the 2-letter ISO 639-1 code, or None if undetectable.
    """
    # Strategy 1: <html lang="...">
    m = re.search(r'<html[^>]+\blang=["\']([a-z]{2})', html, re.IGNORECASE)
    if m:
        return m.group(1).lower()

    # Strategy 2: og:locale meta
    m = re.search(
        r'property=["\']og:locale["\'][^>]+content=["\']([a-z]{2})',
        html,
        re.IGNORECASE,
    )
    if m:
        return m.group(1).lower()

    # Strategy 3: content-language meta
    m = re.search(
        r'http-equiv=["\']content-language["\'][^>]+content=["\']([a-z]{2})',
        html,
        re.IGNORECASE,
    )
    if m:
        return m.group(1).lower()

    return None


def _save_debug_html(html: str, url: str, tag: str) -> None:
    """
    Persist raw HTML to disk for post-mortem analysis.
    Only active when DEBUG_HTML_SAVE=true in config.
    """
    try:
        cfg = get_settings()
        if not getattr(cfg, "DEBUG_HTML_SAVE", False):
            return
        debug_dir = Path("data") / "debug_html"
        debug_dir.mkdir(parents=True, exist_ok=True)
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        path = debug_dir / f"{tag}_{url_hash}.html"
        path.write_text(html, encoding="utf-8", errors="replace")
        logger.debug("Debug HTML saved: %s (%d bytes)", path, len(html))
    except Exception as exc:
        logger.warning("_save_debug_html failed: %s", exc)


# =============================================================================
# SeleniumEngine — SOLE SCRAPING ENGINE (Build 63)
# =============================================================================

class SeleniumEngine:
    """
    Selenium/Brave WebDriver scraping engine.

    Build 63: Promoted to sole engine. CloudScraperEngine removed.
    Build 62: BUG-LANG-002 — _set_language_headers(), reset_browser().
    Build 61: BUG-LANG-001 — Short HTML fast-fail.

    Thread safety: all driver interactions are serialised via self._lock.
    One shared Brave instance per process; reset_browser() discards it
    after VPN rotation so the next call recreates it with a clean profile.
    """

    def __init__(self) -> None:
        self._driver: Optional[webdriver.Chrome] = None
        self._lock: threading.Lock = threading.Lock()
        self._cfg = get_settings()
        self._blocked_count: int = 0
        # Build 109: fotos visibles en galería capturadas en vivo durante el
        # pase EN, indexadas por URL para evitar carreras con max_workers>1.
        # scraper_service las recupera (y descarta) tras scrape().
        self._gallery_photos_by_url: Dict[str, List[Dict[str, Any]]] = {}

    # ── Driver lifecycle ──────────────────────────────────────────────────────

    def _build_chrome_options(self) -> webdriver.ChromeOptions:
        """Construct Chrome/Brave options with anti-detection settings."""
        cfg = self._cfg
        options = webdriver.ChromeOptions()

        brave_path: Optional[str] = getattr(cfg, "BRAVE_PATH", None)
        if brave_path:
            options.binary_location = brave_path

        headless: bool = getattr(cfg, "HEADLESS_BROWSER", False)
        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            # BUG-USER-AGENT-STALE-001-FIX (Build 123): updated from Chrome/131
            # to Chrome/149 to match the actual ChromeDriver version in use
            # (149.0.7827.115 confirmed in production logs 2026-06-12).
            # A UA mismatch between the Selenium header and the real browser
            # version reported via CDP is a strong Cloudflare bot-detection signal.
            "Chrome/149.0.0.0 Safari/537.36"
        )
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        options.add_experimental_option("useAutomationExtension", False)

        # Prevent first-run setup dialogs and default-browser prompts
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-default-apps")

        # ── BUG-BRAVE-001-FIX: Anti-initialization-hang flags (Build 73) ──────
        # Prevent Brave from spending time on network/sync/updates during startup.
        # Each of these can stall Brave initialization beyond ChromeDriver's 60s timeout.
        options.add_argument("--disable-component-update")       # no extension updates on start
        options.add_argument("--disable-background-networking")  # no background network calls
        options.add_argument("--disable-sync")                   # no account sync
        options.add_argument("--disable-translate")              # no translation service init
        options.add_argument("--safebrowsing-disable-auto-update")  # no safe-browsing DB update
        options.add_argument("--disable-client-side-phishing-detection")  # no phishing init
        options.add_argument("--metrics-recording-only")         # minimal metrics
        options.add_argument("--disable-features=OptimizationGuideModelDownloading,"
                             "OptimizationHintsFetching,OptimizationTargetPrediction,"
                             "OptimizationHints")                # no ML model downloads

        return options

    def _enforce_single_tab(self) -> None:
        """
        RULE (Build 71): Brave must have exactly ONE tab at all times.
        If more than one tab is open it is a system error.
        Closes every window_handle after the first. Called from _get_driver()
        after init and from _fetch_with_selenium() before every driver.get().
        Must be called from within self._lock.
        """
        if self._driver is None:
            return
        try:
            handles = self._driver.window_handles
            if len(handles) <= 1:
                return
            logger.warning(
                "RULE-SINGLE-TAB: %d tabs detected — expected 1. Closing extras.",
                len(handles),
            )
            keep = handles[0]
            for handle in handles[1:]:
                try:
                    self._driver.switch_to.window(handle)
                    self._driver.close()
                    logger.info("RULE-SINGLE-TAB: Closed extra tab %s", handle)
                except Exception as exc:
                    logger.warning("RULE-SINGLE-TAB: Could not close tab %s: %s", handle, exc)
            self._driver.switch_to.window(keep)
        except Exception as exc:
            logger.warning("RULE-SINGLE-TAB: tab enforcement skipped: %s", exc)

    def _get_driver(self) -> webdriver.Chrome:
        """
        Lazy-initialise and return the Chrome/Brave WebDriver.
        Assumes called from within self._lock.
        BUILD 74: uses default system Brave profile (no --user-data-dir).
        RULE-SINGLE-TAB: enforces exactly one tab after init.

        BUG-BROWSER-LAUNCH-HANG-001-FIX (Build 115):
        webdriver.Chrome() can block indefinitely if Brave or ChromeDriver
        do not respond during init (e.g. right after a VPN rotation while
        the network stack is still settling). Without a timeout, this holds
        self._lock forever. Fix: Chrome() launched in a daemon thread with
        join(BROWSER_LAUNCH_TIMEOUT_S). On timeout, WebDriverException is
        raised so the language pass fails cleanly for retry in next batch.
        """
        if self._driver is None:
            cfg = self._cfg
            options = self._build_chrome_options()
            chromedriver_path: Optional[str] = getattr(
                cfg, "CHROMEDRIVER_PATH", None
            )
            launch_timeout: int = getattr(cfg, "BROWSER_LAUNCH_TIMEOUT_S", 60)

            # BUG-BROWSER-LAUNCH-HANG-001-FIX (Build 115): run Chrome() in a
            # daemon thread with a hard timeout so a non-responsive Brave/
            # ChromeDriver cannot hold self._lock indefinitely.
            _launch_result: dict = {"driver": None, "error": None}

            def _do_launch() -> None:
                try:
                    if chromedriver_path:
                        # Estrategia 1: CHROMEDRIVER_PATH explícito en .env (legacy / offline)
                        from selenium.webdriver.chrome.service import Service as _Svc
                        _svc = _Svc(executable_path=chromedriver_path)
                        _launch_result["driver"] = webdriver.Chrome(
                            service=_svc, options=options
                        )
                    else:
                        # BUG-CHROMEDRIVER-001-FIX (Build 117):
                        # Estrategia 2: webdriver-manager detecta versión de Brave
                        # y descarga ChromeDriver compatible automáticamente.
                        # Elimina SessionNotCreatedException por desincronización
                        # entre Brave (auto-update) y ChromeDriver (binario fijo).
                        try:
                            from selenium.webdriver.chrome.service import Service as _Svc
                            from webdriver_manager.chrome import ChromeDriverManager
                            from webdriver_manager.core.os_manager import ChromeType
                            _mgr_path = ChromeDriverManager(
                                chrome_type=ChromeType.BRAVE
                            ).install()
                            _svc = _Svc(executable_path=_mgr_path)
                            _launch_result["driver"] = webdriver.Chrome(
                                service=_svc, options=options
                            )
                            logger.info(
                                "BUG-CHROMEDRIVER-001-FIX: webdriver-manager "
                                "resolvió ChromeDriver en: %s", _mgr_path
                            )
                        except ImportError:
                            # Estrategia 3: fallback a ChromeDriver en PATH del sistema
                            logger.warning(
                                "BUG-CHROMEDRIVER-001-FIX: webdriver-manager no "
                                "instalado — usando ChromeDriver del PATH del sistema. "
                                "Instalar con: pip install webdriver-manager>=4.0.0"
                            )
                            _launch_result["driver"] = webdriver.Chrome(options=options)
                        except Exception as _wdm_exc:
                            # webdriver-manager falló (sin internet, error de descarga, etc.)
                            # Intentar PATH del sistema como último recurso.
                            logger.warning(
                                "BUG-CHROMEDRIVER-001-FIX: webdriver-manager falló "
                                "(%s) — usando ChromeDriver del PATH del sistema.",
                                _wdm_exc,
                            )
                            _launch_result["driver"] = webdriver.Chrome(options=options)
                except Exception as _exc:
                    _launch_result["error"] = str(_exc)

            _lt = threading.Thread(target=_do_launch, daemon=True,
                                   name="browser-launch")
            _lt.start()
            _lt.join(timeout=launch_timeout)

            if _launch_result["driver"] is None:
                if _launch_result["error"]:
                    raise WebDriverException(
                        f"BUG-BROWSER-LAUNCH-HANG-001-FIX: "
                        f"Browser launch failed: {_launch_result['error']}"
                    )
                raise WebDriverException(
                    f"BUG-BROWSER-LAUNCH-HANG-001-FIX: Browser launch timed out "
                    f"after {launch_timeout}s — Brave/ChromeDriver did not respond."
                )

            self._driver = _launch_result["driver"]

            # Remove webdriver navigator flag
            self._driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver',"
                " {get: () => undefined})"
            )
            logger.info("Selenium: Brave started")
            self._enforce_single_tab()  # RULE-SINGLE-TAB: ensure clean state on init

        return self._driver

    def _reinit_driver(self) -> None:
        """
        Restart the WebDriver to clear all browser state.
        Assumes called from within self._lock.
        """
        try:
            if self._driver:
                self._driver.quit()
        except Exception as exc:
            logger.debug("_reinit_driver quit error (ignored): %s", exc)
        finally:
            self._driver = None
        logger.info("Selenium: driver reinitialized (clean state)")

    def reset_browser(self) -> bool:
        """
        BUG-LANG-002-FIX: Fully restart Brave after VPN rotation.

        Called by ScraperService._process_url() immediately after any forced
        VPN rotation. Ensures the next scrape uses a completely clean browser
        profile (no cached DNS, no TLS session resumption, no stale cookies).

        BUG-BROWSER-RESTART-HANG-001-FIX (Build 115):
        driver.quit() can block indefinitely on Windows 11 when Brave is stuck
        in a JavaScript challenge page (chal_t=, force_referer=). ChromeDriver
        keeps the IPC pipe waiting for Brave's response, and Brave never replies.
        This held self._lock forever, causing all Selenium ops to hang.
        Observed: 2026-06-02 16:02:55 "Restarting..." → silence → watchdog
        16:03:04 → worker dead → Beat accumulated 2h45m of unconsumed tasks.
        Fix: driver.quit() runs in a daemon thread with join(BROWSER_QUIT_TIMEOUT_S).
        On timeout, psutil force-kills the Brave/ChromeDriver process tree.

        Returns True on success, False if quit raised an error or timed out
        (caller logs a warning but proceeds — _get_driver() creates a fresh
        instance on the next call via the None guard).
        """
        logger.info(
            "BUG-LANG-002-FIX: Restarting Selenium browser after VPN rotation."
        )
        success = True
        with self._lock:
            if self._driver is not None:
                cfg = self._cfg
                quit_timeout: int = getattr(cfg, "BROWSER_QUIT_TIMEOUT_S", 30)

                # BUG-BROWSER-RESTART-HANG-001-FIX (Build 115): run quit() in a
                # daemon thread so we can enforce a hard timeout regardless of
                # whether Brave/ChromeDriver is hung on a challenge page.
                _quit_result: dict = {"done": False, "error": None}

                def _do_quit() -> None:
                    try:
                        self._driver.quit()  # type: ignore[union-attr]
                        _quit_result["done"] = True
                    except Exception as _exc:
                        _quit_result["error"] = str(_exc)
                        _quit_result["done"] = True

                _qt = threading.Thread(target=_do_quit, daemon=True,
                                       name="browser-quit")
                _qt.start()
                _qt.join(timeout=quit_timeout)

                if not _quit_result["done"]:
                    # Timeout: driver.quit() never returned. Force-kill.
                    logger.error(
                        "BUG-BROWSER-RESTART-HANG-001-FIX: driver.quit() did not "
                        "complete within %ds — Brave is likely frozen (challenge "
                        "page). Force-killing browser process tree.",
                        quit_timeout,
                    )
                    success = False
                    try:
                        import psutil  # type: ignore[import]
                        svc_proc = getattr(self._driver, "service", None)
                        raw_pid = getattr(svc_proc, "process", None)
                        raw_pid = getattr(raw_pid, "pid", None) if raw_pid else None
                        if raw_pid:
                            parent = psutil.Process(raw_pid)
                            for child in parent.children(recursive=True):
                                child.kill()
                            parent.kill()
                            logger.info(
                                "BUG-BROWSER-RESTART-HANG-001-FIX: "
                                "ChromeDriver/Brave PID %d force-killed.",
                                raw_pid,
                            )
                    except Exception as _kill_exc:
                        logger.debug(
                            "BUG-BROWSER-RESTART-HANG-001-FIX: "
                            "force-kill error (non-critical): %s", _kill_exc
                        )
                elif _quit_result["error"]:
                    logger.warning(
                        "BUG-LANG-002-FIX: driver.quit() error (ignored): %s",
                        _quit_result["error"],
                    )
                    success = False
                else:
                    logger.debug("BUG-LANG-002-FIX: Old driver quit successfully.")

                self._driver = None

        log_fn = logger.info if success else logger.warning
        log_fn(
            "BUG-LANG-002-FIX: Browser reset %s — "
            "next request will spawn a fresh driver.",
            "complete" if success else "with errors",
        )
        return success

    def quit(self) -> None:
        """Quit the WebDriver and release all resources."""
        with self._lock:
            if self._driver:
                try:
                    self._driver.quit()
                except Exception as exc:
                    logger.warning("SeleniumEngine.quit() error: %s", exc)
                finally:
                    self._driver = None

    # ── Language header injection (BUG-LANG-002) ──────────────────────────────

    def _set_language_headers(
        self, driver: webdriver.Chrome, lang: str
    ) -> None:
        """
        BUG-LANG-002-FIX: Reset language state before every driver.get().

        Booking.com determines page language by priority:
          1. bkng_lang session cookie  ← HIGHEST (overrides URL param)
          2. Accept-Language header    ← Medium
          3. ?lang=XX URL parameter   ← LOWEST (ignored when cookies exist)

        This method eliminates (1) and enforces (2) so the URL parameter
        becomes the effective language selector.

        Must be called INSIDE the retry loop, immediately before driver.get().
        Assumes called from within self._lock.
        """
        accept_lang = LANG_TO_ACCEPT_LANGUAGE.get(lang, f"{lang};q=0.9")

        # Inject Accept-Language via Chrome DevTools Protocol
        try:
            driver.execute_cdp_cmd("Network.enable", {})
            driver.execute_cdp_cmd(
                "Network.setExtraHTTPHeaders",
                {"headers": {"Accept-Language": accept_lang}},
            )
            logger.debug(
                "BUG-LANG-002-FIX: CDP Accept-Language='%s' for lang=%s",
                accept_lang,
                lang,
            )
        except Exception as exc:
            logger.warning(
                "BUG-LANG-002-FIX: CDP header injection failed (%s) "
                "for lang=%s — falling back to cookie-only reset",
                exc,
                lang,
            )

        # Wipe all Booking.com session cookies (removes bkng_lang)
        try:
            driver.delete_all_cookies()
            logger.debug(
                "BUG-LANG-002-FIX: All cookies deleted before lang=%s", lang
            )
        except Exception as exc:
            logger.warning(
                "BUG-LANG-002-FIX: delete_all_cookies() failed: %s", exc
            )

    # ── Facilities expansion helper ───────────────────────────────────────────

    # BUG-SVC-001-FIX: Booking.com renders only the "Most popular facilities"
    # block (~10 items) in the initial DOM.  The full list (up to ~100+ items)
    # is injected via JavaScript only AFTER the user clicks a "See all N
    # facilities" button.  Without this click the extractor always receives a
    # truncated view, explaining the 87-99% coverage gap reported in the audit.
    #
    # Selectors validated against EN/ES/DE/IT/FR/PT page variants:
    #   • Anchor/button containing data-testid="facility-list-toggle"
    #   • Any <a> or <button> whose visible text matches _SEE_ALL_FAC_RE
    #   • Legacy: href fragment "#hp_facilities_box"
    #   • Legacy: element matching CSS "#hp_facilities_box" (scroll-to reveal)
    _SEE_ALL_FAC_RE: re.Pattern = re.compile(
        r"""
        ^(\s*)(
            See\s+all                     # EN
          | Ver\s+(los\s+|todos\s+(los\s+)?)? \d  # ES: "Ver los 101 servicios"
          | Ver\s+todos                   # ES alt
          | Alle\s+\d+\s+Einrichtungen    # DE
          | Alle\s+anzeigen               # DE alt
          | Voir\s+(les\s+)?\d+           # FR
          | Vedi\s+tutti                  # IT
          | Mostra\s+tutti                # IT alt
          | Ver\s+todas                   # PT
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    def _expand_facilities(self, driver: webdriver.Chrome) -> bool:
        """
        BUG-SVC-001-FIX: Click the 'See all N facilities' button so that
        Booking.com injects the full facilities section into the DOM before
        page_source is captured.

        BUG-SVC-LAZY-001-FIX (Build 105):
        Booking.com modern layout uses JavaScript lazy-loading for the
        property-facilities-block-container.  The container is present in
        the initial DOM but EMPTY (<div></div>); its facility-group-container
        children are injected only after:
          (a) the user scrolls the facilities section into view, OR
          (b) a "See all N facilities" button/modal is triggered.

        Previously _expand_facilities() only tried (b) and — when no button
        was found — returned False leaving the container empty.  This caused
        14 hotels to fall through to Strategy 4 (popular-wrapper: ≤10 items,
        no category) instead of Strategy E45 (property-facilities-block-
        container: full categorised list).

        Fix adds Strategy 4 (lazy-load scroll trigger):
          4a. Scroll [data-testid='property-facilities-block-container']
              into view and dispatch a synthetic scroll event to trigger
              Booking.com's IntersectionObserver.
          4b. Wait up to fac_lazy_wait_s for at least one
              [data-testid='facility-group-container'] to appear.

        All existing strategies (1-3) updated to accept EITHER the modern
        selector (facility-group-container) OR the legacy one
        (property-section--facilities) via EC.any_of().

        Strategy order:
          1. data-testid="facility-list-toggle" (most stable — React attr)
          2. Text-match via _SEE_ALL_FAC_RE on <a>/<button> elements
          3. href="#hp_facilities_box" anchor (legacy pages)
          4. Lazy-load scroll trigger (modern Booking.com — no button needed)

        Returns True if the facilities container is non-empty after all
        strategies, False otherwise (non-fatal — caller proceeds with
        remaining extraction strategies).
        """
        fac_wait_s: float = 10.0
        fac_lazy_wait_s: float = 15.0  # BUG-SVC-LAZY-001: longer for JS render

        # EC.any_of() selector set covering both modern and legacy layouts
        # BUG-SVC-LAZY-001-FIX: added facility-group-container (modern primary)
        _fac_any_of = EC.any_of(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='facility-group-container']")
            ),
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='property-section--facilities']")
            ),
        )

        def _already_loaded(drv: webdriver.Chrome) -> bool:
            """Return True if facility-group-container is already in DOM."""
            try:
                els = drv.find_elements(
                    By.CSS_SELECTOR, "[data-testid='facility-group-container']"
                )
                return len(els) > 0
            except WebDriverException:
                return False

        # Fast path: facilities already rendered (e.g. server-side pages)
        if _already_loaded(driver):
            logger.debug("_expand_facilities: facility-group-container already present")
            return True

        # ── Strategy 1: data-testid attribute ────────────────────────────────
        try:
            btn = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='facility-list-toggle']"
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            driver.execute_script("arguments[0].click();", btn)
            WebDriverWait(driver, fac_wait_s).until(_fac_any_of)
            logger.info(
                "BUG-SVC-001-FIX: facilities expanded via data-testid toggle"
            )
            return True
        except (NoSuchElementException, TimeoutException, WebDriverException):
            pass

        # ── Strategy 2: text-match on <a> and <button> ───────────────────────
        try:
            candidates = driver.find_elements(By.CSS_SELECTOR, "a, button")
            for elem in candidates:
                try:
                    text = elem.text.strip()
                except WebDriverException:
                    continue
                if text and self._SEE_ALL_FAC_RE.match(text):
                    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                    driver.execute_script("arguments[0].click();", elem)
                    WebDriverWait(driver, fac_wait_s).until(_fac_any_of)
                    logger.info(
                        "BUG-SVC-001-FIX: facilities expanded via text-match: %r",
                        text,
                    )
                    return True
        except (TimeoutException, WebDriverException):
            pass
        except Exception as exc:
            logger.debug("BUG-SVC-001: strategy2 error: %s", exc)

        # ── Strategy 3: href="#hp_facilities_box" anchor (legacy) ────────────
        try:
            btn = driver.find_element(
                By.CSS_SELECTOR, "a[href='#hp_facilities_box']"
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            driver.execute_script("arguments[0].click();", btn)
            WebDriverWait(driver, fac_wait_s).until(_fac_any_of)
            logger.info(
                "BUG-SVC-001-FIX: facilities expanded via #hp_facilities_box anchor"
            )
            return True
        except (NoSuchElementException, TimeoutException, WebDriverException):
            pass

        # ── Strategy 4: lazy-load scroll trigger (BUG-SVC-LAZY-001-FIX) ─────
        # BUG-EN-LAZY-001-FIX (Build 106):
        # 7 hotels show EN-only empty categories because the IntersectionObserver
        # for facility-group-container fails to fire within the original single
        # 15-second wait.  The same hotels extract 40-150 services with proper
        # categories for all non-EN languages in the same run, confirming the
        # issue is language/timing-specific, not a selector problem.
        #
        # Root cause: the EN Booking.com page may serve a React bundle that
        # delays IntersectionObserver hydration longer than other languages,
        # or VPN routing for the EN endpoint causes slower DOM settling.
        #
        # Fix: multi-pass scroll strategy (3 attempts × 8 s = 24 s max):
        #   4a. Scroll page to bottom — triggers ALL lazy IntersectionObservers.
        #   4b. Scroll back to facility container + dispatch scroll event.
        #   4c. Wait 8 s per attempt; re-scroll between attempts if needed.
        #   4d. Accept result after any attempt where group_count > 0.
        try:
            import time as _time
            fac_container = driver.find_element(
                By.CSS_SELECTOR,
                "[data-testid='property-facilities-block-container']",
            )

            # Pass 4a: scroll entire page to bottom to warm up lazy loaders
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            _time.sleep(0.4)

            # Pass 4b: scroll facility container into view + dispatch scroll
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
                fac_container,
            )
            driver.execute_script("window.dispatchEvent(new Event('scroll'));")
            _time.sleep(0.3)

            # Retry loop: 3 attempts × 8 s each (total budget ≤ 24 s)
            _PER_ATTEMPT_WAIT = 8.0
            _MAX_ATTEMPTS = 3
            group_count = 0
            for _attempt in range(_MAX_ATTEMPTS):
                try:
                    WebDriverWait(driver, _PER_ATTEMPT_WAIT).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR,
                             "[data-testid='facility-group-container']")
                        )
                    )
                    group_count = len(
                        driver.find_elements(
                            By.CSS_SELECTOR,
                            "[data-testid='facility-group-container']",
                        )
                    )
                    if group_count > 0:
                        break
                except TimeoutException:
                    if _attempt < _MAX_ATTEMPTS - 1:
                        # Re-scroll and try again
                        driver.execute_script(
                            "arguments[0].scrollIntoView("
                            "{behavior: 'instant', block: 'center'});",
                            fac_container,
                        )
                        driver.execute_script(
                            "window.dispatchEvent(new Event('scroll'));"
                        )
                        _time.sleep(0.5)
                        logger.debug(
                            "BUG-EN-LAZY-001-FIX: retry scroll attempt %d/%d",
                            _attempt + 2, _MAX_ATTEMPTS,
                        )

            if group_count > 0:
                logger.info(
                    "BUG-EN-LAZY-001-FIX: facilities lazy-loaded via multi-scroll "
                    "(%d facility-group-container elements found)",
                    group_count,
                )
                return True

            logger.debug(
                "BUG-EN-LAZY-001-FIX: facility-group-container not found after "
                "%d scroll attempts (facility block present but empty)",
                _MAX_ATTEMPTS,
            )
        except (NoSuchElementException, WebDriverException) as exc:
            logger.debug(
                "BUG-SVC-LAZY-001: scroll strategy failed: %s", exc
            )
        except Exception as exc:
            logger.debug(
                "BUG-SVC-LAZY-001: scroll strategy unexpected error: %s", exc
            )

        logger.debug(
            "_expand_facilities: all strategies exhausted — "
            "proceeding with partial facilities DOM"
        )
        return False

    # ── Gallery helpers ───────────────────────────────────────────────────────

    def _open_gallery(self, driver: webdriver.Chrome) -> int:
        """
        Click the first hotel image to open the full gallery and
        scroll to load all image thumbnails.

        BUG-GALLERY-CHAL-001-FIX (Build 115): The trigger.click() can cause
        Booking.com/Cloudflare to redirect to a challenge URL if the click
        triggers a JS event that re-evaluates the bot fingerprint. After the
        click, driver.current_url is checked for challenge params. If detected,
        window.stop() is called and 0 is returned (graceful degradation).

        Returns the number of unique images loaded.
        """
        gallery_selector = "img[src*='bstatic.com/xdata/images/hotel/']"
        try:
            trigger = driver.find_element(By.CSS_SELECTOR, gallery_selector)
            trigger.click()
            time.sleep(1.5)

            # BUG-GALLERY-CHAL-001-FIX (Build 115): check for challenge redirect
            # that may have been triggered by the gallery click.
            try:
                _gal_url = driver.current_url
                if _url_has_challenge_params(_gal_url):
                    logger.warning(
                        "BUG-GALLERY-CHAL-001-FIX: Challenge redirect detected "
                        "after gallery click — stopping page load and aborting "
                        "gallery extraction. current_url=%s", _gal_url
                    )
                    try:
                        driver.execute_script("window.stop()")
                    except Exception:
                        pass
                    return 0
            except Exception:
                pass

            # Scroll to load all lazy images
            last_count = 0
            for _ in range(15):
                imgs = driver.find_elements(By.CSS_SELECTOR, gallery_selector)
                count = len(imgs)
                if count == last_count:
                    break
                last_count = count
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight)"
                )
                time.sleep(1)

            # Deduplicate by src
            srcs = {
                img.get_attribute("src")
                for img in driver.find_elements(By.CSS_SELECTOR, gallery_selector)
                if img.get_attribute("src")
            }
            unique = len(srcs)
            logger.info(
                "Gallery opened via: %s", gallery_selector
            )
            logger.info("Gallery: %d images loaded after scroll", last_count)
            logger.info("Gallery: %d unique image URLs extracted", unique)
            return unique

        except (NoSuchElementException, WebDriverException) as exc:
            logger.debug("Gallery not opened: %s", exc)
            return 0

    def _capture_gallery_modal(self, driver: webdriver.Chrome, url: str) -> int:
        """
        Build 109 (BUG-IMG-CLASS-001): captura el subconjunto de galería REAL.

        El _open_gallery() heredado hace clic en la primera imagen y desplaza
        la página, pero NO abre la rejilla del modal, por lo que el page_source
        nunca contiene los botones gallery-grid-photo-action. Verificado contra
        los snapshots de pruebas/ (0 ocurrencias). Este método replica el
        algoritmo VALIDADO por el usuario en pruebas/extraer_imagenes.py: abre
        el modal, espera la rejilla, hace scroll interno y recolecta los
        botones, guardando las fotos (id_photo, src→3 tallas, alt, orden) en
        self._gallery_photos_by_url[url] para que scraper_service las clasifique.

        Tolerante a fallos: ante cualquier error guarda lista vacía y el
        pipeline continúa con el *fallback* de conteo por badge "+N photos".
        Devuelve el número de fotos de galería capturadas.
        """
        from app.image_classifier import GalleryModalExtractor

        photos: List[Dict[str, Any]] = []
        try:
            photos = GalleryModalExtractor(driver, self._cfg).extract(url=None)
        except Exception as exc:
            logger.warning("Gallery modal capture failed for %s: %s", url, exc)
            photos = []
        self._gallery_photos_by_url[url] = photos
        logger.info("Gallery modal: %d gallery-visible photos captured for %s",
                    len(photos), url)
        return len(photos)

    def take_gallery_photos(self, url: str) -> List[Dict[str, Any]]:
        """
        Build 109: devuelve (y descarta) las fotos de galería capturadas para
        ``url`` durante el último fetch EN. Lista vacía si no se capturaron.
        Pop por-URL: evita carreras cuando SCRAPER_MAX_WORKERS > 1.
        """
        return self._gallery_photos_by_url.pop(url, [])

    def _extract_hotel_photos_js(self, driver: webdriver.Chrome) -> int:
        """
        Extract rich photo metadata from the hotelPhotos JavaScript variable.
        Returns count of photos found.
        """
        try:
            photos_js: Optional[object] = driver.execute_script(
                "return typeof hotelPhotos !== 'undefined' ? hotelPhotos : null;"
            )
            if photos_js and isinstance(photos_js, list):
                count = len(photos_js)
                logger.info(
                    "hotelPhotos JS: %d photos extracted from page source",
                    count,
                )
                return count
        except Exception as exc:
            logger.debug("hotelPhotos JS extraction failed: %s", exc)
        return 0

    # ── Core scraping ─────────────────────────────────────────────────────────

    def _fetch_with_selenium(
        self,
        url: str,
        lang: str,
        attempt: int,
        max_retries: int,
    ) -> Optional[str]:
        """
        Execute one Selenium page fetch within the thread lock.

        Sequence:
          1. BUG-LANG-002-FIX: Set Accept-Language + clear cookies
          2. BUG-PERF-001-FIX: Italian pre-scrape delay
          3. driver.set_page_load_timeout (BUG-PERF-001-FIX)
          4. driver.get(url)
          5. Wait for hotel content (BUG-PERF-001-FIX: per-selector timeout capped)
          6. Language verification (mismatch → retry)
          7. Short HTML check (BUG-LANG-001 fast-fail)
          8. Gallery open + photo JS extraction
          9. Return final page_source

        Assumes called from outside self._lock (acquires it internally).
        """
        cfg = self._cfg
        short_threshold: int = getattr(
            cfg, "SHORT_HTML_THRESHOLD", _SHORT_HTML_DEFAULT_THRESHOLD
        )
        page_timeout: int = getattr(cfg, "SCRAPER_REQUEST_TIMEOUT", 30)

        # BUG-PERF-001-FIX: Use a dedicated per-selector wait timeout.
        # Previously page_timeout (30 s) was used for ALL 4 CSS selectors:
        # worst case = 4 × 30 s = 120 s before proceeding with partial load.
        # Observed: it=144.0 s and it=124.6 s in the 2026-04-01 run.
        # New field SELENIUM_CONTENT_WAIT_TIMEOUT_S defaults to 10 s →
        # worst case = 4 × 10 s = 40 s.  SCRAPER_REQUEST_TIMEOUT is now used
        # exclusively for driver.set_page_load_timeout() below.
        content_wait_s: float = getattr(
            cfg, "SELENIUM_CONTENT_WAIT_TIMEOUT_S", 10.0
        )

        # BUG-PERF-001-FIX: Italian pre-scrape delay.
        # Italian pages show avg 73.7 s vs 49-64 s for other languages and
        # 15.4% of Italian scrapes exceeded 120 s.  A short pre-scrape pause
        # reduces anti-bot challenge accumulation across the session.
        if lang == "it":
            it_delay: float = getattr(cfg, "LANG_SCRAPE_DELAY_IT", 5.0)
            if it_delay > 0:
                logger.info(
                    "BUG-PERF-001-FIX: Italian pre-scrape delay %.1f s "
                    "before %s", it_delay, url,
                )
                time.sleep(it_delay)

        with self._lock:
            driver = self._get_driver()
            self._enforce_single_tab()  # RULE-SINGLE-TAB: close any stray tabs before fetch

            # BUG-PERF-001-FIX: Cap the total navigation time.
            # Without this, driver.get() can block indefinitely on slow pages.
            driver.set_page_load_timeout(page_timeout)

            # ── BUG-LANG-002-FIX: Reset language state ─────────────────────
            if getattr(cfg, "SELENIUM_RESET_LANG_ON_EACH_REQUEST", True):
                self._set_language_headers(driver, lang)

            # ── BUG-CHAL-DETECT-001-FIX: detectar URL de bot-detection ANTES de navegar
            # Si la URL contiene chal_t= / force_referer=, Booking.com ya marcó
            # la sesión — navegar causaría una carga indefinida o un desafío JS
            # sin resolver. Abortar inmediatamente y rotar VPN.
            if _url_has_challenge_params(url):
                logger.warning(
                    "BUG-CHAL-DETECT-001: URL con parámetros de bot-detection "
                    "(chal_t/force_referer) detectados antes de navegar para %s "
                    "— abortando para rotar VPN (attempt %d/%d)",
                    url, attempt, max_retries,
                )
                return None

            # ── Navigate ────────────────────────────────────────────────────
            # NAV-TIMEOUT-001-FIX (Build 116):
            # driver.get(url) puede bloquearse indefinidamente cuando Booking.com/
            # Cloudflare sirve una página de desafío que carga inmediatamente (sin
            # disparar TimeoutException) pero luego entra en un loop JS infinito.
            # En ese estado, incluso window.stop() vía execute_script() se bloquea
            # porque ChromeDriver espera respuesta de un Brave congelado.
            # Mecanismo observado en INC-2026-0602-BROWSER-FREEZE-001: la URL
            # vidimo-se.en-gb.html se cargó con chal_t=, el navegador se congeló
            # en los 4 segundos entre el último log y el disparo del watchdog.
            # Fix: driver.get() se ejecuta en un daemon thread con join(
            # NAVIGATION_TIMEOUT_S). En timeout, se intenta window.stop() y se
            # retorna None para que el pase de idioma falle limpiamente y se reintente.
            _nav_timeout: int = getattr(cfg, "NAVIGATION_TIMEOUT_S", 45)
            _nav_result: dict = {"done": False, "error": None}

            def _do_get() -> None:
                try:
                    driver.get(url)
                    _nav_result["done"] = True
                except WebDriverException as _exc:
                    _nav_result["error"] = str(_exc)
                    _nav_result["done"] = True
                except Exception as _exc:
                    _nav_result["error"] = f"unexpected: {_exc}"
                    _nav_result["done"] = True

            _nav_thread = threading.Thread(
                target=_do_get,
                daemon=True,
                name=f"nav-get-{lang}-a{attempt}",
            )
            _nav_thread.start()
            _nav_thread.join(timeout=_nav_timeout)

            if not _nav_result["done"]:
                # driver.get() nunca retornó dentro del timeout → Brave congelado
                logger.error(
                    "NAV-TIMEOUT-001-FIX: driver.get() no completó en %ds "
                    "(attempt %d/%d) para %s — Brave posiblemente congelado en "
                    "página de desafío. Intentando window.stop() y abortando.",
                    _nav_timeout, attempt, max_retries, url,
                )
                try:
                    driver.execute_script("window.stop()")
                except Exception:
                    pass
                return None

            if _nav_result["error"]:
                logger.warning(
                    "Selenium: driver.get() failed (attempt %d/%d): %s",
                    attempt, max_retries, _nav_result["error"],
                )
                return None

            # ── BUG-CHAL-DETECT-002-FIX (Build 115): post-navigation check ──
            # BUG-CHAL-DETECT-001-FIX (Build 114) only checked the URL BEFORE
            # driver.get(). Booking.com/Cloudflare can redirect to a challenge
            # URL (chal_t=, force_referer=) AFTER the initial load, once the
            # JS fingerprinting script evaluates the browser. This is confirmed
            # by INC-2026-0602-VILLADVOR-001: the challenge URL appeared only
            # as driver.current_url after navigation, with activeTab=photosGallery
            # suggesting the gallery JS triggered the challenge evaluation.
            # Fix: inspect driver.current_url immediately after driver.get().
            try:
                _current_url = driver.current_url
                if _url_has_challenge_params(_current_url):
                    logger.warning(
                        "BUG-CHAL-DETECT-002-FIX: Challenge params detected in "
                        "current_url AFTER navigation (attempt %d/%d). "
                        "Booking.com redirected to a bot-challenge page: %s. "
                        "Aborting — caller will rotate VPN and retry.",
                        attempt, max_retries, _current_url,
                    )
                    try:
                        driver.execute_script("window.stop()")
                    except Exception:
                        pass
                    return None
            except Exception:
                pass  # If driver is frozen, current_url may raise — continue anyway

            # ── Wait for hotel content ──────────────────────────────────────
            # BUG-EXTRACT-IT-001-FIX (Build 98): sustituye el bucle for de 4
            # WebDriverWait secuenciales por un único EC.any_of() que evalúa
            # todos los selectores en paralelo dentro de content_wait_s.
            #
            # Antes (Build 97): peor caso = 4 × content_wait_s = 40 s
            # (si los 3 primeros selectores timeout y el 4° coincide)
            # Ahora (Build 98):  peor caso = 1 × content_wait_s = 10 s
            # (cualquier selector que coincida resuelve el wait inmediatamente)
            #
            # Nota: BUG-PERF-001-FIX (Build 64) redujo content_wait_s de 30 s
            # a 10 s; BUG-EXTRACT-IT-001-FIX elimina la multiplicación × 4.
            hotel_selectors = (
                "h2[data-testid='title']",
                "#hp_hotel_name",
                ".hp__hotel-name",
                "h1.pp-header__title",
            )
            loaded = False
            try:
                # EC.any_of(): resuelve True en cuanto cualquier condición
                # se cumpla; levanta TimeoutException si ninguna se cumple
                # dentro de content_wait_s. Disponible en selenium >= 4.0.
                WebDriverWait(driver, content_wait_s).until(
                    EC.any_of(
                        *[
                            EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                            for sel in hotel_selectors
                        ]
                    )
                )
                loaded = True
            except TimeoutException:
                loaded = False

            if not loaded:
                # BUG-SCRAPER-001-FIX: stop ongoing page load BEFORE reading
                # page_source. Booking.com/Cloudflare challenge pages run JS
                # indefinitely — driver.page_source hangs 30+ min without this.
                try:
                    driver.execute_script("window.stop()")
                except Exception:
                    pass
                # Check for Cloudflare / Booking.com challenge
                page_low = driver.page_source.lower()
                if any(ind in page_low for ind in _BLOCK_INDICATORS):
                    logger.warning(
                        "Selenium: Cloudflare challenge detected "
                        "(attempt %d/%d) — reinitializing browser for %s",
                        attempt, max_retries, url,
                    )
                    self._reinit_driver()
                    return None
                logger.warning(
                    "Selenium: timeout waiting for hotel content "
                    "(attempt %d/%d) — proceeding with partial load for %s",
                    attempt, max_retries, url,
                )

            # BUG-SCRAPER-001-FIX: stop page load before reading source to
            # prevent infinite hang on challenge pages that passed indicator check.
            try:
                driver.execute_script("window.stop()")
            except Exception:
                pass
            html = driver.page_source

            # ── BUG-LANG-001-FIX: Short HTML fast-fail ─────────────────────
            html_len = len(html)
            if html_len < short_threshold:
                logger.warning(
                    "BUG-LANG-001-FIX: Short HTML (%d bytes) — "
                    "block page detected, skipping remaining retries for %s",
                    html_len, url,
                )
                _save_debug_html(html, url, f"short_html_selenium_a{attempt}")
                with threading.Lock():
                    self._blocked_count += 1
                return None

            # ── Language verification ───────────────────────────────────────
            detected = _detect_page_language(html)
            lang_iso = lang.split("-")[0].lower()

            if detected and detected not in (lang_iso, "x-default", "en"):
                # Allow 'en' as fallback for some hotels regardless of lang
                logger.warning(
                    "Selenium language mismatch: requested=%s got=%s",
                    lang, detected,
                )
                return None

            # ── Verify it's a real hotel page ───────────────────────────────
            if not _is_hotel_page(html):
                logger.warning(
                    "Selenium: page does not look like a hotel page for %s",
                    url,
                )
                return None

            # ── BUG-EN-LAZY-001-FIX: Pre-scroll facilities into viewport ────
            # BUG-SVC-LAZY-001-FIX (Build 105): initial pre-scroll trigger.
            # BUG-EN-LAZY-001-FIX (Build 106): added full-page bottom scroll
            # before facility scroll to warm up ALL IntersectionObservers on
            # the page simultaneously.  This improves EN-page facility loading
            # which was failing for 7 hotels (empty-category EN services while
            # other languages extracted 40-150 services with proper categories).
            try:
                import time as _pre_time
                # Step 1: scroll to page bottom (warms all lazy loaders)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                _pre_time.sleep(0.3)
                # Step 2: scroll facility container into center view
                _fac_el = driver.find_element(
                    By.CSS_SELECTOR,
                    "[data-testid='property-facilities-block-container']",
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior:'instant',block:'center'});",
                    _fac_el,
                )
                driver.execute_script("window.dispatchEvent(new Event('scroll'));")
                logger.debug(
                    "BUG-EN-LAZY-001-FIX: pre-scrolled page bottom + facilities container"
                )
            except (NoSuchElementException, WebDriverException):
                pass

            # ── BUG-SVC-001-FIX: Expand full facilities list ────────────────
            # BUG-SVC-LAZY-001-FIX (Build 105): _expand_facilities() now
            # includes Strategy 4 (lazy-load scroll trigger) that waits for
            # facility-group-container to appear after scroll.
            # Updated wait conditions use EC.any_of() for both modern and
            # legacy Booking.com layout selectors.
            self._expand_facilities(driver)

            # ── Photo JS extraction (all languages) ─────────────────────────
            # BUG-GALLERY-OPEN-ALL-LANGS-001-FIX (Build 123):
            # hotelPhotos is a page-load JS variable — fully independent of
            # gallery open state. _extract_hotel_photos_js() reads it via
            # execute_script() without any DOM interaction, so it is safe to
            # call for every language. The gallery image click (_open_gallery)
            # was previously called here unconditionally, triggering Cloudflare
            # bot-detection fingerprinting on every non-EN language pass.
            # Evidence: 92/121 gallery challenge events in the 2026-06-12
            # session were from non-EN languages — a direct consequence.
            # Fix: _open_gallery() moved inside the EN-only block below.
            photo_count = self._extract_hotel_photos_js(driver)
            if photo_count > 0:
                logger.info(
                    "Gallery: %d photos with full metadata (hotelPhotos JS)",
                    photo_count,
                )

            # ── Build 109 + BUG-GALLERY-OPEN-ALL-LANGS-001-FIX (Build 123) ──
            # _open_gallery() and _capture_gallery_modal() are EN-only:
            #   - Photos are language-independent; classification is done once
            #     in the EN pass to avoid multiplying Selenium cost × 6 langs.
            #   - _open_gallery() clicks the gallery hero image (triggers bot
            #     detection via JS fingerprinting). Calling it in non-EN passes
            #     produced no useful data and caused 92 avoidable challenge
            #     redirects (chal_t= / force_referer=) in the 2026-06-12 run.
            # IMPORTANT: _capture_gallery_modal() uses GALLERY_MODAL_DISMISS_CONSENT
            # to close any lightbox that _open_gallery() may have opened, so
            # the ordering (open_gallery → capture_modal) remains correct.
            if lang.split("-")[0].lower() == "en" and getattr(
                cfg, "IMAGE_CLASSIFICATION_ENABLED", True
            ):
                self._open_gallery(driver)
                self._capture_gallery_modal(driver, url)

            return driver.page_source

    def scrape(self, url: str, lang: str) -> Optional[str]:
        """
        Scrape a Booking.com hotel page in the specified language.

        Build 63: Sole engine — no CloudScraper fallback.
        Retries up to MAX_LANG_RETRIES times with exponential backoff.

        Args:
            url:  Language-specific Booking.com URL.
            lang: ISO 639-1 language code (e.g. "de", "fr").

        Returns:
            Full page HTML on success, None on all retries exhausted.
        """
        cfg = self._cfg
        max_retries: int = getattr(cfg, "MAX_LANG_RETRIES", 3)
        retry_delay: float = getattr(cfg, "SCRAPER_RETRY_DELAY", 2.0)

        for attempt in range(1, max_retries + 1):
            try:
                html = self._fetch_with_selenium(url, lang, attempt, max_retries)
                if html is not None:
                    return html

                if attempt < max_retries:
                    wait = retry_delay * attempt
                    logger.info(
                        "Selenium retry %d -- waiting %ds -- %s",
                        attempt + 1,
                        int(wait),
                        url,
                    )
                    time.sleep(wait)

            except Exception as exc:
                logger.error(
                    "Selenium unexpected error (attempt %d/%d) for %s: %s",
                    attempt, max_retries, url, exc, exc_info=True,
                )
                if attempt < max_retries:
                    time.sleep(retry_delay * attempt)

        logger.error("Selenium language retries exhausted for %s", url)
        return None
