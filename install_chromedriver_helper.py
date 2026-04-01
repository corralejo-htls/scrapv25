"""
BookingScraper Pro v48 - ChromeDriver installer helper
Called by install_chromedriver.bat
Downloads the ChromeDriver version that matches Brave Browser.
"""
import os, sys, urllib.request, json, zipfile, shutil, subprocess, tempfile

BRAVE_PATHS = [
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
]
DRIVERS_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers")
DRIVER_PATH  = os.path.join(DRIVERS_DIR, "chromedriver.exe")

def get_brave_version(brave_exe: str) -> str:
    """Read Brave version from binary using PowerShell GetFileVersionInfo."""
    try:
        result = subprocess.run(
            ["powershell", "-command",
             f"(Get-Item '{brave_exe}').VersionInfo.FileVersion"],
            capture_output=True, text=True, timeout=10,
        )
        v = result.stdout.strip()
        if v and v[0].isdigit():
            return v
    except Exception:
        pass
    # Fallback: read from Last Version file
    last_ver_path = os.path.join(os.path.dirname(brave_exe), "Last Version")
    if os.path.exists(last_ver_path):
        return open(last_ver_path).read().strip()
    return ""

def download_chromedriver(brave_version: str) -> bool:
    """Download ChromeDriver matching brave_version from Chrome for Testing API."""
    major = brave_version.split(".")[0]
    print(f"  Brave {brave_version} -> buscando ChromeDriver {major}.x ...")

    api = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
    try:
        with urllib.request.urlopen(api, timeout=30) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(f"  ERROR consultando API: {e}")
        return False

    candidates = []
    for v in data.get("versions", []):
        ver = v.get("version", "")
        if ver.startswith(major + "."):
            for d in v.get("downloads", {}).get("chromedriver", []):
                if d.get("platform") == "win64":
                    candidates.append((ver, d["url"]))

    if not candidates:
        print(f"  ERROR: ChromeDriver {major}.x no encontrado en la API.")
        return False

    candidates.sort(key=lambda x: [int(n) for n in x[0].split(".")])
    best_ver, best_url = candidates[-1]
    print(f"  ChromeDriver disponible: {best_ver}")

    os.makedirs(DRIVERS_DIR, exist_ok=True)
    zip_path = os.path.join(DRIVERS_DIR, "chromedriver_tmp.zip")

    print(f"  Descargando desde Chrome for Testing API...")
    urllib.request.urlretrieve(best_url, zip_path)
    print(f"  OK ({os.path.getsize(zip_path)//1024} KB)")

    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            if member.endswith("chromedriver.exe"):
                with zf.open(member) as src, open(DRIVER_PATH, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                print(f"  Extraido: chromedriver.exe ({os.path.getsize(DRIVER_PATH)//1024} KB)")
                break
    os.remove(zip_path)
    return os.path.exists(DRIVER_PATH)

def try_webdriver_manager() -> bool:
    """Fallback: use webdriver-manager to install ChromeDriver for Brave."""
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.core.os_manager import ChromeType
        path = ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
        os.makedirs(DRIVERS_DIR, exist_ok=True)
        shutil.copy2(path, DRIVER_PATH)
        print(f"  webdriver-manager: {path}")
        return True
    except Exception as e:
        print(f"  webdriver-manager (BRAVE) fallo: {e}")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        path = ChromeDriverManager().install()
        shutil.copy2(path, DRIVER_PATH)
        print(f"  webdriver-manager (standard): {path}")
        return True
    except Exception as e:
        print(f"  webdriver-manager (standard) fallo: {e}")
    return False

def test_driver(brave_exe: str) -> bool:
    """Quick headless test: open Brave and navigate to google.com."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    opts = Options()
    opts.binary_location = brave_exe
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,720")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")

    tmp = tempfile.mkdtemp(prefix="bsp_test_")
    opts.add_argument(f"--user-data-dir={tmp}")

    try:
        svc = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=svc, options=opts)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"  OK - Brave abierto. Titulo pagina: {title}")
        return True
    except Exception as e:
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"  ERROR en test: {str(e)[:200]}")
        return False

def main():
    print()
    # --- Localizar Brave ---
    brave_exe = next((p for p in BRAVE_PATHS if os.path.exists(p)), None)
    if not brave_exe:
        print("[ERROR] Brave no encontrado.")
        print("  Instalar desde https://brave.com o indicar la ruta manualmente.")
        sys.exit(1)
    print(f"[1/4] Brave encontrado: {brave_exe}")

    # --- Leer version ---
    brave_ver = get_brave_version(brave_exe)
    if brave_ver:
        print(f"      Version: {brave_ver}")
    else:
        print("      Version: no detectada automaticamente")
        brave_ver = input("      Ingresa la version (ej: 133.0.6943.141): ").strip()

    # --- Descargar ChromeDriver ---
    print()
    print("[2/4] Descargando ChromeDriver...")
    ok = download_chromedriver(brave_ver)
    if not ok:
        print("      Descarga directa fallo. Intentando webdriver-manager...")
        ok = try_webdriver_manager()
    if not ok:
        print()
        print("[ERROR] No se pudo descargar ChromeDriver automaticamente.")
        print()
        print("  INSTALACION MANUAL:")
        major = brave_ver.split(".")[0] if brave_ver else "133"
        print(f"  1. Ve a: https://googlechromelabs.github.io/chrome-for-testing/")
        print(f"  2. Busca la version {major}.x.x.x")
        print(f"  3. Descarga chromedriver-win64.zip")
        print(f"  4. Extrae chromedriver.exe a: {DRIVER_PATH}")
        print(f"  5. Vuelve a ejecutar install_chromedriver.bat")
        sys.exit(1)

    # --- Verificar driver ---
    print()
    print("[3/4] Verificando chromedriver.exe...")
    try:
        result = subprocess.run([DRIVER_PATH, "--version"],
                                capture_output=True, text=True, timeout=5)
        print(f"  OK - {result.stdout.strip() or result.stderr.strip()}")
    except Exception as e:
        print(f"  WARN: {e}")

    # --- Test funcional ---
    print()
    print("[4/4] Test funcional: Brave + chromedriver.exe...")
    try:
        ok = test_driver(brave_exe)
    except ImportError:
        print("  WARN: selenium no instalado todavia (se instalara con pip install -r requirements.txt)")
        ok = True

    print()
    if ok:
        print("=" * 60)
        print("  INSTALACION EXITOSA")
        print()
        print(f"  ChromeDriver: {DRIVER_PATH}")
        print(f"  Brave:        {brave_exe}")
        print()
        print("  IMPORTANTE: si Brave se actualiza automaticamente,")
        print("  volver a ejecutar install_chromedriver.bat.")
        print()
        print("  Siguiente paso: inicio_rapido.bat")
        print("=" * 60)
    else:
        print("  WARN: test fallo. Revisa los errores arriba.")
        print("  Si el error dice 'version mismatch', Brave se actualizo.")
        print("  Vuelve a ejecutar install_chromedriver.bat.")

if __name__ == "__main__":
    main()
