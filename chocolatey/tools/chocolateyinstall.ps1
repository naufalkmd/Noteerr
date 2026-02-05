$ErrorActionPreference = 'Stop'

$packageName = 'noteerr'
$toolsDir = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"

# Check if Python is installed
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonCmd) {
    Write-Error "Python is not installed. Please install Python 3.8+ first."
    throw "Python is required for Noteerr"
}

# Get Python version
$pythonVersion = (python --version 2>&1) -replace 'Python ', ''
$pythonMajor = [int]($pythonVersion.Split('.')[0])
$pythonMinor = [int]($pythonVersion.Split('.')[1])

if ($pythonMajor -lt 3 -or ($pythonMajor -eq 3 -and $pythonMinor -lt 8)) {
    Write-Error "Python 3.8+ is required. Found version: $pythonVersion"
    throw "Incompatible Python version"
}

Write-Host "Found Python $pythonVersion" -ForegroundColor Green

# Install noteerr using pip
Write-Host "Installing Noteerr..." -ForegroundColor Cyan
python -m pip install --user noteerr --quiet --disable-pip-version-check

if ($LASTEXITCODE -ne 0) {
    throw "Failed to install Noteerr"
}

Write-Host "Noteerr installed successfully!" -ForegroundColor Green

# Add Python Scripts to PATH
$pythonVersionNum = "$pythonMajor$pythonMinor"
$scriptsPath = Join-Path $env:APPDATA "Python\Python$pythonVersionNum\Scripts"

if (Test-Path "$scriptsPath\noteerr.exe") {
    Write-Host "Found noteerr at: $scriptsPath" -ForegroundColor Green
    
    # Add to user PATH if not already there
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    if ($currentPath -notlike "*$scriptsPath*") {
        Write-Host "Adding to PATH..." -ForegroundColor Cyan
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$scriptsPath", "User")
        $env:Path = "$env:Path;$scriptsPath"
        Write-Host "PATH updated successfully!" -ForegroundColor Green
    } else {
        Write-Host "Already in PATH" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "Please restart your terminal to use noteerr" -ForegroundColor Yellow
Write-Host ""
Write-Host "Try: noteerr --version" -ForegroundColor Cyan
