@echo off
REM add_memurai_to_path.bat — Agrega Memurai al PATH del sistema
REM BookingScraper Pro v6.0.0 | Windows 11
REM
REM FIX-MEMURAI-008: causa raiz del bug "Memurai no responde PONG".
REM   Memurai instala su ejecutable en C:\Program Files\Memurai\ pero
REM   NO siempre agrega esa ruta al PATH del sistema. Sin redis-cli
REM   en PATH, todos los scripts de polling fallan silenciosamente.
REM
REM REQUIERE: Ejecutar como Administrador.
REM
REM ALTERNATIVA SIN ADMINISTRADOR: los scripts ya usan ruta absoluta
REM   tras FIX-MEMURAI-008 — este bat es opcional pero recomendado.
REM
@echo off
NET SESSION >NUL 2>&1
IF ERRORLEVEL 1 (
    ECHO [ERROR] Este script requiere permisos de Administrador.
    ECHO         Clic derecho sobre el archivo ^> "Ejecutar como administrador"
    PAUSE & EXIT /B 1
)

SET "MEMURAI_DIR=C:\Program Files\Memurai"

IF NOT EXIST "%MEMURAI_DIR%\memurai.exe" (
    ECHO [ERROR] Memurai no encontrado en: %MEMURAI_DIR%
    ECHO         Instala Memurai desde: https://www.memurai.com/
    PAUSE & EXIT /B 1
)

REM Verificar si ya esta en PATH
ECHO %PATH% | findstr /i /c:"%MEMURAI_DIR%" >NUL 2>&1
IF NOT ERRORLEVEL 1 (
    ECHO [OK] Memurai ya esta en el PATH del sistema.
    ECHO      %MEMURAI_DIR%
    PAUSE & EXIT /B 0
)

REM Agregar al PATH del sistema via registro
ECHO [INFO] Agregando al PATH del sistema:
ECHO        %MEMURAI_DIR%

REM Leer PATH actual del registro
FOR /F "usebackq tokens=2*" %%A IN (`reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>NUL`) DO SET "SYS_PATH=%%B"

IF NOT DEFINED SYS_PATH (
    ECHO [ERROR] No se pudo leer el PATH del sistema desde el registro.
    PAUSE & EXIT /B 1
)

REM Escribir PATH actualizado
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH /t REG_EXPAND_SZ /d "%SYS_PATH%;%MEMURAI_DIR%" /f >NUL 2>&1
IF ERRORLEVEL 1 (
    ECHO [ERROR] No se pudo escribir en el registro.
    PAUSE & EXIT /B 1
)

REM Notificar a procesos en ejecucion del cambio de PATH
REM (sin esto, los terminales abiertos no ven el nuevo PATH)
setx MEMURAI_PATH_SET "1" >NUL 2>&1

ECHO [OK] Memurai agregado al PATH del sistema exitosamente.
ECHO.
ECHO IMPORTANTE: Cierra y reabre todos los terminales (cmd/PowerShell)
ECHO             para que el nuevo PATH sea efectivo.
ECHO.
ECHO Verificacion: abre un terminal nuevo y ejecuta:
ECHO   redis-cli PING
ECHO   Respuesta esperada: PONG
ECHO.
PAUSE
