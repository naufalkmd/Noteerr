# 🪟 Windows Setup Guide for Noteerr

Quick guide to get Noteerr working on Windows PowerShell.

## ✅ Installation Complete!

Noteerr is now installed at: `C:\Users\naufalkmd\AppData\Roaming\Python\Python311\Scripts\noteerr.exe`

## 🔧 Make Noteerr Accessible Everywhere

### Option 1: Add to PATH Permanently (Recommended)

Run this command in PowerShell (**as Administrator**):

```powershell
[System.Environment]::SetEnvironmentVariable(
    'PATH',
    [System.Environment]::GetEnvironmentVariable('PATH', 'User') + ';C:\Users\naufalkmd\AppData\Roaming\Python\Python311\Scripts',
    'User'
)
```

Then **restart PowerShell** or run:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","User")
```

### Option 2: Add to Current Session Only

Already done for you! But if you open a new terminal, run:

```powershell
$env:Path += ";C:\Users\naufalkmd\AppData\Roaming\Python\Python311\Scripts"
```

## 🎯 Verify Installation

```powershell
noteerr --version
# Should show: noteerr, version 1.0.0

noteerr list
# Should show your errors
```

## 🚀 Quick Start

### Save an Error
```powershell
# After a command fails:
npm start  # This fails
noteerr save "This is a Python project, not Node.js" --tags npm,mistake
```

### View Errors
```powershell
noteerr list            # List recent errors
noteerr search npm      # Search for npm errors
noteerr show 1          # Show details of error #1
noteerr stats           # View statistics
```

### Add Notes
```powershell
noteerr annotate 1 "Remember: this is a Python CLI tool!"
```

## 🐚 PowerShell Integration (Optional)

To auto-capture errors, add this to your PowerShell profile:

1. **Open your profile:**
   ```powershell
   notepad $PROFILE
   ```

2. **Add this line:**
   ```powershell
   . C:\Users\naufalkmd\Documents\Noteerr\scripts\powershell-integration.ps1
   ```

3. **Reload your profile:**
   ```powershell
   . $PROFILE
   ```

Now you can use shortcuts:
- `ne "note"` → `noteerr save "note"`
- `nel` → `noteerr list`
- `nes keyword` → `noteerr search keyword`

## 📝 Your First Error is Already Saved!

You tried running `npm start` in a Python project. Check it out:

```powershell
noteerr show 1
```

## 🛠️ Troubleshooting

### "noteerr: command not found" after restart

The PATH wasn't set permanently. Use **Option 1** above with Administrator privileges.

### Python Scripts directory different?

If your Python is installed elsewhere, replace the path:
```powershell
# Find your Scripts directory:
python -m site --user-base
# Add "\Scripts" to the output path
```

## 🎉 You're All Set!

Start logging your command errors and never forget solutions again!

**Examples:**
```powershell
# Docker permission error
docker ps  # Fails
noteerr save "need to add user to docker group" --tags docker

# Git push rejected
git push  # Fails
noteerr save "need to pull first" --tags git

# Module not found
python app.py  # Fails
noteerr save "forgot to activate venv" --tags python
```

---

**Need more help?** Check out:
- [README.md](README.md) - Full documentation
- [EXAMPLES.md](EXAMPLES.md) - Real-world examples
- [QUICKSTART.md](QUICKSTART.md) - Quick reference guide
