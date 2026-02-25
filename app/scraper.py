"""
BookingScraper/app/scraper.py  v2.8  [FIXED]
Scraper HTTP para Booking.com - BookingScraper Pro

CAMBIOS v2.8 [FIXES DE IDIOMA]:
  [FIX CRÍTICO #1] build_language_url(): ahora ELIMINA el sufijo de idioma
    existente (.es, .de, .en-gb...) antes de añadir el nuevo. Sin este paso,
    una URL base .es.html generaba:
      - para 'en': devolvía .es.html sin cambios (siempre español)
      - para 'de': producía .es.de.html (404 en Booking.com)
  [FIX CRÍTICO #4] Cookie selectedLanguage: añadida constante LANG_COOKIE_LOCALE
    con locales correctos para Booking.com. "en" → "en-gb", "zh" → "zh-cn",
    "no" → "nb", "pt" → "pt-pt". El valor "en" no era reconocido por Booking.com.
  [FIX CRÍTICO #5] LANG_ACCEPT: diccionario completo para los 19 idiomas
    soportados. Antes, 11 idiomas (ar, tr, hu, pl, zh, no, fi, sv, da, ja, ko)
    enviaban Accept-Language: en-US,en;q=0.9, indicando preferencia por inglés.
  [FIX #6] Selenium: delete_cookie("selectedLanguage") antes de add_cookie()
    para garantizar sobreescritura correcta con un driver compartido entre idiomas.
"""
  [FIX CRITICO] cloudscraper: sesion se reinicia en 403 (sesion "envenenada" antes = fallo total)
  [FIX CRITICO] Selenium: _wait_for_hotel_content mejorado — anade og:title y title tag
  [FIX] Deteccion de pagina de consentimiento/CAPTCHA explicita con aviso
  [FIX] Selenium: scrape_hotel() usa get() con retry interno
  [NEW] USE_SELENIUM=False: fallback httpx si cloudscraper falla

CAMBIOS v2.4:
  [FIX CRITICO] invalid session id: driver se RECREA INMEDIATAMENTE dentro del bucle
    de reintentos de scrape_hotel(). Antes, el bucle seguia usando el driver muerto y
    driver.get() tardaba ~26 minutos en timeout por intento (total: 3 x 26min = 78min
    desperdiciados por idioma). Ahora: deteccion en except → close() → reiniciar browser
    → continue (siguiente intento con driver nuevo, sin espera extra).
    Orden de fallback: Brave → Chrome → Edge.

CAMBIOS v2.6:
  [NEW] BookingScraperSelenium._open_gallery_and_extract_images(): abre el modal
    GalleryGridViewModal antes de tomar page_source, haciendo scroll para cargar
    todas las imágenes lazy. Resuelve el problema de descargar solo ~8 fotos en
    lugar de las 65-97 totales del hotel (foto principal + photo book completo).

CAMBIOS v2.5:
  [FIX CRITICO] _try_brave/chrome/edge/opera(): anadido return self.driver.
    El recovery block de v2.4 usaba self.driver = try_func(), pero try_func() no
    retornaba nada (None implicito). La asignacion sobreescribia el self.driver que
    la funcion acababa de inicializar, dejandolo en None. Resultado: success nunca
    se ponia en True, el recovery siempre abortaba con "No se pudo reiniciar ningun
    browser" aunque Brave/Chrome/Edge si se hubiese iniciado correctamente.
    _setup_driver() no estaba afectado porque llama fn() sin asignar el retorno.
"""

import random
import re
import time
from pathlib import Path
from typing import Optional, Dict

from loguru import logger

from app.config import settings


# ─────────────────────────────────────────────────────────────────────────────
# User-Agents Chrome real en Windows 11
# ─────────────────────────────────────────────────────────────────────────────
USER_AGENTS_WIN = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

# ─────────────────────────────────────────────────────────────────────────────
# [FIX BUG #4] Mapeo de código ISO 639-1 → locale que Booking.com acepta
# en la cookie selectedLanguage. Booking.com NO reconoce "en" como valor
# válido; requiere "en-gb" o "en-us". Para otros idiomas el código de 2 letras
# suele coincidir, excepto chino (zh-cn), noruego (nb) y portugués (pt-pt).
# ─────────────────────────────────────────────────────────────────────────────
LANG_COOKIE_LOCALE: dict = {
    "en": "en-gb",   "es": "es",    "de": "de",    "fr": "fr",
    "it": "it",      "pt": "pt-pt", "nl": "nl",    "ru": "ru",
    "ar": "ar",      "tr": "tr",    "hu": "hu",    "pl": "pl",
    "zh": "zh-cn",   "no": "nb",    "fi": "fi",    "sv": "sv",
    "da": "da",      "ja": "ja",    "ko": "ko",
}

# [FIX BUG #5] Mapeo completo ISO 639-1 → header Accept-Language.
# El diccionario anterior solo cubría 8 de 19 idiomas; los restantes 11
# quedaban con "en-US,en;q=0.9", lo que indicaba al servidor que se
# prefería inglés, anulando la URL y la cookie de idioma.
LANG_ACCEPT: dict = {
    "en": "en-US,en;q=0.9",
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

BOOKING_BYPASS_COOKIES = {
    "OptanonAlertBoxClosed": "2024-01-01T00:00:00.000Z",
    "OptanonConsent":        "isGpcEnabled=0&datestamp=Mon+Jan+01+2024&version=202401.1.0&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1",
    "bkng_sso_ses":          "e30=",
    "cors":                  "1",
    "_ga":                   f"GA1.1.{random.randint(100000000,999999999)}.1700000000",
    "_gid":                  f"GA1.1.{random.randint(100000000,999999999)}.1700000000",
    # [FIX BUG #4] "en-gb" es el locale correcto para inglés en Booking.com
    "selectedLanguage":      "en-gb",
    "selectedCurrency":      "EUR",
}

# Señales de página real de hotel (usado para validar HTML recibido)
HOTEL_PAGE_SIGNALS = [
    "property-description",
    "hp_facilities_box",
    "maxotelroomarea",
    "reviewscore",
    "review-score",
    "b2hotelpage",
    "hoteldetails",
]

# Señales de página de consent/captcha (fallo)
BLOCK_SIGNALS = [
    "just a moment",         # Cloudflare challenge
    "access denied",
    "403 forbidden",
    "privacymanager",
    "cookie-consent",
    "please verify you are a human",
    "enable javascript",
    "checking your browser",
]


def _is_hotel_page(html: str) -> bool:
    html_low = html.lower()
    return any(s in html_low for s in HOTEL_PAGE_SIGNALS)


def _is_blocked(html: str) -> bool:
    html_low = html.lower()
    return any(s in html_low for s in BLOCK_SIGNALS)


# ─────────────────────────────────────────────────────────────────────────────
# SCRAPER CLOUDSCRAPER
# ─────────────────────────────────────────────────────────────────────────────

class BookingScraperCloudScraper:
    """
    Scraper usando cloudscraper.
    v2.3: la sesión se reinicia si recibe 403 (sesión 'envenenada').
    """

    def __init__(self, timeout: int = None):
        self.timeout = timeout or settings.BROWSER_TIMEOUT
        self._session = None
        self._blocked_count = 0  # NEW: contador de bloqueos para forzar reset de sesión

    def _get_session(self, force_new: bool = False):
        """
        Devuelve la sesión de cloudscraper.
        Si force_new=True o la sesión anterior fue bloqueada, crea una nueva.
        """
        if self._session is not None and not force_new:
            return self._session

        try:
            import cloudscraper

            # Si había sesión vieja, cerrarla
            if self._session is not None:
                try:
                    self._session.close()
                except Exception:
                    pass
                logger.debug("  🔄 Reseteando sesión cloudscraper (era bloqueada)")

            self._session = cloudscraper.create_scraper(
                browser={
                    "browser": "chrome",
                    "platform": "windows",
                    "desktop": True,
                },
                delay=5,
            )
            # Inyectar cookies GDPR con User-Agent aleatorio
            ua = random.choice(USER_AGENTS_WIN)
            self._session.headers.update({"User-Agent": ua})

            for k, v in BOOKING_BYPASS_COOKIES.items():
                self._session.cookies.set(k, v, domain=".booking.com")

            self._blocked_count = 0
            logger.debug(f"  ✓ Nueva sesión cloudscraper | UA: {ua[:60]}")
            return self._session

        except ImportError:
            logger.error("❌ cloudscraper no instalado: pip install cloudscraper --break-system-packages")
            raise

    @staticmethod
    def _save_debug_html(url: str, html: str, label: str = ""):
        try:
            debug_dir = Path(settings.LOGS_PATH) / "debug"
            debug_dir.mkdir(parents=True, exist_ok=True)
            slug  = url.split("/")[-1][:40].replace(".", "_")
            ts    = int(time.time())
            fname = f"{label}_{slug}_{ts}.html" if label else f"{slug}_{ts}.html"
            fpath = debug_dir / fname
            fpath.write_text(html[:120000], encoding="utf-8", errors="ignore")
            logger.debug(f"  📄 HTML guardado: {fpath.name}")
        except Exception:
            pass

    def scrape_hotel(self, url: str, language: str = "en") -> Optional[Dict]:
        logger.info(f"🔍 [cloudscraper] {url}")

        for attempt in range(1, settings.MAX_RETRIES + 1):
            # [FIX] Si ya hubo 2+ bloqueos con esta sesión, forzar sesión nueva
            force_new = (attempt > 1 and self._blocked_count >= 2)
            try:
                delay = random.uniform(settings.MIN_REQUEST_DELAY, settings.MAX_REQUEST_DELAY)
                if attempt > 1:
                    delay = min(delay * attempt * 1.5, 25.0)
                    logger.info(f"  ⏳ Reintento {attempt} — esperando {delay:.1f}s...")
                time.sleep(delay)

                session  = self._get_session(force_new=force_new)

                # [FIX BUG #4] Actualizar cookie selectedLanguage con locale correcto.
                # _get_session() la fija en "en-gb" por defecto; aquí la sobreescribimos
                # usando LANG_COOKIE_LOCALE para que Booking.com sirva el contenido
                # en el idioma correcto (e.g. "de", "fr", "zh-cn", "en-gb", etc.)
                locale = LANG_COOKIE_LOCALE.get(language, language)
                session.cookies.set("selectedLanguage", locale, domain=".booking.com")

                response = session.get(
                    url,
                    timeout=self.timeout,
                    headers={
                        # [FIX BUG #5] Usar LANG_ACCEPT completo (19 idiomas)
                        "Accept-Language": LANG_ACCEPT.get(language, "en-US,en;q=0.9"),
                        "Referer":         "https://www.google.com/search?q=booking+hotel",
                        "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    },
                    allow_redirects=True,
                )

                status   = response.status_code
                html_content = response.text
                html_len     = len(html_content)

                logger.debug(f"  HTTP {status} | {html_len:,} bytes")

                # ── Manejo de estados HTTP ─────────────────────────────────────
                if status == 403:
                    self._blocked_count += 1
                    logger.warning(
                        f"  ⚠️ HTTP 403 — bloqueado (bloqueos={self._blocked_count}) "
                        f"— sesión será reseteada en próximo intento"
                    )
                    self._save_debug_html(url, html_content, "403")
                    time.sleep(random.uniform(15, 30))
                    continue

                if status == 429:
                    wait = int(response.headers.get("Retry-After", 90))
                    logger.warning(f"  ⚠️ HTTP 429 — Rate Limit, esperando {wait}s")
                    time.sleep(wait)
                    continue

                if status == 404:
                    logger.error("  ✗ HTTP 404 — URL no existe")
                    return None

                if status >= 500:
                    logger.warning(f"  ⚠️ HTTP {status} — error servidor")
                    time.sleep(random.uniform(10, 20))
                    continue

                # ── Validar contenido recibido ─────────────────────────────────
                if html_len < 5000:
                    logger.warning(f"  ⚠️ HTML corto ({html_len} bytes)")
                    self._save_debug_html(url, html_content, "short")
                    self._blocked_count += 1
                    time.sleep(random.uniform(8, 15))
                    continue

                if _is_blocked(html_content):
                    logger.warning(f"  ⚠️ Página de bloqueo/captcha detectada")
                    self._save_debug_html(url, html_content, "blocked")
                    self._blocked_count += 1
                    time.sleep(random.uniform(20, 40))
                    continue

                if not _is_hotel_page(html_content):
                    logger.warning(f"  ⚠️ HTML no parece página de hotel ({html_len} bytes)")
                    self._save_debug_html(url, html_content, "not_hotel")
                    if attempt < settings.MAX_RETRIES:
                        time.sleep(random.uniform(5, 10))
                        continue

                # ── Extracción ─────────────────────────────────────────────────
                m     = re.search(r"<title[^>]*>(.*?)</title>", html_content, re.I | re.S)
                title = m.group(1).strip() if m else "(sin título)"
                logger.debug(f"  📄 '{title}' | {html_len:,}b")

                from app.extractor import BookingExtractor
                extractor = BookingExtractor(html_content, language)
                data      = extractor.extract_all()
                data["url"]         = url
                data["http_status"] = status
                data["html_length"] = html_len
                data["page_title"]  = title

                if data.get("name"):
                    self._blocked_count = 0  # éxito → reset contador bloqueos
                    logger.success(
                        f"  ✓ '{data['name']}' | rating={data.get('rating')} | {html_len:,}b"
                    )
                else:
                    logger.warning(f"  ⚠️ Sin nombre | '{title}' | {html_len:,}b")
                    self._save_debug_html(url, html_content, "no_name")

                return data

            except Exception as e:
                logger.error(f"  ✗ Error (intento {attempt}): {e}")
                if attempt < settings.MAX_RETRIES:
                    time.sleep(random.uniform(3, 8))

        logger.error(f"✗ Reintentos agotados: {url}")
        return None

    def close(self):
        if self._session:
            try:
                self._session.close()
            except Exception:
                pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


# ─────────────────────────────────────────────────────────────────────────────
# SCRAPER SELENIUM
# ─────────────────────────────────────────────────────────────────────────────

class BookingScraperSelenium:
    """
    Scraper con ChromeDriver real.
    v2.3: _wait_for_hotel_content mejorado — detecta título og/title como señal,
    no solo elementos internos del hotel.
    """

    def __init__(self):
        self.driver = None
        self._setup_driver()

    BROWSER_PATHS = {
        "brave":  [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        ],
        "opera":  [
            r"C:\Users\SA\AppData\Local\Programs\Opera\opera.exe",
            r"C:\Program Files\Opera\opera.exe",
        ],
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\SA\AppData\Local\Google\Chrome\Application\chrome.exe",
        ],
        "edge":   [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ],
    }

    def _setup_driver(self):
        order = [
            ("Brave",  self._try_brave),
            ("Chrome", self._try_chrome),
            ("Edge",   self._try_edge),
            ("Opera",  self._try_opera),
        ]
        errors = []
        for name, fn in order:
            try:
                fn()
                return
            except Exception as e:
                msg = str(e).splitlines()[0][:120]
                logger.warning(f"  {name} no disponible: {msg}")
                errors.append(f"{name}: {msg}")

        raise RuntimeError(
            "Ningún navegador disponible.\n"
            "Instala Brave: https://brave.com/\n"
            "O Google Chrome: https://www.google.com/chrome/"
        )

    @staticmethod
    def _gpu_flags():
        return [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-gpu-sandbox",
            "--use-gl=swiftshader",
            "--disable-software-rasterizer",
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-infobars",
            "--start-maximized",
            "--disable-background-networking",
            "--disable-sync",
            "--metrics-recording-only",
            "--no-first-run",
            "--safebrowsing-disable-auto-update",
            "--log-level=3",
        ]

    def _chrome_options_with_binary(self, binary_path: str):
        from selenium.webdriver.chrome.options import Options
        o = Options()
        o.binary_location = binary_path
        if settings.HEADLESS_BROWSER:
            o.add_argument("--headless=new")
        for flag in self._gpu_flags():
            o.add_argument(flag)
        o.add_argument(f"--user-agent={random.choice(USER_AGENTS_WIN)}")
        o.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        o.add_experimental_option("useAutomationExtension", False)
        return o

    def _edge_options(self):
        from selenium.webdriver.edge.options import Options
        o = Options()
        if settings.HEADLESS_BROWSER:
            o.add_argument("--headless=new")
        for flag in self._gpu_flags():
            o.add_argument(flag)
        o.add_argument(f"--user-agent={random.choice(USER_AGENTS_WIN)}")
        o.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        o.add_experimental_option("useAutomationExtension", False)
        return o

    def _find_binary(self, browser: str) -> str:
        import os
        for path in self.BROWSER_PATHS.get(browser, []):
            if os.path.exists(path):
                return path
        raise FileNotFoundError(f"Ejecutable de {browser} no encontrado")

    def _try_brave(self):
        from selenium import webdriver
        binary = self._find_binary("brave")
        options = self._chrome_options_with_binary(binary)
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(settings.BROWSER_TIMEOUT)
        logger.success("✓ Brave iniciado")
        return self.driver  # [FIX v2.5] necesario para recovery block en scrape_hotel()

    def _try_chrome(self):
        from selenium import webdriver
        binary = self._find_binary("chrome")
        options = self._chrome_options_with_binary(binary)
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(settings.BROWSER_TIMEOUT)
        logger.success("✓ Chrome iniciado")
        return self.driver  # [FIX v2.5]

    def _try_edge(self):
        from selenium import webdriver
        self.driver = webdriver.Edge(options=self._edge_options())
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(settings.BROWSER_TIMEOUT)
        logger.success("✓ Edge iniciado")
        return self.driver  # [FIX v2.5]

    def _try_opera(self):
        from selenium import webdriver
        binary = self._find_binary("opera")
        options = self._chrome_options_with_binary(binary)
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(settings.BROWSER_TIMEOUT)
        logger.success("✓ Opera iniciado")
        return self.driver  # [FIX v2.5]

    def scrape_hotel(self, url: str, language: str = "en") -> Optional[Dict]:
        """
        v2.3: retry interno con re-navegación si la primera carga falla.
        No depende de un solo intento.
        """
        if self.driver is None:
            logger.error("✗ Driver Selenium no disponible")
            return None

        for attempt in range(1, 4):  # hasta 3 reintentos por URL
            try:
                logger.info(f"🔍 [Selenium] {url} (intento {attempt})")

                if attempt > 1:
                    wait_s = random.uniform(10, 20) * attempt
                    logger.info(f"  ⏳ Esperando {wait_s:.0f}s antes de reintentar...")
                    time.sleep(wait_s)
                else:
                    time.sleep(random.uniform(
                        settings.MIN_REQUEST_DELAY,
                        settings.MAX_REQUEST_DELAY
                    ))

                # [v2.7 FIX] Inyectar cookie selectedLanguage para que Booking.com
                # sirva el contenido en el idioma correcto. Requiere navegar primero
                # al dominio para poder establecer la cookie.
                try:
                    # [FIX BUG #5] Establecer Accept-Language vía CDP usando LANG_ACCEPT completo
                    self.driver.execute_cdp_cmd(
                        "Network.setExtraHTTPHeaders",
                        {"headers": {"Accept-Language": LANG_ACCEPT.get(language, "en-US,en;q=0.9")}}
                    )
                    # Inyectar cookie de idioma (sin navegar si ya estamos en booking.com)
                    current_url = self.driver.current_url or ""
                    if "booking.com" not in current_url:
                        self.driver.get("https://www.booking.com")
                        time.sleep(1)
                    # [FIX BUG #6] Eliminar cookie anterior antes de añadir la nueva.
                    # Con un solo driver para todos los idiomas, add_cookie() puede no
                    # sobreescribir la cookie existente en algunos navegadores.
                    try:
                        self.driver.delete_cookie("selectedLanguage")
                    except Exception:
                        pass
                    # [FIX BUG #4] Usar locale correcto (e.g. "en-gb" no "en")
                    locale = LANG_COOKIE_LOCALE.get(language, language)
                    self.driver.add_cookie({
                        "name":   "selectedLanguage",
                        "value":  locale,
                        "domain": ".booking.com",
                        "path":   "/",
                    })
                    logger.debug(f"  🌐 Idioma configurado: {language} (locale={locale})")
                except Exception as lang_err:
                    logger.debug(f"  ⚠️ No se pudo configurar idioma CDP/cookie: {lang_err}")

                self.driver.get(url)

                # Espera inteligente a contenido del hotel
                loaded = self._wait_for_hotel_content()

                if not loaded:
                    html_check = self.driver.page_source.lower()
                    if any(s in html_check for s in ["just a moment", "checking your browser", "access denied"]):
                        logger.warning(f"  ⚠️ Cloudflare challenge detectado (intento {attempt})")
                        continue  # retry
                    # No challenge pero tampoco página hotel → intentar de todas formas

                self._close_popups()
                self._scroll_page()

                # [v2.6] Abrir galería completa para capturar TODAS las imágenes.
                # El modal GalleryGridViewModal queda abierto en el DOM y el
                # extractor lo captura en su paso 1 (selector GalleryGridViewModal-wrapper).
                self._open_gallery_and_extract_images()

                html_content = self.driver.page_source
                html_len     = len(html_content)
                page_title   = self.driver.title or ""

                logger.debug(f"  📄 '{page_title}' | {html_len:,} bytes")

                if html_len < 5000:
                    logger.warning(f"  ⚠️ HTML muy corto ({html_len}b) — posible bloqueo")
                    continue

                if _is_blocked(html_content):
                    logger.warning(f"  ⚠️ Página de bloqueo detectada")
                    continue

                from app.extractor import BookingExtractor
                extractor = BookingExtractor(html_content, language)
                data      = extractor.extract_all()
                data["url"]         = url
                data["html_length"] = html_len
                data["page_title"]  = page_title

                if data.get("name"):
                    logger.success(
                        f"  ✓ '{data['name']}' | rating={data.get('rating')} | {html_len:,}b"
                    )
                    return data
                else:
                    logger.warning(f"  ⚠️ Sin nombre extraído | '{page_title}' | {html_len:,}b")
                    # Si la página cargó pero no hay nombre → guardar debug
                    self._save_debug_html(url, html_content)
                    # Si hay título de página que no sea error → aun así devolver
                    if page_title and "booking.com" in page_title.lower():
                        return data  # el extractor hará lo que pueda

            except Exception as e:
                err_msg = str(e)
                logger.error(f"  ✗ Selenium error (intento {attempt}): {err_msg[:200]}")

                # [FIX v2.4] invalid session id = browser crasheó completamente.
                # driver.get() con sesion muerta puede tardar ~26 minutos en timeout.
                # Solucion: recrear el driver inmediatamente sin esperar ese timeout.
                if "invalid session id" in err_msg.lower():
                    logger.warning(f"  ⚠️ Session Brave muerta (intento {attempt}) — recreando driver...")
                    try:
                        self.close()
                    except Exception:
                        pass
                    try:
                        # Reinicializar usando el mismo flujo que __init__
                        from selenium.webdriver.chrome.options import Options as ChromeOptions
                        self.driver = None
                        success = False
                        for browser_name, try_func in [
                            ("Brave",  self._try_brave),
                            ("Chrome", self._try_chrome),
                            ("Edge",   self._try_edge),
                        ]:
                            try:
                                self.driver = try_func()
                                if self.driver:
                                    logger.info(f"  ✓ {browser_name} reiniciado (intento {attempt})")
                                    success = True
                                    break
                            except Exception as be:
                                logger.debug(f"  {browser_name} fallo al reiniciar: {be}")
                        if not success:
                            logger.error("  ✗ No se pudo reiniciar ningun browser — abortando hotel")
                            return None
                    except Exception as re_err:
                        logger.error(f"  ✗ Error recreando driver: {re_err}")
                        return None
                    # Reintentar inmediatamente sin espera extra
                    continue

                if attempt < 3:
                    time.sleep(random.uniform(5, 10))

        logger.error(f"✗ Reintentos Selenium agotados: {url}")
        return None

    def _wait_for_hotel_content(self, timeout: int = 30) -> bool:
        """
        v2.3: Detecta contenido de hotel O simplemente que la página cargó
        (via título o cualquier elemento conocido).
        Devuelve True si parece página real de hotel, False si no.
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        import selenium.common.exceptions as SE

        # Selectores en orden de más fiable a menos
        selectors = [
            # Estructura 2024/2025 con data-testid
            (By.CSS_SELECTOR,  "[data-testid='title']"),
            (By.CSS_SELECTOR,  "[data-testid='property-description']"),
            (By.CSS_SELECTOR,  "[data-testid='review-score-component']"),
            # Estructura clásica
            (By.ID,            "hp_facilities_box"),
            (By.CSS_SELECTOR,  "h2.pp-header__title"),
            (By.CSS_SELECTOR,  "#maxotelRoomArea"),
            # Señal genérica de que la página terminó de cargar
            (By.CSS_SELECTOR,  "[id='b2hotelPage']"),
            (By.CSS_SELECTOR,  ".bui-review-score"),
        ]

        wait = WebDriverWait(self.driver, timeout)
        for by, selector in selectors:
            try:
                wait.until(EC.presence_of_element_located((by, selector)))
                logger.debug(f"  ✓ Hotel detectado via: {selector}")
                time.sleep(1.5)
                return True
            except SE.TimeoutException:
                continue
            except Exception:
                continue

        # Fallback: esperar a que el <title> contenga "booking.com"
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "booking.com" in (d.title or "").lower()
            )
            logger.debug("  ✓ Título booking.com detectado (fallback)")
            time.sleep(settings.PAGE_LOAD_WAIT)
            return True
        except Exception:
            pass

        logger.debug("  ⚠️ Ningún selector de hotel detectado, usando delay base")
        time.sleep(settings.PAGE_LOAD_WAIT)
        return False

    def _save_debug_html(self, url: str, html: str):
        try:
            debug_dir = Path(settings.LOGS_PATH) / "debug"
            debug_dir.mkdir(parents=True, exist_ok=True)
            slug  = url.split("/")[-1][:40].replace(".", "_")
            ts    = int(time.time())
            fpath = debug_dir / f"selenium_{slug}_{ts}.html"
            fpath.write_text(html[:120000], encoding="utf-8", errors="ignore")
            logger.debug(f"  📄 HTML Selenium guardado: {fpath.name}")
        except Exception:
            pass

    def _open_gallery_and_extract_images(self) -> bool:
        """
        [v2.6 - NEW] Abre el modal de galería completa de Booking.com y hace scroll
        para que se carguen todas las imágenes lazy (photo book).

        Booking.com muestra ~8 fotos en la página principal. Las restantes (hasta 90+)
        solo aparecen en el modal GalleryGridViewModal que se abre al hacer clic en
        cualquier foto del carrusel o en el botón "Ver todas las fotos".

        Returns:
            True si el modal se abrió y se completó el scroll; False en caso contrario.
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import selenium.common.exceptions as SE

        MODAL_SELECTOR = "[data-testid='GalleryGridViewModal-wrapper']"

        # --- Selectores del trigger de la galería (Booking.com 2024-2026) ---
        gallery_triggers = [
            # Botón explícito "Ver todas las fotos" / "See all X photos"
            "[data-testid='bui-gallery-modal-trigger']",
            "[data-testid='hp-gallery-open-bui']",
            "button[data-testid*='photo']",
            # Zona hero de fotos (click en primera foto)
            "[data-testid='b2hotelPage-hero-photos-wrapper']",
            "[data-testid='photosCarouselGalleryImage']",
            ".bh-photo-grid-thumb",
            # Fallback: primera imagen del CDN bstatic visible
            "img[src*='bstatic.com/xdata/images/hotel/']",
        ]

        opened = False
        for selector in gallery_triggers:
            try:
                elem = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", elem)
                time.sleep(2)

                # Confirmar que el modal se abrió
                WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, MODAL_SELECTOR))
                )
                logger.info(f"  📸 Galería abierta via: {selector}")
                opened = True
                break
            except Exception:
                continue

        if not opened:
            logger.debug("  ⚠️ No se pudo abrir el modal de galería — solo fotos de página principal")
            return False

        # --- Scroll dentro del modal para cargar imágenes lazy ---
        try:
            modal = self.driver.find_element(By.CSS_SELECTOR, MODAL_SELECTOR)
            prev_count = 0
            for _ in range(40):  # máximo 40 scrolls (~3000 imágenes)
                self.driver.execute_script("arguments[0].scrollTop += 900;", modal)
                time.sleep(0.25)
                imgs = modal.find_elements(By.TAG_NAME, "img")
                if len(imgs) == prev_count and _ > 5:
                    break  # sin nuevas imágenes → llegamos al fondo
                prev_count = len(imgs)

            final_count = len(modal.find_elements(By.TAG_NAME, "img"))
            logger.info(f"  📷 Galería completa: {final_count} imágenes en DOM")
        except Exception as e:
            logger.debug(f"  ⚠️ Error en scroll galería: {e}")

        time.sleep(0.5)
        return True

    def _close_popups(self):
        from selenium.webdriver.common.by import By
        for selector in [
            "button[aria-label='Dismiss sign-in info.']",
            "button[data-testid='close-banner']",
            "button.bui_button_close",
            "[data-testid='cookie-consent-accept']",
            "button#onetrust-accept-btn-handler",
        ]:
            try:
                self.driver.find_element(By.CSS_SELECTOR, selector).click()
                time.sleep(0.5)
                break
            except Exception:
                continue

    def _scroll_page(self):
        try:
            for i in range(settings.SCROLL_ITERATIONS):
                self.driver.execute_script(f"window.scrollTo(0, {(i+1)*1000});")
                time.sleep(0.3)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            # Volver arriba para capturar header
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.3)
        except Exception:
            pass

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
            except Exception:
                pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


# ─────────────────────────────────────────────────────────────────────────────
# FÁBRICA
# ─────────────────────────────────────────────────────────────────────────────

class BookingScraper:
    """Selecciona el scraper según USE_SELENIUM en .env."""

    def __new__(cls):
        if settings.USE_SELENIUM:
            logger.info("Scraper: Selenium (USE_SELENIUM=True)")
            return BookingScraperSelenium()
        else:
            logger.info("Scraper: cloudscraper (bypass Cloudflare)")
            return BookingScraperCloudScraper()


# ─────────────────────────────────────────────────────────────────────────────
# URL MULTI-IDIOMA
# ─────────────────────────────────────────────────────────────────────────────

def build_language_url(base_url: str, language: str) -> str:
    """
    Construye la URL de Booking.com para el idioma solicitado.

    [FIX BUG #1 CRÍTICO] Antes de añadir el sufijo de idioma nuevo, se elimina
    cualquier sufijo de idioma existente en la URL (.es, .de, .fr, .en-gb, etc.).
    Sin este paso, una URL base como '.../hotel.es.html' genera:
      - Para 'en': devuelve '.../hotel.es.html' sin cambios  ← siempre español
      - Para 'de': devuelve '.../hotel.es.de.html'           ← 404 en Booking.com
      - Para 'fr': devuelve '.../hotel.es.fr.html'           ← 404 en Booking.com

    Patrón eliminado: .<2 letras>[opcional: -<2-4 letras>].html
    Ejemplos: .es.html, .de.html, .en-gb.html, .zh-cn.html, .pt-br.html
    """
    # PASO 1: Eliminar sufijo de idioma existente → obtener URL base neutra
    clean_url = re.sub(
        r'\.[a-z]{2}(?:-[a-z]{2,4})?\.html$',
        '.html',
        base_url.strip(),
        flags=re.IGNORECASE,
    )
    if not clean_url.endswith('.html'):
        clean_url += '.html'

    # PASO 2: Añadir sufijo del idioma solicitado
    ext = settings.LANGUAGE_EXT.get(language, f".{language}")
    if not ext:     # inglés base ("en" → ext = "") → sin sufijo adicional
        return clean_url

    return clean_url[:-5] + ext + '.html'
