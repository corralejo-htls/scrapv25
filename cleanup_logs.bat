@echo off
REM cleanup_logs.bat — Limpia archivos de log y HTML debug antiguos
SETLOCAL
SET PYTHONPATH=%~dp0

IF EXIST "venv\Scripts\activate.bat" CALL "venv\Scripts\activate.bat"

ECHO Limpiando logs antiguos...

REM Eliminar logs de aplicacion con mas de 30 dias
forfiles /P "logs" /S /M "*.log" /D -30 /C "cmd /c del @path" 2>NUL

REM Eliminar HTML debug de data\logs\debug con mas de 1 dia
forfiles /P "data\logs\debug" /S /M "*.html" /D -1 /C "cmd /c del @path" 2>NUL

ECHO Limpieza completada.
ENDLOCAL
