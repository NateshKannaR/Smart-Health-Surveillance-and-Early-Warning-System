@echo off
echo Health Surveillance System - Quick Deploy
echo ==========================================

echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Setting up database...
python setup_database.py
if errorlevel 1 (
    echo ERROR: Failed to setup database
    pause
    exit /b 1
)

echo.
echo Starting backend server...
cd backend
start "Health Surveillance API" python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Checking if Node.js is available for dashboard...
node --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Node.js not found. Dashboard will not start.
    echo You can install Node.js from https://nodejs.org/
    goto :backend_only
)

echo.
echo Installing dashboard dependencies...
cd ..\dashboard
npm install
if errorlevel 1 (
    echo WARNING: Failed to install dashboard dependencies
    goto :backend_only
)

echo.
echo Starting dashboard...
start "Health Surveillance Dashboard" npm start

:backend_only
echo.
echo ========================================
echo   DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Dashboard: http://localhost:3000 (if Node.js available)
echo.
echo Press any key to open API documentation...
pause >nul
start http://localhost:8000/docs

echo.
echo Services are running in background windows.
echo Close those windows to stop the services.
pause