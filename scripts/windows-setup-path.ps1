# Noteerr - Add to PATH (Windows)
# Run this script as Administrator to permanently add noteerr to your PATH

Write-Host "🚀 Noteerr PATH Setup for Windows" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

$scriptsPath = "C:\Users\$env:USERNAME\AppData\Roaming\Python\Python311\Scripts"

# Check if noteerr.exe exists
if (Test-Path "$scriptsPath\noteerr.exe") {
    Write-Host "✓ Found noteerr.exe at: $scriptsPath" -ForegroundColor Green
} else {
    Write-Host "✗ noteerr.exe not found at: $scriptsPath" -ForegroundColor Red
    Write-Host "  Please install noteerr first: pip install -e ." -ForegroundColor Yellow
    exit 1
}

# Check if already in PATH
$currentPath = [System.Environment]::GetEnvironmentVariable('PATH', 'User')
if ($currentPath -like "*$scriptsPath*") {
    Write-Host "⚠ Scripts directory is already in your PATH" -ForegroundColor Yellow
    Write-Host "  You may need to restart PowerShell for changes to take effect." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "Adding Python Scripts directory to your PATH..." -ForegroundColor Cyan
    
    try {
        [System.Environment]::SetEnvironmentVariable(
            'PATH',
            $currentPath + ";$scriptsPath",
            'User'
        )
        Write-Host "✓ Successfully added to PATH!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📝 Next steps:" -ForegroundColor Cyan
        Write-Host "  1. Close this PowerShell window" -ForegroundColor White
        Write-Host "  2. Open a new PowerShell window" -ForegroundColor White
        Write-Host "  3. Run: noteerr --version" -ForegroundColor White
    } catch {
        Write-Host "✗ Failed to update PATH" -ForegroundColor Red
        Write-Host "  Error: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please run this script as Administrator:" -ForegroundColor Yellow
        Write-Host "  Right-click PowerShell → Run as Administrator" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Test noteerr in current session:" -ForegroundColor Cyan
$env:Path += ";$scriptsPath"
& "$scriptsPath\noteerr.exe" --version

Write-Host ""
Write-Host "For shell integration, see:" -ForegroundColor Cyan
Write-Host "  WINDOWS_SETUP.md" -ForegroundColor White
