@echo off
REM FastAPI Expense Tracker - Setup Script
REM This script sets up the application for first-time use

echo ======================================
echo   FastAPI Expense Tracker
echo   Initial Setup
echo ======================================
echo.

cd /d "%~dp0"

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.13 or higher
    pause
    exit /b 1
)

echo [1/4] Python detected:
python --version
echo.

REM Create virtual environment (optional but recommended)
echo [2/4] Setting up virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/4] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo ✓ Dependencies installed
echo.

REM Initialize database
echo [4/4] Checking database...
if not exist fastapi.db (
    echo Creating initial database...
    python -c "from app.db.session import Base, engine; Base.metadata.create_all(bind=engine); print('✓ Database created')"
) else (
    echo ✓ Database already exists
)
echo.

echo ======================================
echo   Setup Complete!
echo ======================================
echo.
echo Next steps:
echo   1. Double-click 'start_server.bat' to start the server
echo   2. Open http://localhost:8000/docs in your browser
echo   3. See DEPLOYMENT.md for auto-start instructions
echo.
pause
