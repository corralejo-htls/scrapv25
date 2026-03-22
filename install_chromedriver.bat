@echo off
title BookingScraper - Instalar ChromeDriver para Brave

cd /d C:\BookingScraper

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo ============================================================
echo  BookingScraper Pro v48 - Instalar ChromeDriver para Brave
echo ============================================================

python install_chromedriver_helper.py

pause
