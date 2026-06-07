@echo off
REM limpiar_cache.bat -- Limpia cachés de Python, Celery y logs temporales
REM BookingScraper Pro v48 | Windows 11
REM Ejecutar con el venv activo desde C:\BookingScraper
SETLOCAL ENABLEDELAYEDEXPANSION

ECHO ============================================================
ECHO  BookingScraper Pro v48 - Limpieza de Cache
ECHO ============================================================
ECHO.

SET BASE=%~dp0

REM -- 1. Cache Python (__pycache__ y .pyc) ----------------------------
ECHO [1/5] Eliminando cache de Python (__pycache__, *.pyc)...
FOR /D /R "%BASE%app" %%d IN (__pycache__) DO (
    IF EXIST "%%d" RD /S /Q "%%d" 2>NUL
)
FOR /D /R "%BASE%scripts" %%d IN (__pycache__) DO (
    IF EXIST "%%d" RD /S /Q "%%d" 2>NUL
)
FOR /D /R "%BASE%tests" %%d IN (__pycache__) DO (
    IF EXIST "%%d" RD /S /Q "%%d" 2>NUL
)
DEL /S /Q "%BASE%*.pyc" 2>NUL
ECHO   OK

REM -- 2. Base de datos de Celery Beat ---------------------------------
ECHO [2/5] Eliminando base de datos de Celery Beat...
IF EXIST "%BASE%celerybeat-schedule.db" (
    DEL /Q "%BASE%celerybeat-schedule.db"
    ECHO   OK - celerybeat-schedule.db eliminado
) ELSE (
    ECHO   OK - no existe
)
IF EXIST "%BASE%celerybeat.pid" (
    DEL /Q "%BASE%celerybeat.pid"
)

REM -- 3. HTML debug del scraper (data\logs\debug) ----------------------
ECHO [3/5] Eliminando HTML debug del scraper (data\logs\debug\)...
IF EXIST "%BASE%data\logs\debug\" (
    DEL /S /Q "%BASE%data\logs\debug\*.html" 2>NUL
    ECHO   OK
) ELSE (
    ECHO   OK - directorio no existe aun
)

REM -- 4. Logs de aplicacion antiguos (>7 dias) -------------------------
ECHO [4/5] Eliminando logs de aplicacion con mas de 7 dias...
IF EXIST "%BASE%logs\" (
    forfiles /P "%BASE%logs" /M "*.log" /D -7 /C "cmd /c del @path" 2>NUL
    forfiles /P "%BASE%logs" /M "*.log.*" /D -7 /C "cmd /c del @path" 2>NUL
    ECHO   OK
) ELSE (
    ECHO   OK - directorio no existe aun
)

REM -- 5. Cache de pytest -----------------------------------------------
ECHO [5/5] Eliminando cache de pytest...
IF EXIST "%BASE%.pytest_cache" RD /S /Q "%BASE%.pytest_cache" 2>NUL
FOR /D /R "%BASE%tests" %%d IN (.pytest_cache) DO (
    IF EXIST "%%d" RD /S /Q "%%d" 2>NUL
)
ECHO   OK

ECHO.
ECHO ============================================================
ECHO  Limpieza completada.
ECHO  Nota: los datos de hoteles (data\images\, data\exports\)
ECHO        NO se han eliminado.
ECHO ============================================================
ENDLOCAL
