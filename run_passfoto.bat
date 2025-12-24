@echo off
REM PassFoto - Windows Startup Script
REM Double-click this file to run PassFoto

echo ========================================
echo    PassFoto - Passport Photo Enhancer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Checking dependencies...

REM Check if dependencies are installed
python -c "import cv2" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo Starting PassFoto...
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo Application exited with an error.
    pause
)
