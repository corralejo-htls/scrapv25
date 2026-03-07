@echo off
REM BookingScraper Pro v6.0 - System Verification
title BookingScraper Pro - Verify System
cd /d "%~dp0"
call .venv\Scripts\activate.bat
echo Running system verification...
python scripts\verify_system.py
if %errorlevel%==0 (
    echo.
    echo All checks passed!
) else (
    echo.
    echo Some checks failed - review output above.
)
pause
