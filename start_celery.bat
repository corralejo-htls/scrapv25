@echo off
REM start_celery.bat — BookingScraper Pro v6.0.0 Build 116
REM BUG-ECHO-BAT-001-FIX: ECHO. reemplazado por ECHO( (CMD Win11 compatible)
REM BUG-WORKER-NORESTART-001-FIX: bucle auto-reinicio si exit code != 0
REM BUG-TASK-STORM-001-FIX: purge Redis backlog antes de cada reinicio
SETLOCAL
SET PYTHONPATH=%~dp0
SET PYTHONUNBUFFERED=1
SET FORKED_BY_MULTIPROCESSING=1

IF EXIST ".venv\Scripts\activate.bat" (
    CALL ".venv\Scripts\activate.bat"
) ELSE IF EXIST "venv\Scripts\activate.bat" (
    CALL "venv\Scripts\activate.bat"
)

ECHO ============================================================
ECHO  BookingScraper Pro v6.0.0 - Celery Worker auto-restart
ECHO  Build 116
ECHO ============================================================
ECHO(

SET _RESTART_COUNT=0

:RESTART_LOOP

IF %_RESTART_COUNT% GTR 0 (
    ECHO [%TIME%] Purgando backlog Redis...
    python -m celery -A app.celery_app purge -f >NUL 2>&1
    ECHO [%TIME%] Colas purgadas.
    ECHO(
)
SET /A _RESTART_COUNT=%_RESTART_COUNT%+1

ECHO [%TIME%] Iniciando Celery worker inicio #%_RESTART_COUNT%...
ECHO(

python -m celery -A app.celery_app worker --loglevel=info --pool=solo --queues=default,maintenance,monitoring --hostname=worker@%COMPUTERNAME%

SET EXIT_CODE=%ERRORLEVEL%

IF %EXIT_CODE%==0 (
    ECHO(
    ECHO [%TIME%] Worker detenido limpiamente exit code 0. No se reinicia.
    GOTO :END
)

ECHO(
ECHO [%TIME%] Worker termino con exit code %EXIT_CODE%. Reiniciando en 10s...
ECHO(
timeout /t 10 /nobreak >NUL
IF ERRORLEVEL 1 (
    ECHO [%TIME%] Reinicio cancelado.
    GOTO :END
)
GOTO :RESTART_LOOP

:END
ENDLOCAL
ECHO [%TIME%] start_celery.bat finalizado.
