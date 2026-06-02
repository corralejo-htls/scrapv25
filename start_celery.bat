@echo off
REM start_celery.bat — Inicia el worker de Celery con reinicio automatico
REM BookingScraper Pro v6.0.0 Build 115 | Windows 11
REM
REM BUG-WORKER-NORESTART-001-FIX (Build 115):
REM   Cuando el watchdog TASK_WATCHDOG_TIMEOUT_S dispara os._exit(1), el
REM   proceso Celery muere con exit code 1. Sin bucle de reinicio, el Beat
REM   seguia enviando tareas (hasta 2h45m observado) sin consumidor.
REM   Fix: bucle :RESTART_LOOP reinicia automaticamente si exit code != 0.
REM   Si el operador cierra con Ctrl+C (exit code 0), NO se reinicia.
REM
REM Para detener permanentemente: stop_celery.bat (o Ctrl+C en este terminal)
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

ECHO ============================================================
ECHO  BookingScraper Pro v6.0.0 - Celery Worker (auto-restart)
ECHO  Build 115 - BUG-WORKER-NORESTART-001-FIX activo
ECHO  Ctrl+C para detener permanentemente.
ECHO ============================================================
ECHO.

:RESTART_LOOP
ECHO [%TIME%] Iniciando Celery worker...
ECHO.

python -m celery -A app.celery_app worker ^
    --loglevel=info ^
    --pool=solo ^
    --queues=default,maintenance,monitoring ^
    --hostname=worker@%COMPUTERNAME%

SET EXIT_CODE=%ERRORLEVEL%

IF %EXIT_CODE%==0 (
    ECHO.
    ECHO [%TIME%] Worker detenido limpiamente (exit code 0). No se reinicia.
    GOTO :END
)

ECHO.
ECHO [%TIME%] Worker termino con exit code %EXIT_CODE% (watchdog o crash).
ECHO          Reiniciando en 10 segundos... (Ctrl+C para cancelar)
ECHO.
timeout /t 10 /nobreak >NUL
IF ERRORLEVEL 1 (
    ECHO [%TIME%] Reinicio cancelado por el operador.
    GOTO :END
)
GOTO :RESTART_LOOP

:END
ENDLOCAL
ECHO [%TIME%] start_celery.bat finalizado.
