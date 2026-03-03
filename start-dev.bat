@echo off
echo ========================================
echo Basic Shirts Costing Tool v2 - DEV MODE
echo ========================================
echo.
echo Starting development servers...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press Ctrl+C to stop both servers
echo ========================================
echo.

:: Start both servers using concurrently
npx concurrently "npx ts-node server/index.ts" "cd client && npm run dev"
