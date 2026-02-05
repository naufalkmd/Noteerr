$ErrorActionPreference = 'Stop'

$packageName = 'noteerr'

Write-Host "Uninstalling Noteerr..." -ForegroundColor Cyan

# Try to uninstall using pip
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if ($pythonCmd) {
    python -m pip uninstall -y noteerr 2>&1 | Out-Null
    Write-Host "Noteerr uninstalled successfully!" -ForegroundColor Green
} else {
    Write-Warning "Python not found. Noteerr may not be fully uninstalled."
}

Write-Host "Uninstallation complete!" -ForegroundColor Green
