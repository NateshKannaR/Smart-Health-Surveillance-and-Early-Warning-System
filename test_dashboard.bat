@echo off
echo Testing Health Surveillance Dashboard...
echo.

echo 1. Checking backend server...
curl -s http://localhost:8000/health
echo.

echo 2. Checking alerts API...
curl -s http://localhost:8000/api/alerts | jq length
echo.

echo 3. Starting dashboard (if not running)...
echo Navigate to: http://localhost:3000/alerts
echo.

echo Dashboard should show:
echo - 1 Critical alert (Mumbai Central)
echo - 2 High alerts (Delhi NCR, Test Location)  
echo - 1 Medium alert (Bangalore)
echo - 1 Low alert (Chennai)
echo.

echo If dashboard is not working:
echo 1. cd dashboard
echo 2. npm start
echo 3. Open http://localhost:3000/alerts

pause