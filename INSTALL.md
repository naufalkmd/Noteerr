# 📦 Installation Guide

Choose your installation method:

---

## 🚀 Quick Install (Recommended)

### Windows

```
Step 1: Download
  ↓
Step 2: Double-click install.bat
  ↓
Step 3: Restart terminal
  ↓
✓ Done!
```

**Detailed steps:**

1. Download or clone this repository
2. Find and **double-click** `install.bat`
3. Wait for "Installation Complete!"
4. Close and reopen your terminal
5. Run: `noteerr --version`

### macOS / Linux

```bash
git clone https://github.com/yourusername/noteerr.git
cd noteerr
bash install.sh
# Close and reopen terminal
noteerr --version
```

---

## 📥 Install from PyPI (When Available)

```bash
pip install noteerr
```

That's it! Works everywhere.

---

## 🔧 Manual Installation

### Step 1: Install with pip

```bash
pip install --user -e .
```

### Step 2: Fix PATH (if needed)

If you get "command not found" or "not recognized":

```bash
# Automatic fixer
noteerr install --check-path

# Or for Python module invocation
python -m noteerr install --check-path
```

---

## ❓ Troubleshooting

### "Python is not recognized"

**Windows:**
- Install Python from python.org
- ✅ Check "Add Python to PATH" during install
- Restart terminal

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo dnf install python3 python3-pip  # Fedora
```

### "noteerr is not recognized" (after install)

This means PATH wasn't updated or you need a new terminal session.

**Fix:**
```bash
# Close terminal completely
# Open a NEW terminal window
noteerr --version
```

Or use the built-in fixer:
```bash
python -m noteerr install --check-path
```

### "pip is not recognized"

```bash
python -m ensurepip --upgrade
```

### Permission denied

Use `--user` flag:
```bash
pip install --user -e .
```

---

## ✅ Verify Installation

After installing, run these commands:

```bash
# Check version
noteerr --version
# Expected: noteerr, version 1.1.0

# Show help
noteerr --help
# Expected: Shows command list

# Test functionality
noteerr save "test" --command "test" --error "test"
noteerr list
# Expected: Shows saved test error
```

If all commands work → **Installation successful!** 🎉

---

## 🎓 Next Steps

1. **Quick Start**: Read `README.md`
2. **Examples**: See `EXAMPLES.md`  
3. **New Features**: Check `NEW_FEATURES.md`
4. **Shell Integration**: Run `noteerr install --shell powershell`

---

## 📊 Installation Comparison

| Method | Difficulty | Time | 
|--------|-----------|------|
| **Double-click install.bat** | ⭐ Easy | 30 sec |
| **bash install.sh** | ⭐ Easy | 30 sec |
| **pip install** | ⭐⭐ Medium | 1 min |
| **Manual** | ⭐⭐⭐ Advanced | 2-5 min |

**Recommended**: Use the installer scripts! They handle everything automatically.

---

## 📞 Need Help?

- **Installation issues**: See troubleshooting section above
- **Windows setup**: Read `WINDOWS_SETUP.md`
- **General questions**: Read `README.md`
- **Bug reports**: Open a GitHub issue

---

**Installation should take less than 1 minute!** ⚡

If it's taking longer, you may be missing Python or pip. See troubleshooting above.
