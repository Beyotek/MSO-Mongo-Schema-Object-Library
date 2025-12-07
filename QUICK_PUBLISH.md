# Quick Start - Publishing MSO

## ⚡ Fast Track Publishing

### 1. First Time Setup (Do Once)

**A. Update Git Remote**
```bash
git remote set-url origin https://github.com/Beyotek/MSO-Mongo-Schema-Object-Library.git
```

**B. Configure PyPI Trusted Publisher**
1. Go to: https://pypi.org/manage/project/MSO/settings/publishing/
2. Click "Add a new publisher"
3. Fill in:
   - **Owner**: `Beyotek`
   - **Repository**: `MSO-Mongo-Schema-Object-Library`
   - **Workflow**: `python-publish.yml`
   - **Environment**: `release`
4. Click "Add"

**C. Verify GitHub Token**
- Go to: https://github.com/Beyotek/MSO-Mongo-Schema-Object-Library/settings/secrets/actions
- Ensure `GH_TOKEN` exists

---

### 2. Publishing a New Version

**Step 1: Make your changes**
```bash
# Edit files
git add .
git commit -m "Your changes"
git push origin master
```

**Step 2: Create and push tag**
```bash
# Check current version on PyPI first
# https://pypi.org/project/MSO/

# Create tag (must be higher than PyPI version)
git tag 1.0.85

# Push tag to trigger workflow
git push origin 1.0.85
```

**Step 3: Monitor**
- Go to: https://github.com/Beyotek/MSO-Mongo-Schema-Object-Library/actions
- Wait for workflow to complete (~5 minutes)

**Step 4: Handle merge conflict (if needed)**
If the workflow shows a merge error:
```bash
git checkout master
git pull origin version-1.0.85
# Edit pyproject.toml to resolve conflict (keep higher version)
git add .
git commit -m "Merge version-1.0.85"
git push origin master
```

**Step 5: Verify**
- Check: https://pypi.org/project/MSO/
- New version should appear within 5-10 minutes

---

## 🔧 Common Commands

```bash
# Check current PyPI version
curl -s https://pypi.org/pypi/MSO/json | grep '"version"' | head -1

# List local tags
git tag -l

# Delete a tag (if you made a mistake)
git tag -d 1.0.85
git push --delete origin 1.0.85

# View workflow runs
# Visit: https://github.com/Beyotek/MSO-Mongo-Schema-Object-Library/actions
```

---

## 📝 Version Numbering

Format: `MAJOR.MINOR.PATCH`

- **1**.0.0 - Breaking changes
- 1.**1**.0 - New features
- 1.0.**1** - Bug fixes

Current: `1.0.84`
Next: `1.0.85`

---

## ❌ Common Mistakes

**DON'T:**
```bash
git push --tag 1.0.85        # Wrong syntax
git push --tags 1.0.85       # Wrong syntax
git tag v1.0.85              # Don't use 'v' prefix
```

**DO:**
```bash
git tag 1.0.85               # Correct
git push origin 1.0.85       # Correct
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Trusted publisher not found" | Configure PyPI Trusted Publisher (see Setup) |
| "Version not higher than PyPI" | Use a higher version number |
| "Merge conflict" | Manually merge (see Step 4 above) |
| "Repository not found" | Update git remote (see Setup) |

---

## 📚 Full Documentation

For detailed information, see:
- **PUBLISHING.md** - Complete publishing guide
- **WORKFLOW_ANALYSIS.md** - Technical workflow analysis

---

## ✅ Pre-Publish Checklist

- [ ] Code tested locally
- [ ] Changes committed and pushed to master
- [ ] Version number chosen (higher than PyPI)
- [ ] PyPI Trusted Publisher configured
- [ ] Git remote updated to Beyotek org
