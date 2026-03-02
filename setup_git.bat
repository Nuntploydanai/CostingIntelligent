@echo off
REM Initialize Git Repository for Basic Shirts Costing Webapp

echo ========================================
echo Setting up Git repository...
echo ========================================

cd basicshirts_web

REM Initialize git repository
git init

REM Add all files
git add .

REM Create initial commit
git commit -m "Initial commit: Basic Shirts Costing Webapp

- Excel-parity calculations for Steps 1-6
- Auto-calculate with 500ms debounce
- Total cost summary section
- Grey input field styling
- Master data extracted from Excel
- FastAPI backend + vanilla JS frontend"

echo.
echo ========================================
echo Git repository initialized!
echo ========================================
echo.
echo Next steps:
echo 1. Create a new repository on GitHub (https://github.com/new)
echo 2. Copy the repository URL
echo 3. Run these commands:
echo.
echo    git remote add origin ^<your-repo-url^>
echo    git branch -M main
echo    git push -u origin main
echo.
echo Or use GitHub CLI (if installed):
echo.
echo    gh repo create basicshirts-web --public --source=. --push
echo.
pause
