"""
verify_system.py — Pre-flight system verification.
Run before starting the application to confirm all dependencies are available.
BookingScraper Pro v6.0.0 Build 63-fix | Windows 11
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def check(name: str, fn, optional: bool = False) -> bool:
    try:
        fn()
        print(f"  [OK]   {name}")
        return True
    except Exception as exc:
        tag = "[INFO]" if optional else "[FAIL]"
        print(f"  {tag}  {name}: {exc}")
        return optional  # optional failures don't count as failures


def main() -> int:
    print("=" * 64)
    print("BookingScraper Pro v6.0.0 Build 63-fix — System Verification")
    print("=" * 64)
    print()

    failures = 0

    # ── Python version ────────────────────────────────────────────────────────
    print("[ Python ]")
    py = sys.version_info
    if py >= (3, 11):
        print(f"  [OK]   Python {py.major}.{py.minor}.{py.micro}")
        if py >= (3, 14):
            print(f"  [INFO] Python 3.14 es pre-release. Para produccion se recomienda 3.11/3.12.")
    else:
        print(f"  [FAIL] Python {py.major}.{py.minor} detectado — se requiere 3.11+")
        failures += 1

    # ── Dependencias críticas ─────────────────────────────────────────────────
    print()
    print("[ Dependencias criticas ]")
    critical = [
        ("fastapi",            lambda: __import__("fastapi")),
        ("uvicorn",            lambda: __import__("uvicorn")),
        ("pydantic",           lambda: __import__("pydantic")),
        ("pydantic-settings",  lambda: __import__("pydantic_settings")),
        ("psycopg (v3)",       lambda: __import__("psycopg")),
        ("SQLAlchemy",         lambda: __import__("sqlalchemy")),
        ("alembic",            lambda: __import__("alembic")),
        ("celery",             lambda: __import__("celery")),
        ("redis",              lambda: __import__("redis")),
        # Build 63: cloudscraper eliminado — movido a opcional
        ("requests",           lambda: __import__("requests")),
        ("beautifulsoup4",     lambda: __import__("bs4")),
        ("selenium",           lambda: __import__("selenium")),
        ("psutil",             lambda: __import__("psutil")),
        ("python-dotenv",      lambda: __import__("dotenv")),
        ("httpx",              lambda: __import__("httpx")),
    ]
    for name, fn in critical:
        if not check(name, fn):
            failures += 1

    # Windows-only
    if sys.platform == "win32":
        if not check("pywin32", lambda: __import__("win32service")):
            failures += 1

    # ── Dependencias opcionales ───────────────────────────────────────────────
    print()
    print("[ Dependencias opcionales ]")
    print("  (las marcadas [INFO] no bloquean el arranque)")

    # lxml — OPCIONAL: Python 3.14 no tiene wheel binario todavía
    try:
        import lxml
        print(f"  [OK]   lxml {lxml.__version__} (parser acelerado)")
    except ImportError:
        print("  [INFO] lxml no instalado — usando html.parser (stdlib)")
        print("         Ejecuta fix_lxml.bat para instalar lxml si lo necesitas.")

    # html.parser — siempre disponible (stdlib)
    check("html.parser (stdlib)", lambda: __import__("html.parser"), optional=True)

    # ── Configuracion ─────────────────────────────────────────────────────────
    print()
    print("[ Configuracion ]")
    if not Path(".env").exists():
        print("  [FAIL] .env no encontrado — ejecuta: copy .env.example .env")
        failures += 1
    else:
        try:
            from app.config import get_settings
            s = get_settings()
            print(f"  [OK]   .env cargado — app={s.APP_NAME} v{s.APP_VERSION} build={s.BUILD_VERSION}")
        except Exception as exc:
            print(f"  [FAIL] Error al cargar .env: {exc}")
            failures += 1

    # ── Estructura de directorios ─────────────────────────────────────────────
    print()
    print("[ Directorios del proyecto ]")
    base = Path(__file__).resolve().parent.parent
    required_dirs = [
        "app", "scripts", "tests", "migrations",
        "data/images", "data/exports", "data/logs/debug",
        "logs", "backups",
    ]
    for d in required_dirs:
        path = base / d
        if path.exists():
            print(f"  [OK]   {d}/")
        else:
            print(f"  [INFO] {d}/ no existe — se creara al arrancar")

    # ── Conectividad ──────────────────────────────────────────────────────────
    print()
    print("[ Conectividad ]")

    # PostgreSQL
    try:
        from app.config import get_settings
        s = get_settings()
        import psycopg
        conn = psycopg.connect(
            host=s.DB_HOST, port=s.DB_PORT,
            dbname=s.DB_NAME, user=s.DB_USER, password=s.DB_PASSWORD,
            connect_timeout=5,
        )
        conn.close()
        print(f"  [OK]   PostgreSQL {s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}")
    except Exception as exc:
        print(f"  [INFO] PostgreSQL: {exc}")
        print("         Ejecuta create_db.bat para crear la base de datos.")

    # Redis / Memurai
    try:
        from app.config import get_settings
        import redis as redis_lib
        r = redis_lib.from_url(get_settings().REDIS_URL, socket_connect_timeout=3)
        r.ping()
        r.close()
        print(f"  [OK]   Redis/Memurai en {get_settings().REDIS_URL}")
    except Exception as exc:
        print(f"  [INFO] Redis/Memurai: {exc}")
        print("         Inicia Memurai o ejecuta start_redis.bat")

    # ── Resumen ───────────────────────────────────────────────────────────────
    print()
    print("=" * 64)
    if failures == 0:
        print("  RESULTADO: Sistema listo para arrancar.")
        print("  Ejecuta: start_server.bat / start_celery.bat / start_celery_beat.bat")
    else:
        print(f"  RESULTADO: {failures} problema(s) critico(s) detectado(s).")
        print("  Revisa los errores [FAIL] anteriores antes de arrancar.")
    print("=" * 64)
    return failures


if __name__ == "__main__":
    sys.exit(main())
