@echo off
REM Employee Attrition Prediction System - Setup Script for Windows

echo ==========================================
echo Employee Attrition System - Setup Script
echo ==========================================
echo.

REM Check Python installation
echo 1. Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

python --version
echo.

REM Create virtual environment
echo 2. Creating virtual environment...
if exist "venv\" (
    echo Virtual environment already exists.
) else (
    python -m venv venv
    echo OK Virtual environment created
)
echo.

REM Activate virtual environment
echo 3. Activating virtual environment...
call venv\Scripts\activate.bat
echo OK Virtual environment activated
echo.

REM Install dependencies
echo 4. Installing dependencies...
pip install -r requirements.txt
echo OK Dependencies installed
echo.

REM Create database
echo 5. Initializing database...
python -c "from app import create_app, db; app = create_app(); db.create_all() if app else None"
echo OK Database initialized
echo.

REM Summary
echo ==========================================
echo OK Setup Complete!
echo ==========================================
echo.
echo To run the application:
echo   1. Activate virtual environment:
echo      venv\Scripts\activate.bat
echo   2. Run the application:
echo      python run.py
echo   3. Open browser at http://localhost:5000
echo.
echo Default Credentials:
echo   Username: demo
echo   Password: demo123
echo.
echo ==========================================
pause
