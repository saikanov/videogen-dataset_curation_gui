@echo off

echo activating virtual environment..
call venv\Scripts\activate.bat

echo running script
python vlc-script.py

pause
