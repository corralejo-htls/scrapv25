@echo off
REM setup_env.bat — Configura el entorno de instalacion
REM BookingScraper Pro v48 | Windows 11 | Compatible Python 3.11, 3.12, 3.14
SETLOCAL

ECHO ============================================================
ECHO  BookingScraper Pro v48 - Setup de Entorno
ECHO ============================================================

REM ── Verificar Python ──────────────────────────────────────────────────────
python --version 2>NUL
IF ERRORLEVEL 1 (
    ECHO ERROR: Python no encontrado.
    ECHO Descarga Python 3.11+ desde: https://www.python.org/downloads/windows/
    PAUSE & EXIT /B 1
)

REM ── Crear entorno virtual ─────────────────────────────────────────────────
IF NOT EXIST ".venv" (
    ECHO Creando entorno virtual .venv ...
    python -m venv .venv
    IF ERRORLEVEL 1 (
        ECHO ERROR: No se pudo crear el entorno virtual.
        PAUSE & EXIT /B 1
    )
) ELSE (
    ECHO Entorno virtual .venv ya existe.
)

REM ── Activar venv ──────────────────────────────────────────────────────────
IF EXIST ".venv\Scripts\activate.bat" (
    CALL ".venv\Scripts\activate.bat"
) ELSE (
    ECHO ERROR: .venv\Scripts\activate.bat no encontrado.
    PAUSE & EXIT /B 1
)

REM ── Actualizar pip ────────────────────────────────────────────────────────
ECHO Actualizando pip...
python -m pip install --upgrade pip --quiet

REM ── Instalar dependencias principales ────────────────────────────────────
ECHO Instalando dependencias (sin lxml — compatible Python 3.14)...
pip install -r requirements.txt
IF ERRORLEVEL 1 (
    ECHO ERROR: Fallo al instalar dependencias.
    ECHO Revisa el error anterior y vuelve a intentarlo.
    PAUSE & EXIT /B 1
)

REM ── Intentar instalar lxml con wheel binario ──────────────────────────────
ECHO.
ECHO Intentando instalar lxml (opcional — wheel binario)...
pip install lxml --prefer-binary --only-binary=lxml --quiet 2>NUL
IF NOT ERRORLEVEL 1 (
    ECHO [OK] lxml instalado correctamente.
) ELSE (
    ECHO [INFO] lxml no disponible para tu version de Python.
    ECHO        El sistema usara html.parser automaticamente.
    ECHO        Ejecuta fix_lxml.bat para ver las opciones disponibles.
)

REM ── Crear estructura de directorios ──────────────────────────────────────
ECHO.
ECHO Creando estructura de directorios del proyecto...
python scripts\create_project_structure.py

REM ── Configurar .env ───────────────────────────────────────────────────────
IF NOT EXIST ".env" (
    COPY ".env.example" ".env" >NUL
    ECHO.
    ECHO ============================================================
    ECHO  IMPORTANTE: Edita .env con tus credenciales antes de arrancar
    ECHO ============================================================
    ECHO.
    ECHO  SECRET_KEY  - Genera con:
    ECHO    python -c "import secrets; print(secrets.token_urlsafe(48))"
    ECHO.
    ECHO  DB_USER     - Usuario PostgreSQL (bookingscraper_user)
    ECHO  DB_PASSWORD - Contrasena PostgreSQL
    ECHO.
    ECHO  Luego ejecuta: create_db.bat
    ECHO ============================================================
) ELSE (
    ECHO .env ya existe.
)

ECHO.
ECHO Setup completado. Proximos pasos:
ECHO   1. Edita .env con tus credenciales
ECHO   2. Ejecuta create_db.bat para crear la base de datos
ECHO   3. Ejecuta verify_system.bat para comprobar la instalacion
ENDLOCAL
