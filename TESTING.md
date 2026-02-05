# Testing Guide for Noteerr

This guide covers all testing methods for Noteerr, including automated tests and manual testing procedures.

## 🚀 Quick Test

Run the automated test script:

```powershell
python test_noteerr.py
```

This will verify:
- ✅ Noteerr is installed
- ✅ Basic commands work
- ✅ Save and retrieve functionality
- ✅ Data directory creation

## 📋 Manual Testing - Core Features (v1.0.0)

### 1. Save Error

```powershell
# Test basic save
noteerr save "Test error description" --command "test-cmd" --error "test error"

# Test save with tags
noteerr save "Another test" --tags debug,testing

# Expected: Success message with error ID
```

### 2. List Errors

```powershell
# List recent errors
noteerr list

# List all errors
noteerr list --all

# List with limit
noteerr list --limit 5

# Filter by tag
noteerr list --tag testing

# Expected: Table showing errors with ID, Command, Error snippet, Tags, Project
```

### 3. Show Error Details

```powershell
# Show error by ID
noteerr show 1

# Expected: Panel with full error details
```

### 4. Search Errors

```powershell
# Search by keyword
noteerr search "test"

# Expected: List of matching errors
```

### 5. Annotate Errors

```powershell
# Add note to error
noteerr annotate 1 "This is a test note"

# Add note with tags
noteerr annotate 1 "Updated note" --tags fixed,resolved

# Expected: Success message
```

### 6. Statistics

```powershell
# View all stats
noteerr stats

# Stats for specific tag
noteerr stats --tag testing

# Expected: Statistics panel showing counts and top commands
```

### 7. Delete & Clear

```powershell
# Delete specific error
noteerr delete 1

# Clear all (with confirmation)
noteerr clear

# Expected: Confirmation prompts and success messages
```

## 🆕 Manual Testing - New Features (v1.1.0)

### 1. Copy to Clipboard 📋

```powershell
# Test text format (default)
noteerr copy 1
# Then paste (Ctrl+V) to verify

# Test markdown format
noteerr copy 1 --format markdown
# Paste to verify markdown formatting

# Test JSON format
noteerr copy 1 --format json
# Paste to verify valid JSON structure

# Expected: 
# - Success message: "✓ Copied error #1 to clipboard (text/markdown/json format)"
# - Content in clipboard ready to paste
```

**Verification Steps:**
1. Copy error with each format
2. Paste into notepad/VS Code
3. Verify content matches expected format
4. Check multiline errors are preserved

### 2. Smart Duplicate Detection 🔒

```powershell
# Create initial error
noteerr save "npm install failed" --command "npm install" --error "network timeout"

# Try to save similar error (should detect duplicate)
noteerr save "npm install failed" --command "npm install" --error "network timeout"

# Expected: 
# - Warning: "⚠ Found 1 similar error(s)"
# - Shows similar errors in table
# - Prompts: "Do you still want to save this error? [y/N]:"
# - Type 'N' to cancel or 'y' to save anyway

# Test force flag (bypass detection)
noteerr save "npm install failed" --command "npm install" --error "network timeout" --force

# Expected: Saves without prompt
```

**Verification Steps:**
1. Save an error
2. Try saving same/similar error
3. Verify prompt appears with similar errors
4. Test both 'y' and 'n' responses
5. Test --force flag bypasses detection

### 3. Project Organization 📁

```powershell
# Save with project (first time)
noteerr save "Frontend bug" --project "MyWebApp"

# Save with same project (should suggest existing)
noteerr save "Another frontend issue"
# Expected: Interactive prompt with "MyWebApp" suggestion

# Save with different project
noteerr save "Backend issue" --project "API"

# List all projects
noteerr projects
# Expected: Table showing "MyWebApp" and "API" with error counts

# Filter list by project
noteerr list --project MyWebApp
# Expected: Only errors from MyWebApp

# Show error with project
noteerr show 1
# Expected: Panel includes "Project: MyWebApp"
```

**Verification Steps:**
1. Create errors with different projects
2. Verify `noteerr projects` shows all projects
3. Verify project counts are accurate
4. Test filtering with `--project` flag
5. Check project appears in list table
6. Verify show command displays project

## 🧪 Complete Test Scenario

Run this complete workflow to test all features:

```powershell
# 1. Clean slate
noteerr clear

# 2. Create test errors with projects
noteerr save "Database connection failed" --command "npm start" --error "ECONNREFUSED" --project "Backend" --tags database,critical

noteerr save "Build error" --command "npm run build" --error "Module not found" --project "Frontend" --tags build

noteerr save "API timeout" --command "curl api.example.com" --error "timeout after 30s" --project "Backend" --tags api,network

# 3. Test list and filtering
noteerr list                    # Should show all 3 with Project column
noteerr list --project Backend  # Should show 2 errors
noteerr list --tag database     # Should show 1 error

# 4. Test projects command
noteerr projects                # Should show Backend (2) and Frontend (1)

# 5. Test copy
noteerr copy 1                  # Copy first error
# Paste to verify

noteerr copy 1 --format markdown
# Paste to verify markdown format

# 6. Test duplicate detection
noteerr save "Database connection failed" --command "npm start" --error "ECONNREFUSED"
# Should detect duplicate and prompt
# Type 'N' to cancel

# 7. Test force save
noteerr save "Database connection failed" --command "npm start" --error "ECONNREFUSED" --force
# Should save without prompt

# 8. Test search
noteerr search "database"       # Should find database-related errors

# 9. Test annotate
noteerr annotate 1 "Fixed by restarting Redis" --tags resolved

# 10. Test show
noteerr show 1                  # Should show full details with project

# 11. Test stats
noteerr stats                   # Should show statistics
noteerr stats --tag database    # Should show database stats

# 12. Test delete
noteerr delete 4                # Delete the duplicate

# Expected Result: All commands work without errors
```

## ✅ Testing Checklist

### Installation
- [ ] `noteerr --version` shows correct version (1.1.0)
- [ ] `noteerr --help` displays help text
- [ ] Data directory created at `~/.noteerr/`
- [ ] Data file created at `~/.noteerr/errors.json`

### Core Commands (v1.0.0)
- [ ] Save error with basic info
- [ ] Save with tags
- [ ] List all errors
- [ ] List with filters (--limit, --tag, --all)
- [ ] Show error details
- [ ] Search errors
- [ ] Annotate with notes
- [ ] Annotate with tags
- [ ] View statistics
- [ ] Delete error
- [ ] Clear all (with confirmation)

### New Features (v1.1.0)
- [ ] Copy error (text format)
- [ ] Copy error (markdown format)
- [ ] Copy error (JSON format)
- [ ] Clipboard content verified (paste test)
- [ ] Duplicate detection triggers prompt
- [ ] Can save duplicate with 'y' confirmation
- [ ] Can cancel duplicate with 'n'
- [ ] Force flag bypasses duplicate detection
- [ ] Save with --project flag
- [ ] Interactive project prompt suggests existing projects
- [ ] Projects command lists all projects
- [ ] Projects show correct error counts
- [ ] List --project filter works
- [ ] Project appears in list table
- [ ] Project appears in show details

### Edge Cases
- [ ] Save without any errors logged (fresh install)
- [ ] Show non-existent error ID (should error gracefully)
- [ ] Delete non-existent error ID (should error gracefully)
- [ ] Copy non-existent error ID (should error gracefully)
- [ ] Search with no matches (should show "No errors found")
- [ ] Stats with no errors (should show appropriate message)
- [ ] List with empty database (should show "No errors logged yet")
- [ ] Very long error messages (test truncation/display)
- [ ] Special characters in notes/errors
- [ ] Project names with spaces
- [ ] Tag names with special characters

### Cross-Platform (if applicable)
- [ ] Windows - PowerShell clipboard (Set-Clipboard)
- [ ] macOS - pbcopy clipboard
- [ ] Linux - xclip/xsel clipboard

## 🐛 Debugging Failed Tests

If tests fail, check:

1. **Installation Issues**
   ```powershell
   pip show noteerr  # Verify installation
   where noteerr     # Check PATH
   ```

2. **Python Environment**
   ```powershell
   python --version  # Should be 3.8+
   pip list | Select-String "noteerr"
   ```

3. **Data Directory Permissions**
   ```powershell
   Test-Path ~\.noteerr
   Get-Content ~\.noteerr\errors.json
   ```

4. **Clipboard Issues (Windows)**
   ```powershell
   # Test clipboard manually
   "test" | Set-Clipboard
   Get-Clipboard
   ```

5. **View Logs/Errors**
   ```powershell
   noteerr --help    # Should work without errors
   noteerr list 2>&1 # Capture stderr
   ```

## 📊 Expected Test Results

### Automated Test (test_noteerr.py)
```
============================================================
🚀 Noteerr Installation Test Script
============================================================
🔍 Testing Noteerr installation...
✅ Noteerr is installed correctly!
   Version: noteerr, version 1.1.0

🧪 Testing basic commands...

Testing: List command
  ✅ List command works!
Testing: Stats command
  ✅ Stats command works!
Testing: Help command
  ✅ Help command works!

📊 Results: 3 passed, 0 failed
...
```

### Manual Tests
Each command should:
- Execute without Python errors
- Display formatted output (Rich tables/panels)
- Save data persistently
- Show appropriate success/error messages

## 🎯 Performance Testing

Optional performance checks:

```powershell
# Test with many errors (100+)
for ($i=1; $i -le 100; $i++) {
    noteerr save "Test error $i" --command "test-$i" --project "TestProject" --force
}

# Test list performance
Measure-Command { noteerr list --all }

# Test search performance
Measure-Command { noteerr search "test" }

# Expected: Commands should complete in < 1 second
```

## 📝 Reporting Issues

If you find bugs during testing:

1. Note the exact command that failed
2. Copy the error message
3. Check your Python version and OS
4. Check [test_noteerr.py](test_noteerr.py) output
5. Open an issue on GitHub with details

## ✨ Success Criteria

Testing is successful when:
- ✅ All automated tests pass
- ✅ All manual test commands execute without errors
- ✅ Data persists between commands
- ✅ Clipboard copy/paste works
- ✅ Duplicate detection prompts correctly
- ✅ Project organization displays properly
- ✅ No Python tracebacks or crashes

---

**Ready to test?** Start with `python test_noteerr.py` then run through the manual test scenarios above!
