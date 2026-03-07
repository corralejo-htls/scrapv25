@echo off
REM BookingScraper Pro v6.0 - Clean Old Log Files
title BookingScraper Pro - Cleanup Logs
cd /d "%~dp0"
echo Cleaning log files older than 30 days...
forfiles /p "logs" /s /m *.log /d -30 /c "cmd /c del @path" 2>nul
forfiles /p "C:\BookingScraper\debug" /s /m *.html /d -7 /c "cmd /c del @path" 2>nul
echo Log cleanup complete.
pause
