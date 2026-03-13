"""
scraper.py — BookingScraper Pro v49
Enterprise rebuild merging v48 architecture with v5.1 field-validated fixes.

Fixes applied (v48 baseline):
  BUG-004 / BUG-106 : build_language_url — no double-.html stripping.
  BUG-008           : BOOKING_BYPASS_COOKIES not captured at import time.
  BUG-013           : _is_blocked wrapped in try/except; structured detection.
  BUG-018           : USER_AGENTS_WIN weighted by realistic market share.
  SCRAP-SEC-003     : Debug HTML saved to isolated directory only.

Fixes restored from v5.1 (field-validated):
  FIX-024           : build_language_url — en → .en-gb.html?lang=en-gb (canonical)
  FIX-025           : LANG_COOKIE_LOCALE["en"] = "en-gb" (not "en-us")
  FIX-026           : BOOKING_BYPASS_COOKIES selectedLanguage = "en-gb"
  FIX-027           : LANG_ACCEPT["en"] = "en-GB,en;q=0.9"
  FIX-028           : _is_blocked() 500KB threshold — "checking your browser"
                      removed from signals (appears in Booking.com GDPR banners)
  FIX-029           : SeleniumEngine — skip _is_blocked if hotel content confirmed
  FIX-016           : _detect_page_language() — 5-strategy language detection
  FIX-020           : Language mismatch → retry, not silent bad save
  FIX-021           : SeleniumEngine uses Brave as primary browser
                      Fallback order: Brave → Chrome → Edge → Opera

Fixes applied (v49):
  BUG-DESC-001      : Thread-unsafe CloudScraperEngine session.
                      Root cause: one shared requests.Session used by all threads in
                      ThreadPoolExecutor (workers=2). Concurrent scrapes mutated
                      cookies/headers for each other → Booking.com returned wrong HTML
                      (different hotel) → wrong description saved to DB.
                      Fix: thread-local storage (_cloud_tls = threading.local()) so
                      each worker thread owns an independent CloudScraper instance.

  BUG-DESC-002      : Thread-unsafe SeleniumEngine — single _driver navigated by
                      multiple threads simultaneously → race condition → wrong page
                      HTML captured → wrong fields (description, etc.) saved.
                      Fix: threading.Lock() on SeleniumEngine; only one thread drives
                      the browser at a time (Selenium is inherently single-threaded).

  BUG-IMG-401       : _extract_image_urls_from_page() stripped ?k=... auth token.
                      The line `norm.split("?")[0]` removed the mandatory Booking.com
                      CDN authentication parameter, causing 401 on every image.
                      Fix: removed query-param stripping. Full URL including k= is now
                      preserved and passed to ImageDownloader.

  NEW-PHOTOS-001    : _extract_hotel_photos_js() — new SeleniumEngine method.
                      Extracts full hotelPhotos metadata from page_source JavaScript:
                      id_photo, thumb_url, large_url, highres_url (with k= params),
                      alt, orientation, photo_width, photo_height, created.
                      Stored in self._last_gallery_photos for scraper_service.py.

Platform: Windows 11 / Selenium 4 / Brave browser primary.
"""

from __future__ import annotations

import hashlib
import logging
import os
import random
import re
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import cloudscraper
import requests

from app.config import get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# User-Agent pool — BUG-018: weighted by market share
# ---------------------------------------------------------------------------
_USER_AGENTS_WIN: List[Tuple[str, float]] = [
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", 0.25),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", 0.20),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", 0.15),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", 0.10),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0", 0.12),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0", 0.08),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36", 0.10),
]
_UA_POPULATION = [ua for ua, _ in _USER_AGENTS_WIN]
_UA_WEIGHTS     = [w  for _, w  in _USER_AGENTS_WIN]


def _random_user_agent() -> str:
    return random.choices(_UA_POPULATION, weights=_UA_WEIGHTS, k=1)[0]


# ---------------------------------------------------------------------------
# Language maps — FIX-024/025/027: full 19-language coverage, en=en-gb
# ---------------------------------------------------------------------------

LANG_COOKIE_LOCALE: Dict[str, str] = {
    "en": "en-gb",   "es": "es",     "de": "de",    "fr": "fr",
    "it": "it",      "pt": "pt-pt",  "nl": "nl",    "ru": "ru",
    "ar": "ar",      "tr": "tr",     "hu": "hu",    "pl": "pl",
    "zh": "zh-cn",   "no": "nb",     "fi": "fi",    "sv": "sv",
    "da": "da",      "ja": "ja",     "ko": "ko",
}

# FIX-027: full Accept-Language headers per language
LANG_ACCEPT: Dict[str, str] = {
    "en": "en-GB,en;q=0.9",
    "es": "es-ES,es;q=0.9,en;q=0.8",
    "de": "de-DE,de;q=0.9,en;q=0.8",
    "fr": "fr-FR,fr;q=0.9,en;q=0.8",
    "it": "it-IT,it;q=0.9,en;q=0.8",
    "pt": "pt-PT,pt;q=0.9,en;q=0.8",
    "nl": "nl-NL,nl;q=0.9,en;q=0.8",
    "ru": "ru-RU,ru;q=0.9,en;q=0.8",
    "ar": "ar-SA,ar;q=0.9,en;q=0.8",
    "tr": "tr-TR,tr;q=0.9,en;q=0.8",
    "hu": "hu-HU,hu;q=0.9,en;q=0.8",
    "pl": "pl-PL,pl;q=0.9,en;q=0.8",
    "zh": "zh-CN,zh;q=0.9,en;q=0.8",
    "no": "nb-NO,nb;q=0.9,no;q=0.8,en;q=0.7",
    "fi": "fi-FI,fi;q=0.9,en;q=0.8",
    "sv": "sv-SE,sv;q=0.9,en;q=0.8",
    "da": "da-DK,da;q=0.9,en;q=0.8",
    "ja": "ja-JP,ja;q=0.9,en;q=0.8",
    "ko": "ko-KR,ko;q=0.9,en;q=0.8",
}

# Language suffix map — FIX-024
LANGUAGE_EXT: Dict[str, str] = {
    "en": "en-gb",  "es": "es",    "de": "de",    "fr": "fr",
    "it": "it",     "pt": "pt-pt", "nl": "nl",    "ru": "ru",
    "ar": "ar",     "tr": "tr",    "hu": "hu",    "pl": "pl",
    "zh": "zh-cn",  "no": "nb",    "fi": "fi",    "sv": "sv",
    "da": "da",     "ja": "ja",    "ko": "ko",
}

# ---------------------------------------------------------------------------
# Bypass cookies — BUG-008: built fresh per call, not at import time
# FIX-026: selectedLanguage = "en-gb"
# ---------------------------------------------------------------------------

_BYPASS_COOKIES_BASE: Dict[str, str] = {
    "OptanonAlertBoxClosed": "2024-01-01T00:00:00.000Z",
    "OptanonConsent":        "isGpcEnabled=0&datestamp=Mon+Jan+01+2024&version=202401.1.0&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1",
    "bkng_sso_ses":          "e30=",
    "cors":                  "1",
    "selectedLanguage":      "en-gb",
    "selectedCurrency":      "EUR",
}


def get_bypass_cookies(language: str = "en") -> Dict[str, str]:
    """Build bypass cookies per request with unique GA IDs (anti-fingerprinting)."""
    cookies = dict(_BYPASS_COOKIES_BASE)
    cookies["selectedLanguage"] = LANG_COOKIE_LOCALE.get(language, "en-gb")
    cookies["_ga"]  = f"GA1.1.{random.randint(100000000,999999999)}.{int(time.time()) - random.randint(86400, 2592000)}"
    cookies["_gid"] = f"GA1.1.{random.randint(100000000,999999999)}.{int(time.time()) - random.randint(3600, 86400)}"
    return cookies


# ---------------------------------------------------------------------------
# Block detection — FIX-028
# ---------------------------------------------------------------------------

_BLOCK_SIGNALS_FULL: List[str] = [
    "just a moment",
    "access denied",
    "403 forbidden",
    "please verify you are a human",
    "enable javascript",
    "ddos-guard",
    "cf-browser-verification",
    "captcha",
    "too many requests",
]

_BLOCK_SIGNALS_LARGE: List[str] = [
    "just a moment",
    "enable javascript",
    "ddos-guard",
]

_BLOCK_CHECK_MAX_BYTES = 500_000

_HOTEL_PAGE_SIGNALS: List[str] = [
    "property-description",
    "hp_facilities_box",
    "maxotelroomarea",
    "reviewscore",
    "review-score",
    "b2hotelpage",
    "hoteldetails",
]


def _is_blocked(html: str) -> bool:
    """FIX-028: pages >500KB skip the full signal list."""
    try:
        html_low = html.lower()
        if len(html) > _BLOCK_CHECK_MAX_BYTES:
            return any(s in html_low for s in _BLOCK_SIGNALS_LARGE)
        return any(s in html_low for s in _BLOCK_SIGNALS_FULL)
    except Exception as exc:
        logger.warning("_is_blocked parsing error: %s — treating as blocked.", exc)
        return True


def _is_hotel_page(html: str) -> bool:
    html_low = html.lower()
    return any(s in html_low for s in _HOTEL_PAGE_SIGNALS)


# ---------------------------------------------------------------------------
# Language detection — FIX-016: 5-strategy detection
# ---------------------------------------------------------------------------

_INVALID_LANGS = {"x-default", "und", "xx", "zz", "qaa", ""}

_LANG_DOM_SIGNALS: Dict[str, List[str]] = {
    "es": ["Ver disponibilidad", "Normas de la casa", "Servicios", "Valoración de los huéspedes"],
    "de": ["Verfügbarkeit prüfen", "Hausregeln", "Ausstattung", "Bewertungen"],
    "fr": ["Vérifier la disponibilité", "Règlement", "Services", "Commentaires"],
    "it": ["Verifica disponibilità", "Regole della casa", "Servizi", "Recensioni"],
    "pt": ["Verificar disponibilidade", "Regras da casa", "Serviços", "Avaliações"],
    "nl": ["Beschikbaarheid controleren", "Huisregels", "Diensten", "Beoordelingen"],
    "en": ["Check availability", "House rules", "Facilities", "Guest reviews"],
}


def _detect_page_language(html: str) -> Optional[str]:
    """FIX-016: 5-strategy language detection. Returns 2-letter ISO 639-1 or None."""
    # Strategy 1: <html lang="...">
    m = re.search(
        r'<html[^>]+\blang=["\']([a-zA-Z]{2,10}(?:-[a-zA-Z0-9]{2,8})?)["\']',
        html[:3000], re.IGNORECASE
    )
    if m:
        code = m.group(1).lower()[:2]
        if code not in _INVALID_LANGS and len(code) == 2 and code.isalpha():
            return code

    # Strategy 2: og:locale meta
    for pattern in [
        r'property=["\']og:locale["\'][^>]+content=["\']([a-zA-Z]{2,5}(?:[_-][a-zA-Z]{2,4})?)["\']',
        r'content=["\']([a-zA-Z]{2,5}(?:[_-][a-zA-Z]{2,4})?)["\'][^>]+property=["\']og:locale["\']',
    ]:
        m = re.search(pattern, html[:8000], re.IGNORECASE)
        if m:
            code = m.group(1).lower().replace("_", "-")[:2]
            if code not in _INVALID_LANGS and len(code) == 2 and code.isalpha():
                return code

    # Strategy 3: Content-Language meta
    m = re.search(
        r'http-equiv=["\']Content-Language["\'][^>]+content=["\']([a-zA-Z]{2})',
        html[:8000], re.IGNORECASE
    )
    if m:
        code = m.group(1).lower()
        if code not in _INVALID_LANGS:
            return code

    # Strategy 4: Language suffix in canonical URL
    for pattern in [
        r'property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']',
        r'content=["\']([^"\']+)["\'][^>]+property=["\']og:url["\']',
        r'rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        r'href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
    ]:
        mu = re.search(pattern, html[:8000], re.IGNORECASE)
        if mu:
            canon = mu.group(1)
            ms = re.search(r'\.([a-z]{2}(?:-[a-z]{2,4})?)\.html', canon, re.IGNORECASE)
            if ms:
                code = ms.group(1).lower()[:2]
                if code not in _INVALID_LANGS and code.isalpha():
                    return code
            elif re.search(r'\.html', canon, re.IGNORECASE):
                return "en"

    # Strategy 5: DOM text signals
    html_body = html[2000:50000]
    for lang_code, signals in _LANG_DOM_SIGNALS.items():
        if sum(1 for s in signals if s in html_body) >= 2:
            return lang_code

    return None


# ---------------------------------------------------------------------------
# URL language builder — FIX-024
# ---------------------------------------------------------------------------

_LANG_SUFFIX_RE = re.compile(
    r"\.[a-z]{2}(?:-[a-z]{2,4})?\.html$",
    re.IGNORECASE,
)


def build_language_url(base_url: str, language: str) -> str:
    """
    Build language-specific Booking.com URL.
    FIX-024: Three vectors aligned — path suffix, ?lang= param, cookie.
    en → hotel.en-gb.html?lang=en-gb
    """
    stripped = base_url.strip()
    if "?" in stripped:
        stripped = stripped.split("?")[0]

    clean = _LANG_SUFFIX_RE.sub(".html", stripped)
    if not clean.lower().endswith(".html"):
        clean += ".html"

    ext = LANGUAGE_EXT.get(language, language)
    new_url = clean[:-5] + f".{ext}.html"

    locale = LANG_COOKIE_LOCALE.get(language, language)
    return f"{new_url}?lang={locale}"


# ---------------------------------------------------------------------------
# Filename / debug helpers
# ---------------------------------------------------------------------------

def url_to_filename(url: str, tag: str = "debug", ext: str = ".html") -> str:
    digest = hashlib.sha256(url.encode()).hexdigest()[:32]
    return f"{digest}_{tag}{ext}"


def _save_debug_html(html: str, url: str, tag: str = "debug") -> None:
    cfg = get_settings()
    if not cfg.DEBUG_HTML_SAVE:
        return
    try:
        target = cfg.DEBUG_HTML_DIR / url_to_filename(url, tag)
        target.write_text(html, encoding="utf-8", errors="replace")
        logger.debug("Debug HTML: %s", target.name)
    except OSError as exc:
        logger.warning("Debug HTML save failed: %s", exc)


# ---------------------------------------------------------------------------
# CloudScraper engine
# BUG-DESC-001 FIX (v49): Thread-local sessions via threading.local()
# ---------------------------------------------------------------------------

# Module-level thread-local storage — each worker thread gets its own
# CloudScraper instance, preventing cookie/header cross-contamination.
_cloud_tls = threading.local()


class CloudScraperEngine:
    """
    HTTP scraping engine using cloudscraper for Cloudflare bypass.

    BUG-DESC-001 FIX (v49): Thread-safe via thread-local sessions.
    Previously a single self._session was shared across all ThreadPoolExecutor
    threads. Concurrent scrapes mutated language cookies for each other, causing
    Booking.com to return HTML for the wrong hotel/language.
    Fix: _cloud_tls = threading.local() — each thread owns its own session.
    The _lock now protects only the counters, not the session object.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()   # protects counters only (not session)
        self._session_resets: int = 0
        self._blocked_count:  int = 0

    def _new_session(self) -> cloudscraper.CloudScraper:
        sess = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False},
            delay=5,
        )
        ua = _random_user_agent()
        sess.headers.update({
            "User-Agent":      ua,
            "Accept-Language": "en-GB,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "DNT":             "1",
            "Referer":         "https://www.google.com/search?q=booking+hotel",
        })
        for k, v in get_bypass_cookies("en").items():
            sess.cookies.set(k, v, domain=".booking.com")
        logger.debug("CloudScraper new session (thread=%s) | UA: %s",
                     threading.current_thread().name, ua[:60])
        return sess

    def _get_or_create_session(self) -> cloudscraper.CloudScraper:
        """
        BUG-DESC-001 FIX: Return this thread's own CloudScraper session.
        Each thread in the ThreadPoolExecutor has an isolated _cloud_tls namespace,
        so session cookies and headers are never shared between concurrent scrapes.
        """
        if not getattr(_cloud_tls, "session", None):
            _cloud_tls.session = self._new_session()
            logger.debug(
                "CloudScraper: created thread-local session for thread=%s",
                threading.current_thread().name,
            )
        return _cloud_tls.session

    def _reset_session(self) -> None:
        """Reset only the current thread's session. BUG-DESC-001 fix."""
        if getattr(_cloud_tls, "session", None):
            try:
                _cloud_tls.session.close()
            except Exception:
                pass
        _cloud_tls.session = self._new_session()
        with self._lock:
            self._session_resets += 1
            self._blocked_count = 0
        logger.debug(
            "CloudScraper session reset (thread=%s reset_count=%d)",
            threading.current_thread().name, self._session_resets,
        )

    def scrape(self, url: str, language: str = "en", retries: int = 3) -> Optional[str]:
        """
        Fetch URL and return HTML or None.
        FIX-025/027: language-aware cookies and Accept-Language header.
        FIX-028: _is_blocked() with 500KB threshold.
        BUG-DESC-001: uses thread-local session (no cross-thread mutation).
        """
        cfg     = get_settings()
        locale  = LANG_COOKIE_LOCALE.get(language, language)
        session = self._get_or_create_session()

        # Per-language cookie/header update on this thread's session only
        session.cookies.set("selectedLanguage", locale, domain=".booking.com")
        session.headers.update({
            "Accept-Language": LANG_ACCEPT.get(language, "en-GB,en;q=0.9"),
        })

        lang_mismatch_retries = 0

        for attempt in range(1, retries + 1):
            force_new = (attempt > 1 and self._blocked_count >= 2)
            if force_new:
                self._reset_session()
                session = self._get_or_create_session()
                session.cookies.set("selectedLanguage", locale, domain=".booking.com")

            try:
                delay = cfg.SCRAPER_RETRY_DELAY * attempt if attempt > 1 else cfg.SCRAPER_RETRY_DELAY
                if attempt > 1:
                    logger.info("CloudScraper retry %d/%d — waiting %.1fs — %s", attempt, retries, delay, url)
                time.sleep(delay)

                response = session.get(
                    url,
                    timeout=cfg.SCRAPER_REQUEST_TIMEOUT,
                    cookies=get_bypass_cookies(language),
                    allow_redirects=True,
                )

                if response.status_code == 403:
                    with self._lock:
                        self._blocked_count += 1
                    logger.warning("HTTP 403 (blocked=%d) for %s", self._blocked_count, url)
                    _save_debug_html(response.text, url, f"403_a{attempt}")
                    time.sleep(random.uniform(15, 30))
                    continue
                if response.status_code == 429:
                    wait = int(response.headers.get("Retry-After", 90))
                    logger.warning("HTTP 429 — waiting %ds for %s", wait, url)
                    time.sleep(wait)
                    continue
                if response.status_code == 404:
                    logger.error("HTTP 404 for %s", url)
                    return None
                if response.status_code >= 500:
                    logger.warning("HTTP %d for %s", response.status_code, url)
                    time.sleep(random.uniform(10, 20))
                    continue

                response.raise_for_status()
                html = response.text
                html_len = len(html)

                if html_len < 5000:
                    logger.warning("Short HTML (%d bytes) for %s", html_len, url)
                    with self._lock:
                        self._blocked_count += 1
                    time.sleep(random.uniform(8, 15))
                    continue

                if _is_blocked(html):
                    logger.warning("Block detected attempt %d for %s", attempt, url)
                    _save_debug_html(html, url, f"blocked_a{attempt}")
                    with self._lock:
                        self._blocked_count += 1
                    time.sleep(random.uniform(20, 40))
                    continue

                # FIX-020: language mismatch check
                detected = _detect_page_language(html)
                if detected and detected != language:
                    logger.warning("Language mismatch — requested=%s got=%s for %s", language, detected, url)
                    if lang_mismatch_retries < 2:
                        lang_mismatch_retries += 1
                        with self._lock:
                            self._blocked_count += 1
                        _save_debug_html(html, url, f"lang_mismatch_{detected}_a{attempt}")
                        time.sleep(random.uniform(20, 40))
                        continue
                    else:
                        logger.error("Language mismatch retries exhausted for %s — got=%s", url, detected)
                        return None

                _save_debug_html(html, url, f"ok_a{attempt}")
                with self._lock:
                    self._blocked_count = 0
                return html

            except requests.exceptions.RequestException as exc:
                logger.warning("CloudScraper attempt %d/%d failed: [%s] %s", attempt, retries, type(exc).__name__, exc)
                if attempt < retries:
                    time.sleep(cfg.SCRAPER_RETRY_DELAY * attempt)
                    self._reset_session()
                    session = self._get_or_create_session()

        logger.error("CloudScraper exhausted retries for %s", url)
        return None


# ---------------------------------------------------------------------------
# Selenium engine
# FIX-021: Brave primary. Fallback Chrome → Edge → Opera
# BUG-DESC-002 FIX (v49): threading.Lock() — serial browser access
# ---------------------------------------------------------------------------

class SeleniumEngine:
    """
    Selenium-based scraping engine.
    FIX-021: Brave is primary browser. Falls back to Chrome → Edge → Opera.

    BUG-DESC-002 FIX (v49): Added _scrape_lock (threading.Lock).
    The Selenium WebDriver is a single browser process — not thread-safe.
    With workers=2, two threads calling scrape() concurrently would navigate
    the browser to two different URLs simultaneously, causing race conditions:
    one thread captures the other hotel's HTML → wrong data saved to DB.
    Fix: acquire _scrape_lock before navigating; only one thread drives
    the browser at a time. I/O-bound waits (page load, gallery scroll) still
    allow other threads to run Python code concurrently via the GIL.
    """

    _BROWSER_PATHS: Dict[str, List[str]] = {
        "brave": [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        ],
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\SA\AppData\Local\Google\Chrome\Application\chrome.exe",
        ],
        "edge": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ],
        "opera": [
            r"C:\Users\SA\AppData\Local\Programs\Opera\opera.exe",
            r"C:\Program Files\Opera\opera.exe",
        ],
    }

    def __init__(self) -> None:
        self._driver = None
        self._current_browser: Optional[str] = None
        # BUG-DESC-002 FIX: serial access lock for single browser instance
        self._scrape_lock = threading.Lock()
        # Per-scrape outputs — reset at start of each English scrape
        self._last_gallery_urls: List[str] = []
        self._last_gallery_photos: List[Dict] = []

    # ── Driver setup ─────────────────────────────────────────────────────────

    def _find_binary(self, browser: str) -> Optional[str]:
        for path in self._BROWSER_PATHS.get(browser, []):
            if os.path.exists(path):
                return path
        import shutil
        path_names = {
            "brave":  ["brave", "brave.exe", "brave-browser"],
            "opera":  ["opera", "opera.exe"],
            "chrome": ["chrome", "chrome.exe", "google-chrome"],
            "edge":   ["msedge", "msedge.exe"],
        }
        for name in path_names.get(browser, []):
            found = shutil.which(name)
            if found and os.path.exists(found):
                logger.info("Selenium: %s found via PATH: %s", browser, found)
                return found
        return None

    def _gpu_flags(self) -> List[str]:
        return [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-gpu-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-infobars",
            "--start-maximized",
            "--disable-background-networking",
            "--disable-sync",
            "--no-first-run",
            "--log-level=3",
        ]

    def _chrome_options(self, binary: str) -> Any:
        from selenium.webdriver.chrome.options import Options
        cfg = get_settings()
        o = Options()
        o.binary_location = binary
        if cfg.HEADLESS_BROWSER:
            o.add_argument("--headless=new")
        for f in self._gpu_flags():
            o.add_argument(f)
        o.add_argument(f"--user-agent={_random_user_agent()}")
        o.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        o.add_experimental_option("useAutomationExtension", False)
        return o

    def _edge_options(self) -> Any:
        from selenium.webdriver.edge.options import Options
        cfg = get_settings()
        o = Options()
        if cfg.HEADLESS_BROWSER:
            o.add_argument("--headless=new")
        for f in self._gpu_flags():
            o.add_argument(f)
        o.add_argument(f"--user-agent={_random_user_agent()}")
        o.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        o.add_experimental_option("useAutomationExtension", False)
        return o

    def _chrome_service(self):
        from selenium.webdriver.chrome.service import Service as ChromeService
        cached = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "drivers", "chromedriver.exe",
        )
        if os.path.exists(cached):
            logger.debug("ChromeService: using cached driver %s", cached)
            return ChromeService(cached)
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.core.os_manager import ChromeType
            path = ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
            logger.info("ChromeService: webdriver-manager driver %s", path)
            return ChromeService(path)
        except Exception as wdm_exc:
            logger.warning("ChromeService: webdriver-manager failed: %s", wdm_exc)
        logger.warning("ChromeService: falling back to Selenium auto-detect (may fail)")
        return ChromeService()

    def _edge_service(self):
        from selenium.webdriver.edge.service import Service as EdgeService
        try:
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            path = EdgeChromiumDriverManager().install()
            logger.debug("EdgeService: webdriver-manager driver %s", path)
            return EdgeService(path)
        except Exception:
            return EdgeService()

    def _chrome_options_with_tmpprofile(self, binary: str) -> Any:
        opts = self._chrome_options(binary)
        uid  = f"bsp_{os.getpid()}_{threading.get_ident()}"
        tmp  = os.path.join(os.environ.get("TEMP", "C:\\Temp"), uid)
        opts.add_argument(f"--user-data-dir={tmp}")
        opts.add_argument("--no-default-browser-check")
        opts.add_argument("--disable-default-apps")
        opts.add_argument("--window-size=1920,1080")
        try:
            opts._arguments.remove("--start-maximized")
        except (ValueError, AttributeError):
            pass
        return opts

    def _init_driver(self) -> bool:
        from selenium import webdriver
        order = [
            ("brave",  lambda b: webdriver.Chrome(
                service=self._chrome_service(),
                options=self._chrome_options_with_tmpprofile(b))),
            ("opera",  lambda b: webdriver.Chrome(
                service=self._chrome_service(),
                options=self._chrome_options_with_tmpprofile(b))),
            ("edge",   lambda _: webdriver.Edge(
                service=self._edge_service(),
                options=self._edge_options())),
            ("chrome", lambda b: webdriver.Chrome(
                service=self._chrome_service(),
                options=self._chrome_options_with_tmpprofile(b))),
        ]
        for browser_name, factory in order:
            binary = self._find_binary(browser_name)
            if browser_name not in ("edge",) and not binary:
                continue
            driver = None
            try:
                driver = factory(binary) if binary else factory(None)
                driver.implicitly_wait(10)
                cfg = get_settings()
                driver.set_page_load_timeout(cfg.SCRAPER_REQUEST_TIMEOUT)
                driver.get("about:blank")
                self._driver = driver
                self._current_browser = browser_name
                logger.info("Selenium: %s started", browser_name.capitalize())
                return True
            except Exception as exc:
                if driver is not None:
                    try:
                        driver.quit()
                    except Exception:
                        pass
                logger.warning("Selenium: %s unavailable -- %s", browser_name, str(exc)[:100])
        logger.error("Selenium: no browser available. Install Brave or Chrome.")
        return False

    def _ensure_driver(self) -> bool:
        if self._driver is None:
            return self._init_driver()
        return True

    def _reinit_driver(self) -> bool:
        try:
            if self._driver:
                self._driver.quit()
        except Exception:
            pass
        self._driver = None
        return self._init_driver()

    # ── Language setup via CDP ────────────────────────────────────────────────

    def _set_language(self, language: str) -> None:
        """Inject language via CDP headers + cookie (3-vector approach)."""
        locale = LANG_COOKIE_LOCALE.get(language, language)
        accept = LANG_ACCEPT.get(language, "en-GB,en;q=0.9")

        try:
            self._driver.delete_all_cookies()
            logger.debug("Selenium: cleared all cookies before language=%s", language)
        except Exception as e:
            logger.debug("Selenium: delete_all_cookies failed: %s", e)

        try:
            self._driver.execute_cdp_cmd(
                "Network.setExtraHTTPHeaders",
                {"headers": {"Accept-Language": accept}},
            )
        except Exception as e:
            logger.debug("CDP Accept-Language failed: %s", e)

        try:
            expire_ts = int(time.time()) + 86400 * 365
            self._driver.execute_cdp_cmd("Network.setCookies", {"cookies": [{
                "name": "selectedLanguage", "value": locale,
                "domain": ".booking.com", "path": "/",
                "secure": False, "httpOnly": False, "expires": expire_ts,
            }]})
        except Exception as e:
            logger.debug("CDP cookie failed: %s — trying add_cookie fallback", e)
            try:
                if "booking.com" in (self._driver.current_url or ""):
                    self._driver.add_cookie({
                        "name": "selectedLanguage", "value": locale,
                        "domain": ".booking.com", "path": "/",
                    })
            except Exception:
                pass

    # ── Hotel content detection ───────────────────────────────────────────────

    def _wait_for_hotel_content(self, timeout: int = 30) -> bool:
        """FIX-029: Detect hotel page content. Returns True if confirmed."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        selectors = [
            (By.CSS_SELECTOR, "[data-testid='title']"),
            (By.CSS_SELECTOR, "[data-testid='property-description']"),
            (By.CSS_SELECTOR, "[data-testid='review-score-component']"),
            (By.ID,           "hp_facilities_box"),
            (By.CSS_SELECTOR, "h2.pp-header__title"),
            (By.CSS_SELECTOR, "#maxotelRoomArea"),
            (By.CSS_SELECTOR, "[id='b2hotelPage']"),
            (By.CSS_SELECTOR, ".bui-review-score"),
        ]

        try:
            WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located(selectors[0])
            )
            logger.debug("Hotel confirmed via: %s", selectors[0][1])
            time.sleep(1.5)
            return True
        except Exception:
            pass

        for by, sel in selectors[1:]:
            try:
                WebDriverWait(self._driver, 3).until(
                    EC.presence_of_element_located((by, sel))
                )
                logger.debug("Hotel confirmed via: %s", sel)
                time.sleep(1.5)
                return True
            except Exception:
                continue

        try:
            WebDriverWait(self._driver, 10).until(
                lambda d: "booking.com" in (d.title or "").lower()
            )
            cfg = get_settings()
            time.sleep(getattr(cfg, "PAGE_LOAD_WAIT", 3))
            return True
        except Exception:
            pass

        cfg = get_settings()
        time.sleep(getattr(cfg, "PAGE_LOAD_WAIT", 3))
        return False

    # ── Page interaction ──────────────────────────────────────────────────────

    def _close_popups(self) -> None:
        from selenium.webdriver.common.by import By
        for sel in [
            "button[aria-label='Dismiss sign-in info.']",
            "button[data-testid='close-banner']",
            "button.bui_button_close",
            "[data-testid='cookie-consent-accept']",
            "button#onetrust-accept-btn-handler",
        ]:
            try:
                self._driver.find_element(By.CSS_SELECTOR, sel).click()
                time.sleep(0.5)
                break
            except Exception:
                continue

    def _scroll_page(self) -> None:
        try:
            cfg = get_settings()
            iterations = getattr(cfg, "SCROLL_ITERATIONS", 5)
            for i in range(iterations):
                self._driver.execute_script(f"window.scrollTo(0, {(i+1)*1000});")
                time.sleep(0.3)
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            self._driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.3)
        except Exception:
            pass

    def _open_gallery_and_extract_images(self) -> bool:
        """
        Open photo gallery modal and extract all image data.

        BUG-IMG-003 FIX (v48): extract URLs after gallery scroll.
        NEW-PHOTOS-001 (v49):  also extract full hotelPhotos JS metadata
          (id_photo, thumb_url, large_url, highres_url with k= params,
          alt, orientation, photo_width, photo_height, created).
          Stored in self._last_gallery_photos for use by ImageDownloader.
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Reset per-scrape outputs
        self._last_gallery_urls = []
        self._last_gallery_photos = []

        MODAL_SEL = "[data-testid='GalleryGridViewModal-wrapper']"
        triggers  = [
            "[data-testid='bui-gallery-modal-trigger']",
            "[data-testid='hp-gallery-open-bui']",
            "button[data-testid*='photo']",
            "[data-testid='b2hotelPage-hero-photos-wrapper']",
            "[data-testid='photosCarouselGalleryImage']",
            ".bh-photo-grid-thumb",
            "img[src*='bstatic.com/xdata/images/hotel/']",
        ]
        opened = False
        for sel in triggers:
            try:
                elem = WebDriverWait(self._driver, 5).until(
                    EC.element_to_be_clickable(("css selector", sel))
                )
                self._driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                time.sleep(0.5)
                self._driver.execute_script("arguments[0].click();", elem)
                time.sleep(2)
                WebDriverWait(self._driver, 8).until(
                    EC.presence_of_element_located(("css selector", MODAL_SEL))
                )
                logger.info("Gallery opened via: %s", sel)
                opened = True
                break
            except Exception:
                continue

        if not opened:
            logger.debug("Could not open gallery modal — extracting page-level photos only")
            self._last_gallery_urls = self._extract_image_urls_from_page()
            # NEW-PHOTOS-001: also try JS extraction even without modal
            self._last_gallery_photos = self._extract_hotel_photos_js()
            return False

        # Scroll modal to load lazy images
        try:
            modal = self._driver.find_element("css selector", MODAL_SEL)
            prev = 0
            for _ in range(40):
                self._driver.execute_script("arguments[0].scrollTop += 900;", modal)
                time.sleep(0.25)
                imgs = modal.find_elements("tag name", "img")
                if len(imgs) == prev and _ > 5:
                    break
                prev = len(imgs)
            logger.info("Gallery: %d images loaded after scroll", prev)
        except Exception as e:
            logger.debug("Gallery scroll error: %s", e)
        time.sleep(0.5)

        # Extract URL list from DOM (fallback path — used if JS extraction fails)
        self._last_gallery_urls = self._extract_image_urls_from_page()
        logger.info("Gallery: %d unique image URLs extracted", len(self._last_gallery_urls))

        # NEW-PHOTOS-001: extract rich photo metadata from JS (preferred path)
        self._last_gallery_photos = self._extract_hotel_photos_js()
        if self._last_gallery_photos:
            logger.info("Gallery: %d photos with full metadata (hotelPhotos JS)",
                        len(self._last_gallery_photos))
        else:
            logger.info("Gallery: hotelPhotos JS not found — using URL list (%d URLs) as fallback",
                        len(self._last_gallery_urls))

        return True

    def _extract_image_urls_from_page(self) -> List[str]:
        """
        Extract bstatic hotel image URLs from <img> elements.
        BUG-IMG-401 FIX (v49): query params (k= auth token) are now preserved.
        Previously `norm.split("?")[0]` stripped the mandatory auth parameter,
        causing 401 Unauthorized on every image download attempt.

        Note: this method provides the URL-only fallback list. When hotelPhotos JS
        is available (_extract_hotel_photos_js), those URLs are preferred because
        they include all three size variants with correct auth tokens.
        """
        seen: set = set()
        urls: List[str] = []
        try:
            imgs = self._driver.find_elements("tag name", "img")
            for img in imgs:
                for attr in ("src", "data-src", "data-lazy-src"):
                    try:
                        raw = img.get_attribute(attr) or ""
                    except Exception:
                        raw = ""
                    if not raw or "bstatic.com/xdata/images/hotel/" not in raw:
                        continue
                    # Normalise size segment in PATH only — DO NOT touch query params.
                    # BUG-IMG-401 FIX: k= query param is mandatory auth token for bstatic CDN.
                    # Stripping ?k=... → 401 Unauthorized on every download.
                    norm = re.sub(
                        r"/(square\d+|max\d+x?\d*|thumb[^/?]*)\.jpg",
                        "/max_400.jpg",
                        raw,
                    )
                    # ⚠ DO NOT strip query params — the old `norm.split("?")[0]` was REMOVED.
                    if norm not in seen:
                        seen.add(norm)
                        urls.append(norm)
        except Exception as exc:
            logger.warning("_extract_image_urls_from_page error: %s", exc)
        return urls

    def _extract_hotel_photos_js(self) -> List[Dict]:
        """
        NEW-PHOTOS-001 (v49): Extract full photo metadata from hotelPhotos JS variable.

        Reads the raw page_source JavaScript (not DOM elements), so:
        - All three size URLs are available: thumb_url, large_url, highres_url
        - Full k= auth tokens are preserved in each URL
        - Photo metadata is included: id_photo, orientation, dimensions, alt, created

        Returns list of photo dicts compatible with ImageDownloader.download_photo_batch().
        Falls back to empty list if the JS variable is not present.
        """
        try:
            from app.extractor import extract_hotel_photos_from_html
            page_source = self._driver.page_source
            photos = extract_hotel_photos_from_html(page_source)
            logger.info("hotelPhotos JS: %d photos extracted from page source", len(photos))
            return photos
        except Exception as exc:
            logger.warning("_extract_hotel_photos_js error: %s", exc)
            return []

    # ── Main scrape method ────────────────────────────────────────────────────

    def scrape(self, url: str, language: str = "en") -> Optional[str]:
        """
        BUG-DESC-002 FIX (v49): Acquire _scrape_lock before driving the browser.
        Selenium uses a single browser process; concurrent thread access causes
        navigation race conditions → wrong page HTML captured → wrong data saved.
        The lock ensures only one thread navigates at a time. Python's GIL still
        allows other threads to execute non-Selenium code while waiting.
        """
        with self._scrape_lock:
            return self._scrape_locked(url, language)

    def _scrape_locked(self, url: str, language: str = "en") -> Optional[str]:
        """
        Core Selenium scrape logic — called only while _scrape_lock is held.
        FIX-029: Skip _is_blocked() when hotel content confirmed.
        FIX-020: Language mismatch → retry.
        BUG-HTML-CAPTURE: Capture HTML before gallery navigation.
        BUG-GALLERY-LANG: Gallery only for English (images are language-independent).
        BUG-CHAL-PARAM FIX: Strip Booking.com challenge query params.
        """
        if not self._ensure_driver():
            logger.error("Selenium: no driver available")
            return None

        # BUG-CHAL-PARAM FIX: strip challenge parameters
        _CHALLENGE_PARAMS = {"chal_t", "force_referer"}
        parsed = urlparse(url)
        if parsed.query:
            from urllib.parse import parse_qs, urlencode
            qs = {k: v for k, v in parse_qs(parsed.query, keep_blank_values=True).items()
                  if k not in _CHALLENGE_PARAMS}
            clean_query = urlencode(qs, doseq=True)
            url = parsed._replace(query=clean_query).geturl()
            if parsed.query != clean_query:
                logger.info("Selenium: stripped challenge params → %s", url)

        cfg = get_settings()
        lang_mismatch_retries = 0

        for attempt in range(1, 4):
            try:
                if attempt > 1:
                    wait_s = random.uniform(10, 20) * attempt
                    logger.info("Selenium retry %d -- waiting %.0fs -- %s", attempt, wait_s, url)
                    time.sleep(wait_s)
                else:
                    time.sleep(random.uniform(
                        getattr(cfg, "MIN_REQUEST_DELAY", 2),
                        getattr(cfg, "MAX_REQUEST_DELAY", 5),
                    ))

                self._set_language(language)
                self._driver.get(url)

                loaded = self._wait_for_hotel_content()

                if not loaded:
                    page_low = self._driver.page_source.lower()
                    if any(s in page_low for s in ["just a moment", "enable javascript", "ddos-guard", "access denied"]):
                        logger.warning("Selenium: Cloudflare challenge on attempt %d", attempt)
                        continue

                self._close_popups()
                self._scroll_page()

                # BUG-HTML-CAPTURE: capture hotel HTML BEFORE gallery navigation.
                html     = self._driver.page_source
                html_len = len(html)

                if html_len < 5000:
                    logger.warning("Selenium: short HTML (%d bytes)", html_len)
                    continue

                # FIX-020: language mismatch check
                detected = _detect_page_language(html)
                if detected and detected != language:
                    logger.warning("Selenium language mismatch: requested=%s got=%s", language, detected)
                    if lang_mismatch_retries < 2:
                        lang_mismatch_retries += 1
                        _save_debug_html(html, url, f"lang_mismatch_{detected}")
                        time.sleep(random.uniform(20, 40))
                        continue
                    else:
                        logger.error("Selenium language retries exhausted for %s", url)
                        return None

                # BUG-GALLERY-LANG: gallery only for English
                if language == "en":
                    self._open_gallery_and_extract_images()
                    try:
                        self._driver.get(url)
                        self._wait_for_hotel_content()
                    except Exception as nav_exc:
                        logger.debug("Gallery back-navigation (non-critical): %s", nav_exc)

                _save_debug_html(html, url, "selenium_ok")
                return html

            except Exception as exc:
                err = str(exc)
                logger.error("Selenium error attempt %d: %s", attempt, err[:200])
                if "invalid session id" in err.lower():
                    logger.warning("Selenium session dead -- reinitialising driver")
                    if not self._reinit_driver():
                        logger.error("Selenium: could not reinitialise driver -- aborting")
                        return None
                elif attempt < 3:
                    time.sleep(random.uniform(5, 10))

        logger.error("Selenium exhausted retries for %s", url)
        return None

    def close(self) -> None:
        if self._driver:
            try:
                self._driver.quit()
            except Exception:
                pass
            self._driver = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
