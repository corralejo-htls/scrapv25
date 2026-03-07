@echo off
REM BookingScraper Pro v6.0 - Setup Virtual Environment
title BookingScraper Pro - Setup
cd /d "%~dp0"
echo === BookingScraper Pro v6.0 Setup ===
echo.
echo Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ERROR: Python not found or venv creation failed.
    pause & exit /b 1
)
call .venv\Scripts\activate.bat
echo.
echo Installing dependencies from project root requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Dependency installation failed.
    pause & exit /b 1
)
echo.
echo Creating project directories...
python scripts\create_project_structure.py
echo.
echo Setup complete!
echo Next: Edit .env with your database credentials, then run create_db.bat
pause
