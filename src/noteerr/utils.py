"""Utility functions for noteerr."""
import os
import subprocess
import sys
from pathlib import Path
from typing import Tuple, Optional


def get_last_command() -> str:
    """Get the last command from shell history."""
    shell = os.environ.get('SHELL', '').lower()
    
    if 'bash' in shell:
        history_file = Path.home() / '.bash_history'
    elif 'zsh' in shell:
        history_file = Path.home() / '.zsh_history'
    else:
        # On Windows or other shells
        return ""
    
    if history_file.exists():
        try:
            with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    # Second to last line (last line is the noteerr command itself)
                    return lines[-2].strip()
        except Exception:
            pass
    
    return ""


def get_last_exit_code() -> int:
    """Get the last exit code from the shell."""
    # This is typically passed via environment variable or argument
    return int(os.environ.get('NOTEERR_EXIT_CODE', '1'))


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def extract_first_line(text: str) -> str:
    """Extract the first non-empty line from text."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return lines[0] if lines else text


def run_command(command: str, cwd: Optional[str] = None) -> Tuple[int, str, str]:
    """
    Run a shell command and return exit code, stdout, stderr.
    
    Args:
        command: Command to execute
        cwd: Working directory for command execution
        
    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    try:
        # Use shell=True to run in shell context (works cross-platform)
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out after 30 seconds"
    except Exception as e:
        return -1, "", str(e)


def format_tags(tags: list) -> str:
    """Format tags for display."""
    if not tags:
        return ""
    return " ".join(f"[{tag}]" for tag in tags)


def parse_tags(tag_string: str) -> list:
    """Parse comma-separated tags."""
    if not tag_string:
        return []
    return [tag.strip() for tag in tag_string.split(',') if tag.strip()]


def get_terminal_width() -> int:
    """Get the current terminal width."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80  # Default width
