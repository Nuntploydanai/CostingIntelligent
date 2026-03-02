@echo off
REM Fix Git Push Error - Step by Step
REM Repository: https://github.com/Nuntploydanai/CostingIntelligent

echo ========================================
echo Fixing Git Push Error
echo ========================================
echo.

cd /d "C:\Users\dploy\.openclaw\workspace\basicshirts_web"

echo Step 1: Checking current status...
git status
echo.

echo Step 2: Adding all files...
git add .
echo.

echo Step 3: Checking what will be committed...
git status
echo.

echo Step 4: Creating commit...
git commit -m "Initial commit: Basic Shirts Costing Webapp"
echo.

echo Step 5: Checking branches...
git branch
echo.

echo Step 6: Renaming branch to main (if needed)...
git branch -M main
echo.

echo Step 7: Checking remote...
git remote -v
echo.

echo Step 8: Removing old remote (if exists)...
git remote remove origin 2>nul
echo.

echo Step 9: Adding remote repository...
git remote add origin https://github.com/Nuntploydanai/CostingIntelligent.git
echo.

echo Step 10: Pushing to GitHub...
git push -u origin main
echo.

if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo SUCCESS! Your code is on GitHub!
    echo ========================================
    echo.
    echo Visit: https://github.com/Nuntploydanai/CostingIntelligent
    echo.
) else (
    echo ========================================
    echo Push failed. Check the error above.
    echo ========================================
    echo.
    echo Common fixes:
    echo 1. You may need to authenticate with GitHub
    echo 2. Run: gh auth login
    echo 3. Or use Personal Access Token instead of password
    echo.
)

pause
