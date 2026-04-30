@echo off
echo ========================================
echo Mutual Fund FAQ Assistant - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Navigate to phase 1
cd "phase 1"

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.
echo Dependencies installed successfully!
echo.

REM Run Phase 1 setup
echo ========================================
echo Running Phase 1 Setup...
echo ========================================
echo.
cd src
python phase1_setup.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Check the output above for any errors
echo 2. Update .env file with your GROQ_API_KEY
echo 3. Proceed to Phase 2 implementation
echo.
pause
