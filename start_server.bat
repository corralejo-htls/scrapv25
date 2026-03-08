@echo off
REM start_server.bat — Inicia el servidor FastAPI/Uvicorn
REM BookingScraper Pro v48 | Windows 11
SETLOCAL
SET PYTHONPATH=%~dp0
SET PYTHONUNBUFFERED=1

IF NOT EXIST ".env" (
    ECHO ERROR: Archivo .env no encontrado.
    ECHO Ejecuta setup_env.bat primero o copia .env.example a .env y configura las credenciales.
    PAUSE & EXIT /B 1
)

IF EXIST "venv\Scripts\activate.bat" CALL "venv\Scripts\activate.bat"

ECHO Iniciando BookingScraper Pro API en http://127.0.0.1:8000 ...
ECHO Documentacion API: http://127.0.0.1:8000/docs
ECHO.

python -m uvicorn app.main:app ^
    --host 127.0.0.1 ^
    --port 8000 ^
    --workers 1 ^
    --log-level info ^
    --access-log

ENDLOCAL
