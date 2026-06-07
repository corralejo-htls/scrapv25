@echo off

REM Configura variables
set filename=schema_v77_complete.sql
set DB_NAME=bookingscraper
set DB_USER=postgres

echo Eliminando base de datos %DB_NAME%...
psql -U %DB_USER% -c "DROP DATABASE IF EXISTS %DB_NAME%;"
echo " "
echo "- - - "
pause

echo Creando base de datos %DB_NAME%...
psql -U %DB_USER% -c "CREATE DATABASE %DB_NAME%;"
echo " "
echo "- - - "
pause

echo Ejecutando script SQL...
psql -U %DB_USER% -d %DB_NAME% -f %filename%

echo Proceso completado.
pause

