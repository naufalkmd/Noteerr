# Quick Start Examples

This file contains practical examples to help you get started with Noteerr quickly!

## Scenario 1: NPM/Node.js Development

```bash
# Forgot to install dependencies
$ npm start
Error: Cannot find module 'express'

$ noteerr save "need to run npm install" --tags npm,node
✓ Saved error #1

# Later, when you encounter it again
$ noteerr search npm
# Shows your note: "need to run npm install"
```

## Scenario 2: Git Workflow Issues

```bash
# Push rejected
$ git push
! [rejected] main -> main (non-fast-forward)

$ noteerr save "need to pull first" --tags git
✓ Saved error #2

# Update with more details
$ noteerr annotate 2 "always git pull before push, or use git push --force-with-lease for safer force push" --tags git,workflow
✓ Updated error #2
```

## Scenario 3: Docker Permissions

```bash
# Permission denied
$ docker ps
permission denied while trying to connect to the Docker daemon socket

$ noteerr save "need to add user to docker group" --tags docker,linux
✓ Saved error #3

$ noteerr annotate 3 "run: sudo usermod -aG docker $USER, then logout and login"
✓ Updated error #3
```

## Scenario 4: Python Import Errors

```bash
# Module not found
$ python app.py
ModuleNotFoundError: No module named 'requests'

$ noteerr save "forgot to activate venv" --tags python,venv
✓ Saved error #4
```

## Scenario 5: Database Connection Issues

```bash
# Connection refused
$ npm run dev
Error: connect ECONNREFUSED 127.0.0.1:5432

$ noteerr save "PostgreSQL not running" --tags database,postgres
✓ Saved error #5

$ noteerr annotate 5 "start postgres: sudo systemctl start postgresql"
✓ Updated error #5
```

## Power User Workflow

### 1. Auto-capture errors (with shell integration)

```bash
# Shell integration automatically captures failed commands
$ some-failing-command
# Error occurs...

# Just type 'ne' (alias for noteerr save)
$ ne "here's what fixed it"
✓ Saved error with automatic command and error detection
```

### 2. Build a knowledge base over time

```bash
# Week 1
$ noteerr save "issue A" --tags project-x
$ noteerr save "issue B" --tags project-x

# Week 2
$ noteerr save "issue C" --tags project-y

# Later, when switching back to project-x
$ noteerr list --tag project-x
# See all project-x related errors and solutions!
```

### 3. Share knowledge with team

```bash
# Export your fixes to markdown (future feature)
$ noteerr export --tag docker > docker-fixes.md

# Or just search and share specific errors
$ noteerr show 5
# Copy the solution and share in Slack/Teams
```

## Command Cheat Sheet

| Command | What it does |
|---------|-------------|
| `noteerr save "note"` | Save last error with note |
| `noteerr list` | List recent 10 errors |
| `noteerr list --all` | List all errors |
| `noteerr search "text"` | Search errors |
| `noteerr show 5` | Show error #5 details |
| `noteerr annotate 5 "fix"` | Add note to error #5 |
| `noteerr rerun 5` | Re-run command from error #5 |
| `noteerr stats` | Show statistics |
| `noteerr delete 5` | Delete error #5 |
| `noteerr clear` | Delete all errors |

## Tips & Tricks

### 1. Use descriptive notes

❌ Bad: `noteerr save "error"`
✅ Good: `noteerr save "missing env var DB_HOST, add to .env file"`

### 2. Tag consistently

```bash
# Create a tagging system
--tags git              # Git issues
--tags npm,node         # Node.js/NPM
--tags docker,devops    # Docker/DevOps
--tags db,postgres      # Database
--tags python,django    # Python/Framework
```

### 3. Review your errors weekly

```bash
# See what's been troubling you
$ noteerr stats
$ noteerr list --limit 20

# Find patterns in your mistakes
$ noteerr search "permission"  # Common permission issues
```

### 4. Use shell aliases

```bash
# Add to your shell config (~/.bashrc, ~/.zshrc, etc.)
alias ne='noteerr save'
alias nel='noteerr list'
alias nes='noteerr search'
alias nest='noteerr stats'

# Ultra-quick save: just type 'ne' after an error!
```

### 5. Combine with other tools

```bash
# Copy last error to clipboard (macOS)
$ noteerr show 1 | pbcopy

# Search and filter with grep
$ noteerr list | grep docker

# Export to file
$ noteerr list --all > my-errors.txt
```

## Real-World Workflow Example

```bash
# 1. Working on feature, hit an error
$ npm test
FAIL src/component.test.js

# 2. Quick save
$ ne "test failing, need to mock API call"
✓ Saved error #42

# 3. Fix the issue and add solution
$ noteerr annotate 42 "added jest.mock('@/api') at top of test file"

# 4. Week later, similar test fails
$ nes "mock"
# Found error #42 with the solution!

# 5. View full details
$ noteerr show 42
# See exactly what you did before
```

## Daily Developer Routine

### Morning
```bash
# Check what broke yesterday
$ noteerr list --limit 5
```

### During Development
```bash
# Hit an error? Save it immediately
$ failing-command
$ ne "quick note about what's wrong"

# Fixed it? Add the solution
$ noteerr annotate [id] "here's how I fixed it"
```

### End of Day
```bash
# Review your day's errors
$ noteerr stats
$ noteerr list --limit 10

# Clean up duplicates if needed
$ noteerr delete [id]
```

### Weekly Review
```bash
# See your most common issues
$ noteerr stats

# Identify patterns
$ noteerr search "permission"
$ noteerr search "not found"

# Share knowledge with team
$ noteerr show [id]  # Copy & paste to team wiki
```

---

**Pro Tip:** The more you use Noteerr, the more valuable it becomes. Think of it as building a personal Stack Overflow for your specific development environment!
