@echo off
REM verify_system.bat — Verifica que el sistema esta correctamente configurado
SETLOCAL
SET PYTHONPATH=%~dp0

IF EXIST "venv\Scripts\activate.bat" CALL "venv\Scripts\activate.bat"

ECHO Verificando sistema BookingScraper Pro v48...
python scripts\verify_system.py
ENDLOCAL
