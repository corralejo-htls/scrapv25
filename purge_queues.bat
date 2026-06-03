@echo off
REM purge_queues.bat — Elimina todas las tareas pendientes en Redis/Memurai
REM BookingScraper Pro v6.0.0 Build 115 | Windows 11
REM
REM USO: Ejecutar cuando el worker lleva tiempo detenido y Redis ha acumulado
REM      cientos/miles de tareas scrape_pending_urls, collect_system_metrics, etc.
REM      que el worker consumira en rafaga al reiniciar (inutil, solo ruido).
REM
REM SEGURO: Las tareas periodicas se re-encolan en el proximo ciclo del Beat.
REM   scrape_pending_urls    → max 30s  para re-encolar
REM   collect_system_metrics → max 300s para re-encolar
REM   reset_stale_urls       → max 30min para re-encolar
REM
REM NO EJECUTAR mientras el worker esta procesando URLs activamente.
SETLOCAL
SET PYTHONPATH=%~dp0

IF EXIST ".venv\Scripts\activate.bat" (
    CALL ".venv\Scripts\activate.bat"
) ELSE IF EXIST "venv\Scripts\activate.bat" (
    CALL "venv\Scripts\activate.bat"
)

ECHO ============================================================
ECHO  BookingScraper Pro — Purge de colas Redis
ECHO ============================================================
ECHO.
ECHO  ATENCION: Esto elimina TODAS las tareas en cola (default,
ECHO  maintenance, monitoring). Las tareas periodicas se
ECHO  re-encolan automaticamente en el siguiente ciclo del Beat.
ECHO.
ECHO  NO ejecutar si el worker esta scrapeando activamente.
ECHO.

ECHO.
ECHO [%TIME%] Purgando colas Celery (default + maintenance + monitoring)...
python -m celery -A app.celery_app purge -f
ECHO.
ECHO [%TIME%] Purge completado.
ECHO          El Beat re-encolara las tareas periodicas automaticamente.

:END
ENDLOCAL
