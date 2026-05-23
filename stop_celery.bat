@echo off
REM stop_celery.bat — Detiene workers Celery
SETLOCAL
ECHO Deteniendo workers Celery...
IF EXIST "venv\Scripts\activate.bat" CALL "venv\Scripts\activate.bat"
python -m celery -A app.celery_app control shutdown 2>NUL
taskkill /IM celery.exe /F >NUL 2>&1
ECHO Workers Celery detenidos.
ENDLOCAL
