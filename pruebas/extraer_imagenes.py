"""
Booking.com Image Gallery Extractor -- v1.1 (fixed)
Extracts structured photo data from Booking.com property gallery grids.

For each hotel URL:
- Navigates to the property page using Brave (headless) via Selenium.
- Opens the photo gallery modal (tries multiple opener selectors).
- Waits for the gallery grid modal to render.
- Extracts every <button data-testid^="gallery-grid-photo-action-"> element.
- For each button, captures:
    • aria-label (from the button attribute)
    • src        (from the inner <img> tag)
- Persists two CSV files:
    _Calidad__images1.csv  -> url ; aria-label ; src        (one row per image)
    _Calidad__images2.csv  -> url ; count(aria-label)       (one row per URL)

Includes NordVPN CLI rotation to minimise request fingerprinting.
"""

import subprocess
import sys
import time
import csv
import zipfile
import platform
import random
import requests
import re
from pathlib import Path
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# -- CONFIG ---------------------------------------------------------
HEADLESS = True
TIMEOUT = 25
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
DEBUG_DIR = Path("debug")
DEBUG_DIR.mkdir(exist_ok=True)

ROTATE_EVERY_N_URLS = 1

BRAVE_BINARY = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
CHROMEDRIVER_DIR = Path(r"C:\SA\Codigo\chromedriver_cache")
CHROMEDRIVER_DIR.mkdir(exist_ok=True)

URLS = [
    "https://www.booking.com/hotel/mk/villa-dvor.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/wild-amp-bolz-emotel.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/vidimo-se.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/ambassador.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/melia-vienna.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/hilton-vienna-plaza.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/steigenberger-herrenhof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/vienna-marriott.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/le-meridien-vienna.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/vienna-stephansdom.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/grand-wien.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/topazz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/the-leo-grand.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/intercontinental-wien.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/the-ritz-carlton-vienna.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/the-guesthouse-vienna.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/sans-souci-wien.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/do-co-vienna.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/sacher-wien.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/hotelimperialwien.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/anantara-palais-hansen-vienna.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/rosewood-vienna-wien.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/almanac-palais-vienna.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/park-hyatt-vienna.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/the-ring.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/palais-coburg-residenz-gmbh.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/andaz-vienna-am-belvedere.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/ibis-budget-graz-city.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/intercityhotel-graz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/mariahilf.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/palais-erzerzog-johann.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/bandbgraz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/motel-one-graz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/mercuregrazcity.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/shome-hotels-smart-business.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/dreiraben.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/zur-steirerstubn.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/strasser.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/zum-dom-betriebsgesmbh.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/feichtinger-graz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/ibis-styles-graz-messe.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/schlossberg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/wasser-palast.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/kai-36-graz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/minihotel-graz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/radisson-graz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/hotelbristolsalzburg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/hotelsachersalzburg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/goldenerhirschsalzburg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/schloss-monchstein.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/posthotel-achenkirch.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/spirodom-admont.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jufa-schloss-rothestein.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/seevilla-altaussee.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/narzissenhotel-bad-aussee.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/blumau.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/thermenwelt-pulverer.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/thermenhotel-ronacher.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jagdhof-hubler.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/garni-birkenhof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/reiter-s-supreme.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/quellenhotel-spa-heiltherme-bad-waltersdorf.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/spa-resort-styria-adults-only-bad-waltersdorf.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jufa-bruck-weitental.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jufa-deutschlandsberg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jufa-donnersbachwald.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/georgi-schloss.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/kaiserhof-ellmau.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/der-larchenhof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/kiwano.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/sporthotel-stock.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/schlosshotel-fiss.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/restaurant-neudorferhof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/weinrefugium-brolli.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jaglhof-by-domanies-kilger.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/schloss-gamlitz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/traumhotel-alpina.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/bergblick-gra-n.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/steinerhaus-berggasthof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/hotel-sued-graz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/aton.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/ferdls-gasthof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/haus-mobene-garni.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/roomz-graz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/wellnesshotel-edelweiss.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/familien-natur-resort-moar-gut.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jufa-grundlsee.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/seehotel-grundlsee.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/travel-charme-ifen.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/adler-hirschegg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/suitehotel-kleinwalsertal.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/schlosshotel-romantica.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/trofana-royal.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/sporthotel-silvretta.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/elisbeth.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/kempinski-hotel-das-tirol.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jufa-judenburg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/stadthotel-schwesterbra-u.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/gasthof-murblick.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/zhero-alps-fashion.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/gasthof-ochnerbauer.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/gasthof-pension-stieber.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/das-friedrich.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/gasthof-rothwangl-hannes.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/naturhotel-waldklause.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/lachtalhaus.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/alpengasthof-tanzstatt.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/gasthof-niggas-kranerwirt.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/dolomitengolf-suites-lavant.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/sonnenburg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/arlberg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/gasthof-post.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/burg-vital-resort.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/blumen-haus-lech.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/der-krallerhof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/cafe-bar-highway.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/grand-lienz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/seehof-loibichl-am-mondsee.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jufa-maria-lankowitz.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jufa-sigmundsberg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/zum-heiligen-geist.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/drei-hasen.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/cocoon.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/spa-jagdhof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/bruecklwirt.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/sporthotel-cinderella.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/das-seekarhaus.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/gesundheits-amp-wellness-resort-oberzeiring.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jufa-pollau.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/jufa-planneralm.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/post-ramsau-am-dachstein.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/pehab-kirchenwirt.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/roesslhof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/bergland-solden.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/central-spa-solden.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/hyperion-salzburg-salzburg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/sheratonsalzburg.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/rosewood-schloss-fuschl.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/raffl-s-st-antoner-hof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/lambrechterhof.en-gb.html?lang=en-gb",
    "https://www.booking.com/hotel/at/waldschlossl-gasthof.en-gb.html?lang=en-gb",
]

# -- SELECTORS -------------------------------------------------------
# Primary: buttons whose data-testid starts with gallery-grid-photo-action-
GALLERY_BUTTON_SELECTOR = 'button[data-testid^="gallery-grid-photo-action-"]'

# Gallery modal wrapper (appears after clicking the gallery opener)
GALLERY_MODAL_SELECTORS = [
    '[data-testid="GalleryGridViewModal-wrapper"]',
    '[data-testid="gallery-modal-grid"]',
]

# Gallery opener selectors (tried in order)
GALLERY_OPENER_SELECTORS = [
    'button[data-testid="property-hero-gallery-desktop"]',
    'a[data-testid="property-hero-photos-gallery"]',
    '[data-testid="property-hero-photos"]',
    '[data-testid="property-hero-gallery"]',
    '.js-bh-photo-modal-trigger',
]

# -- CHROMEDRIVER AUTO-DOWNLOAD -------------------------------------
def get_brave_major_version():
    try:
        ps_cmd = [
            "powershell", "-Command",
            f"(Get-ItemProperty '{BRAVE_BINARY}').VersionInfo.FileVersion"
        ]
        result = subprocess.run(ps_cmd, capture_output=True, text=True, timeout=20)
        version = result.stdout.strip()
        if version and "." in version:
            major = version.split(".")[0]
            print(f"[Driver] Detected Brave version: {version} (major: {major})")
            return major
    except Exception:
        pass
    print("[Driver] Could not auto-detect Brave version.")
    major = input("[Driver] Enter Brave major version (e.g., 148): ").strip()
    return major if major else "148"


def download_chromedriver(major_version):
    zip_path = CHROMEDRIVER_DIR / "chromedriver.zip"
    driver_path = CHROMEDRIVER_DIR / "chromedriver.exe"

    if driver_path.exists():
        print(f"[Driver] Found cached chromedriver: {driver_path}")
        return str(driver_path)

    print(f"[Driver] Downloading chromedriver for Brave major version {major_version}...")
    latest_url = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{major_version}"
    try:
        resp = requests.get(latest_url, timeout=25)
        resp.raise_for_status()
        full_version = resp.text.strip()
        print(f"[Driver] Latest driver version: {full_version}")
    except Exception as e:
        print(f"[Driver] Failed to query version API: {e}")
        sys.exit(1)

    download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{full_version}/win64/chromedriver-win64.zip"
    print(f"[Driver] Downloading from: {download_url}")
    try:
        resp = requests.get(download_url, timeout=60)
        resp.raise_for_status()
        zip_path.write_bytes(resp.content)
        print(f"[Driver] Downloaded {len(resp.content)} bytes")
    except Exception as e:
        print(f"[Driver] Download failed: {e}")
        sys.exit(1)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(CHROMEDRIVER_DIR)

    extracted = CHROMEDRIVER_DIR / "chromedriver-win64" / "chromedriver.exe"
    if extracted.exists():
        extracted.rename(driver_path)
        zip_path.unlink()
        import shutil
        shutil.rmtree(CHROMEDRIVER_DIR / "chromedriver-win64", ignore_errors=True)

    print(f"[Driver] Ready: {driver_path}")
    return str(driver_path)


# -- DRIVER SETUP ---------------------------------------------------
def get_driver():
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--lang=en-GB")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.binary_location = BRAVE_BINARY

    major = get_brave_major_version()
    driver_exe = download_chromedriver(major)

    service = Service(executable_path=driver_exe)
    driver = webdriver.Chrome(service=service, options=opts)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver


# -- NORDVPN --------------------------------------------------------
def nordvpn(texto="", max_reintentos=3, backoff_inicial=5):
    intentos = 0
    backoff = backoff_inicial

    nordvpn_paises = [
        "Jersey", "Glasgow", "Adelaide","Argentina","Brasil", "Brisbane", "Melbourne","Perth", "Sydney", "Sweden", "Switzerland", "Belgium", "Denmark", "Norway","Poland", "Ireland", "Czech Republic", "Cyprus", "Finland", "Serbia", "Austria",
        "Slovakia", "Slovenia", "Bulgaria", "Hungary", "Latvia", "Romania", "Portugal","Luxembourg", "Italy", "Greece", "Estonia", "Iceland", "Albania", "Cyprus","Croatia", "Moldova", "Georgia", "Lithuania", "Canada", "Barcelona"
    ]

    while intentos < max_reintentos:
        try:
            print(f"nordvpn :  cambio de IP - {texto}")
            time.sleep(backoff)
            backoff *= 3

            pais_aleatorio = random.choice(nordvpn_paises)

            command = f'nordvpn -c -g "{pais_aleatorio}"'

            time.sleep(6)
            resultado = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if resultado.returncode != 0:
                print("Error:")
                print(resultado.stderr)
                intentos += 1
                continue

            print(f"IP cambiada exitosamente.........: {pais_aleatorio} ")
            print(f"{command} \n")
            time.sleep(40)
            return True

        except Exception as e:
            print(f"nordvpn {intentos} - {texto} \n Error inesperado:\n {e}")
            return False

    return True


# -- DEBUG & UTILS --------------------------------------------------
def save_debug(driver, slug, stage):
    ts = int(time.time())
    html_path = DEBUG_DIR / f"{slug}_{stage}_{ts}.html"
    png_path = DEBUG_DIR / f"{slug}_{stage}_{ts}.png"
    try:
        html_path.write_text(driver.page_source, encoding="utf-8")
        driver.save_screenshot(str(png_path))
        print(f"    [DEBUG] Saved: {html_path.name} + {png_path.name}")
    except Exception as e:
        print(f"    [DEBUG] Failed to save debug files: {e}")


def scroll_to_lazy_load(driver):
    print("    [SCROLL] Scrolling to trigger lazy load...")
    for i in range(5):
        driver.execute_script(f"window.scrollBy(0, {800 + i*200});")
        time.sleep(2.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)


def find_element_with_fallbacks(driver, selectors, by=By.CSS_SELECTOR, timeout=5):
    for sel in selectors:
        try:
            el = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, sel))
            )
            print(f"    [SELECTOR] Matched: {sel}")
            return el
        except Exception:
            continue
    return None


def clean_text(text):
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\r", " ")
    text = " ".join(text.split())
    return text.strip()


# -- GALLERY MODAL --------------------------------------------------
def open_gallery_modal(driver):
    """
    Attempts to open the photo gallery modal by clicking known opener elements.
    Returns True if an opener was clicked, False otherwise.
    """
    for sel in GALLERY_OPENER_SELECTORS:
        try:
            opener = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
            )
            opener.click()
            print(f"    [GALLERY] Clicked opener: {sel}")
            time.sleep(4)
            return True
        except Exception:
            continue

    # Fallback: try clicking the first large hero image
    try:
        hero_img = driver.find_element(
            By.CSS_SELECTOR,
            '[data-testid="property-hero"] img, .k2-hp--gallery-header img, .bh-photo-modal-trigger img'
        )
        hero_img.click()
        print("    [GALLERY] Clicked hero image fallback")
        time.sleep(4)
        return True
    except Exception:
        pass

    return False


def wait_for_gallery_modal(driver, timeout=TIMEOUT):
    """Wait until the gallery modal wrapper or grid is present in the DOM."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ', '.join(GALLERY_MODAL_SELECTORS)))
        )
        return True
    except Exception:
        return False


def scroll_inside_modal(driver):
    """Scroll inside the gallery modal to ensure all lazy elements are rendered."""
    try:
        modal = driver.find_element(By.CSS_SELECTOR, '[data-testid="GalleryGridViewModal-wrapper"]')
        print("    [SCROLL] Scrolling inside gallery modal...")
        for i in range(8):
            driver.execute_script("arguments[0].scrollBy(0, 1000);", modal)
            time.sleep(1.5)
    except Exception:
        # If no modal scroll container, scroll the whole window
        scroll_to_lazy_load(driver)


# -- EXTRACTION LOGIC ------------------------------------------------
def extract_images(driver, url):
    hotel_slug = urlparse(url).path.strip("/").split("/")[-1]
    print(f"[->] Processing {hotel_slug} ...")

    # Validate URL
    url = url.strip()
    if not url:
        print(f"[!] Empty URL, skipping...")
        return [], 0

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Navigation with retry
    max_retries = 3
    for attempt in range(max_retries):
        try:
            driver.get(url)
            print(f"    [NAV] URL loaded successfully (attempt {attempt + 1})")
            break
        except Exception as e:
            print(f"    [NAV] Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                print(f"    [!] All navigation attempts failed for {url}")
                save_debug(driver, hotel_slug, "nav_failed")
                return [], 0

    print("    [WAIT] Page loaded. Waiting 15s before extraction...")
    time.sleep(15)

    # Accept cookies
    try:
        accept_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "button[aria-label*='Consent'], button[aria-label*='accept'], "
                "#onetrust-accept-btn-handler, .a83ed08757"))
        )
        accept_btn.click()
        time.sleep(2)
    except Exception:
        pass

    scroll_to_lazy_load(driver)

    # --- OPEN GALLERY MODAL -----------------------------------------
    modal_opened = open_gallery_modal(driver)
    if not modal_opened:
        print("    [!] Could not locate or click gallery opener.")
        save_debug(driver, hotel_slug, "no_gallery_opener")
        return [], 0

    # --- WAIT FOR MODAL TO RENDER -----------------------------------
    if not wait_for_gallery_modal(driver):
        print("    [!] Gallery modal did not appear in DOM.")
        save_debug(driver, hotel_slug, "modal_not_found")
        return [], 0
    print("    [GALLERY] Modal rendered.")

    # --- SCROLL TO LOAD ALL IMAGES --------------------------------
    scroll_inside_modal(driver)
    time.sleep(2)

    # --- EXTRACT BUTTONS --------------------------------------------
    buttons = []
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, GALLERY_BUTTON_SELECTOR)
        print(f"    [EXTRACT] Found {len(buttons)} gallery button(s).")
    except Exception as e:
        print(f"    [!] Error locating gallery buttons: {e}")
        save_debug(driver, hotel_slug, "no_gallery_buttons")
        return [], 0

    rows = []
    for idx, btn in enumerate(buttons):
        try:
            # aria-label: prefer button attribute
            aria_label = btn.get_attribute("aria-label") or ""
            if not aria_label:
                # Fallback: inner img aria-label
                try:
                    img = btn.find_element(By.TAG_NAME, "img")
                    aria_label = img.get_attribute("aria-label") or ""
                except Exception:
                    pass

            # src: from inner <img>
            src = ""
            try:
                img = btn.find_element(By.TAG_NAME, "img")
                src = img.get_attribute("src") or ""
            except Exception:
                pass

            aria_label = clean_text(aria_label)
            src = clean_text(src)

            rows.append({
                "url": url,
                "aria_label": aria_label,
                "src": src,
            })
            print(f"    [IMG-{idx+1}] aria-label={aria_label[:60]}... | src={src[:80]}...")
        except Exception as e:
            print(f"    [!] Error processing button {idx}: {e}")

    count = len(rows)
    if count == 0:
        print("    [!] No image data extracted.")
        save_debug(driver, hotel_slug, "no_image_data")
    else:
        print(f"    [SUMMARY] {count} image rows extracted")

    return rows, count


# -- MAIN -----------------------------------------------------------
def main():
    driver = get_driver()
    print("[INIT] Driver initialized. Waiting 3s for stability...")
    time.sleep(3)

    csv1_path = OUTPUT_DIR / "_Calidad__images1.csv"
    csv2_path = OUTPUT_DIR / "_Calidad__images2.csv"

    file1_exists = csv1_path.exists() and csv1_path.stat().st_size > 0
    file2_exists = csv2_path.exists() and csv2_path.stat().st_size > 0

    with open(csv1_path, "a", newline="", encoding="utf-8") as csv1, \
         open(csv2_path, "a", newline="", encoding="utf-8") as csv2:

        writer1 = csv.DictWriter(
            csv1,
            fieldnames=["url", "aria_label", "src"],
            delimiter=";"
        )
        writer2 = csv.DictWriter(
            csv2,
            fieldnames=["url", "count(aria-label)"],
            delimiter=";"
        )

        if not file1_exists:
            writer1.writeheader()
            print(f"[CSV] Header written to {csv1_path}")
        if not file2_exists:
            writer2.writeheader()
            print(f"[CSV] Header written to {csv2_path}")

        try:
            for idx, url in enumerate(URLS, 1):
                url = url.strip()
                if not url:
                    print(f"[!] Empty URL at index {idx}, skipping...")
                    continue

                if idx > 1 and (idx - 1) % ROTATE_EVERY_N_URLS == 0:
                    nordvpn(texto=f"URL {idx-1}/{len(URLS)}")

                print(f"\n{'='*60}")
                print(f"[{idx}/{len(URLS)}] {url}")
                print("="*60)

                rows, count = extract_images(driver, url)

                for row in rows:
                    writer1.writerow(row)
                csv1.flush()

                writer2.writerow({
                    "url": url,
                    "count(aria-label)": count,
                })
                csv2.flush()

                print(f"    [CSV] Saved {len(rows)} rows to _Calidad__images1.csv")
                print(f"    [CSV] Saved count={count} to _Calidad__images2.csv")

                time.sleep(3)
        finally:
            driver.quit()
            print("[CSV] Files closed.")

    print("\n" + "="*80)
    print("PREVIEW _Calidad__images1.csv (first 15 rows)")
    print("="*80)
    try:
        with open(csv1_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for i, row in enumerate(reader):
                if i > 15:
                    break
                print("; ".join(row))
    except Exception as e:
        print(f"[!] Could not preview _Calidad__images1.csv: {e}")

    print("\n" + "="*80)
    print("PREVIEW _Calidad__images2.csv")
    print("="*80)
    try:
        with open(csv2_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                print("; ".join(row))
    except Exception as e:
        print(f"[!] Could not preview _Calidad__images2.csv: {e}")


if __name__ == "__main__":
    main()
