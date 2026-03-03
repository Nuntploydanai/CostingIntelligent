@echo off
echo ========================================
echo Basic Shirts Costing Tool v2
echo Node.js + React Full Stack
echo ========================================
echo.

echo [1/4] Installing backend dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Backend installation failed
    pause
    exit /b 1
)

echo.
echo [2/4] Installing frontend dependencies...
cd client
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Frontend installation failed
    pause
    exit /b 1
)
cd ..

echo.
echo [3/4] Building frontend...
cd client
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Frontend build failed
    pause
    exit /b 1
)
cd ..

echo.
echo [4/4] Starting server...
echo.
echo ========================================
echo Server will run on: http://localhost:8000
echo Press Ctrl+C to stop
echo ========================================
echo.

node dist/server/index.js
