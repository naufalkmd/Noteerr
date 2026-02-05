# 🎯 Quick Start Guide

Get Noteerr up and running in 2 minutes!

## Step 1: Install (Choose One)

### Option A: Install from Source (Recommended for Testing)

```powershell
# On Windows PowerShell
cd C:\Users\naufalkmd\Documents\Noteerr
pip install -e .

# Verify installation
noteerr --version
```

```bash
# On macOS/Linux
cd ~/Documents/Noteerr
pip install -e .

# Verify installation
noteerr --version
```

### Option B: Install from PyPI (Once Published)

```bash
pip install noteerr
```

### Option C: Install from GitHub

```bash
pip install git+https://github.com/yourusername/noteerr.git
```

## Step 2: Test Installation

```bash
# Run the test script
python test_noteerr.py

# Or manually test
noteerr --help
noteerr list
```

## Step 3: Save Your First Error

### Method 1: Manual Save

```bash
# Run a command that fails
npm start

# Save the error
noteerr save "need to run npm install first" --tags npm
```

### Method 2: Automatic Capture (After Shell Integration)

```bash
# Run a failing command
npm start

# Just type 'ne' (shorthand alias)
ne "need to run npm install first"
```

## Step 4: Set Up Shell Integration (Optional but Recommended)

### For PowerShell (Windows)

1. Open PowerShell profile:
   ```powershell
   notepad $PROFILE
   ```

2. Add this line:
   ```powershell
   . C:\Users\naufalkmd\Documents\Noteerr\scripts\powershell-integration.ps1
   ```

3. Reload your profile:
   ```powershell
   . $PROFILE
   ```

### For Bash (macOS/Linux)

1. Edit your `.bashrc`:
   ```bash
   nano ~/.bashrc
   ```

2. Add this line:
   ```bash
   source ~/Documents/Noteerr/scripts/bash-integration.sh
   ```

3. Reload:
   ```bash
   source ~/.bashrc
   ```

### For Zsh (macOS/Linux)

1. Edit your `.zshrc`:
   ```bash
   nano ~/.zshrc
   ```

2. Add this line:
   ```bash
   source ~/Documents/Noteerr/scripts/zsh-integration.sh
   ```

3. Reload:
   ```bash
   source ~/.zshrc
   ```

## Step 5: Use Noteerr Daily!

### Common Commands

```bash
# Save an error
noteerr save "description of fix" --tags tag1,tag2

# List recent errors
noteerr list

# Search errors
noteerr search "keyword"

# Show error details
noteerr show 1

# Add notes to error
noteerr annotate 1 "additional notes"

# View statistics
noteerr stats

# With shell integration, use shortcuts:
ne "quick save"     # Same as: noteerr save
nel                 # Same as: noteerr list
nes "search term"   # Same as: noteerr search
```

## Troubleshooting

### "noteerr: command not found"

**Solution:**
```bash
# Ensure Python scripts directory is in PATH
# Windows: Add %USERPROFILE%\AppData\Roaming\Python\Python311\Scripts to PATH
# macOS/Linux: Add ~/.local/bin to PATH

# Or reinstall with:
pip install --user -e .
```

### "Module not found" errors

**Solution:**
```bash
# Install dependencies manually
pip install click colorama rich

# Or reinstall
pip install -e .
```

### Shell integration not working

**Solution:**
1. Verify the source command is correct
2. Check file paths match your installation
3. Reload your shell profile
4. Try opening a new terminal window

## What's Next?

✅ You're all set! Start using Noteerr to track your errors.

📖 **Read More:**
- [EXAMPLES.md](EXAMPLES.md) - Real-world usage examples
- [README.md](README.md) - Full documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - How to deploy/distribute

💡 **Pro Tips:**
1. Save errors immediately when they happen
2. Use descriptive notes about the fix
3. Tag consistently for easy searching
4. Review your errors weekly to find patterns

🎉 **Happy Error Tracking!**
