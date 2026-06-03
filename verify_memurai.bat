@echo off
REM verify_memurai.bat -- Verifica rapida conectividad Memurai
REM BookingScraper Pro v6.0.0 | Windows 11
REM
REM Usa memurai-cli.exe (no redis-cli.exe) para verificar PONG.
REM
SETLOCAL ENABLEDELAYEDEXPANSION

SET "CLI=C:\Program Files\Memurai\memurai-cli.exe"

IF NOT EXIST "%CLI%" (
    ECHO [ERROR] No encontrado: %CLI%
    PAUSE & EXIT /B 1
)

ECHO [INFO] Probando: "%CLI%" PING
SET "RESP="
FOR /F "usebackq delims=" %%p IN (`"%CLI%" PING 2^>NUL`) DO (
    IF NOT DEFINED RESP SET "RESP=%%p"
)

IF /I "!RESP!"=="PONG" (
    ECHO [OK] PONG recibido -- Memurai esta activo y escuchando.
) ELSE (
    ECHO [ERROR] No se recibio PONG. Respuesta: "!RESP!"
    ECHO         Memurai no esta corriendo o no escucha en 127.0.0.1:6379
)

ECHO.
ECHO [INFO] Prueba adicional INFO server:
"%CLI%" INFO server 2>NUL | findstr /i "redis_version\|memurai\|uptime\|port"
ECHO.
PAUSE
ENDLOCAL
