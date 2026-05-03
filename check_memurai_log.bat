@echo off
REM check_memurai_log.bat — Lee memurai.log y muestra causa raiz del fallo
REM BookingScraper Pro v6.0.0 | Windows 11
REM
REM CUANDO USAR: Cuando Memurai lanza ventana negra y no responde PONG.
REM   La ventana negra es NORMAL cuando logfile apunta a un archivo:
REM   Memurai escribe todo al archivo, nada a consola.
REM   Este script muestra las ultimas lineas del log para diagnosticar.
REM
SETLOCAL ENABLEDELAYEDEXPANSION

SET "BASE=%~dp0"
IF "%BASE:~-1%"=="\" SET "BASE=%BASE:~0,-1%"

SET "LOGFILE=%BASE%\logs\memurai.log"

ECHO ============================================================
ECHO  BookingScraper Pro — Diagnóstico Memurai Log
ECHO ============================================================
ECHO  Log: %LOGFILE%
ECHO ============================================================
ECHO.

IF NOT EXIST "%LOGFILE%" (
    ECHO [INFO] El archivo de log no existe todavia.
    ECHO        Memurai no ha llegado a escribir en el — fallo muy temprano.
    ECHO.
    ECHO  Causas probables:
    ECHO   1. El directorio logs\ no existe (ejecuta: mkdir "%BASE%\logs")
    ECHO   2. Permisos NTFS insuficientes sobre logs\
    ECHO   3. Memurai.exe no encontrado en la ruta configurada
    ECHO.
    GOTO :debug_mode
)

ECHO [OK] Log encontrado. Ultimas 50 lineas:
ECHO ============================================================
REM Mostrar ultimas 50 lineas del log
REM PowerShell es mas fiable que MORE para logs grandes en Windows
powershell -NoProfile -Command "Get-Content '%LOGFILE%' -Tail 50" 2>NUL
IF ERRORLEVEL 1 (
    REM Fallback: tipo directo
    type "%LOGFILE%"
)

ECHO.
ECHO ============================================================
ECHO.
ECHO  Analisis de errores conocidos:
ECHO.

REM Buscar errores conocidos en el log
powershell -NoProfile -Command "Select-String -Path '%LOGFILE%' -Pattern 'Error|Fatal|failed|bind|permission|Access|denied|invalid|unrecognized|unknown|license' -CaseSensitive:$false | Select-Object -Last 20" 2>NUL

ECHO.
ECHO ============================================================
ECHO.
ECHO  Si el log esta vacio o no muestra el error, usa:
ECHO    debug_memurai.bat  --  lanza Memurai con log en consola
ECHO.
PAUSE
GOTO :END

:debug_mode
ECHO.
ECHO ============================================================
ECHO  Creando logs\ si no existe...
IF NOT EXIST "%BASE%\logs" MKDIR "%BASE%\logs"
ECHO [OK] Directorio logs\ verificado.
ECHO.
ECHO  Prueba ahora:
ECHO    1. debug_memurai.bat  (Memurai con salida en consola)
ECHO    2. setup_memurai.bat  (regenera conf y lanza)
ECHO ============================================================
PAUSE

:END
ENDLOCAL
