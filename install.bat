@echo off

echo installing virtual environment..
python -m venv venv

echo activating virtual environment..
call venv\Scripts\activate.bat

echo installing dependencies..
pip install -r requirements.txt

echo running script
python vlc-script.py

pause
