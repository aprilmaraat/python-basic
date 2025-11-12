@echo off
REM FastAPI Expense Tracker - Startup Script
REM This script starts the FastAPI application server

echo ======================================
echo   FastAPI Expense Tracker
echo   Starting Server...
echo ======================================

cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Start the FastAPI server
echo Starting FastAPI server on http://localhost:8000
echo.
echo Access the application at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ======================================
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
