# Package Manager Publishing Checklist

Complete checklist for making Noteerr available on all major package managers.

---

## ✅ Pre-Publishing Checklist

### Version Numbers

Update version to `1.1.0` in ALL these files:

- [ ] `src/noteerr/__init__.py` - `__version__ = "1.1.0"`
- [ ] `setup.py` - `version="1.1.0"`
- [ ] `pyproject.toml` - `version = "1.1.0"`
- [ ] `winget/YourPublisher.Noteerr.yaml` - `PackageVersion: 1.1.0`
- [ ] `winget/YourPublisher.Noteerr.installer.yaml` - `PackageVersion: 1.1.0`
- [ ] `winget/YourPublisher.Noteerr.locale.en-US.yaml` - `PackageVersion: 1.1.0`
- [ ] `chocolatey/noteerr.nuspec` - `<version>1.1.0</version>`
- [ ] `homebrew/noteerr.rb` - `version "1.1.0"`

### Personal Information

Replace placeholder text in ALL package files:

- [ ] Replace `yourusername` with your GitHub username
- [ ] Replace `Your Name` with your actual name
- [ ] Replace `YourPublisher` with your winget publisher name
- [ ] Update email addresses (if any)

Files to update:
- All winget YAML files
- chocolatey/noteerr.nuspec
- homebrew/noteerr.rb
- README.md
- DISTRIBUTION.md
- GITHUB_PUBLISHING.md

### Documentation

- [ ] Update CHANGELOG.md with v1.1.0 changes
- [ ] Update README.md with final installation instructions
- [ ] Verify all links work
- [ ] Check for typos

---

## 📦 Step-by-Step Publishing Guide

### 1️⃣ GitHub (Do This First!)

**Why first?** All other package managers need the GitHub release URL and files.

#### Setup Repository

```bash
cd C:\Users\naufalkmd\Documents\Noteerr
git init
git add .
git commit -m "Initial commit: Noteerr v1.1.0"
git branch -M main
git remote add origin https://github.com/yourusername/noteerr.git
git push -u origin main
```

#### Build Distribution

```bash
# Install build tools
pip install build twine

# Build packages
python -m build

# Verify
twine check dist/*
```

This creates:
- `dist/noteerr-1.1.0-py3-none-any.whl`
- `dist/noteerr-1.1.0.tar.gz`

#### Create Release

```bash
# Create annotated tag
git tag -a v1.1.0 -m "Release v1.1.0: Copy, Dedup, Projects"

# Push tag (triggers GitHub Actions)
git push origin v1.1.0
```

GitHub Actions will:
- ✅ Build package
- ✅ Create GitHub Release
- ✅ Upload distribution files
- ✅ Publish to PyPI (if configured)

#### Manual Release (Alternative)

1. Go to https://github.com/yourusername/noteerr/releases
2. Click "Create a new release"
3. Tag: `v1.1.0`
4. Title: `Noteerr v1.1.0 - Copy, Dedup, Projects`
5. Description: Use content from `RELEASE_NOTES_TEMPLATE.md`
6. Upload files from `dist/` folder
7. Click "Publish release"

**Checklist:**
- [ ] Repository created on GitHub
- [ ] Code pushed to main branch
- [ ] Distribution built (`dist/` folder exists)
- [ ] Tag v1.1.0 created and pushed
- [ ] GitHub Release published
- [ ] Distribution files attached to release

---

### 2️⃣ PyPI (Python Package Index)

**Time to publish:** Instant  
**Approval:** None required  
**Audience:** All Python users

#### Setup PyPI Account

1. Create account at https://pypi.org/account/register/
2. Verify email
3. Go to Account Settings → API tokens
4. Create token with "Upload packages" scope
5. Save token securely

#### Configure Credentials

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

#### Publish to PyPI

```bash
# Upload distribution
twine upload dist/*

# Verify at:
# https://pypi.org/project/noteerr/
```

#### Add PyPI Secret to GitHub (for auto-publish)

1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: Your PyPI token
5. Save

Now future releases will auto-publish to PyPI!

**Checklist:**
- [ ] PyPI account created
- [ ] API token generated
- [ ] Package uploaded to PyPI
- [ ] Verify package page: https://pypi.org/project/noteerr/
- [ ] Test installation: `pip install noteerr`
- [ ] GitHub secret added for future releases

---

### 3️⃣ Chocolatey (Windows)

**Time to publish:** 1-2 days (first package needs approval)  
**Approval:** Required for first package  
**Audience:** Windows users

#### Setup Chocolatey Account

1. Create account at https://community.chocolatey.org/account/register
2. Verify email

#### Get API Key

1. Go to https://community.chocolatey.org/account
2. Copy your API key

#### Build Package

```bash
cd chocolatey
choco pack

# Creates: noteerr.1.1.0.nupkg
```

#### Set API Key

```bash
choco apikey --key YOUR_API_KEY --source https://push.chocolatey.org/
```

#### Publish Package

```bash
choco push noteerr.1.1.0.nupkg --source https://push.chocolatey.org/
```

#### Wait for Approval

- First package: Manual review (1-2 days)
- Updates: Usually automated

#### Monitor Status

Check at: https://community.chocolatey.org/packages/noteerr

**Checklist:**
- [ ] Chocolatey account created
- [ ] API key obtained and configured
- [ ] Package built successfully
- [ ] Package uploaded to Chocolatey
- [ ] Monitor moderation status
- [ ] Test after approval: `choco install noteerr`

---

### 4️⃣ Winget (Windows Package Manager)

**Time to publish:** 1-2 days  
**Approval:** Automated validation  
**Audience:** Windows 10/11 users

#### Update Manifests

1. **Calculate SHA256 hash** of your .whl file:
   ```bash
   certutil -hashfile dist\noteerr-1.1.0-py3-none-any.whl SHA256
   ```

2. **Update `winget/YourPublisher.Noteerr.installer.yaml`**:
   - Set correct `InstallerUrl` (your GitHub release URL)
   - Set `InstallerSha256` (hash from step 1)

3. **Update publisher name** in all YAML files:
   - Replace `YourPublisher` with your actual publisher name
   - Use format: `FirstnameLastname.Noteerr` (e.g., `JohnDoe.Noteerr`)

#### Fork winget-pkgs Repository

```bash
git clone https://github.com/microsoft/winget-pkgs.git
cd winget-pkgs
```

#### Create Manifest Directory

```bash
# Use first letter of publisher name
# Example: YourPublisher → y/YourPublisher/Noteerr/1.1.0
mkdir -p manifests/y/YourPublisher/Noteerr/1.1.0
```

#### Copy Manifests

```bash
cp C:\Users\naufalkmd\Documents\Noteerr\winget\*.yaml manifests/y/YourPublisher/Noteerr/1.1.0/
```

#### Submit Pull Request

```bash
git checkout -b noteerr-1.1.0
git add manifests/y/YourPublisher/Noteerr/
git commit -m "New package: YourPublisher.Noteerr version 1.1.0"
git push origin noteerr-1.1.0

# Create PR on GitHub
```

#### Monitor PR

- Automated validation runs
- Fix any issues if validation fails
- Usually merged within 1-2 days

**Checklist:**
- [ ] SHA256 hash calculated and updated
- [ ] Publisher name updated in all YAML files
- [ ] GitHub release URL updated
- [ ] winget-pkgs repository forked
- [ ] Manifest files copied
- [ ] Pull Request submitted
- [ ] Validation passed
- [ ] PR merged
- [ ] Test after merge: `winget install YourPublisher.Noteerr`

---

### 5️⃣ Homebrew (macOS/Linux)

**Time to publish:** 1-7 days (if submitting to core)  
**Approval:** Required for homebrew-core  
**Audience:** macOS and Linux users

#### Option A: Your Own Tap (Recommended for New Packages)

**Faster and easier!**

1. **Create tap repository on GitHub**:
   - Name: `homebrew-tap`
   - Public repository

2. **Initialize tap locally**:
   ```bash
   git clone https://github.com/yourusername/homebrew-tap.git
   cd homebrew-tap
   mkdir Formula
   ```

3. **Calculate SHA256**:
   ```bash
   # Download your GitHub release tarball
   curl -L https://github.com/yourusername/noteerr/archive/v1.1.0.tar.gz -o noteerr.tar.gz
   
   # Calculate hash
   shasum -a 256 noteerr.tar.gz
   ```

4. **Update formula**:
   - Copy `homebrew/noteerr.rb` to `Formula/noteerr.rb`
   - Update `url` with your GitHub release URL
   - Update `sha256` with calculated hash
   - Update `homepage` with your repository URL

5. **Commit and push**:
   ```bash
   git add Formula/noteerr.rb
   git commit -m "Add Noteerr formula"
   git push
   ```

6. **Users install with**:
   ```bash
   brew tap yourusername/tap
   brew install noteerr
   ```

**Checklist:**
- [ ] Tap repository created: `homebrew-tap`
- [ ] SHA256 hash calculated
- [ ] Formula updated with correct URL and hash
- [ ] Formula committed and pushed
- [ ] Test installation: `brew install yourusername/tap/noteerr`

#### Option B: Submit to Homebrew Core

**For more visibility, but takes longer:**

1. **Test formula locally**:
   ```bash
   brew install --build-from-source homebrew/noteerr.rb
   brew test noteerr
   brew audit --strict --online noteerr
   ```

2. **Fork homebrew-core**:
   ```bash
   cd $(brew --repo homebrew/core)
   git checkout -b noteerr
   ```

3. **Add formula**:
   ```bash
   cp /path/to/noteerr.rb Formula/
   git add Formula/noteerr.rb
   git commit -m "noteerr 1.1.0 (new formula)"
   ```

4. **Submit PR** via GitHub CLI:
   ```bash
   gh pr create
   ```

**Checklist:**
- [ ] Formula tested locally
- [ ] Audit passed
- [ ] PR submitted to homebrew-core
- [ ] Wait for review and merge

---

## 🎉 Post-Publishing

### Update README.md

Add installation badges:

```markdown
![PyPI](https://img.shields.io/pypi/v/noteerr)
![Downloads](https://img.shields.io/pypi/dm/noteerr)
![GitHub release](https://img.shields.io/github/v/release/yourusername/noteerr)
```

### Test All Installation Methods

```bash
# Windows
winget install YourPublisher.Noteerr
choco install noteerr
pip install noteerr

# macOS
brew install yourusername/tap/noteerr
pip install noteerr

# Linux
brew install yourusername/tap/noteerr
pip install noteerr
```

### Share Your Release

- [ ] Reddit: r/Python, r/commandline
- [ ] Hacker News: Show HN
- [ ] Twitter/X
- [ ] LinkedIn
- [ ] Dev.to
- [ ] Product Hunt

---

## 📊 Comparison Matrix

| Package Manager | Publish Time | Approval | Command |
|----------------|--------------|----------|---------|
| **PyPI** | Instant | None | `pip install noteerr` |
| **Your Homebrew Tap** | Instant | None | `brew install user/tap/noteerr` |
| **Chocolatey** | 1-2 days | First only | `choco install noteerr` |
| **Winget** | 1-2 days | Automated | `winget install Publisher.Noteerr` |
| **Homebrew Core** | 1-7 days | Required | `brew install noteerr` |

**Recommended Publishing Order:**
1. ✅ GitHub + PyPI (instant, essential)
2. ✅ Your Homebrew Tap (instant, for macOS/Linux)
3. ⏳ Chocolatey (Windows users)
4. ⏳ Winget (built-in Windows PM)
5. ⏳ Homebrew Core (optional, for discoverability)

---

## 🔄 Future Updates

For v1.2.0 and beyond:

1. **Update version** in all files
2. **Update CHANGELOG.md**
3. **Build distribution**: `python -m build`
4. **Push tag**: `git tag v1.2.0 && git push origin v1.2.0`
5. **PyPI**: Auto-published via GitHub Actions
6. **Chocolatey**: `choco pack && choco push`
7. **Winget**: Submit new PR with updated manifests
8. **Homebrew**: Update formula in your tap

---

## 📞 Need Help?

- **GitHub**: https://docs.github.com
- **PyPI**: https://packaging.python.org/
- **Chocolatey**: https://docs.chocolatey.org/
- **Winget**: https://github.com/microsoft/winget-pkgs
- **Homebrew**: https://docs.brew.sh/

---

**Ready to publish? Follow the steps in order and check off each item!** 🚀
