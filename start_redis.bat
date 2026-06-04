@echo off
REM start_redis.bat -- Lanza Memurai/Redis como proceso directo
REM BookingScraper Pro v6.0.0 | Windows 11
REM
REM FIX-MEMURAI-010: el cliente se llama memurai-cli.exe, NO redis-cli.exe
REM   La instalacion de Memurai incluye memurai-cli.exe unicamente.
REM   Todos los scripts anteriores buscaban redis-cli.exe y fallaban
REM   silenciosamente -- el polling nunca recibia PONG.
REM
SETLOCAL ENABLEDELAYEDEXPANSION

SET "BASE=%~dp0"
IF "%BASE:~-1%"=="\" SET "BASE=%BASE:~0,-1%"

REM ── 0. Localizar memurai-cli / redis-cli ──────────────────────────────────
SET "REDIS_CLI="
IF EXIST "C:\Program Files\Memurai\memurai-cli.exe" SET "REDIS_CLI=C:\Program Files\Memurai\memurai-cli.exe"
IF NOT DEFINED REDIS_CLI IF EXIST "C:\Memurai\memurai-cli.exe" SET "REDIS_CLI=C:\Memurai\memurai-cli.exe"
IF NOT DEFINED REDIS_CLI IF EXIST "C:\Program Files\Memurai\redis-cli.exe" SET "REDIS_CLI=C:\Program Files\Memurai\redis-cli.exe"
IF NOT DEFINED REDIS_CLI IF EXIST "C:\Program Files\Redis\redis-cli.exe" SET "REDIS_CLI=C:\Program Files\Redis\redis-cli.exe"
IF NOT DEFINED REDIS_CLI (
    WHERE memurai-cli >NUL 2>&1
    IF NOT ERRORLEVEL 1 SET "REDIS_CLI=memurai-cli"
)
IF NOT DEFINED REDIS_CLI (
    WHERE redis-cli >NUL 2>&1
    IF NOT ERRORLEVEL 1 SET "REDIS_CLI=redis-cli"
)
IF NOT DEFINED REDIS_CLI (
    ECHO [ERROR] memurai-cli.exe no encontrado en ninguna ruta conocida.
    PAUSE & EXIT /B 1
)
ECHO [INFO] cliente: %REDIS_CLI%

REM ── 1. Ya activo? ─────────────────────────────────────────────────────────
SET "REDIS_RESP="
FOR /F "usebackq delims=" %%p IN (`"%REDIS_CLI%" PING 2^>NUL`) DO (
    IF NOT DEFINED REDIS_RESP SET "REDIS_RESP=%%p"
)
IF /I "!REDIS_RESP!"=="PONG" (
    ECHO [OK] Memurai ya activo y responde PONG.
    GOTO :END
)

REM ── 2. Asegurar logs\ ─────────────────────────────────────────────────────
IF NOT EXIST "%BASE%\logs" MKDIR "%BASE%\logs"

REM ── 3. Liberar puerto zombie ──────────────────────────────────────────────
ECHO [INFO] Verificando puerto 6379...
SET "ZOMBIE_PID="
FOR /F "tokens=5" %%z IN ('netstat -ano 2^>NUL ^| findstr ":6379 " ^| findstr "LISTENING"') DO (
    IF NOT DEFINED ZOMBIE_PID SET "ZOMBIE_PID=%%z"
)
IF DEFINED ZOMBIE_PID (
    ECHO [INFO] Liberando PID !ZOMBIE_PID! en puerto 6379...
    taskkill /F /PID !ZOMBIE_PID! >NUL 2>&1
    timeout /t 1 /nobreak >NUL
) ELSE (
    ECHO [INFO] Puerto 6379 libre.
)

REM ── 4. Buscar Memurai ─────────────────────────────────────────────────────
SET "MEMURAI_EXE="
IF EXIST "C:\Program Files\Memurai\memurai.exe" SET "MEMURAI_EXE=C:\Program Files\Memurai\memurai.exe"
IF NOT DEFINED MEMURAI_EXE IF EXIST "C:\Memurai\memurai.exe" SET "MEMURAI_EXE=C:\Memurai\memurai.exe"

SET "MEMURAI_CONF=%BASE%\memurai.conf"

IF NOT DEFINED MEMURAI_EXE (
    ECHO [ERROR] memurai.exe no encontrado.
    ECHO         Descarga Memurai: https://www.memurai.com/
    PAUSE & EXIT /B 1
)

REM ── 5. Lanzar Memurai (FIX-MEMURAI-009: start directo sin cmd /k) ─────────
IF EXIST "!MEMURAI_CONF!" (
    ECHO [INFO] Lanzando: !MEMURAI_EXE!
    ECHO        Conf:     !MEMURAI_CONF!
    start "BSP - Memurai" "!MEMURAI_EXE!" "!MEMURAI_CONF!"
) ELSE (
    ECHO [AVISO] memurai.conf no encontrado -- config default.
    start "BSP - Memurai" "!MEMURAI_EXE!"
)

REM ── 6. Polling PONG hasta 25s ─────────────────────────────────────────────
ECHO [INFO] Esperando que Memurai acepte conexiones...
SET /A WAIT=0
:wait_pong
timeout /t 1 /nobreak >NUL
SET "RESP="
FOR /F "usebackq delims=" %%p IN (`"%REDIS_CLI%" PING 2^>NUL`) DO (
    IF NOT DEFINED RESP SET "RESP=%%p"
)
IF /I "!RESP!"=="PONG" (
    ECHO [OK] Memurai activo y responde PONG ^(!WAIT!s^).
    GOTO :END
)
SET /A WAIT+=1
IF !WAIT! LSS 25 GOTO :wait_pong

ECHO.
ECHO [ERROR] Memurai no responde tras 25 segundos.
SET "LOGFILE=%BASE%\logs\memurai.log"
IF EXIST "!LOGFILE!" (
    ECHO  Ultimas lineas del log:
    powershell -NoProfile -Command "Get-Content '!LOGFILE!' -Tail 10" 2>NUL
)
ECHO  Prueba manual: "%MEMURAI_EXE%" "%MEMURAI_CONF%"
PAUSE

:END
ENDLOCAL
