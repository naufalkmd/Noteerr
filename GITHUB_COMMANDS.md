# GitHub Actions Quick Reference

Commands for common GitHub publishing tasks.

---

## 🚀 First Time Setup

```bash
cd C:\Users\naufalkmd\Documents\Noteerr

# Initialize git (if needed)
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Noteerr v1.1.0

- Copy to clipboard functionality
- Smart duplicate detection
- Project organization
- Enhanced installation
- Package manager ready"

# Set main branch
git branch -M main

# Add remote (replace yourusername with your GitHub username)
git remote add origin https://github.com/yourusername/noteerr.git

# Push to GitHub
git push -u origin main
```

---

## 🏷️ Creating a Release

### Method 1: Tag and Let GitHub Actions Handle It

```bash
# Make sure everything is committed
git status

# Build distribution
python -m build

# Create annotated tag
git tag -a v1.1.0 -m "Release v1.1.0: Copy, Dedup, Projects"

# Push tag to trigger release workflow
git push origin v1.1.0

# GitHub Actions will:
# ✓ Build the package
# ✓ Run tests
# ✓ Create GitHub Release
# ✓ Upload distribution files
# ✓ Publish to PyPI (if token configured)
```

### Method 2: Manual Release Creation

```bash
# Build distributions
python -m build

# Creates:
# - dist/noteerr-1.1.0-py3-none-any.whl
# - dist/noteerr-1.1.0.tar.gz

# Then go to GitHub:
# 1. Navigate to your repository
# 2. Click "Releases" → "Create a new release"
# 3. Choose tag: v1.1.0 (or create new tag)
# 4. Fill in title and description
# 5. Upload files from dist/ folder
# 6. Click "Publish release"
```

---

## 🔄 Regular Development Workflow

```bash
# Make changes to code
# ...

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: [feature description]"

# Push to GitHub
git push

# GitHub Actions will run CI tests automatically
```

---

## 📦 Publishing to PyPI

### Automatic (via GitHub Actions)

```bash
# Just push a tag!
git tag v1.1.0
git push origin v1.1.0

# Requires PYPI_API_TOKEN secret in GitHub
```

### Manual

```bash
# Install tools
pip install build twine

# Build
python -m build

# Check
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Or test first on TestPyPI
twine upload --repository testpypi dist/*
```

---

## 🔍 Checking Status

```bash
# View all tags
git tag -l

# View remote URL
git remote -v

# Check current branch
git branch

# View commit history
git log --oneline

# Check workflow runs (visit GitHub)
# https://github.com/yourusername/noteerr/actions
```

---

## 🛠️ Common Tasks

### Update Version Number

Files to update:
1. `src/noteerr/__init__.py` - `__version__ = "1.1.0"`
2. `setup.py` - `version="1.1.0"`
3. `pyproject.toml` - `version = "1.1.0"`
4. `chocolatey/noteerr.nuspec` - `<version>1.1.0</version>`
5. All winget manifests
6. `homebrew/noteerr.rb` - version field

### Delete a Tag (if made a mistake)

```bash
# Delete local tag
git tag -d v1.1.0

# Delete remote tag
git push origin --delete v1.1.0

# Create corrected tag
git tag -a v1.1.0 -m "Corrected release"
git push origin v1.1.0
```

### View File Differences

```bash
# See what changed
git diff

# See differences in a specific file
git diff README.md

# See differences between commits
git diff v1.0.0 v1.1.0
```

### Undo Last Commit (not pushed)

```bash
# Keep changes in working directory
git reset --soft HEAD~1

# Discard changes completely
git reset --hard HEAD~1
```

---

## 🎯 Release Checklist Commands

```bash
# 1. Update version numbers
# (manually edit files)

# 2. Update CHANGELOG.md
# (manually edit)

# 3. Test locally
python -m build
pip install dist/noteerr-1.1.0-py3-none-any.whl --force-reinstall
noteerr --version

# 4. Run tests
python test_noteerr.py

# 5. Commit version bump
git add .
git commit -m "Bump version to 1.1.0"
git push

# 6. Create and push tag
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0

# 7. Monitor GitHub Actions
# Visit: https://github.com/yourusername/noteerr/actions

# 8. Verify PyPI upload
# Visit: https://pypi.org/project/noteerr/

# 9. Test installation from PyPI
pip install noteerr --upgrade
```

---

## 📊 View Package Downloads

```bash
# GitHub releases
# Visit: https://github.com/yourusername/noteerr/releases

# PyPI stats
# Visit: https://pypistats.org/packages/noteerr
```

---

## 🔐 Setting Up PyPI Token

1. **Create PyPI account**: https://pypi.org/account/register/
2. **Go to Account Settings** → API tokens
3. **Create token** with "Upload packages" scope
4. **Add to GitHub Secrets**:
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: `pypi-...` (your token)

---

## 🌐 Setting Up GitHub Personal Access Token (for CLI)

```bash
# Install GitHub CLI
winget install GitHub.cli

# Login
gh auth login

# Now you can use GitHub CLI for releases
gh release create v1.1.0 dist/* --title "v1.1.0" --notes "Release notes here"
```

---

## 📝 Quick Reference Links

- **Repository**: https://github.com/yourusername/noteerr
- **Releases**: https://github.com/yourusername/noteerr/releases
- **Actions**: https://github.com/yourusername/noteerr/actions
- **PyPI**: https://pypi.org/project/noteerr/
- **Issues**: https://github.com/yourusername/noteerr/issues

---

## 🆘 Troubleshooting

### "remote: Permission denied"
```bash
# Check your GitHub auth
gh auth status

# Re-authenticate if needed
gh auth login
```

### "tag already exists"
```bash
# Delete and recreate
git tag -d v1.1.0
git push origin --delete v1.1.0
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

### "failed to push some refs"
```bash
# Pull first, then push
git pull --rebase
git push
```

### GitHub Actions Failing
1. Check workflow run logs in Actions tab
2. Common issues:
   - Missing `PYPI_API_TOKEN` secret
   - Syntax errors in YAML files
   - Python version incompatibility

---

**Copy these commands and replace `yourusername` with your actual GitHub username!**
