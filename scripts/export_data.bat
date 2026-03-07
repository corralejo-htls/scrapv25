@echo off
REM BookingScraper Pro v6.0 - Export Hotel Data
title BookingScraper Pro - Export Data
cd /d "%~dp0"
call .venv\Scripts\activate.bat
set /p FORMAT="Export format csv or excel (default: csv): "
if "%FORMAT%"=="" set FORMAT=csv
set OUTFILE=C:\BookingScraper\exports\hotels_%date:~-4,4%%date:~-7,2%%date:~-10,2%.%FORMAT%
echo Exporting to %OUTFILE%...
python scripts\export_data.py --format %FORMAT% --output "%OUTFILE%"
if %errorlevel%==0 (
    echo Export complete: %OUTFILE%
    explorer "C:\BookingScraper\exports"
) else (
    echo Export failed.
)
pause
