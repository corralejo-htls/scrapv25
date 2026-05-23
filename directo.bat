@echo off
SETLOCAL
cd \
cd C:\BookingScraper

DEL /Q "_arbol_.txt"
DEL /Q "_list_pip.txt"
dir /o:e /s >_arbol_.txt

REM ── Generar lista de paquetes pip instalados ──────────────────────────────
ECHO [2/3] Generando lista pip...
SET "PIP_EXE=pip"
IF EXIST "%~dp0.venv\Scripts\pip.exe"  SET "PIP_EXE=%~dp0.venv\Scripts\pip.exe"
IF EXIST "%~dp0venv\Scripts\pip.exe"   SET "PIP_EXE=%~dp0venv\Scripts\pip.exe"
"%PIP_EXE%" list > "%~dp0_list_pip.txt" 2>&1

ECHO.
ECHO Limpiando logs...
CALL cleanup_logs.bat

