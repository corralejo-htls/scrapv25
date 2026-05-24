"""
test_config.py — BookingScraper Pro v6.0.0 Build 107
=====================================================
Diagnóstico de carga de configuración sobre la clase de producción
app.config.Settings.

PROPÓSITO (Build 107 — NEUTRALIZADO):
  Las versiones anteriores de este script demostraban un modo de fallo de
  pydantic-settings usando clases de juguete con campos `List[str]`
  (SettingsA/B/C/D) e insinuaban que app/config.py necesitaba un parche
  llamado "FIX-CFG-001" con una fuente `_CommaAwareEnvSource`.

  Eso era ENGAÑOSO. La clase Settings de producción declara
  VPN_COUNTRIES y ENABLED_LANGUAGES como `str` (NO `List[str]`), por lo que
  pydantic-settings NO ejecuta json.loads sobre el valor y el formato
  separado por comas se acepta de forma nativa, sin ningún override. El
  troceado a lista se realiza aguas abajo con el patrón canónico
  cfg.ENABLED_LANGUAGES.split(",") (ver app/completeness_service.py,
  app/main.py, app/scraper_service.py, app/api_export_system.py).

  Por tanto NO existe ni se necesita FIX-CFG-001 en app/config.py. Este
  script ahora valida el comportamiento REAL de app.config.Settings:
    TEST 1 — Los defaults parsean correctamente.
    TEST 2 — Un valor comma en os.environ carga sin error.
    TEST 3 — Un valor comma en un archivo .env real carga sin error.
    TEST 4 — El accesor canónico get_settings().<campo>.split(",") limpia
             espacios y produce una lista correcta.

NOTA sobre 'en' primero: la regla de negocio "'en' siempre primero" se
  aplica AGUAS ABAJO (scraper_service.build_language_list y la capa API),
  NO en el parseo de configuración. Este test solo verifica el parseo fiel
  del orden tal cual aparece en .env, no el reordenado posterior.

Código de salida: 0 si todo OK, 1 si hay algún FAIL (apto para CI).
Ejecutar desde C:\\BookingScraper con el .venv activo:  python test_config.py
"""
import os
import sys
import tempfile

# Settings exige DB_USER/DB_PASSWORD (campos requeridos sin default). Se
# proveen credenciales dummy para poder instanciar; no afectan a la lógica
# de listas comma que este test verifica.
os.environ.setdefault("DB_USER", "test_user")
os.environ.setdefault("DB_PASSWORD", "test_password")

import pydantic
import pydantic_settings
from app.config import Settings, get_settings, reset_settings

LIST_KEYS = ("VPN_COUNTRIES", "ENABLED_LANGUAGES")
EXPECTED_DEFAULT_LANGS = ["en", "es", "de", "it", "fr", "pt"]

_passed = 0
_failed = 0


def _ok(msg: str) -> None:
    global _passed
    _passed += 1
    print(f"  [OK] {msg}")


def _fail(msg: str) -> None:
    global _failed
    _failed += 1
    print(f"  [FAIL] {msg}")


def _clean_list_keys() -> None:
    """Aísla cada test: quita las claves de lista de os.environ."""
    for k in LIST_KEYS:
        os.environ.pop(k, None)


def _split(value: str) -> list:
    """Patrón canónico de consumo usado en toda la app."""
    return [x.strip() for x in value.split(",") if x.strip()]


print("=" * 60)
print("  BookingScraper -- Diagnóstico de configuración (Settings)")
print("=" * 60)
print()
print(f"[INFO] Python:            {sys.version.split()[0]}")
print(f"[INFO] pydantic:          {pydantic.__version__}")
print(f"[INFO] pydantic-settings: {pydantic_settings.__version__}")
print(f"[INFO] Campos tipados como str (no List[str]): {', '.join(LIST_KEYS)}")
print("[INFO] -> el formato comma se acepta de forma nativa; el split se")
print("        realiza aguas abajo. No se requiere FIX-CFG-001.")
print()

# ── TEST 1: defaults ──────────────────────────────────────────────────────
print("[TEST 1] Defaults de Settings (sin .env, entorno limpio)")
_clean_list_keys()
try:
    s = Settings(_env_file=None)
    langs = _split(s.ENABLED_LANGUAGES)
    countries = _split(s.VPN_COUNTRIES)
    if langs == EXPECTED_DEFAULT_LANGS:
        _ok(f"ENABLED_LANGUAGES default = {langs}")
    else:
        _fail(f"ENABLED_LANGUAGES default inesperado = {langs}")
    if "en" in langs:
        _ok("'en' presente en ENABLED_LANGUAGES (obligatorio por _API_.md)")
    else:
        _fail("'en' ausente en ENABLED_LANGUAGES")
    if countries and all(isinstance(c, str) and c for c in countries):
        _ok(f"VPN_COUNTRIES default = {countries}")
    else:
        _fail(f"VPN_COUNTRIES default inválido = {countries}")
except Exception as e:  # noqa: BLE001
    _fail(f"{type(e).__name__}: {e}")
print()

# ── TEST 2: comma en os.environ ─────────────────────────────────────────────
print("[TEST 2] Valor comma en os.environ (tipado str -> sin SettingsError)")
_clean_list_keys()
os.environ["VPN_COUNTRIES"] = "Spain,Germany,France"
os.environ["ENABLED_LANGUAGES"] = "en,es,de"
try:
    s = Settings(_env_file=None)
    got_c = _split(s.VPN_COUNTRIES)
    got_l = _split(s.ENABLED_LANGUAGES)
    _ok(f"VPN_COUNTRIES     = {got_c}") if got_c == ["Spain", "Germany", "France"] \
        else _fail(f"VPN_COUNTRIES     = {got_c}")
    _ok(f"ENABLED_LANGUAGES = {got_l}") if got_l == ["en", "es", "de"] \
        else _fail(f"ENABLED_LANGUAGES = {got_l}")
except Exception as e:  # noqa: BLE001
    _fail(f"{type(e).__name__}: {e}  (el tipado str debería evitar este error)")
_clean_list_keys()
print()

# ── TEST 3: comma en archivo .env real ──────────────────────────────────────
print("[TEST 3] Valor comma en archivo .env real (escenario de producción)")
_clean_list_keys()
tmp_path = None
try:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".env", delete=False, encoding="utf-8"
    ) as f:
        f.write("VPN_COUNTRIES=Spain,Germany,France,Netherlands,Italy\n")
        f.write("ENABLED_LANGUAGES=en,es,de,fr,it\n")
        tmp_path = f.name

    s = Settings(_env_file=tmp_path)
    got_c = _split(s.VPN_COUNTRIES)
    got_l = _split(s.ENABLED_LANGUAGES)
    _ok(f"VPN_COUNTRIES     = {got_c}") \
        if got_c == ["Spain", "Germany", "France", "Netherlands", "Italy"] \
        else _fail(f"VPN_COUNTRIES     = {got_c}")
    _ok(f"ENABLED_LANGUAGES = {got_l}") \
        if got_l == ["en", "es", "de", "fr", "it"] \
        else _fail(f"ENABLED_LANGUAGES = {got_l}")
except Exception as e:  # noqa: BLE001
    _fail(f"{type(e).__name__}: {e}")
finally:
    if tmp_path:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
print()

# ── TEST 4: accesor canónico get_settings().<campo>.split(",") ──────────────
print("[TEST 4] Accesor canónico get_settings().ENABLED_LANGUAGES.split(',')")
_clean_list_keys()
# os.environ tiene mayor precedencia que el .env del proyecto -> determinista
# en cualquier máquina. Se incluyen espacios a propósito para verificar limpieza.
os.environ["ENABLED_LANGUAGES"] = " en , es , de "
try:
    reset_settings()  # invalida el cache lru de get_settings()
    cfg = get_settings()
    langs = _split(cfg.ENABLED_LANGUAGES)
    _ok(f"split limpio (sin espacios sobrantes) = {langs}") \
        if langs == ["en", "es", "de"] else _fail(f"split = {langs}")
except Exception as e:  # noqa: BLE001
    _fail(f"{type(e).__name__}: {e}")
finally:
    _clean_list_keys()
    reset_settings()
print()

# ── Resumen ─────────────────────────────────────────────────────────────────
print("=" * 60)
print(f"  RESUMEN: {_passed} OK / {_failed} FAIL")
if _failed == 0:
    print("  La clase Settings de producción carga y parsea listas comma")
    print("  correctamente. No se requiere ningún parche en app/config.py")
    print("  (el tipado str maneja el formato comma de forma nativa).")
else:
    print("  Hay fallos: revisar el detalle arriba.")
print("=" * 60)

sys.exit(1 if _failed else 0)
