@echo off
REM export_data.bat — Exporta datos de hoteles a CSV o JSON
REM Los exports se guardan en data\exports\
SETLOCAL
SET PYTHONPATH=%~dp0

IF EXIST "venv\Scripts\activate.bat" CALL "venv\Scripts\activate.bat"

SET FORMAT=%1
IF "%FORMAT%"=="" SET FORMAT=csv

ECHO Exportando datos de hoteles (formato: %FORMAT%)...
python scripts\export_data.py --format %FORMAT%
ECHO Exportacion completada. Revisa la carpeta data\exports\
ENDLOCAL
