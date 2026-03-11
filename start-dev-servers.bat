@echo off
echo ========================================
echo Starting Node.js v2 Development Server
echo ========================================
echo.

echo Starting backend server...
start /B cmd /k "npx ts-node server/dev-server.ts" powershell -NoExit -Command "cd C:\Users\dploy\.openclaw\workspace\basicshirts_web; npx ts-node server/dev-server.ts"

timeout /t 3 >nul 2>&1

echo.
echo Backend server starting on http://localhost:8000
echo.
echo Now starting frontend...
cd client
call npm run dev

echo.
echo ========================================
echo Both servers are running!
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo ========================================
