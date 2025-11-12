# FastAPI Expense Tracker - Stop Server Script
# This script stops the running FastAPI server

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  FastAPI Expense Tracker" -ForegroundColor Red
Write-Host "  Stopping Server..." -ForegroundColor Red
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Find running uvicorn processes
$processes = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*main:app*"
}

if ($processes) {
    $count = ($processes | Measure-Object).Count
    Write-Host "Found $count running server process(es)" -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($proc in $processes) {
        Write-Host "Stopping process ID: $($proc.Id)" -ForegroundColor Yellow
        Stop-Process -Id $proc.Id -Force
        Write-Host "✓ Process stopped" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "✓ Server stopped successfully!" -ForegroundColor Green
} else {
    Write-Host "No running server found" -ForegroundColor Yellow
}

Write-Host ""
