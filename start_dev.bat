@echo off
REM ========================================
REM Start Development Environment
REM ========================================

echo.
echo ========================================
echo STARTING DEVELOPMENT ENVIRONMENT
echo ========================================
echo.
echo This will start:
echo 1. Backend (Python) on port 8000
echo 2. Frontend (React) on port 5173
echo.
echo Press any key to start...
pause >nul

echo.
echo Starting Backend (Python)...
echo.
start "Backend Server" cmd /k "cd /d C:\Users\dploy\.openclaw\workspace\basicshirts_web && python server.py"

timeout /t 2 /nobreak >nul

echo.
echo Starting Frontend (React)...
echo.
start "Frontend Dev Server" cmd /k "cd /d C:\Users\dploy\.openclaw\workspace\basicshirts_web\frontend && npm run dev"

echo.
echo ========================================
echo BOTH SERVERS STARTED!
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo Frontend UI:  http://localhost:5173
echo.
echo Press any key to open browser...
pause >nul

start http://localhost:5173

echo.
echo Browser opened!
echo.
echo To stop: Close both terminal windows
echo.
pause
