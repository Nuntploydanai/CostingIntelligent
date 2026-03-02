@echo off
REM ========================================
REM Push Code to GitHub - Step by Step
REM ========================================
REM Repository: https://github.com/Nuntploydanai/CostingIntelligent
REM ========================================

echo.
echo ========================================
echo PUSHING YOUR CODE TO GITHUB
echo ========================================
echo.
echo This will upload your Basic Shirts Costing Webapp to:
echo https://github.com/Nuntploydanai/CostingIntelligent
echo.
pause

cd /d "C:\Users\dploy\.openclaw\workspace\basicshirts_web"

echo.
echo ========================================
echo STEP 1: Checking Git Status
echo ========================================
echo.
git status
echo.
pause

echo.
echo ========================================
echo STEP 2: Adding All Files
echo ========================================
echo.
git add .
echo.
echo Files added successfully!
echo.
pause

echo.
echo ========================================
echo STEP 3: Creating Commit
echo ========================================
echo.
git commit -m "Initial commit: Basic Shirts Costing Webapp"
echo.
echo Commit created!
echo.
pause

echo.
echo ========================================
echo STEP 4: Setting Branch to Main
echo ========================================
echo.
git branch -M main
echo.
echo Branch set to 'main'
echo.
pause

echo.
echo ========================================
echo STEP 5: Adding Remote Repository
echo ========================================
echo.
git remote remove origin 2>nul
git remote add origin https://github.com/Nuntploydanai/CostingIntelligent.git
echo.
echo Remote added!
echo.
pause

echo.
echo ========================================
echo STEP 6: Pushing to GitHub
echo ========================================
echo.
echo This will upload your code to GitHub...
echo A browser window may open for authentication.
echo Please click "Authorize" if asked.
echo.
pause

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Your code is on GitHub!
    echo ========================================
    echo.
    echo Visit your repository:
    echo https://github.com/Nuntploydanai/CostingIntelligent
    echo.
    echo You should see all your files!
    echo.
) else (
    echo.
    echo ========================================
    echo Push failed. Trying force push...
    echo ========================================
    echo.
    git push -f origin main
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ========================================
        echo SUCCESS! Your code is on GitHub!
        echo ========================================
        echo.
        echo Visit: https://github.com/Nuntploydanai/CostingIntelligent
        echo.
    ) else (
        echo.
        echo ========================================
        echo Still having issues?
        echo ========================================
        echo.
        echo Run this command in PowerShell:
        echo git push -f origin main
        echo.
    )
)

echo.
pause
