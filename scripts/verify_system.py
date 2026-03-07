"""
BookingScraper Pro v6.0 - System Verification Script
=====================================================
Platform : Windows 11 + Python 3.11+
Run      : python scripts/verify_system.py

Corrections Applied (v46):
- BUG-015 : app.core.database  → app.database
- BUG-016 : app.core.config    → app.config
- BUG-017 : app.core.database  → app.database  (second reference)
- BUG-018 : app.tasks.celery_app → app.celery_app
- GENERAL : psycopg2 replaced with psycopg (v3)
- GENERAL : No bare except: clauses; KeyboardInterrupt / SystemExit re-raised.
"""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import NamedTuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"[OK] Loaded .env from {env_file}")
    else:
        print(f"[WARN] .env not found at {env_file}")
except ImportError:
    print("[WARN] python-dotenv not installed")


class CheckResult(NamedTuple):
    name  : str
    passed: bool
    message: str


results: list[CheckResult] = []


def check(name: str, passed: bool, message: str) -> bool:
    results.append(CheckResult(name, passed, message))
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}: {message}")
    return passed


# ── 1. Python ──────────────────────────────────────────────────────────────
print("\n=== 1. Python Version ===")
pv = sys.version_info
check("Python >= 3.11", pv >= (3, 11), f"{pv.major}.{pv.minor}.{pv.micro}")
check("Windows 11 platform", sys.platform == "win32",
      f"{'OK' if sys.platform == 'win32' else 'WARNING: ' + sys.platform}")

# ── 2. Packages ─────────────────────────────────────────────────────────────
print("\n=== 2. Python Packages ===")
PACKAGES = {
    "fastapi"         : "fastapi",
    "uvicorn"         : "uvicorn",
    "sqlalchemy"      : "sqlalchemy",
    "psycopg (v3)"    : "psycopg",        # BUG FIX: NOT psycopg2
    "pydantic"        : "pydantic",
    "pydantic_settings": "pydantic_settings",
    "celery"          : "celery",
    "redis"           : "redis",
    "loguru"          : "loguru",
    "dotenv"          : "dotenv",
    "cloudscraper"    : "cloudscraper",
    "bs4"             : "bs4",
    "selenium"        : "selenium",
    "requests"        : "requests",
    "pandas"          : "pandas",
}
for display, mod in PACKAGES.items():
    try:
        m = importlib.import_module(mod)
        check(f"pkg:{display}", True, getattr(m, "__version__", "installed"))
    except ImportError as exc:
        check(f"pkg:{display}", False, str(exc))

# ── 3. App Modules (BUG-015 to BUG-018 FIX) ─────────────────────────────────
print("\n=== 3. App Module Imports ===")
APP_MODULES = {
    "app.database"      : "BUG-015/017 FIX: was app.core.database",
    "app.config"        : "BUG-016 FIX: was app.core.config",
    "app.celery_app"    : "BUG-018 FIX: was app.tasks.celery_app",
    "app.models"        : "ORM models",
    "app.scraper_service": "Scraper service",
    "app.tasks"         : "Celery tasks",
}
for mod_path, note in APP_MODULES.items():
    try:
        importlib.import_module(mod_path)
        check(f"import:{mod_path}", True, note)
    except EnvironmentError as exc:
        check(f"import:{mod_path}", False, f"EnvironmentError (missing .env creds): {exc}")
    except ImportError as exc:
        check(f"import:{mod_path}", False, str(exc))
    except Exception as exc:
        check(f"import:{mod_path}", False, f"{type(exc).__name__}: {exc}")

# ── 4. Database ──────────────────────────────────────────────────────────────
print("\n=== 4. Database ===")
try:
    from app.database import get_pool_status, test_connection
    db_ok = test_connection(max_retries=2, base_delay=1.0)
    check("PostgreSQL connection", db_ok, "Connected")
    if db_ok:
        pool = get_pool_status()
        check("Connection pool", pool.get("status") == "ok", str(pool))
except EnvironmentError as exc:
    check("PostgreSQL connection", False, f"Credentials: {exc}")
except Exception as exc:
    check("PostgreSQL connection", False, f"{type(exc).__name__}: {exc}")

# ── 5. Redis ─────────────────────────────────────────────────────────────────
print("\n=== 5. Redis / Memurai ===")
try:
    import redis as _redis
    r = _redis.Redis(host=os.environ.get("REDIS_HOST","localhost"),
                     port=int(os.environ.get("REDIS_PORT","6379")),
                     socket_timeout=5)
    check("Redis ping", r.ping(), "Connected")
except ImportError:
    check("Redis ping", False, "redis not installed")
except _redis.exceptions.ConnectionError as exc:
    check("Redis ping", False, f"Connection refused: {exc}")
except Exception as exc:
    check("Redis ping", False, f"{type(exc).__name__}: {exc}")

# ── 6. Celery ────────────────────────────────────────────────────────────────
print("\n=== 6. Celery App ===")
try:
    from app.celery_app import celery_app   # BUG-018 FIX
    check("celery_app import", celery_app is not None,
          f"Broker: {celery_app.conf.broker_url}")
except Exception as exc:
    check("celery_app import", False, f"{type(exc).__name__}: {exc}")

# ── 7. Windows ───────────────────────────────────────────────────────────────
print("\n=== 7. Windows Environment ===")
if sys.platform == "win32":
    # NordVPN
    try:
        r = subprocess.run(["nordvpn","--version"], capture_output=True, text=True, timeout=10)
        check("NordVPN CLI", r.returncode == 0, r.stdout.strip() or "Available")
    except FileNotFoundError:
        check("NordVPN CLI", False, "not found (optional if VPN_ENABLED=false)")
    except Exception as exc:
        check("NordVPN CLI", False, str(exc))

    # pywin32
    try:
        import win32service
        check("pywin32", True, "Available for Windows Service")
    except ImportError:
        check("pywin32", False, "Not installed — optional for Windows Service")

    # Directories
    from app.config import get_settings
    cfg = get_settings()
    for label, d in [("Images dir", cfg.IMAGES_DIR), ("Log dir", cfg.LOG_DIR)]:
        p = Path(d)
        check(label, True, f"{'exists' if p.exists() else 'will be created'}: {p}")
else:
    check("Windows platform", False, f"Running on {sys.platform}")

# ── 8. Environment Variables ──────────────────────────────────────────────────
print("\n=== 8. Environment Variables ===")
for var in ["DB_USER","DB_PASSWORD","DB_NAME"]:
    val = os.environ.get(var,"")
    check(f"ENV:{var}", bool(val), "Set" if val else "MISSING")
for var in ["DB_HOST","REDIS_HOST","LOG_LEVEL"]:
    val = os.environ.get(var,"")
    check(f"ENV:{var} (optional)", True, val or "(default)")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "="*60)
passed = sum(1 for r in results if r.passed)
failed = sum(1 for r in results if not r.passed)
print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed}")
if failed == 0:
    print("\n✅ ALL CHECKS PASSED — System ready")
    sys.exit(0)
else:
    print(f"\n⚠️  {failed} check(s) failed:")
    for r in results:
        if not r.passed:
            print(f"  ✗ {r.name}: {r.message}")
    sys.exit(1)
