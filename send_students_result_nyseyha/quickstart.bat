@echo off
REM Quick Start Script for Send Student Result System (Windows)

echo.
echo ========================================
echo Send Student Result System - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/5] Installing dependencies...
pip install -r requirements.txt

echo.
echo [4/5] Checking for .env file...
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env file with your email configuration!
    echo Open .env and update:
    echo   - MAIL_USERNAME
    echo   - MAIL_PASSWORD
    echo   - MAIL_DEFAULT_SENDER
    echo.
    pause
)

echo.
echo [5/5] Starting application...
echo.
echo ========================================
echo Application is starting...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause

