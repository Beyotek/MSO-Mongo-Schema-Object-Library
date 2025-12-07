# MSO Library - Publishing Guide

## Overview
This guide explains how to publish a new version of the MSO library to PyPI using the automated GitHub Actions workflow.

---

## Prerequisites

### 1. PyPI Trusted Publisher Configuration
You **MUST** configure Trusted Publisher on PyPI before the workflow will work.

Go to: https://pypi.org/manage/project/MSO/settings/publishing/

Add a new publisher with these **exact** settings:
- **Owner**: `Beyotek` (your organization name)
- **Repository name**: `MSO-Mongo-Schema-Object-Library`
- **Workflow name**: `python-publish.yml`
- **Environment name**: `release`

### 2. GitHub Token Secret
Ensure you have a `GH_TOKEN` secret configured in your GitHub repository:
- Go to: Settings → Secrets and variables → Actions
- Create a secret named `GH_TOKEN`
- Value: A GitHub Personal Access Token with `repo` and `workflow` permissions

---

## Publishing Steps

### Step 1: Make Your Changes
Make all code changes on the `master` branch locally.

```bash
# Make your changes
# Test them
# Commit them
git add .
git commit -m "Description of changes"
git push origin master
```

### Step 2: Create and Push a Tag
The workflow is triggered by pushing a git tag.

```bash
# Create a tag with the new version number
git tag 1.0.85

# Push the tag to GitHub
git push origin 1.0.85
```

**Important**: 
- Tag format should be just the version number: `1.0.85` (not `v1.0.85`)
- The version MUST be higher than the current version on PyPI
- Do NOT use `git push --tags 1.0.85` (wrong syntax)
- Use `git push origin 1.0.85` (correct)

### Step 3: Monitor the Workflow
1. Go to GitHub Actions: https://github.com/Beyotek/MSO-Mongo-Schema-Object-Library/actions
2. You should see a new "release" workflow running
3. Monitor the progress through these stages:
   - ✅ Prepare Data
   - ✅ Check PyPI (verifies version is newer)
   - ✅ Setup & Build (creates version branch, builds package)
   - ✅ Upload release to PyPI (publishes to PyPI)

---

## Workflow Breakdown

### What the Workflow Does:

1. **Prepare Data** (Job 1)
   - Extracts version from the tag you pushed
   - Gets package name from `pyproject.toml`

2. **Check PyPI** (Job 2)
   - Fetches latest version from PyPI
   - Verifies your new version is higher
   - Fails if version already exists or isn't newer

3. **Setup & Build** (Job 3)
   - Creates a new branch: `version-X.X.X`
   - Updates `pyproject.toml` with the new version
   - Commits and pushes this branch
   - Builds the Python package (wheel + source)
   - **Attempts to merge** `version-X.X.X` → `master`

4. **PyPI Publish** (Job 4)
   - Downloads the built package
   - Publishes to PyPI using Trusted Publisher

---

## Common Issues and Solutions

### Issue 1: Merge Conflict
**Error**: `409 - Merge conflict`

**Cause**: The workflow tries to merge the version branch back to master, but there are conflicts.

**Solution**:
```bash
# Manually merge the version branch
git checkout master
git pull origin version-1.0.X
# Resolve any conflicts in files (usually just pyproject.toml)
git add .
git commit -m "Merge version-1.0.X"
git push origin master
```

### Issue 2: Trusted Publisher Not Found
**Error**: `invalid-publisher: valid token, but no corresponding publisher`

**Solution**: 
- Verify PyPI Trusted Publisher is configured correctly
- Owner must be `Beyotek` (not `chuckbeyor101`)
- Repository must be `MSO-Mongo-Schema-Object-Library`
- Environment must be `release`

### Issue 3: Version Not Higher
**Error**: `The new version X.X.X is not greater than the latest version Y.Y.Y on PyPI`

**Solution**:
```bash
# Check current PyPI version
# Visit: https://pypi.org/project/MSO/

# Delete local tag
git tag -d 1.0.X

# Delete remote tag (if pushed)
git push --delete origin 1.0.X

# Create new tag with higher version
git tag 1.0.Y
git push origin 1.0.Y
```

### Issue 4: Wrong Tag Syntax
**Error**: `fatal: '1.0.80' does not appear to be a git repository`

**Wrong**:
```bash
git push --tag 1.0.80
git push --tags 1.0.80
```

**Correct**:
```bash
git tag 1.0.80
git push origin 1.0.80
```

---

## Manual Publishing (Alternative)

If the automated workflow fails, you can publish manually:

```bash
# Install poetry if not already installed
pip install poetry

# Update version in pyproject.toml manually
# Edit the version number

# Build the package
poetry build

# Publish to PyPI (requires PyPI token)
poetry publish
# Or with token:
poetry publish -u __token__ -p pypi-YOUR-TOKEN-HERE
```

---

## Version Strategy

### Current Version Scheme: `MAJOR.MINOR.PATCH`
- Example: `1.0.84`

### When to Increment:
- **MAJOR** (1.x.x): Breaking changes, major rewrites
- **MINOR** (x.1.x): New features, significant additions
- **PATCH** (x.x.1): Bug fixes, small improvements

### Current Status:
- Latest on PyPI: Check at https://pypi.org/project/MSO/
- Current in code: `1.0.84` (in `pyproject.toml`)

---

## Checklist Before Publishing

- [ ] All changes committed and pushed to `master`
- [ ] Code tested locally
- [ ] Version number is higher than current PyPI version
- [ ] PyPI Trusted Publisher configured (one-time setup)
- [ ] `GH_TOKEN` secret configured in GitHub
- [ ] Git remote points to `Beyotek/MSO-Mongo-Schema-Object-Library`
- [ ] README and documentation updated
- [ ] Examples tested

---

## Quick Reference Commands

```bash
# Update git remote (one-time)
git remote set-url origin https://github.com/Beyotek/MSO-Mongo-Schema-Object-Library.git

# Check current version on PyPI
curl -s https://pypi.org/pypi/MSO/json | grep -oP '"version":"\K[^"]+'

# Create and push tag
git tag 1.0.85
git push origin 1.0.85

# Delete tag if needed
git tag -d 1.0.85
git push --delete origin 1.0.85

# View tags
git tag -l

# Check workflow status
# Visit: https://github.com/Beyotek/MSO-Mongo-Schema-Object-Library/actions
```

---

## Workflow File Location
`.github/workflows/python-publish.yml`

## Support
- PyPI: https://pypi.org/project/MSO/
- GitHub: https://github.com/Beyotek/MSO-Mongo-Schema-Object-Library
- Issues: https://github.com/Beyotek/MSO-Mongo-Schema-Object-Library/issues
