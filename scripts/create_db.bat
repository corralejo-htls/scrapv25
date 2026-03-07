@echo off
REM BookingScraper Pro v6.0 - Create Database Schema
REM Runs install_clean_v46.sql via psql
title BookingScraper Pro - Create DB
cd /d "%~dp0"
call .venv\Scripts\activate.bat
set /p DB_USER="Enter PostgreSQL username (default: bookingscraper_app): "
if "%DB_USER%"=="" set DB_USER=bookingscraper_app
set /p DB_NAME="Enter database name (default: bookingscraper): "
if "%DB_NAME%"=="" set DB_NAME=bookingscraper
echo.
echo Running install_clean_v46.sql...
psql -U %DB_USER% -d %DB_NAME% -f install_clean_v46.sql
if %errorlevel%==0 (
    echo Schema created successfully.
) else (
    echo ERROR: Schema creation failed. Check PostgreSQL is running and credentials are correct.
)
pause
