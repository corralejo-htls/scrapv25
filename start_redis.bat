@echo off
REM start_redis.bat — Lanza Memurai/Redis como proceso directo
REM BookingScraper Pro v6.0.0 | Windows 11
REM
REM POLITICA: no se instala ningun servicio de Windows.
REM   Memurai se lanza como proceso normal. Vive mientras
REM   su terminal este abierta.
REM
REM FIX-MEMURAI-002: libera puerto 6379 si hay un proceso zombie antes de lanzar.
REM FIX-MEMURAI-003: pasa memurai.conf como argumento para configuracion correcta.
REM
SETLOCAL ENABLEDELAYEDEXPANSION

SET "BASE=%~dp0"

REM ── 1. Ya activo? ─────────────────────────────────────────────
SET "REDIS_RESP="
FOR /F "usebackq delims=" %%p IN (`redis-cli PING 2^>NUL`) DO (
    IF NOT DEFINED REDIS_RESP SET "REDIS_RESP=%%p"
)
IF /I "!REDIS_RESP!"=="PONG" (
    ECHO [OK] Memurai/Redis ya esta activo y responde PONG.
    GOTO :END
)

REM ── 2. Liberar puerto 6379 si hay zombie ──────────────────────
ECHO [INFO] Verificando puerto 6379...
SET "ZOMBIE_PID="
FOR /F "tokens=5" %%z IN ('netstat -ano 2^>NUL ^| findstr ":6379 " ^| findstr "LISTENING"') DO (
    IF NOT DEFINED ZOMBIE_PID SET "ZOMBIE_PID=%%z"
)
IF DEFINED ZOMBIE_PID (
    ECHO [INFO] Puerto 6379 ocupado por PID !ZOMBIE_PID! ^(no responde PING^). Liberando...
    taskkill /F /PID !ZOMBIE_PID! >NUL 2>&1
    timeout /t 1 /nobreak >NUL
    ECHO [INFO] Puerto 6379 liberado.
) ELSE (
    ECHO [INFO] Puerto 6379 libre.
)

REM ── 3. Buscar Memurai ─────────────────────────────────────────
SET "MEMURAI_EXE="
IF EXIST "C:\Program Files\Memurai\memurai.exe"       SET "MEMURAI_EXE=C:\Program Files\Memurai\memurai.exe"
IF NOT DEFINED MEMURAI_EXE IF EXIST "C:\Memurai\memurai.exe" SET "MEMURAI_EXE=C:\Memurai\memurai.exe"

SET "MEMURAI_CONF=%BASE%memurai.conf"

IF DEFINED MEMURAI_EXE (
    IF EXIST "!MEMURAI_CONF!" (
        ECHO [INFO] Lanzando Memurai con !MEMURAI_CONF!...
        start "BSP - Memurai" cmd /k ""!MEMURAI_EXE!" "!MEMURAI_CONF!""
    ) ELSE (
        ECHO [AVISO] memurai.conf no encontrado en !BASE! -- lanzando con config default.
        start "BSP - Memurai" cmd /k ""!MEMURAI_EXE!""
    )

    REM Esperar PONG hasta 20s
    SET /A WAIT=0
    :wait_pong
    timeout /t 1 /nobreak >NUL
    SET "RESP="
    FOR /F "usebackq delims=" %%p IN (`redis-cli PING 2^>NUL`) DO (
        IF NOT DEFINED RESP SET "RESP=%%p"
    )
    IF /I "!RESP!"=="PONG" (
        ECHO [OK] Memurai activo y responde PONG.
        GOTO :END
    )
    SET /A WAIT+=1
    IF !WAIT! LSS 20 GOTO :wait_pong

    ECHO [ERROR] Memurai no responde tras 20 segundos.
    ECHO         Revisa la ventana "BSP - Memurai" para ver el error.
    PAUSE
    GOTO :END
)

REM ── 4. Fallback: Redis nativo ─────────────────────────────────
IF EXIST "C:\Program Files\Redis\redis-server.exe" (
    ECHO [INFO] Lanzando Redis nativo como proceso...
    start "BSP - Redis" cmd /k "C:\Program Files\Redis\redis-server.exe"
    timeout /t 5 /nobreak >NUL
    redis-cli PING
    GOTO :END
)

REM ── 5. No encontrado ──────────────────────────────────────────
ECHO [ERROR] Memurai ni Redis encontrados.
ECHO         Descarga Memurai: https://www.memurai.com/
PAUSE

:END
ENDLOCAL
