echo off
cls
del _arbol_.txt
del _list_pip.txt
dir /o:e /s >_arbol_.txt
pip list >_list_pip.txt
dir _*.txt
cleanup_logs.bat
