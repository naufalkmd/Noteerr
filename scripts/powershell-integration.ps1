# Noteerr - PowerShell Integration
# Add this to your PowerShell profile ($PROFILE)

# Function to capture command errors automatically
function Invoke-NoteerrCapture {
    if ($? -eq $false) {
        $lastCommand = (Get-History -Count 1).CommandLine
        
        # Don't capture noteerr commands
        if ($lastCommand -notmatch '^noteerr') {
            $env:NOTEERR_EXIT_CODE = "$LASTEXITCODE"
            $env:NOTEERR_COMMAND = $lastCommand
            
            # Get the last error
            if ($Error.Count -gt 0) {
                $env:NOTEERR_ERROR = $Error[0].Exception.Message
            }
        }
    }
}

# Hook into PowerShell prompt
$Global:OriginalPrompt = $function:prompt

function Global:prompt {
    Invoke-NoteerrCapture
    & $Global:OriginalPrompt
}

# Quick save aliases
Set-Alias -Name ne -Value noteerr
function nel { noteerr list @args }
function nes { noteerr search @args }

Write-Host "Noteerr PowerShell integration loaded! Use 'ne save' to quickly save errors." -ForegroundColor Green
