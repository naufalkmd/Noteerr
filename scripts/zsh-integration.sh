#!/bin/zsh
# Noteerr - Zsh Shell Integration
# Add this to your ~/.zshrc

# Function to capture command errors automatically
noteerr_capture_error() {
    local exit_code=$?
    local last_command="${history[$HISTCMD]}"
    
    # Don't capture noteerr commands or successful commands
    if [[ $exit_code -ne 0 ]] && [[ ! "$last_command" =~ ^noteerr ]]; then
        # Save exit code and command for noteerr
        export NOTEERR_EXIT_CODE=$exit_code
        export NOTEERR_COMMAND="$last_command"
    fi
}

# Hook into zsh prompt
autoload -Uz add-zsh-hook
add-zsh-hook precmd noteerr_capture_error

# Quick save alias - use this after a command fails
alias ne='noteerr save'
alias nel='noteerr list'
alias nes='noteerr search'

echo "Noteerr zsh integration loaded! Use 'ne' to quickly save errors."
