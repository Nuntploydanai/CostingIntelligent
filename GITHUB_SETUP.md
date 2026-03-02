# How to Share to GitHub

## Step 1: Initialize Git Repository

Open PowerShell in the project directory and run:

```powershell
cd C:\Users\dploy\.openclaw\workspace\basicshirts_web

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Basic Shirts Costing Webapp"
```

## Step 2: Create GitHub Repository

### Option A: Using GitHub Website

1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name**: `basicshirts-web`
   - **Description**: Web-based Basic Shirts Costing Tool with Excel-parity calculations
   - **Public** or **Private** (your choice)
   - **Don't initialize** with README (we already have one)
3. Click **Create repository**
4. Copy the repository URL (e.g., `https://github.com/yourusername/basicshirts-web.git`)

### Option B: Using GitHub CLI (if installed)

```powershell
# Create repository and push in one command
gh repo create basicshirts-web --public --source=. --push
```

## Step 3: Push to GitHub

If you used Option A (website):

```powershell
# Add remote repository
git remote add origin https://github.com/yourusername/basicshirts-web.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Verify

1. Go to your repository on GitHub
2. Check that all files are uploaded
3. The README.md should be displayed on the main page

## What's Included

✅ All Python backend files
✅ All calculation modules
✅ Web frontend (index.html)
✅ Master data (CSV files)
✅ README.md with documentation
✅ .gitignore to exclude unnecessary files

## What's Excluded

❌ Python cache files (__pycache__/)
❌ Virtual environments (venv/)
❌ IDE settings (.vscode/, .idea/)
❌ Secrets and credentials
❌ Media files
❌ Excel source file (too large, contains data)

## Future Updates

When you make changes:

```powershell
# Check what changed
git status

# Add changed files
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Quick Command Summary

```powershell
# First time setup
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main

# Future updates
git add .
git commit -m "Your message"
git push
```

## Troubleshooting

**Error: "git not found"**
- Install Git from https://git-scm.com/downloads

**Error: "Authentication failed"**
- Use GitHub CLI: `gh auth login`
- Or use Personal Access Token instead of password

**Large files warning**
- The .gitignore excludes large files
- If needed, use Git LFS for large files

---

Need help? Ask me anytime! 🚀
