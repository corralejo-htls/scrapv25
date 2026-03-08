@echo off
REM start_redis.bat — Inicia Memurai/Redis en Windows
REM BookingScraper Pro v48 | Windows 11
SETLOCAL

ECHO Iniciando Memurai (Redis para Windows)...

REM Intentar Memurai primero (recomendado para Windows 11)
IF EXIST "C:\Program Files\Memurai\memurai.exe" (
    START "" "C:\Program Files\Memurai\memurai.exe"
    ECHO Memurai iniciado.
    GOTO :END
)

REM Intentar Redis nativo
IF EXIST "C:\Program Files\Redis\redis-server.exe" (
    START "" "C:\Program Files\Redis\redis-server.exe"
    ECHO Redis iniciado.
    GOTO :END
)

ECHO ERROR: Memurai o Redis no encontrado.
ECHO Descarga Memurai desde: https://www.memurai.com/
PAUSE

:END
ENDLOCAL
