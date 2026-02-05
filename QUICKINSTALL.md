# Quick Installation Guide

**Get Noteerr up and running in under 1 minute!** ⏱️

---

## ⚡ Fastest Method (Like Installing Git!)

### Windows → Just Double-Click! 🖱️

```
1. Download/Clone Noteerr
2. Find "install.bat" 
3. Double-click it
4. Wait for "Installation Complete!"
5. Close terminal
6. Open NEW terminal
7. Type: noteerr --version
```

**That's it!** No commands to remember, no PATH to configure manually.

### macOS / Linux → One Command 🚀

```bash
git clone https://github.com/yourusername/noteerr.git
cd noteerr
bash install.sh
```

Close and reopen terminal, then: `noteerr --version`

---

## 📋 Detailed Windows Instructions

### Method 1: Double-Click Installer (Recommended)

1. **Get Noteerr**
   - Download ZIP from GitHub and extract
   - Or: `git clone https://github.com/yourusername/noteerr.git`

2. **Navigate to folder**
   - Open the `noteerr` folder in File Explorer
   - Find `install.bat` (it has a gear icon ⚙️)

3. **Run installer**
   - Double-click `install.bat`
   - A black window appears with green text
   - Wait for "Installation Complete!"
   - Press any key to close

4. **Verify**
   - Open PowerShell or Command Prompt (NEW window!)
   - Type: `noteerr --version`
   - Should show: `noteerr, version 1.1.0`

**✅ Done! You're ready to use Noteerr.**

### Method 2: PowerShell Installer

For users comfortable with PowerShell:

```powershell
cd noteerr
.\install.ps1
```

Same result, slightly more verbose output.

---

## 📋 Detailed macOS / Linux Instructions

### Quick Install

```bash
# Navigate to noteerr directory
cd noteerr

# Install
pip install --user -e .

# Check if it works
noteerr --version
```

### If Command Not Found

```bash
# Make sure ~/.local/bin is in your PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or for zsh:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## PyPI Install (When Available)

```bash
# Simplest method once published to PyPI
pip install --user noteerr

# Verify
noteerr --version
```

## Install from GitHub (No Clone)

```bash
# Install directly from GitHub
pip install --user git+https://github.com/yourusername/noteerr.git

# Verify
noteerr --version
```

## Troubleshooting

### "pip is not recognized"

**Windows:**
```powershell
# Install pip
python -m ensurepip --upgrade

# Or reinstall Python with pip included
# Download from: https://www.python.org/downloads/
```

**macOS/Linux:**
```bash
python -m ensurepip --upgrade
```

### "Python is not recognized" (Windows)

1. Download Python from https://www.python.org/downloads/
2. During installation, **check "Add Python to PATH"**
3. Restart your terminal

### Permission Errors

```bash
# Use --user flag to install for current user only
pip install --user -e .
```

### Still Not Working?

Run the built-in diagnostic:
```bash
python -m noteerr install --check-path
```

This will:
- Check if noteerr is installed
- Find the installation location
- Offer to fix PATH automatically
- Show manual fix instructions if needed

## Verification Checklist

After installation, verify everything works:

```bash
# 1. Check version
noteerr --version
# Expected: noteerr, version 1.1.0

# 2. Check help
noteerr --help
# Expected: Shows command list

# 3. Test basic functionality
noteerr list
# Expected: "No errors logged yet" or shows existing errors

# 4. Test save
noteerr save "test installation" --command "test" --error "test error"
# Expected: "✓ Saved error #1"

# 5. Test list
noteerr list
# Expected: Shows the test error

# 6. Test copy
noteerr copy error latest
# Expected: "✓ Copied error #1..."
```

## Next Steps

Once installed:

1. **Read the quick start**: `README.md`
2. **Try examples**: `EXAMPLES.md`
3. **Set up shell integration**: `noteerr install --shell powershell`
4. **Learn new features**: `NEW_FEATURES.md`

## Need Help?

- **Documentation**: Check `README.md` and `EXAMPLES.md`
- **Issues**: Open an issue on GitHub
- **Windows Setup**: See `WINDOWS_SETUP.md`
- **Testing**: Run `python test_noteerr.py`

---

**Installation time: < 2 minutes** ⏱️

**Difficulty: Easy** ✅

**Support: Windows, macOS, Linux** 🌍
