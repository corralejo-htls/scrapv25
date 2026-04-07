@echo off
REM start_server.bat -- Inicia el servidor FastAPI/Uvicorn
REM BookingScraper Pro v6.0.0 build 53 | Windows 11
REM Nota: inicio_rapido.bat arranca los 3 servicios automaticamente.
SETLOCAL
SET PYTHONPATH=%~dp0
SET PYTHONUNBUFFERED=1

IF NOT EXIST ".env" (
    ECHO ERROR: Archivo .env no encontrado.
    ECHO Copia .env.example a .env y configura tus credenciales.
    PAUSE & EXIT /B 1
)

REM Activar venv si no esta activo
IF EXIST ".venv\Scripts\activate.bat" (
    CALL ".venv\Scripts\activate.bat"
) ELSE IF EXIST "venv\Scripts\activate.bat" (
    CALL "venv\Scripts\activate.bat"
)

ECHO Iniciando BookingScraper Pro API...
ECHO   URL:   http://127.0.0.1:8000
ECHO   Docs:  http://127.0.0.1:8000/docs
ECHO.

python -m uvicorn app.main:app ^
    --host 127.0.0.1 ^
    --port 8000 ^
    --workers 1 ^
    --log-level info ^
    --access-log

ENDLOCAL
