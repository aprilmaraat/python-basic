# FastAPI Expense Tracker - Background Startup Script
# This script starts the server in the background without a console window

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectPath

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  FastAPI Expense Tracker" -ForegroundColor Green
Write-Host "  Starting Server in Background..." -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if server is already running
$existingProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*main:app*"
}

if ($existingProcess) {
    Write-Host "⚠ Server is already running (PID: $($existingProcess.Id))" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To stop it, run: Stop-Process -Id $($existingProcess.Id)" -ForegroundColor Yellow
    exit
}

# Start the server in background
Write-Host "Starting FastAPI server..." -ForegroundColor Green

$process = Start-Process python `
    -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" `
    -WindowStyle Hidden `
    -PassThru `
    -WorkingDirectory $projectPath

if ($process) {
    Write-Host "✓ Server started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Process ID: $($process.Id)" -ForegroundColor Cyan
    Write-Host "Access URL: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To stop the server, run:" -ForegroundColor Yellow
    Write-Host "  Stop-Process -Id $($process.Id)" -ForegroundColor White
    Write-Host ""
    Write-Host "Or use Task Manager to end the 'python.exe' process" -ForegroundColor Yellow
} else {
    Write-Host "✗ Failed to start server" -ForegroundColor Red
    exit 1
}
