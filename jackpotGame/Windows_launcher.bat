@echo off
CD
python --version >NUL 2>NUL
if errorlevel 1 goto NOPYTHON
goto :HASPYTHON
:NOPYTHON
echo No tienes Python instalado, en la instalacion debes marcar VARIABLE DE ENTORNO
echo.
pause
Python


:HASPYTHON
pip install windows-curses
python jackpotGame.py

pause>NUL