@echo off
REM Push to GitHub Repository
REM Repository: https://github.com/Nuntploydanai/CostingIntelligent

echo ========================================
echo Pushing to GitHub...
echo ========================================
echo.

cd /d "C:\Users\dploy\.openclaw\workspace\basicshirts_web"

echo Current directory: %CD%
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing git repository...
    git init
    echo.
)

REM Add all files
echo Adding files...
git add .
echo.

REM Create commit
echo Creating commit...
git commit -m "Initial commit: Basic Shirts Costing Webapp

- Excel-parity calculations for Steps 1-6
- Auto-calculate with 500ms debounce
- Total cost summary section
- Grey input field styling
- Master data extracted from Excel
- FastAPI backend + vanilla JS frontend"
echo.

REM Add remote repository
echo Adding remote repository...
git remote add origin https://github.com/Nuntploydanai/CostingIntelligent.git
echo.

REM Set branch to main
echo Setting branch to main...
git branch -M main
echo.

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main
echo.

echo ========================================
echo Success! Your code is now on GitHub!
echo ========================================
echo.
echo Repository URL:
echo https://github.com/Nuntploydanai/CostingIntelligent
echo.
pause
