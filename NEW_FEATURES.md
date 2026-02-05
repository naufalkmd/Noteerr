# 🆕 New Features Guide

Noteerr v1.1.0 introduces powerful new capabilities for better error management!

## ✨ What's New

### 1. 📋 Copy Errors to Clipboard

Quickly copy error details to share with your team or paste into documentation.

**Usage:**
```powershell
# Copy in plain text format
noteerr copy 1

# Copy as Markdown
noteerr copy 1 --format markdown

# Copy as JSON
noteerr copy 1 --format json
```

**Example output (text):**
```
Error #2
Command: npm start
Exit Code: 1
Directory: C:\Users\...\project
Timestamp: 2026-02-05 18:32:02
Project: MyApp
Tags: npm, javascript
Notes: Need to run npm install first

Error Output:
Error: Cannot find module 'express'
```

**Example output (markdown):**
```markdown
# Error #2

**Command:** `npm start`
**Exit Code:** 1
**Directory:** `C:\Users\...\project`
**Timestamp:** 2026-02-05 18:32:02
**Project:** MyApp
**Tags:** npm, javascript

**Notes:** Need to run npm install first

## Error Output

```
Error: Cannot find module 'express'
```
```

---

### 2. 🚫 Smart Duplicate Detection

Noteerr now automatically detects duplicate errors and asks before saving!

**How it works:**
- Compares command name and error message
- Uses fuzzy matching for similar errors
- Shows you existing similar errors before saving
- Option to skip or force save with `--force`

**Example:**
```powershell
$ noteerr save "npm error" --command "npm start" --error "missing module"

⚠ Found 1 similar error(s):
  #5: npm start
       Error: Cannot find module
       Note: Need to run npm install first

Save anyway? [y/N]:
```

**Force save (skip duplicate check):**
```powershell
noteerr save "forcing save" --command "test" --error "err" --force
```

**Benefits:**
- Keeps your error log clean
- Prevents clutter from repeated errors
- Reminds you of existing solutions
- Efficient storage usage

---

### 3. 📁 Project-Based Organization

Tag errors by project for better organization across multiple codebases!

**Save with project name:**
```powershell
# Specify project name
noteerr save "bug fix" --project "MyApp" --tags bug

# Interactive project selection
noteerr save "another bug"
# Will prompt: Project name (press Enter to skip):
# Shows list of existing projects for quick selection
```

**Interactive project prompt:**
```
Available projects:
  1. Noteerr
  2. MyApp
  3. WebsiteProject
  (or enter a new project name)

Project name (press Enter to skip):
```

**Filter by project:**
```powershell
# List errors for specific project
noteerr list --project MyApp

# Interactive project selection
noteerr list --project
# Will show project list to choose from
```

**View all projects:**
```powershell
noteerr projects
```

**Example output:**
```
Projects:

┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Project        ┃ Errors ┃ Latest Error ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Noteerr        │      5 │ 2026-02-05   │
│ MyApp          │     12 │ 2026-02-04   │
│ WebsiteProject │      3 │ 2026-02-03   │
└────────────────┴────────┴──────────────┘

💡 Tip: Use 'noteerr list --project <name>' to see errors for a specific project
```

---

## 🎯 Updated Commands

### Save Command
```powershell
noteerr save [NOTE] [OPTIONS]

Options:
  -c, --command TEXT      Command that failed
  -e, --error TEXT        Error message
  -t, --tags TEXT         Comma-separated tags
  -p, --project TEXT      Project name
  -f, --force             Force save (skip duplicate check)
```

### List Command
```powershell
noteerr list [OPTIONS]

Options:
  -n, --limit INTEGER     Number of entries to show
  -t, --tag TEXT          Filter by tag
  -p, --project TEXT      Filter by project
  -a, --all               Show all entries
```

### Copy Command (NEW)
```powershell
noteerr copy ENTRY_ID [OPTIONS]

Options:
  -f, --format [text|markdown|json]  Output format
```

### Projects Command (NEW)
```powershell
noteerr projects

Lists all projects with error counts and latest error date.
```

---

## 📊 Enhanced Display

The `list` command now includes a **Project** column:

```
                    Recent Errors - Project: MyApp
┏━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━┓
┃  ┃ Command   ┃ Error           ┃ Project ┃ Date       ┃ Tags ┃
┡━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━┩
│ 5│ npm start │ missing module  │ MyApp   │ 2026-02-05 │ npm  │
└──┴───────────┴─────────────────┴─────────┴────────────┴──────┘
```

---

## 💡 Usage Examples

### Example 1: Working on Multiple Projects

```powershell
# Project A - Web API
cd C:\Projects\WebAPI
npm start  # Error occurs
noteerr save "missing env variables" --project "WebAPI" --tags npm,env

# Project B - Mobile App
cd C:\Projects\MobileApp
flutter run  # Error occurs
noteerr save "SDK version mismatch" --project "MobileApp" --tags flutter

# View all projects
noteerr projects

# View errors for specific project
noteerr list --project WebAPI
```

### Example 2: Sharing Errors with Team

```powershell
# Copy error as markdown for Slack/Teams
noteerr copy 5 --format markdown
# Paste into your team chat

# Copy as JSON for bug tracking
noteerr copy 5 --format json
# Paste into Jira or GitHub issue
```

### Example 3: Avoiding Duplicates

```powershell
# First time seeing error
docker build .  # Error
noteerr save "Docker build failed" --tags docker
✓ Saved error #10

# Same error happens again later
docker build .  # Same error
noteerr save "Docker build failed again" --tags docker

⚠ Found 1 similar error(s):
  #10: docker build
       Error: failed to solve...
       Note: Docker build failed

Save anyway? [y/N]: N
Skipped - error not saved

# If you need to save anyway:
noteerr save "new context" --tags docker --force
```

---

## 🔄 Migration Notes

**Existing errors are compatible!**

- Old errors without `project` field will show `-` in the Project column
- You can add project info to old errors using `annotate` (future feature)
- No data loss or breaking changes

---

## 🎨 Tips & Tricks

### Quick Project Workflow

```powershell
# Set project in shell variable for session
$PROJECT = "MyApp"
noteerr save "error note" --project $PROJECT

# Or use aliases
function ne-myapp { noteerr save $args --project "MyApp" }
ne-myapp "quick save"
```

### Copy Formats

**Text format:** Best for terminal/email
**Markdown format:** Best for documentation/Slack/GitHub
**JSON format:** Best for APIs/automation/bug trackers

### Project Naming

Use consistent names:
- ✅ `MyWebApp`, `mobile-app`, `api-server`
- ❌ `My Web App` (spaces make filtering harder)
- ❌ Changing case (`MyApp` vs `myapp` are different!)

---

## 📝 Future Enhancements

Coming soon:
- Bulk update projects for existing errors
- Project-based statistics
- Export errors by project
- Project aliases/shortcuts
- Auto-detect project from git repo

---

## 🆘 Need Help?

```powershell
# View command help
noteerr save --help
noteerr copy --help
noteerr list --help

# Check version
noteerr --version
```

---

**Happy error tracking! 🎉**

These new features make Noteerr even more powerful for managing errors across multiple projects and teams!
