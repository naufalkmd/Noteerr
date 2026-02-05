# Noteerr Installation Script for Windows
# Run this script to install Noteerr and set up PATH automatically

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Noteerr Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonCmd) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.8+ from:" -ForegroundColor Yellow
    Write-Host "  https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    exit 1
}

# Check Python version
$pythonVersion = (python --version 2>&1) -replace 'Python ', ''
Write-Host "Found Python: $pythonVersion" -ForegroundColor Green

# Check if pip is available
$pipCmd = Get-Command pip -ErrorAction SilentlyContinue

if (-not $pipCmd) {
    Write-Host "ERROR: pip is not installed" -ForegroundColor Red
    Write-Host "Install pip with: python -m ensurepip --upgrade" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found pip" -ForegroundColor Green
Write-Host ""

# Ask for installation type
Write-Host "Installation Options:" -ForegroundColor Cyan
Write-Host "  1. Install from PyPI (recommended - when available)"
Write-Host "  2. Install from source (development mode)"
Write-Host ""

$choice = Read-Host "Choose installation type [1/2] (default: 2)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "Installing Noteerr from PyPI..." -ForegroundColor Cyan
    python -m pip install --user noteerr
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERROR: Installation failed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "Installing Noteerr from source..." -ForegroundColor Cyan
    
    # Check if setup.py exists
    if (-not (Test-Path "setup.py")) {
        Write-Host "ERROR: setup.py not found" -ForegroundColor Red
        Write-Host "Make sure you're running this script from the Noteerr directory" -ForegroundColor Yellow
        exit 1
    }
    
    python -m pip install --user -e .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERROR: Installation failed" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Installation completed!" -ForegroundColor Green
Write-Host ""

# Check if noteerr is in PATH
$noteerrCmd = Get-Command noteerr -ErrorAction SilentlyContinue

if ($noteerrCmd) {
    Write-Host "SUCCESS: noteerr is already in your PATH!" -ForegroundColor Green
    Write-Host ""
    noteerr --version
} else {
    Write-Host "Setting up PATH..." -ForegroundColor Cyan
    Write-Host ""
    
    # Find Python Scripts directory
    $pythonVersion = python -c "import sys; print(f'{sys.version_info.major}{sys.version_info.minor}')"
    $scriptsPath = Join-Path $env:APPDATA "Python\Python$pythonVersion\Scripts"
    
    # Also check sys.prefix\Scripts
    $sysPrefixScripts = python -c "import sys; print(sys.prefix + '\\Scripts')"
    
    # Check which one has noteerr.exe
    $noteerrPath = $null
    
    if (Test-Path "$scriptsPath\noteerr.exe") {
        $noteerrPath = $scriptsPath
    } elseif (Test-Path "$sysPrefixScripts\noteerr.exe") {
        $noteerrPath = $sysPrefixScripts
    }
    
    if ($noteerrPath) {
        Write-Host "Found noteerr at: $noteerrPath" -ForegroundColor Green
        Write-Host ""
        
        # Check if already in PATH
        $currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
        
        if ($currentUserPath -like "*$noteerrPath*") {
            Write-Host "PATH already contains the Scripts directory" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "IMPORTANT: Please close and reopen your terminal," -ForegroundColor Yellow
            Write-Host "then run: noteerr --version" -ForegroundColor Cyan
        } else {
            # Add to PATH
            Write-Host "Adding to PATH..." -ForegroundColor Cyan
            [Environment]::SetEnvironmentVariable("Path", "$currentUserPath;$noteerrPath", "User")
            
            Write-Host ""
            Write-Host "SUCCESS: PATH updated!" -ForegroundColor Green
            Write-Host ""
            Write-Host "IMPORTANT: Please close and reopen your terminal," -ForegroundColor Yellow
            Write-Host "then run: noteerr --version" -ForegroundColor Cyan
        }
    } else {
        Write-Host "WARNING: Could not locate noteerr.exe" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Try running: noteerr install --check-path" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Close and reopen your terminal"
Write-Host "  2. Verify: noteerr --version"
Write-Host "  3. Try: noteerr --help"
Write-Host "  4. Read: README.md for usage examples"
Write-Host ""
Write-Host "For shell integration (auto-capture errors):" -ForegroundColor Cyan
Write-Host "  noteerr install --shell powershell"
Write-Host ""
