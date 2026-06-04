@echo off
REM load_urls.bat — Carga URLs desde un archivo CSV
REM Uso: load_urls.bat [archivo.csv]
REM Por defecto usa urls_ejemplo.csv
SETLOCAL
SET PYTHONPATH=%~dp0

IF EXIST "venv\Scripts\activate.bat" CALL "venv\Scripts\activate.bat"

SET CSV_FILE=%1
IF "%CSV_FILE%"=="" SET CSV_FILE=urls_ejemplo.csv

IF NOT EXIST "%CSV_FILE%" (
    ECHO ERROR: Archivo %CSV_FILE% no encontrado.
    EXIT /B 1
)

ECHO Cargando URLs desde %CSV_FILE%...
python scripts\load_urls.py "%CSV_FILE%"
ENDLOCAL
