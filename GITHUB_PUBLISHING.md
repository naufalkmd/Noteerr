# GitHub Publishing Guide

Step-by-step guide to publish Noteerr on GitHub.

---

## 🚀 Initial Setup

### 1. Create GitHub Repository

1. **Go to GitHub** (https://github.com/new)
2. **Repository name**: `noteerr`
3. **Description**: "Command Error Memory Tool - Never forget how you fixed that bug again"
4. **Visibility**: Public
5. **Don't** initialize with README (we have one)
6. Click **Create repository**

### 2. Configure Local Repository

```bash
cd C:\Users\naufalkmd\Documents\Noteerr

# Initialize git (if not already)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Noteerr v1.1.0"

# Set main branch
git branch -M main

# Add remote (replace yourusername)
git remote add origin https://github.com/yourusername/noteerr.git

# Push to GitHub
git push -u origin main
```

---

## 🏷️ Creating Your First Release

### Option 1: Using GitHub Web Interface

1. **Go to your repository** on GitHub
2. **Click "Releases"** (right sidebar)
3. **Click "Create a new release"**
4. **Choose a tag**: `v1.1.0`
5. **Release title**: `Noteerr v1.1.0 - Copy, Dedup, Projects`
6. **Description**: Copy from `RELEASE_NOTES_v1.1.0.md`
7. **Attach binaries**: Upload files from `dist/` folder (after building)
8. **Click "Publish release"**

### Option 2: Using Git Tags (triggers GitHub Actions)

```bash
# Build distribution first
python -m build

# Create annotated tag
git tag -a v1.1.0 -m "Release v1.1.0: Copy to clipboard, Smart duplicate detection, Project organization"

# Push tag
git push origin v1.1.0

# GitHub Actions will automatically:
# - Build the package
# - Create GitHub release  
# - Publish to PyPI (if PYPI_API_TOKEN is set)
```

---

## ⚙️ GitHub Repository Settings

### 1. Add Topics (for discoverability)

Go to repository → About → ⚙️ Settings

Add topics:
- `cli`
- `command-line`
- `developer-tools`
- `error-logging`
- `productivity`
- `python`
- `terminal`
- `debugging`
- `annotations`
- `clipboard`

### 2. Set Repository Description

```
Command Error Memory Tool - Never forget how you fixed that bug again! 🚨
```

### 3. Enable Features

- ✅ Issues
- ✅ Discussions (optional)
- ✅ Projects (optional)
- ✅ Wiki (optional)

---

## 🔐 GitHub Secrets (for CI/CD)

Add secrets for automated publishing:

1. **Go to repository Settings** → Secrets and variables → Actions
2. **Click "New repository secret"**
3. **Add**:
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token from https://pypi.org/manage/account/

---

## 📋 Repository Files to Add

Make sure these files exist (they do in your project):

- ✅ `.gitignore` - Ignore unnecessary files
- ✅ `LICENSE` - MIT License
- ✅ `README.md` - Main documentation
- ✅ `CHANGELOG.md` - Version history
- ✅ `.github/workflows/ci.yml` - CI tests
- ✅ `.github/workflows/release.yml` - Auto-release on tags

---

## 🎨 Add a Logo/Icon (Optional)

1. Create a `logo.png` or `icon.png` (256x256 recommended)
2. Add to repository root
3. Update:
   - `chocolatey/noteerr.nuspec` iconUrl
   - Social preview in repository settings

---

## 📝 Update Links in Files

Replace `yourusername` with your actual GitHub username in:

- [x] `setup.py` - url field
- [x] `README.md` - all GitHub links
- [x] `CHANGELOG.md` - release links
- [x] `DISTRIBUTION.md` - repository URLs
- [x] All `winget/*.yaml` files
- [x] `chocolatey/noteerr.nuspec`
- [x] `homebrew/noteerr.rb`

**Find and replace:**
```bash
# Find all occurrences
grep -r "yourusername" .

# Replace (adjust as needed)
# Manually update each file
```

---

## 🏃 Continuous Integration

The `.github/workflows/ci.yml` runs on every push:

- Tests on Windows, macOS, Linux
- Tests Python 3.8, 3.9, 3.10, 3.11
- Verifies installation works
- Runs basic functionality tests

**Status badge** for README:
```markdown
![CI](https://github.com/yourusername/noteerr/actions/workflows/ci.yml/badge.svg)
```

---

## 🚢 Release Workflow

When you push a tag (e.g., `v1.1.0`):

1. **GitHub Actions** triggers `release.yml`
2. **Builds** Python wheel and source distribution
3. **Creates GitHub Release** with changelog
4. **Uploads** distribution files to release
5. **Publishes to PyPI** (if token configured)

All automatic! 🎉

---

## 📦 Building Distributions

Before creating a release:

```bash
# Install build tools
pip install build twine

# Build distributions
python -m build

# This creates:
# - dist/noteerr-1.1.0-py3-none-any.whl (wheel)
# - dist/noteerr-1.1.0.tar.gz (source)

# Verify
twine check dist/*
```

---

## 🌟 Post-Publication

### 1. Add Shields/Badges to README

```markdown
![Version](https://img.shields.io/github/v/release/yourusername/noteerr)
![Downloads](https://img.shields.io/github/downloads/yourusername/noteerr/total)
![Stars](https://img.shields.io/github/stars/yourusername/noteerr)
![License](https://img.shields.io/github/license/yourusername/noteerr)
![CI](https://github.com/yourusername/noteerr/actions/workflows/ci.yml/badge.svg)
```

### 2. Share Your Project

- Reddit: r/Python, r/commandline
- Hacker News: news.ycombinator.com
- Twitter/X
- LinkedIn
- Dev.to

### 3. Submit to Lists

- **Awesome Lists**: Search for "awesome-cli" on GitHub
- **Product Hunt**: producthunt.com
- **Hacker News Show HN**: news.ycombinator.com

---

## 🔄 Future Updates

For subsequent releases:

```bash
# 1. Update version numbers
# - src/noteerr/__init__.py
# - setup.py
# - pyproject.toml
# - All package manager files

# 2. Update CHANGELOG.md

# 3. Commit changes
git add .
git commit -m "Bump version to 1.2.0"
git push

# 4. Create and push tag
git tag -a v1.2.0 -m "Release v1.2.0: New features..."
git push origin v1.2.0

# 5. GitHub Actions handles the rest!
```

---

## ✅ Quick Start Checklist

- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Update all `yourusername` references
- [ ] Add `PYPI_API_TOKEN` secret (for auto-publish)
- [ ] Build distributions (`python -m build`)
- [ ] Create release tag (`git tag v1.1.0`)
- [ ] Push tag (`git push origin v1.1.0`)
- [ ] Verify GitHub Release was created
- [ ] Verify PyPI publish (if configured)
- [ ] Add badges to README
- [ ] Share on social media

---

## 📞 Getting Help

- **GitHub Docs**: https://docs.github.com
- **GitHub Actions**: https://docs.github.com/actions
- **PyPI Publishing**: https://packaging.python.org/

---

**Ready to publish?** Just follow the steps above! The automation will handle most of the work. 🚀
