@echo off
REM start_celery.bat -- Inicia el worker de Celery
REM BookingScraper Pro v48 | Windows 11
REM Nota: inicio_rapido.bat arranca los 3 servicios automaticamente.
SETLOCAL
SET PYTHONPATH=%~dp0
SET PYTHONUNBUFFERED=1
SET FORKED_BY_MULTIPROCESSING=1

REM Activar venv si no esta activo
IF EXIST ".venv\Scripts\activate.bat" (
    CALL ".venv\Scripts\activate.bat"
) ELSE IF EXIST "venv\Scripts\activate.bat" (
    CALL "venv\Scripts\activate.bat"
)

ECHO Iniciando Celery worker...
ECHO.

python -m celery -A app.celery_app worker ^
    --loglevel=info ^
    --pool=solo ^
    --queues=default,maintenance,monitoring ^
    --hostname=worker@%COMPUTERNAME%

ENDLOCAL
