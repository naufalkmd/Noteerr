"""Main CLI interface for noteerr."""
import os
import sys
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from . import __version__
from .storage import Storage
from .utils import (
    get_last_command,
    get_last_exit_code,
    truncate_text,
    extract_first_line,
    run_command,
    format_tags,
    parse_tags
)

console = Console()
storage = Storage()


@click.group()
@click.version_option(version=__version__)
def cli():
    """
    🚨 Noteerr - Command Error Memory Tool
    
    Automatically log, annotate, and recall command errors.
    Never forget how you fixed that mysterious bug again!
    
    ═══════════════════════════════════════════════════════════════════
    QUICK START
    ═══════════════════════════════════════════════════════════════════
    
        1. Run a command that fails
        2. Use 'noteerr save \"your note\"' to log it
        3. Use 'noteerr list' to see all errors
        4. Use 'noteerr search' to find similar issues
    
    ═══════════════════════════════════════════════════════════════════
    COMMANDS
    ═══════════════════════════════════════════════════════════════════
    
        save       Save a failed command with error and notes
        list       View recent or filtered error entries
        search     Find errors by command, text, notes, or tags
        show       Display full details of a specific error
        delete     Remove an error entry from the database
        stats      Display statistics about your logged errors
        copy       Copy error details to clipboard
        projects   Manage and organize errors by project
        tags       Manage error tags and categories
    
    ═══════════════════════════════════════════════════════════════════
    COMMON EXAMPLES
    ═══════════════════════════════════════════════════════════════════
    
        # Save an error after a command fails
        npm start || noteerr save \"missing dependency\"
        
        # View all recent errors
        noteerr list
        
        # Search for npm-related errors
        noteerr search npm
        
        # View errors from a specific project
        noteerr list --project MyApp
        
        # See detailed info about error #5
        noteerr show 5
        
        # Copy error #1 to clipboard
        noteerr copy 1
    
    ═══════════════════════════════════════════════════════════════════
    OPTIONS
    ═══════════════════════════════════════════════════════════════════
    
        --version       Show version and exit
        --help          Show this help message
    
    ═══════════════════════════════════════════════════════════════════
    GET HELP FOR A SPECIFIC COMMAND
    ═══════════════════════════════════════════════════════════════════
    
        noteerr COMMAND --help
        
        Examples:
            noteerr save --help
            noteerr list --help
            noteerr search --help
    """
    pass


@cli.command()
@click.argument('notes', required=False, default="")
@click.option('--command', '-c', help='Command that failed (auto-detected if not specified)')
@click.option('--error', '-e', help='Error message (read from stdin if not specified)')
@click.option('--exit-code', type=int, default=None, help='Exit code of failed command')
@click.option('--tags', '-t', help='Comma-separated tags (e.g., git,npm,docker)')
@click.option('--project', '-p', help='Project name (will prompt if not specified)')
@click.option('--force', '-f', is_flag=True, help='Force save even if duplicate exists')
def save(notes, command, error, exit_code, tags, project, force):
    """
    Save a failed command and error message for future reference.
    
    This command captures the last failed command along with its error output
    and saves it to the database with optional annotations, tags, and project info.
    
    ARGUMENTS:
        NOTES                    Optional annotation describing the fix or issue
    
    OPTIONS:
        -c, --command TEXT       The command that failed (auto-detected if omitted)
        -e, --error TEXT         Error message output (read from stdin if omitted)
        --exit-code INTEGER      Exit code of the failed command (auto-detected if omitted)
        -t, --tags TEXT          Comma-separated tags for categorization (e.g., git,npm,docker)
        -p, --project TEXT       Project name for organization (prompted if omitted)
        -f, --force              Force save even if a similar error already exists
    
    EXAMPLES:
        # After a command fails, save it with a note
        npm start || noteerr save "Missing dependencies - run npm install"
        
        # Manually specify command and error
        noteerr save --command "git push" --error "permission denied" "Check SSH keys"
        
        # Save with project and tags
        noteerr save "Fixed by restarting service" --project MyApp --tags deployment,restart
        
        # Pipe error output directly
        npm install 2>&1 | noteerr save "npm install failed"
    
    NOTES:
        • The command is auto-detected from shell history if not specified
        • Error output is read from stdin if --error is not provided
        • Duplicate detection prevents saving nearly identical errors
        • Use --force to bypass duplicate detection
    """
    # Get command if not specified
    if not command:
        command = os.environ.get('NOTEERR_COMMAND', get_last_command())
        if not command:
            console.print("[red]Error: Could not detect last command. Use --command flag.[/red]")
            sys.exit(1)
    
    # Get error from stdin if not specified
    if not error:
        error = os.environ.get('NOTEERR_ERROR', '')
        if not error and not sys.stdin.isatty():
            error = sys.stdin.read().strip()
        if not error:
            error = "Command failed"
    
    # Get exit code
    if exit_code is None:
        exit_code = get_last_exit_code()
    
    # Get current directory
    directory = os.getcwd()
    
    # Parse tags
    tag_list = parse_tags(tags) if tags else []
    
    # Get or prompt for project name
    if not project:
        # Get list of existing projects
        existing_projects = storage.get_all_projects()
        
        if existing_projects:
            console.print("\n[bold cyan]Available projects:[/bold cyan]")
            for i, proj in enumerate(existing_projects, 1):
                console.print(f"  {i}. {proj}")
            console.print("  [dim](or enter a new project name)[/dim]")
        
        project = click.prompt(
            "\nProject name (press Enter to skip)",
            default="",
            show_default=False
        ).strip()
    
    # Create a temporary entry for duplicate checking
    temp_entry = type('obj', (object,), {
        'command': command,
        'error': error,
        'is_similar_to': lambda self, other, threshold=0.85: (
            self.command.lower() == other.command.lower() and
            self.error.lower() == other.error.lower()
        )
    })()
    
    # Check for duplicates unless --force is used
    if not force:
        similar = storage.find_similar_entries(temp_entry, threshold=0.85)
        
        if similar:
            console.print(f"\n[yellow]⚠ Found {len(similar)} similar error(s):[/yellow]")
            for sim in similar[:3]:  # Show up to 3 similar errors
                console.print(f"  #{sim.id}: {truncate_text(sim.command, 50)}")
                console.print(f"       {truncate_text(extract_first_line(sim.error), 50)}")
                if sim.notes:
                    console.print(f"       [dim]Note: {truncate_text(sim.notes, 50)}[/dim]")
            
            if not click.confirm("\nSave anyway?", default=False):
                console.print("[yellow]Skipped - error not saved[/yellow]")
                return
    
    # Save to storage
    entry = storage.add_entry(
        command=command,
        error=error,
        exit_code=exit_code,
        directory=directory,
        notes=notes,
        tags=tag_list,
        project=project
    )
    
    console.print(f"\n[green]✓[/green] Saved error #{entry.id}")
    console.print(f"  Command: [cyan]{truncate_text(command, 60)}[/cyan]")
    console.print(f"  Error: [red]{truncate_text(extract_first_line(error), 60)}[/red]")
    if project:
        console.print(f"  Project: [blue]{project}[/blue]")
    if notes:
        console.print(f"  Notes: [yellow]{notes}[/yellow]")
    if tag_list:
        console.print(f"  Tags: [magenta]{format_tags(tag_list)}[/magenta]")


@cli.command()
@click.option('--limit', '-n', type=int, default=10, help='Number of entries to show')
@click.option('--tag', '-t', help='Filter by tag')
@click.option('--project', '-p', help='Filter by project')
@click.option('--all', '-a', 'show_all', is_flag=True, help='Show all entries')
def list(limit, tag, project, show_all):
    """
    Display recent error entries with filtering options.
    
    Shows a formatted table of logged errors sorted by most recent first.
    Filter by tags, projects, or limit the number of results.
    
    OPTIONS:
        -n, --limit INTEGER      Number of recent entries to show (default: 10)
        -t, --tag TEXT           Filter results by a specific tag
        -p, --project TEXT       Filter results by project name
        -a, --all                Show all entries (ignores --limit)
    
    EXAMPLES:
        # Show 10 most recent errors
        noteerr list
        
        # Show 20 most recent errors
        noteerr list --limit 20
        
        # Show all git-related errors
        noteerr list --tag git
        
        # Show errors from MyApp project
        noteerr list --project MyApp
        
        # Show all errors (no limit)
        noteerr list --all
    
    OUTPUT COLUMNS:
        ID           Unique error identifier
        Command      The failed command
        Error        First line of error output
        Project      Associated project (if any)
        Date         When the error was logged
        Tags         Associated tags
    
    NOTES:
        • Most recent errors appear first
        • Use 'noteerr show ID' to see full details
        • Use 'noteerr search' to find specific errors
    """
    # Prompt for project if --project flag used without value
    if project == "":
        projects = storage.get_all_projects()
        if projects:
            console.print("\n[bold cyan]Select a project:[/bold cyan]")
            for i, proj in enumerate(projects, 1):
                console.print(f"  {i}. {proj}")
            choice = click.prompt("Enter number or project name", type=str)
            
            # Try to parse as number
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(projects):
                    project = projects[idx]
                else:
                    project = choice
            except ValueError:
                project = choice
        else:
            console.print("[yellow]No projects found[/yellow]")
            return
    
    entries = storage.get_all_entries()
    
    # Filter by project
    if project:
        entries = [e for e in entries if e.project.lower() == project.lower()]
        if not entries:
            console.print(f"[yellow]No errors found for project '{project}'[/yellow]")
            return
    
    # Filter by tag
    if tag:
        entries = [e for e in entries if tag in e.tags]
    
    if not entries:
        console.print("[yellow]No errors logged yet. Start by running a command that fails![/yellow]")
        return
    
    # Show most recent first
    entries = [*reversed(entries)]
    
    if not show_all:
        entries = entries[:limit]
    
    # Build title with filter info
    title = "Recent Errors"
    if project:
        title += f" - Project: {project}"
    
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Command", style="white", width=25)
    table.add_column("Error", style="red", width=30)
    table.add_column("Project", style="blue", width=12)
    table.add_column("Date", style="green", width=12)
    table.add_column("Tags", style="magenta", width=12)
    
    for entry in entries:
        table.add_row(
            str(entry.id),
            truncate_text(entry.command, 23),
            truncate_text(extract_first_line(entry.error), 28),
            truncate_text(entry.project, 10) if entry.project else "-",
            entry.short_date,
            truncate_text(format_tags(entry.tags), 10)
        )
    
    console.print(table)
    
    if len(entries) == limit and not show_all:
        console.print(f"\n[dim]Showing {limit} most recent entries. Use --all to see everything.[/dim]")


@cli.command()
@click.argument('query')
@click.option('--limit', '-n', type=int, default=10, help='Max results to show')
def search(query, limit):
    """
    Search for errors across all fields (command, error text, notes, tags).
    
    Find previously logged errors using flexible keyword matching.
    
    ARGUMENTS:
        QUERY                    Search term (command name, error message, note, or tag)
    
    OPTIONS:
        -n, --limit INTEGER      Maximum number of results to show (default: 10)
    
    EXAMPLES:
        # Search for npm-related errors
        noteerr search npm
        
        # Search for permission errors
        noteerr search "permission denied"
        
        # Search for docker issues
        noteerr search docker --limit 5
        
        # Search for specific error messages
        noteerr search "ENOSPC"
    
    SEARCH FIELDS:
        • Command name
        • Error message text
        • Saved notes
        • Tags
        • Project names
    
    OUTPUT COLUMNS:
        ID           Unique error identifier
        Command      The failing command
        Error        Error message (truncated)
        Date         When logged
    
    TIPS:
        • Use 'noteerr show ID' for full details
        • Search is case-insensitive
        • Partial matches are supported
    """
    entries = storage.search_entries(query)
    
    if not entries:
        console.print(f"[yellow]No errors found matching '{query}'[/yellow]")
        return
    
    # Show most recent first
    entries = [*reversed(entries)][:limit]
    
    console.print(f"[bold]Found {len(entries)} error(s) matching '{query}':[/bold]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Command", style="white", width=30)
    table.add_column("Error", style="red", width=40)
    table.add_column("Date", style="green", width=12)
    
    for entry in entries:
        table.add_row(
            str(entry.id),
            truncate_text(entry.command, 28),
            truncate_text(extract_first_line(entry.error), 38),
            entry.short_date
        )
    
    console.print(table)


@cli.command()
@click.argument('entry_id', type=int)
def show(entry_id):
    """
    Display complete details of a specific error entry.
    
    Shows all information: command, error output, notes, tags, timestamp, and more.
    
    ARGUMENTS:
        ENTRY_ID                 The error ID number (from 'noteerr list' or 'noteerr search')
    
    EXAMPLES:
        # View error #1
        noteerr show 1
        
        # View error #42
        noteerr show 42
    
    DISPLAYED INFORMATION:
        • Error ID and timestamp
        • Full command that failed
        • Exit code
        • Working directory
        • Project name (if assigned)
        • Tags (if any)
        • Your notes about the fix
        • Complete error output
    
    RELATED COMMANDS:
        • noteerr list             See all errors
        • noteerr search           Find specific errors
        • noteerr copy ID          Copy error details
        • noteerr delete ID        Remove this error
    """
    entry = storage.get_entry_by_id(entry_id)
    
    if not entry:
        console.print(f"[red]Error #{entry_id} not found[/red]")
        sys.exit(1)
    
    # Create a detailed panel
    content = Text()
    content.append(f"Command: ", style="bold cyan")
    content.append(f"{entry.command}\n\n", style="white")
    
    content.append(f"Exit Code: ", style="bold yellow")
    content.append(f"{entry.exit_code}\n\n", style="white")
    
    content.append(f"Directory: ", style="bold blue")
    content.append(f"{entry.directory}\n\n", style="white")
    
    content.append(f"Timestamp: ", style="bold green")
    content.append(f"{entry.formatted_timestamp}\n\n", style="white")
    
    if entry.project:
        content.append(f"Project: ", style="bold blue")
        content.append(f"{entry.project}\n\n", style="blue")
    
    if entry.tags:
        content.append(f"Tags: ", style="bold magenta")
        content.append(f"{format_tags(entry.tags)}\n\n", style="magenta")
    
    if entry.notes:
        content.append(f"Notes: ", style="bold yellow")
        content.append(f"{entry.notes}\n\n", style="yellow")
    
    content.append(f"Error Output:\n", style="bold red")
    
    panel = Panel(content, title=f"Error #{entry.id}", border_style="blue")
    console.print(panel)
    
    # Show error in syntax-highlighted box
    console.print(Panel(entry.error, title="Error Details", border_style="red"))
    
    # Show tip about copying
    console.print("\n[dim]💡 Tip: Use 'noteerr copy " + str(entry_id) + "' to copy this error to clipboard[/dim]")


def _copy_terminal_output(format='text'):
    """Copy the last command and its output from terminal to clipboard."""
    import subprocess
    
    if sys.platform == 'win32':
        # Try to capture from PowerShell using PSReadLine history and console buffer
        ps_script = r'''
# Try to get command from PSReadLine history file (persistent across sessions)
$historyPath = (Get-PSReadLineOption).HistorySavePath

if (Test-Path $historyPath) {
    # Read last 20 lines, exclude noteerr commands, get the most recent
    $history = Get-Content $historyPath -Tail 20 | Where-Object { $_ -notlike '*noteerr*' -and $_.Trim() -ne '' }
    
    if ($history) {
        if ($history -is [array]) {
            $lastCmd = $history[-1]
        } else {
            $lastCmd = $history
        }
        
        # Try to read console screen buffer for recent output
        try {
            $bufferWidth = $host.UI.RawUI.BufferSize.Width
            $cursorPos = $host.UI.RawUI.CursorPosition
            
            # Read last 50 lines or up to cursor position
            $linesToRead = [Math]::Min(50, $cursorPos.Y + 1)
            $startY = [Math]::Max(0, $cursorPos.Y - $linesToRead + 1)
            
            $rect = New-Object System.Management.Automation.Host.Rectangle(0, $startY, $bufferWidth - 1, $cursorPos.Y)
            $buffer = $host.UI.RawUI.GetBufferContents($rect)
            
            $output = ""
            for ($y = 0; $y -lt $buffer.GetLength(0); $y++) {
                $line = ""
                for ($x = 0; $x -lt $buffer.GetLength(1); $x++) {
                    $line += $buffer[$y, $x].Character
                }
                $output += $line.TrimEnd() + "`n"
            }
            
            Write-Output "NOTEERR_COMMAND: $lastCmd"
            Write-Output "NOTEERR_OUTPUT_START"
            Write-Output $output.Trim()
            Write-Output "NOTEERR_OUTPUT_END"
        } catch {
            # Fallback: just return the command
            Write-Output "NOTEERR_COMMAND: $lastCmd"
            Write-Output "NOTEERR_OUTPUT: (Console buffer not accessible - output capture works best in Windows PowerShell console)"
        }
    } else {
        Write-Output "NOTEERR_ERROR: No command history found"
        exit 1
    }
} else {
    Write-Output "NOTEERR_ERROR: PSReadLine history not found at $historyPath"
    exit 1
}
'''
        
        try:
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_script],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0 or "NOTEERR_ERROR" in result.stdout:
                console.print("[yellow]No recent command found to copy[/yellow]")
                console.print()
                console.print("[dim]This feature reads from PowerShell history and console buffer.[/dim]")
                console.print("[dim]It works best in Windows PowerShell console or Windows Terminal.[/dim]")
                console.print()
                console.print("[dim]Alternatives:[/dim]")
                console.print("  • Copy saved errors: [cyan]noteerr copy error latest[/cyan]")
                console.print("  • Pipe to clipboard: [cyan]your-command | Set-Clipboard[/cyan]")
                return
            
            output = result.stdout
            
            # Parse the output
            if "NOTEERR_COMMAND:" in output:
                lines = output.split('\n')
                command = ""
                console_output = []
                in_output = False
                
                for line in lines:
                    if line.startswith("NOTEERR_COMMAND:"):
                        command = line.replace("NOTEERR_COMMAND:", "").strip()
                    elif line == "NOTEERR_OUTPUT_START":
                        in_output = True
                    elif line == "NOTEERR_OUTPUT_END":
                        in_output = False
                    elif in_output:
                        console_output.append(line)
                    elif line.startswith("NOTEERR_OUTPUT:"):
                        msg = line.replace("NOTEERR_OUTPUT:", "").strip()
                        if "not accessible" in msg:
                            console.print(f"[yellow]{msg}[/yellow]")
                            console_output = []
                
                # Format the content
                content = f"Command:\n{command}\n\n"
                if console_output:
                    output_text = '\n'.join(console_output).strip()
                    if output_text:
                        # Clean up the output - remove duplicate command echoes
                        lines = output_text.split('\n')
                        cleaned_lines = []
                        for line in lines:
                            # Skip lines that are just the PS prompt or the command itself
                            if not line.strip().startswith('PS ') and line.strip() != command:
                                cleaned_lines.append(line)
                        
                        if cleaned_lines:
                            content += f"Output:\n" + '\n'.join(cleaned_lines)
                        else:
                            content += "Output: (captured but appears empty)"
                    else:
                        content += "Output: (captured but appears empty)"
                else:
                    content = f"Command:\n{command}\n\nOutput: (Console buffer not accessible from this context)"
                
                # Copy to clipboard
                _copy_to_clipboard(content, "latest command and output")
            else:
                console.print("[yellow]Could not parse command output[/yellow]")
                
        except subprocess.TimeoutExpired:
            console.print("[red]Timeout while trying to capture console buffer[/red]")
            console.print("[dim]💡 Tip: Use 'noteerr copy error latest' to copy saved errors[/dim]")
        except Exception as e:
            console.print(f"[red]Error capturing terminal output: {e}[/red]")
            console.print()
            console.print("[dim]Alternatives:[/dim]")
            console.print("  • Pipe to clipboard: [cyan]your-command | Set-Clipboard[/cyan]")
            console.print("  • Copy saved errors: [cyan]noteerr copy error latest[/cyan]")
    else:
        # macOS/Linux - terminal output capture is more complex
        console.print("[yellow]⚠ Terminal output capture is not yet fully implemented on this platform[/yellow]")
        console.print()
        console.print("[dim]To copy command output:[/dim]")
        console.print()
        console.print("  1. Pipe to clipboard directly:")
        if sys.platform == 'darwin':
            console.print("     [cyan]your-command | pbcopy[/cyan]")
        else:
            console.print("     [cyan]your-command | xclip -selection clipboard[/cyan]")
        console.print()
        console.print("  2. Copy logged errors (copies full error details from saved errors):")
        console.print("     [cyan]noteerr copy error latest[/cyan]")



def _copy_to_clipboard(content, description="content"):
    """Helper function to copy content to clipboard across platforms."""
    import subprocess
    
    try:
        if sys.platform == 'win32':
            process = subprocess.Popen(
                ['powershell', '-command', '$input | Set-Clipboard'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(content.encode('utf-8'))
            if process.returncode == 0:
                console.print(f"[green]✓[/green] Copied {description} to clipboard")
            else:
                console.print(f"[red]Failed to copy to clipboard[/red]")
                if stderr:
                    console.print(f"[dim]{stderr.decode('utf-8')}[/dim]")
                console.print("\n[dim]Content:[/dim]")
                console.print(content)
        elif sys.platform == 'darwin':
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(content.encode('utf-8'))
            console.print(f"[green]✓[/green] Copied {description} to clipboard")
        else:
            # Linux - try xclip
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'],
                                         stdin=subprocess.PIPE)
                process.communicate(content.encode('utf-8'))
                console.print(f"[green]✓[/green] Copied {description} to clipboard")
            except FileNotFoundError:
                console.print("[yellow]xclip not found. Install it with: sudo apt-get install xclip[/yellow]")
                console.print("\n[dim]Content:[/dim]")
                console.print(content)
    except Exception as e:
        console.print(f"[red]Error copying to clipboard: {e}[/red]")
        console.print("\n[dim]Content:[/dim]")
        console.print(content)


@cli.command()
@click.argument('what', type=str)
@click.argument('specifier', type=str, required=False)
@click.option('--format', '-f', type=click.Choice(['text', 'markdown', 'json']), default='text',
              help='Output format for clipboard')
def copy(what, specifier, format):
    """
    Copy error details to clipboard in various formats.
    
    Copy a saved error or terminal output to your clipboard for sharing or documentation.
    
    ARGUMENTS:
        WHAT                     What to copy: error ID, 'latest', etc.
        SPECIFIER                Additional argument (optional, e.g., 'error 1' or 'latest error')
    
    OPTIONS:
        -f, --format TEXT        Output format: text, markdown, or json (default: text)
    
    EXAMPLES:
        # Copy error #1 to clipboard
        noteerr copy 1
        
        # Copy the latest error
        noteerr copy latest
        
        # Copy specific error
        noteerr copy error 42
        
        # Copy as Markdown (great for documentation)
        noteerr copy 1 --format markdown
        
        # Copy latest error as JSON
        noteerr copy latest --format json
    
    FORMATS:
        text       Plain text format - easy to paste in messages
        markdown   Markdown format - suitable for documentation and tickets
        json       JSON format - for programmatic use
    
    USE CASES:
        • Share errors with teammates
        • Document solutions
        • Create issue tickets
        • Archive important errors
    
    TIPS:
        • After copying, paste with Ctrl+V (or Cmd+V on Mac)
        • Markdown format is best for GitHub issues
        • JSON is useful for tool integration
    """
    # Determine what to copy
    copy_type = None
    entry_id = None
    
    # Parse arguments
    if specifier:
        # Two arguments: "error latest", "error 1", etc.
        if what.lower() == 'error':
            copy_type = 'error'
            if specifier.lower() == 'latest':
                entry_id = 'latest'
            else:
                try:
                    entry_id = int(specifier)
                except ValueError:
                    console.print(f"[red]Invalid error ID: '{specifier}'[/red]")
                    sys.exit(1)
        elif what.lower() == 'latest' and specifier.lower() == 'error':
            # "latest error" -> copy latest error
            copy_type = 'error'
            entry_id = 'latest'
        else:
            console.print(f"[red]Invalid syntax. Use: copy <id>, copy latest, copy error <id>, or copy latest error[/red]")
            sys.exit(1)
    else:
        # Single argument
        if what.lower() == 'latest':
            # Copy last command output from terminal
            copy_type = 'terminal'
        else:
            # Assume it's an error ID
            copy_type = 'error'
            try:
                entry_id = int(what)
            except ValueError:
                console.print(f"[red]Invalid error ID: '{what}'. Use a number, 'latest', or 'error latest'[/red]")
                sys.exit(1)
    
    # Handle terminal output copy
    if copy_type == 'terminal':
        _copy_terminal_output(format)
        return
    
    # Handle error copy
    if entry_id == 'latest':
        all_entries = storage.get_all_entries()
        if not all_entries:
            console.print("[yellow]No errors logged yet[/yellow]")
            sys.exit(1)
        entry = all_entries[-1]  # Most recent is last in list
    else:
        entry = storage.get_entry_by_id(entry_id)
    
    if not entry:
        console.print(f"[red]Error #{entry_id} not found[/red]")
        sys.exit(1)
    
    # Format the content based on chosen format
    if format == 'json':
        import json
        content = json.dumps(entry.to_dict(), indent=2)
    elif format == 'markdown':
        content = f"""# Error #{entry.id}

**Command:** `{entry.command}`
**Exit Code:** {entry.exit_code}
**Directory:** `{entry.directory}`
**Timestamp:** {entry.formatted_timestamp}
"""
        if entry.project:
            content += f"**Project:** {entry.project}\n"
        if entry.tags:
            content += f"**Tags:** {', '.join(entry.tags)}\n"
        if entry.notes:
            content += f"\n**Notes:** {entry.notes}\n"
        
        content += f"\n## Error Output\n\n```\n{entry.error}\n```"
    else:  # text format
        content = f"""Error #{entry.id}
Command: {entry.command}
Exit Code: {entry.exit_code}
Directory: {entry.directory}
Timestamp: {entry.formatted_timestamp}
"""
        if entry.project:
            content += f"Project: {entry.project}\n"
        if entry.tags:
            content += f"Tags: {', '.join(entry.tags)}\n"
        if entry.notes:
            content += f"Notes: {entry.notes}\n"
        
        content += f"\nError Output:\n{entry.error}"
    
    # Copy to clipboard
    _copy_to_clipboard(content, f"error #{entry.id} ({format} format)")


@cli.command()
@click.argument('entry_id', type=int)
@click.argument('notes')
@click.option('--tags', '-t', help='Update tags (comma-separated)')
def annotate(entry_id, notes, tags):
    """
    Add or update notes and tags for an error entry.
    
    Examples:
        noteerr annotate 1 "run npm install first"
        noteerr annotate 1 "fixed by updating Node" --tags npm,node
    """
    entry = storage.get_entry_by_id(entry_id)
    
    if not entry:
        console.print(f"[red]Error #{entry_id} not found[/red]")
        sys.exit(1)
    
    tag_list = parse_tags(tags) if tags else None
    
    if storage.update_entry(entry_id, notes=notes, tags=tag_list):
        console.print(f"[green]✓[/green] Updated error #{entry_id}")
        console.print(f"  Notes: [yellow]{notes}[/yellow]")
        if tag_list:
            console.print(f"  Tags: [magenta]{format_tags(tag_list)}[/magenta]")
    else:
        console.print(f"[red]Failed to update error #{entry_id}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('entry_id', type=int)
@click.option('--dry-run', is_flag=True, help='Show command without executing')
def rerun(entry_id, dry_run):
    """
    Re-execute a previously failed command.
    
    Examples:
        noteerr rerun 1
        noteerr rerun 1 --dry-run
    """
    entry = storage.get_entry_by_id(entry_id)
    
    if not entry:
        console.print(f"[red]Error #{entry_id} not found[/red]")
        sys.exit(1)
    
    console.print(f"[bold]Command:[/bold] {entry.command}")
    console.print(f"[bold]Directory:[/bold] {entry.directory}\n")
    
    if dry_run:
        console.print("[yellow]Dry run - command not executed[/yellow]")
        return
    
    if not click.confirm("Execute this command?"):
        console.print("[yellow]Cancelled[/yellow]")
        return
    
    console.print("[cyan]Executing...[/cyan]\n")
    
    exit_code, stdout, stderr = run_command(entry.command, entry.directory)
    
    if stdout:
        console.print(stdout)
    
    if stderr:
        console.print(f"[red]{stderr}[/red]")
    
    if exit_code == 0:
        console.print(f"\n[green]✓ Command succeeded (exit code: {exit_code})[/green]")
    else:
        console.print(f"\n[red]✗ Command failed (exit code: {exit_code})[/red]")


@cli.command()
@click.option('--tag', '-t', help='Show stats for specific tag')
def stats(tag):
    """
    Display statistics about your logged errors.
    
    Shows summary information about all errors or errors with a specific tag.
    
    OPTIONS:
        -t, --tag TEXT           Show statistics for only errors with this tag
    
    EXAMPLES:
        # Overview of all errors
        noteerr stats
        
        # Statistics for npm errors
        noteerr stats --tag npm
        
        # Statistics for git-related errors
        noteerr stats --tag git
    
    DISPLAYS:
        • Total number of logged errors
        • Most frequently failing command
        • Most recent error
        • All tags and their usage counts
    
    TIPS:
        • Use stats to identify problem areas
        • High error counts for same command suggest a systemic issue
        • Tag distribution shows your most problematic areas
    """
    if tag:
        entries = [e for e in storage.get_all_entries() if tag in e.tags]
        if not entries:
            console.print(f"[yellow]No errors found with tag '{tag}'[/yellow]")
            return
        console.print(f"[bold]Statistics for tag '{tag}':[/bold]")
        console.print(f"Total errors: {len(entries)}\n")
        return
    
    stats_data = storage.get_statistics()
    
    if stats_data['total_errors'] == 0:
        console.print("[yellow]No errors logged yet[/yellow]")
        return
    
    table = Table(title="Error Statistics", show_header=False, box=None)
    table.add_column("Metric", style="cyan", width=25)
    table.add_column("Value", style="white")
    
    table.add_row("Total Errors Logged", str(stats_data['total_errors']))
    table.add_row("Most Common Command", 
                  f"{stats_data['most_common_command']} ({stats_data['most_common_count']} times)")
    
    if stats_data['most_recent']:
        recent = stats_data['most_recent']
        table.add_row("Most Recent Error", 
                      f"#{recent.id} - {truncate_text(recent.command, 40)}")
        table.add_row("", recent.short_date)
    
    console.print(table)
    
    if stats_data['tags']:
        console.print("\n[bold]Tags:[/bold]")
        for tag, count in sorted(stats_data['tags'].items(), key=lambda x: x[1], reverse=True):
            console.print(f"  [magenta]{tag}[/magenta]: {count}")


@cli.command()
def projects():
    """
    List all projects and their error counts.
    
    Shows Summary of errors organized by project.
    
    EXAMPLES:
        # View all projects
        noteerr projects
    
    DISPLAYS:
        • Project name
        • Number of errors per project
        • Most recent error in each project
    
    RELATED COMMANDS:
        • noteerr list --project NAME     View errors in a project
        • noteerr save --project NAME     Create error with project tag
    
    NOTES:
        • Projects are assigned when saving errors with --project flag
        • Use projects to organize errors across multiple codebases
    """
    all_projects = storage.get_all_projects()
    
    if not all_projects:
        console.print("[yellow]No projects found. Add --project when saving errors.[/yellow]")
        return
    
    console.print("[bold cyan]Projects:[/bold cyan]\n")
    
    # Get error counts for each project
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Project", style="blue")
    table.add_column("Errors", style="cyan", justify="right")
    table.add_column("Latest Error", style="green")
    
    for project in all_projects:
        project_entries = storage.get_entries_by_project(project)
        latest = max(project_entries, key=lambda e: e.timestamp) if project_entries else None
        
        table.add_row(
            project,
            str(len(project_entries)),
            latest.short_date if latest else "-"
        )
    
    console.print(table)
    console.print(f"\n[dim]💡 Tip: Use 'noteerr list --project <name>' to see errors for a specific project[/dim]")


@cli.command()
@click.argument('entry_id', type=int)
@click.confirmation_option(prompt='Are you sure you want to delete this error?')
def delete(entry_id):
    """
    Permanently delete a specific error entry.
    
    Remove an error from the database. You will be asked to confirm.
    
    ARGUMENTS:
        ENTRY_ID                 The ID of the error to delete (from 'noteerr list')
    
    EXAMPLES:
        # Delete error #5
        noteerr delete 5
        
        # Delete error #42
        noteerr delete 42
    
    WARNING:
        • This action is permanent and cannot be undone
        • You will be prompted to confirm before deletion
    
    RELATED COMMANDS:
        • noteerr clear           Delete ALL errors
        • noteerr list            See all errors with their IDs
    """
    if storage.delete_entry(entry_id):
        console.print(f"[green]✓ Deleted error #{entry_id}[/green]")
    else:
        console.print(f"[red]Error #{entry_id} not found[/red]")
        sys.exit(1)


@cli.command()
@click.confirmation_option(prompt='Are you sure you want to delete ALL errors?')
def clear():
    """
    Permanently delete ALL error entries.
    
    Remove the entire error database. You will be asked to confirm.
    
    WARNING:
        • This action is PERMANENT and CANNOT be undone
        • All logged errors will be deleted
        • You must confirm before execution
    
    USE CASES:
        • Starting fresh
        • Privacy cleanup
        • Resetting the database
    
    EXAMPLES:
        # Clear all errors (with confirmation)
        noteerr clear
    
    SAFER ALTERNATIVES:
        • Use 'noteerr delete ID' to remove individual errors
        • Use 'noteerr list --tag TAG' to find specific errors
    """
    count = storage.clear_all()
    console.print(f"[green]✓ Cleared {count} error(s)[/green]")


@cli.command()
@click.option('--shell', type=click.Choice(['bash', 'zsh', 'powershell']), 
              help='Generate shell integration script')
@click.option('--check-path', is_flag=True, help='Check and fix PATH on Windows')
def install(shell, check_path):
    """
    Install shell integration for automatic error capture.
    
    Examples:
        noteerr install --check-path           # Check/fix PATH on Windows
        noteerr install --shell bash
        noteerr install --shell zsh
        noteerr install --shell powershell
    """
    # Handle PATH check for Windows
    if check_path or (not shell and sys.platform == 'win32'):
        _check_and_fix_path()
        if not shell:
            return
    
    if not shell:
        console.print("[yellow]Please specify a shell: --shell bash|zsh|powershell[/yellow]")
        console.print("\nFor manual integration, add this to your shell config:")
        console.print("\n[cyan]Bash/Zsh:[/cyan]")
        console.print('  noteerr_auto() { [ $? -ne 0 ] && noteerr save; }')
        console.print('  PROMPT_COMMAND="noteerr_auto;$PROMPT_COMMAND"')
        console.print("\n[cyan]PowerShell:[/cyan]")
        console.print('  See scripts/powershell-integration.ps1')
        return
    
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 
                               f'{shell}-integration.{"ps1" if shell == "powershell" else "sh"}')
    
    if os.path.exists(script_path):
        with open(script_path, 'r') as f:
            console.print(f.read())
    else:
        console.print(f"[yellow]Integration script for {shell} not found[/yellow]")


def _check_and_fix_path():
    """Check if noteerr is in PATH and offer to fix it on Windows."""
    import subprocess
    import shutil
    
    # Check if noteerr is already in PATH
    if shutil.which('noteerr'):
        console.print("[green]✓ noteerr is already in your PATH![/green]")
        return
    
    console.print("[yellow]⚠ noteerr is not in your PATH[/yellow]")
    console.print()
    
    if sys.platform == 'win32':
        # Find where noteerr.exe is installed
        import site
        
        # Check common locations
        possible_paths = [
            os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Python', 
                        f'Python{sys.version_info.major}{sys.version_info.minor}', 'Scripts'),
            os.path.join(sys.prefix, 'Scripts'),
            os.path.join(site.USER_BASE, 'Scripts'),
        ]
        
        noteerr_path = None
        for path in possible_paths:
            if os.path.exists(os.path.join(path, 'noteerr.exe')):
                noteerr_path = path
                break
        
        if not noteerr_path:
            console.print("[red]Could not locate noteerr.exe[/red]")
            console.print("[dim]You may need to reinstall: pip install --user noteerr[/dim]")
            return
        
        console.print(f"[dim]Found noteerr at: {noteerr_path}[/dim]")
        console.print()
        console.print("[bold]Would you like to add it to your PATH automatically?[/bold]")
        console.print("[dim](This will add the directory to your user PATH environment variable)[/dim]")
        console.print()
        
        response = input("Add to PATH? [Y/n]: ").strip().lower()
        
        if response in ['', 'y', 'yes']:
            try:
                # Add to user PATH using PowerShell
                ps_command = f'''
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*{noteerr_path}*") {{
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;{noteerr_path}", "User")
    Write-Output "SUCCESS"
}} else {{
    Write-Output "ALREADY_EXISTS"
}}
'''
                result = subprocess.run(
                    ['powershell', '-NoProfile', '-Command', ps_command],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if "SUCCESS" in result.stdout:
                    console.print()
                    console.print("[green]✓ Successfully added to PATH![/green]")
                    console.print()
                    console.print("[yellow]⚠ Important:[/yellow] Close and reopen your terminal for changes to take effect.")
                    console.print()
                    console.print("[dim]Then verify with:[/dim] [cyan]noteerr --version[/cyan]")
                elif "ALREADY_EXISTS" in result.stdout:
                    console.print()
                    console.print("[yellow]Path already exists in your PATH variable[/yellow]")
                    console.print("[dim]Try closing and reopening your terminal[/dim]")
                else:
                    console.print()
                    console.print("[red]Failed to update PATH[/red]")
                    console.print(f"[dim]Error: {result.stderr}[/dim]")
                    _show_manual_path_instructions(noteerr_path)
                    
            except Exception as e:
                console.print()
                console.print(f"[red]Error updating PATH: {e}[/red]")
                _show_manual_path_instructions(noteerr_path)
        else:
            console.print()
            console.print("[yellow]Skipped PATH update[/yellow]")
            _show_manual_path_instructions(noteerr_path)
    else:
        # macOS/Linux
        console.print("[dim]On macOS/Linux, pip usually installs to a location already in PATH.[/dim]")
        console.print("[dim]If not, try:[/dim]")
        console.print("  [cyan]pip install --user noteerr[/cyan]")
        console.print("[dim]Then add to your ~/.bashrc or ~/.zshrc:[/dim]")
        console.print("  [cyan]export PATH=\"$HOME/.local/bin:$PATH\"[/cyan]")


def _show_manual_path_instructions(noteerr_path):
    """Show manual instructions for adding to PATH."""
    console.print()
    console.print("[bold]Manual PATH setup:[/bold]")
    console.print()
    console.print("1. Open PowerShell and run:")
    console.print(f"   [cyan][Environment]::SetEnvironmentVariable(\"Path\", $env:Path + \";{noteerr_path}\", \"User\")[/cyan]")
    console.print()
    console.print("2. Close and reopen your terminal")
    console.print()
    console.print("3. Verify with: [cyan]noteerr --version[/cyan]")


def main():
    """Entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
