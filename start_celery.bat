@echo off
REM start_celery.bat — Inicia el worker de Celery
REM BookingScraper Pro v48 | Windows 11
SETLOCAL
SET PYTHONPATH=%~dp0
SET PYTHONUNBUFFERED=1
SET FORKED_BY_MULTIPROCESSING=1

IF EXIST "venv\Scripts\activate.bat" CALL "venv\Scripts\activate.bat"

ECHO Iniciando Celery worker...
python -m celery -A app.celery_app worker ^
    --loglevel=info ^
    --pool=solo ^
    --queues=default,maintenance,monitoring ^
    --hostname=worker@%%COMPUTERNAME%%

ENDLOCAL
