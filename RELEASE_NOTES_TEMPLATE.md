# Noteerr Release Notes Template

Use this template when creating GitHub releases.

---

## v1.1.0 - Copy, Dedup, Projects (Current Release)

**Release Date**: 2026-02-05

### ✨ New Features

#### 🖨️ Copy to Clipboard
- Copy errors in multiple formats: text, markdown, JSON
- Syntax: `noteerr copy <id> [--format text|markdown|json]`
- Copy latest errors: `noteerr copy latest` or `noteerr copy latest error`
- Copy latest terminal command + output (Windows PowerShell)
- Cross-platform clipboard support (Windows, macOS, Linux)

#### 🔍 Smart Duplicate Detection
- Automatically detects duplicate errors
- Similarity threshold: 80% match
- Shows warning when saving duplicates
- Suggests existing error IDs
- Can force save duplicates with `--force` flag

#### 📁 Project Organization  
- Group errors by project context
- Set/view projects with `noteerr project [name]`
- Filter errors by project
- Per-project statistics

### 🛠️ Improvements
- Enhanced `copy` command with flexible syntax
- Automatic PATH configuration on installation
- Built-in PATH checker: `noteerr install --check-path`
- Improved error messages and user feedback
- Better list command compatibility

### 🐛 Bug Fixes
- Fixed list command display issues
- Improved cross-platform compatibility
- Better PowerShell integration

### 📦 Installation
- Double-click installer for Windows (`install.bat`)
- One-command installer for macOS/Linux (`install.sh`)
- Automated PATH setup
- Git-level installation simplicity

---

## v1.0.0 - Initial Release

### Core Features
- ✅ Save command errors with annotations
- ✅ List all saved errors with details
- ✅ Search by command, error text, or notes
- ✅ Tag management system
- ✅ Statistics and insights
- ✅ Shell integration (Bash, Zsh, PowerShell)
- ✅ Annotate existing errors
- ✅ Delete errors
- ✅ Clean old errors
- ✅ Export error database

---

## Future Roadmap

### v1.2.0 (Planned)
- 🔄 Error templates for common issues
- 🌐 Cloud sync (optional)
- 📊 Advanced analytics dashboard
- 🔗 Integration with issue trackers
- 📸 Screenshot support
- 🎨 Custom themes

### v1.3.0 (Ideas)
- 🤖 AI-powered error suggestions
- 👥 Team collaboration features
- 📈 Trend analysis
- 🔔 Error notifications
- 🌍 Multi-language support

---

## How to Use This Template

1. **Copy the relevant section** for your release
2. **Update the release date**
3. **Paste into GitHub Release description**
4. **Add installation instructions**:

```markdown
### 📦 Installation

#### Windows
```powershell
winget install YourPublisher.Noteerr
# or
choco install noteerr
# or
pip install noteerr
```

#### macOS/Linux
```bash
brew install noteerr
# or
pip install noteerr
```

### 📥 Assets

Download the appropriate file:
- `noteerr-1.1.0-py3-none-any.whl` - Universal Python wheel
- `noteerr-1.1.0.tar.gz` - Source distribution

### 🚀 Upgrade from v1.0.0

```bash
pip install --upgrade noteerr
```

### 📚 Documentation

- [Installation Guide](INSTALL.md)
- [Testing Guide](TESTING.md)
- [Distribution Guide](DISTRIBUTION.md)
- [Full README](README.md)

```

---

**Note**: Replace `YourPublisher` with your actual publisher name when submitting to package managers.
