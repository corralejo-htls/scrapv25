"""
test_config.py - BookingScraper Pro v48
Diagnostico independiente del problema VPN_COUNTRIES / EnvSettingsSource.
Ejecutar desde C:\\BookingScraper con .venv activo: python test_config.py

FIX-TEST-001: os.environ limpiado entre tests (TEST A dejaba JSON en env,
  contaminando TEST B/C que intentan usar formato comma).
FIX-TEST-002: TEST C ahora sustituye AMBAS fuentes (env + dotenv) con
  versiones comma-aware. La version anterior solo sustituia dotenv,
  dejando EnvSettingsSource con json.loads puro -> FAIL.
FIX-TEST-003: Eliminado backslash invalido en docstring (SyntaxWarning).
FIX-TEST-004: Nuevo TEST D verifica lectura desde archivo .env real.
"""
import sys
import os
import json
import tempfile
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, DotEnvSettingsSource, SettingsConfigDict

print("=" * 60)
print("  BookingScraper -- Diagnostico pydantic-settings")
print("=" * 60)
print()

import pydantic
import pydantic_settings
print(f"[INFO] Python:            {sys.version.split()[0]}")
print(f"[INFO] pydantic:          {pydantic.__version__}")
print(f"[INFO] pydantic-settings: {pydantic_settings.__version__}")
print()

import inspect
sig = inspect.signature(BaseSettings.settings_customise_sources)
print("[INFO] Firma real de settings_customise_sources:")
for name, param in sig.parameters.items():
    print(f"         {name}: {param.annotation}")
print()

init_sig = inspect.signature(DotEnvSettingsSource.__init__)
print("[INFO] Firma real de DotEnvSettingsSource.__init__:")
for name, param in init_sig.parameters.items():
    if name != "self":
        print(f"         {name}: {param.annotation} = {param.default!r}")
print()

# ── Importar EnvSettingsSource (disponible en pydantic-settings >= 2.0) ───────
from pydantic_settings import EnvSettingsSource

# ── Clases comma-aware (identicas a las de app/config.py corregido) ──────────
class _CommaAwareDotEnvSource(DotEnvSettingsSource):
    """DotEnv source con soporte para listas comma-separated en archivo .env."""
    def decode_complex_value(self, field_name, field_info, value):
        if not isinstance(value, str):
            return value
        value = value.strip()
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
        if "," in value:
            return [x.strip() for x in value.split(",") if x.strip()]
        return [value] if value else []

class _CommaAwareEnvSource(EnvSettingsSource):
    """
    FIX-CFG-001: os.environ source con soporte para listas comma-separated.
    Sin este override, EnvSettingsSource llama json.loads("Spain,Germany,...")
    y lanza SettingsError ANTES de que model_validator pueda normalizarlo.
    """
    def decode_complex_value(self, field_name, field_info, value):
        if not isinstance(value, str):
            return value
        value = value.strip()
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
        if "," in value:
            return [x.strip() for x in value.split(",") if x.strip()]
        return [value] if value else []

# ── Helper de aislamiento entre tests ────────────────────────────────────────
_TEST_KEYS = ["VPN_COUNTRIES", "ENABLED_LANGUAGES"]

def _clean_env():
    """FIX-TEST-001: elimina las claves de test de os.environ."""
    for k in _TEST_KEYS:
        os.environ.pop(k, None)

# ── TEST A: JSON en os.environ (siempre funciona, sin fix necesario) ──────────
print("[TEST A] os.environ con formato JSON")
_clean_env()
os.environ["VPN_COUNTRIES"]    = '["Spain","Germany","France"]'
os.environ["ENABLED_LANGUAGES"] = '["es","en","de"]'

class SettingsA(BaseSettings):
    VPN_COUNTRIES:    List[str] = Field(default=["Spain"])
    ENABLED_LANGUAGES: List[str] = Field(default=["es"])

try:
    s = SettingsA()
    print(f"  [OK] VPN_COUNTRIES     = {s.VPN_COUNTRIES}")
    print(f"  [OK] ENABLED_LANGUAGES = {s.ENABLED_LANGUAGES}")
except Exception as e:
    print(f"  [FAIL] {e}")
_clean_env()
print()

# ── TEST B: comma en os.environ SIN fix (debe fallar — confirma el bug) ───────
print("[TEST B] os.environ comma SIN _CommaAwareEnvSource (EXPECTED-FAIL)")
print("         Confirma que FIX-CFG-001 es necesario en config.py")
_clean_env()
os.environ["VPN_COUNTRIES"]    = "Spain,Germany,France"
os.environ["ENABLED_LANGUAGES"] = "es,en,de"

class SettingsB(BaseSettings):
    VPN_COUNTRIES:    List[str] = Field(default=["Spain"])
    ENABLED_LANGUAGES: List[str] = Field(default=["es"])

try:
    s = SettingsB()
    print(f"  [UNEXPECTED-OK] VPN_COUNTRIES = {s.VPN_COUNTRIES}")
    print(f"  (pydantic-settings cambio de comportamiento en esta version)")
except Exception as e:
    print(f"  [EXPECTED-FAIL] {type(e).__name__} -- confirma bug en EnvSettingsSource")
_clean_env()
print()

# ── TEST C: comma en os.environ CON _CommaAwareEnvSource (debe pasar) ─────────
print("[TEST C] os.environ comma CON _CommaAwareEnvSource (FIX-CFG-001)")
_clean_env()
os.environ["VPN_COUNTRIES"]    = "Spain,Germany,France"
os.environ["ENABLED_LANGUAGES"] = "es,en,de"

class SettingsC(BaseSettings):
    VPN_COUNTRIES:    List[str] = Field(default=["Spain"])
    ENABLED_LANGUAGES: List[str] = Field(default=["es"])

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):
        init   = kwargs.get("init_settings")
        dotenv = kwargs.get("dotenv_settings")
        if dotenv is None:
            return super().settings_customise_sources(settings_cls, **kwargs)
        # FIX: reemplazar AMBAS fuentes (env + dotenv) con versiones comma-aware
        try:
            comma_env = _CommaAwareEnvSource(settings_cls)
        except Exception:
            comma_env = kwargs.get("env_settings")
        env_file = getattr(dotenv, "env_file", None)
        try:
            comma_dotenv = _CommaAwareDotEnvSource(settings_cls,
                                                    env_file=env_file,
                                                    env_file_encoding="utf-8")
        except TypeError:
            comma_dotenv = _CommaAwareDotEnvSource(settings_cls)
        return (init, comma_env, comma_dotenv)

try:
    s = SettingsC()
    print(f"  [OK] VPN_COUNTRIES     = {s.VPN_COUNTRIES}")
    print(f"  [OK] ENABLED_LANGUAGES = {s.ENABLED_LANGUAGES}")
except Exception as e:
    print(f"  [FAIL] {e}")
_clean_env()
print()

# ── TEST D: archivo .env real con comma (escenario de produccion) ─────────────
print("[TEST D] Archivo .env con formato comma (escenario produccion real)")
_clean_env()

_env_content = (
    "VPN_COUNTRIES=Spain,Germany,France,Netherlands,Italy\n"
    "ENABLED_LANGUAGES=es,en,de,fr,it\n"
)

_tmp_env_path = None
try:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".env", delete=False, encoding="utf-8"
    ) as f:
        f.write(_env_content)
        _tmp_env_path = f.name

    class SettingsD(BaseSettings):
        model_config = SettingsConfigDict(
            env_file=_tmp_env_path, env_file_encoding="utf-8"
        )
        VPN_COUNTRIES:    List[str] = Field(default=["Spain"])
        ENABLED_LANGUAGES: List[str] = Field(default=["es"])

        @classmethod
        def settings_customise_sources(cls, settings_cls, **kwargs):
            init   = kwargs.get("init_settings")
            dotenv = kwargs.get("dotenv_settings")
            if dotenv is None:
                return super().settings_customise_sources(settings_cls, **kwargs)
            try:
                comma_env = _CommaAwareEnvSource(settings_cls)
            except Exception:
                comma_env = kwargs.get("env_settings")
            try:
                comma_dotenv = _CommaAwareDotEnvSource(
                    settings_cls,
                    env_file=_tmp_env_path,
                    env_file_encoding="utf-8",
                )
            except TypeError:
                comma_dotenv = _CommaAwareDotEnvSource(settings_cls)
            return (init, comma_env, comma_dotenv)

    s = SettingsD()
    print(f"  [OK] VPN_COUNTRIES     = {s.VPN_COUNTRIES}")
    print(f"  [OK] ENABLED_LANGUAGES = {s.ENABLED_LANGUAGES}")
except Exception as e:
    print(f"  [FAIL] {e}")
finally:
    if _tmp_env_path:
        try:
            os.unlink(_tmp_env_path)
        except Exception:
            pass
_clean_env()
print()

# ── Resumen ───────────────────────────────────────────────────────────────────
print("=" * 60)
print("  RESUMEN ESPERADO:")
print()
print("  TEST A  JSON en os.environ     -> [OK]")
print("  TEST B  comma SIN fix          -> [EXPECTED-FAIL]  <- confirma bug")
print("  TEST C  comma CON fix env      -> [OK]             <- FIX-CFG-001")
print("  TEST D  comma en archivo .env  -> [OK]")
print()
print("  Si TEST C y TEST D pasan -> app/config.py corregido funciona.")
print("  Si TEST B muestra UNEXPECTED-OK -> pydantic-settings cambio de")
print("  comportamiento en esta version y el fix es inofensivo.")
print("=" * 60)
