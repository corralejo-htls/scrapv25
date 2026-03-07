@echo off
REM BookingScraper Pro v6.0 - Load URLs from CSV
title BookingScraper Pro - Load URLs
cd /d "%~dp0"
call .venv\Scripts\activate.bat
set /p CSV_FILE="Enter CSV file path (default: urls_ejemplo.csv): "
if "%CSV_FILE%"=="" set CSV_FILE=urls_ejemplo.csv
set /p LANGUAGE="Enter language code (default: en): "
if "%LANGUAGE%"=="" set LANGUAGE=en
set /p PRIORITY="Enter priority 1-10 (default: 5): "
if "%PRIORITY%"=="" set PRIORITY=5
echo.
echo Loading URLs from %CSV_FILE% (language=%LANGUAGE% priority=%PRIORITY%)...
python scripts\load_urls.py "%CSV_FILE%" --language %LANGUAGE% --priority %PRIORITY%
pause
