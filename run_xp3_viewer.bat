@echo off
REM XP3 Viewer and Converter Launcher for Windows
REM This batch file will run the XP3 Viewer and Converter application

echo Starting XP3 Viewer and Converter...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.7 or later from https://python.org
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Checking and installing dependencies...
pip install -r requirements.txt

REM Run the application
echo Launching XP3 Viewer and Converter...
python xp3_viewer_converter.py

REM Pause to see any error messages
if errorlevel 1 (
    echo.
    echo The application exited with an error.
    pause
)
