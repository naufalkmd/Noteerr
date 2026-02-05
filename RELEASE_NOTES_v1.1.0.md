# Release Notes - Noteerr v1.1.0

**Release Date:** February 5, 2026

## 🎉 What's New

Version 1.1.0 brings three major enhancements to improve your error management workflow:

### 1. 📋 Copy to Clipboard
Copy error details directly to your clipboard in multiple formats:
- **Text Format**: Plain text for quick sharing
- **Markdown Format**: Formatted for documentation
- **JSON Format**: Structured data for scripts

```bash
noteerr copy 1                    # Copy as text
noteerr copy 1 --format markdown  # Copy as markdown
noteerr copy 1 --format json      # Copy as JSON
```

**Cross-platform support:** Windows (PowerShell), macOS (pbcopy), Linux (xclip/xsel)

### 2. 🔒 Smart Duplicate Detection
Noteerr now automatically detects similar errors before saving:
- **Intelligent Matching**: Uses fuzzy word-based similarity (85% threshold)
- **Interactive Prompts**: Asks for confirmation when duplicates are found
- **Force Override**: Use `--force` flag to save anyway

```bash
noteerr save "npm ERR! network error"  # Auto-detects if similar error exists
noteerr save "error desc" --force      # Bypass duplicate detection
```

The duplicate detection compares:
- Command text
- Error messages
- Context clues

### 3. 📁 Project-Based Organization
Organize errors by project for better multi-project management:
- **Interactive Prompts**: Suggests existing projects when saving
- **Project Commands**: New `projects` command to view all projects
- **Filtering**: Filter errors by project in list and show commands
- **Project Column**: Added to list view for easy identification

```bash
noteerr save "bug" --project myapp  # Save with project
noteerr projects                     # List all projects
noteerr list --project frontend      # Filter by project
```

## 🔄 Migration from v1.0.0

No breaking changes! Your existing error database will work seamlessly:
- Existing errors will show "N/A" in the Project column
- You can start using project tags immediately
- All v1.0.0 commands remain fully compatible

## 📦 Installation

### For New Users
```bash
pip install noteerr
```

### Upgrading from v1.0.0
```bash
pip install --upgrade noteerr
```

### From Source
```bash
git clone https://github.com/yourusername/noteerr.git
cd noteerr
git checkout v1.1.0
pip install -e .
```

## 🐛 Bug Fixes

- Fixed `list()` function name collision with Python built-in
- Improved clipboard copy functionality for Windows PowerShell
- Enhanced multiline error handling in clipboard operations

## 📊 Statistics

- **Total Commits**: 50+
- **Files Changed**: 8 core files
- **New Commands**: 2 (`copy`, `projects`)
- **New Features**: 3 major feature sets
- **Lines Added**: ~400
- **Test Coverage**: All new features tested on Windows

## 🔮 Coming Soon (v1.2.0)

- Export errors to Markdown by project
- Bulk project assignment for existing errors
- Auto-detect project from git repository
- Project-based statistics and insights
- fzf integration for fuzzy finding

## 📚 Documentation

Updated documentation available:
- [NEW_FEATURES.md](NEW_FEATURES.md) - Detailed guide for v1.1.0 features
- [README.md](README.md) - Updated with new commands
- [EXAMPLES.md](EXAMPLES.md) - New usage examples
- [CHANGELOG.md](CHANGELOG.md) - Full version history

## 🙏 Acknowledgments

Thank you to all users who provided feedback and feature requests!

## 📝 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

---

**Questions or Issues?**
- Open an issue on [GitHub](https://github.com/yourusername/noteerr/issues)
- Check the [documentation](README.md)
- See [NEW_FEATURES.md](NEW_FEATURES.md) for detailed examples
