# Package Manager Distribution Guide

This guide covers how to distribute Noteerr through various package managers.

---

## 📦 Supported Package Managers

- **Winget** (Windows Package Manager)
- **Chocolatey** (Windows)
- **Homebrew** (macOS/Linux)
- **PyPI** (Cross-platform)

---

## 🪟 Winget (Windows Package Manager)

### Setup

Winget manifests are located in the `winget/` directory.

### Files

- `YourPublisher.Noteerr.yaml` - Main manifest
- `YourPublisher.Noteerr.locale.en-US.yaml` - Locale manifest
- `YourPublisher.Noteerr.installer.yaml` - Installer manifest

### Publishing to Winget

1. **Fork the winget-pkgs repository**
   ```bash
   git clone https://github.com/microsoft/winget-pkgs.git
   cd winget-pkgs
   ```

2. **Create manifest directory**
   ```bash
   mkdir -p manifests/y/YourPublisher/Noteerr/1.1.0
   ```

3. **Copy manifests**
   ```bash
   cp ../noteerr/winget/*.yaml manifests/y/YourPublisher/Noteerr/1.1.0/
   ```

4. **Update SHA256 hash**
   - Download your release .whl file
   - Calculate SHA256: `certutil -hashfile noteerr-1.1.0-py3-none-any.whl SHA256`
   - Update hash in `YourPublisher.Noteerr.installer.yaml`

5. **Submit PR**
   ```bash
   git checkout -b noteerr-1.1.0
   git add manifests/y/YourPublisher/Noteerr/
   git commit -m "Add Noteerr version 1.1.0"
   git push origin noteerr-1.1.0
   ```

6. **Create Pull Request** on GitHub

### User Installation

```powershell
winget install YourPublisher.Noteerr
```

---

## 🍫 Chocolatey (Windows)

### Setup

Chocolatey package files are in the `chocolatey/` directory.

### Files

- `noteerr.nuspec` - Package specification
- `tools/chocolateyinstall.ps1` - Install script
- `tools/chocolateyuninstall.ps1` - Uninstall script

### Building Package

```powershell
cd chocolatey
choco pack
```

This creates `noteerr.1.1.0.nupkg`

### Publishing to Chocolatey

1. **Get API key** from https://community.chocolatey.org/account

2. **Set API key**
   ```powershell
   choco apikey --key YOUR_API_KEY --source https://push.chocolatey.org/
   ```

3. **Push package**
   ```powershell
   choco push noteerr.1.1.0.nupkg --source https://push.chocolatey.org/
   ```

4. **Wait for moderation** (first package requires manual approval)

### User Installation

```powershell
choco install noteerr
```

### Testing Locally

```powershell
choco install noteerr.1.1.0.nupkg
```

---

## 🍺 Homebrew (macOS/Linux)

### Setup

Homebrew formula is in `homebrew/noteerr.rb`

### Publishing to Homebrew

#### Option 1: Your Own Tap (Recommended for new packages)

1. **Create a tap repository**
   ```bash
   # On GitHub, create a repo named: homebrew-tap
   ```

2. **Add formula**
   ```bash
   git clone https://github.com/yourusername/homebrew-tap.git
   cd homebrew-tap
   mkdir Formula
   cp ../noteerr/homebrew/noteerr.rb Formula/
   git add Formula/noteerr.rb
   git commit -m "Add noteerr formula"
   git push
   ```

3. **Users install with**
   ```bash
   brew tap yourusername/tap
   brew install noteerr
   ```

#### Option 2: Submit to Homebrew Core

1. **Update formula**
   - Calculate SHA256: `shasum -a 256 noteerr-1.1.0.tar.gz`
   - Update hash in `noteerr.rb`

2. **Test formula**
   ```bash
   brew install --build-from-source homebrew/noteerr.rb
   brew test noteerr
   ```

3. **Fork homebrew-core**
   ```bash
   brew tap homebrew/core
   cd $(brew --repo homebrew/core)
   git checkout -b noteerr
   ```

4. **Add formula and submit PR**
   ```bash
   cp /path/to/noteerr.rb Formula/
   brew audit --strict --online noteerr
   git add Formula/noteerr.rb
   git commit -m "noteerr 1.1.0 (new formula)"
   gh pr create
   ```

### User Installation

```bash
brew install noteerr
```

---

## 🐍 PyPI (Python Package Index)

### Building for PyPI

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Check package
twine check dist/*
```

### Publishing to PyPI

1. **Create account** at https://pypi.org

2. **Create API token**
   - Go to Account settings → API tokens
   - Create token with "Upload packages" scope

3. **Configure credentials**
   ```bash
   # Create ~/.pypirc
   [pypi]
   username = __token__
   password = pypi-YOUR_TOKEN_HERE
   ```

4. **Upload to PyPI**
   ```bash
   twine upload dist/*
   ```

### User Installation

```bash
pip install noteerr
```

### Publishing to Test PyPI (for testing)

```bash
twine upload --repository testpypi dist/*
```

---

## 🤖 Automated Releases with GitHub Actions

The `.github/workflows/release.yml` workflow automatically:

1. Builds distribution when you push a tag
2. Creates GitHub release
3. Publishes to PyPI (requires `PYPI_API_TOKEN` secret)

### To Create a Release

```bash
# Tag the release
git tag v1.1.0
git push origin v1.1.0

# GitHub Actions will:
# 1. Build the package
# 2. Create GitHub release
# 3. Upload to PyPI
```

### Required GitHub Secrets

Add in repository Settings → Secrets:

- `PYPI_API_TOKEN` - Your PyPI API token

---

## 📋 Pre-Release Checklist

Before publishing to package managers:

- [ ] Update version in all files:
  - `setup.py`
  - `pyproject.toml`
  - `src/noteerr/__init__.py`
  - `winget/*.yaml`
  - `chocolatey/noteerr.nuspec`
  - `homebrew/noteerr.rb`

- [ ] Update CHANGELOG.md

- [ ] Test installation locally:
  ```bash
  pip install -e .
  noteerr --version
  ```

- [ ] Build and test distribution:
  ```bash
  python -m build
  pip install dist/noteerr-1.1.0-py3-none-any.whl
  ```

- [ ] Run tests:
  ```bash
  python test_noteerr.py
  ```

- [ ] Update documentation

- [ ] Commit all changes

- [ ] Create and push tag:
  ```bash
  git tag -a v1.1.0 -m "Release version 1.1.0"
  git push origin v1.1.0
  ```

---

## 🎯 Installation Instructions for Users

Update your README.md with:

### Windows

```powershell
# Winget (Windows 10/11)
winget install YourPublisher.Noteerr

# Chocolatey
choco install noteerr

# pip
pip install noteerr
```

### macOS

```bash
# Homebrew
brew install noteerr

# pip
pip install noteerr
```

### Linux

```bash
# Homebrew
brew install noteerr

# pip
pip install noteerr
```

---

## 📊 Package Manager Comparison

| Manager | OS | Submit | Approval | Update Time |
|---------|-----|--------|----------|-------------|
| **PyPI** | All | Instant | None | Instant |
| **Chocolatey** | Windows | Easy | Required (first time) | ~1-2 days |
| **Winget** | Windows | PR | Automated | ~1-2 days |
| **Homebrew** | macOS/Linux | PR | Required | ~1-7 days |

**Recommended order:**
1. PyPI (easiest, fastest)
2. Chocolatey (Windows users)
3. Winget (Windows 10/11)
4. Homebrew (power users)

---

## 🔄 Updating Packages

When releasing a new version:

1. **Update version numbers** in all package files
2. **Build new distribution**: `python -m build`
3. **Tag release**: `git tag vX.Y.Z && git push origin vX.Y.Z`
4. **GitHub Actions** will auto-publish to PyPI
5. **Submit updates** to Chocolatey, Winget, Homebrew

---

## 📞 Support

- **PyPI**: Support tickets at https://pypi.org/help/
- **Chocolatey**: https://community.chocolatey.org/
- **Winget**: https://github.com/microsoft/winget-pkgs/issues
- **Homebrew**: https://github.com/Homebrew/homebrew-core/issues

---

## 📚 Additional Resources

- **Winget**: https://docs.microsoft.com/en-us/windows/package-manager/
- **Chocolatey**: https://docs.chocolatey.org/en-us/create/create-packages
- **Homebrew**: https://docs.brew.sh/Formula-Cookbook
- **PyPI**: https://packaging.python.org/
