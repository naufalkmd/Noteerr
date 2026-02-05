#!/bin/bash
# Noteerr - Bash Shell Integration
# Add this to your ~/.bashrc or ~/.bash_profile

# Function to capture command errors automatically
noteerr_capture_error() {
    local exit_code=$?
    local last_command=$(history 1 | sed 's/^[ ]*[0-9]*[ ]*//')
    
    # Don't capture noteerr commands or successful commands
    if [[ $exit_code -ne 0 ]] && [[ ! "$last_command" =~ ^noteerr ]]; then
        # Save exit code and command for noteerr
        export NOTEERR_EXIT_CODE=$exit_code
        export NOTEERR_COMMAND="$last_command"
    fi
}

# Hook into bash prompt
if [[ ! "$PROMPT_COMMAND" =~ noteerr_capture_error ]]; then
    PROMPT_COMMAND="noteerr_capture_error;${PROMPT_COMMAND}"
fi

# Quick save alias - use this after a command fails
alias ne='noteerr save'
alias nel='noteerr list'
alias nes='noteerr search'

echo "Noteerr bash integration loaded! Use 'ne' to quickly save errors."
