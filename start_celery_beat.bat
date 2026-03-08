@echo off
REM start_celery_beat.bat — Inicia el scheduler Celery Beat
REM BookingScraper Pro v48 | Windows 11
SETLOCAL
SET PYTHONPATH=%~dp0
SET PYTHONUNBUFFERED=1

IF EXIST "venv\Scripts\activate.bat" CALL "venv\Scripts\activate.bat"

ECHO Iniciando Celery Beat scheduler...
python -m celery -A app.celery_app beat ^
    --loglevel=info ^
    --scheduler celery.beat.PersistentScheduler ^
    --schedule celerybeat-schedule.db

ENDLOCAL
