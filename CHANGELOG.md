# Changelog

All notable changes to Noteerr will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-05

### Added
- **Copy to Clipboard**: New `copy` command to copy error details in text, markdown, or JSON format
- **Smart Duplicate Detection**: Automatically detects similar errors before saving to avoid duplicates
- **Project Organization**: Tag errors by project name for better multi-project management
  - Interactive project name prompt with existing project suggestions
  - `--project` flag for save and list commands
  - New `projects` command to view all projects with error counts
- **Enhanced List Display**: Added Project column to error listings
- **Force Save Option**: `--force` flag to bypass duplicate detection when needed
- Copy error details in multiple formats (text, markdown, JSON)
- Cross-platform clipboard support (Windows, macOS, Linux)

### Changed
- Updated `save` command with `--project` and `--force` options
- Updated `list` command with `--project` filter option
- Enhanced error display to include project information
- Improved table formatting with project column
- Better error similarity matching algorithm

### Fixed
- Fixed `list()` function name collision with Python built-in
- Improved clipboard copy functionality for Windows PowerShell

## [1.0.0] - 2026-02-05

### Added
- Initial release of Noteerr
- Command error capture with automatic detection
- Save errors with notes and tags
- List recent errors with filtering
- Search errors by command, error text, notes, or tags
- Detailed error view with full information
- Annotate errors with notes and update tags
- Command replay functionality
- Statistics tracking (total errors, most common commands)
- Delete individual errors or clear all
- Shell integration for Bash, Zsh, and PowerShell
- Rich terminal UI with colors and tables
- JSON-based persistent storage
- Cross-platform support (Windows, macOS, Linux)

### Features
- 🎯 Automatic error capture via shell hooks
- 📝 Annotation and note-taking system
- 🔍 Powerful search capabilities
- 🏷️ Tag-based organization
- 📊 Error statistics and insights
- 🔄 Command replay functionality
- 🎨 Beautiful terminal UI
- 🐚 Shell integration (Bash/Zsh/PowerShell)

## [Unreleased]

### Planned Features
- Export to Markdown by project
- Integration with fzf for fuzzy search
- Cloud sync across machines
- AI-powered solution suggestions
- Team collaboration features
- Web dashboard for visualization
- Bulk project assignment for existing errors
- Project-based statistics
- Auto-detect project from git repository

