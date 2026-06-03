@echo off
SETLOCAL

cd /d C:\BookingScraper
cls
REM Crear venv si no existe
IF NOT EXIST ".venv\Scripts\activate.bat" (
    python -m venv .venv
)

REM Activar entorno virtual
call .venv\Scripts\activate.bat

echo VIRTUAL_ENV=%VIRTUAL_ENV%
where python
python --version


REM Ejecutar purge de colas
call purge_queues.bat

ECHO [1] Eliminar archivos...

REM Eliminar subdirectorios de images
for /d %%i in (C:\BookingScraper\data\images\*) do rd /s /q "%%i"

DEL /Q "_arbol_.*"
DEL /Q "_list_pip.txt"

CALL limpiar_cache.bat
CALL cleanup_logs.bat



ECHO [2] Generando lista pip...

SET "PIP_EXE=pip"

IF EXIST "%~dp0.venv\Scripts\pip.exe" SET "PIP_EXE=%~dp0.venv\Scripts\pip.exe"

"%PIP_EXE%" list > "%~dp0_list_pip.txt" 2>&1

ECHO [3] Listando directorio...

DIR /b /s > "_arbol_.csv"

ECHO.
ECHO Proceso completado.

call cmd /k

ENDLOCAL