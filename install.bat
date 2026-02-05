@echo off
REM Noteerr Quick Installer for Windows
REM Double-click this file to install Noteerr

title Noteerr Installer
color 0B

echo.
echo ========================================
echo    Noteerr Quick Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Install Noteerr
echo Installing Noteerr...
echo.
python -m pip install --user -e . --quiet --disable-pip-version-check

if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] Installation failed!
    echo.
    echo Try running as administrator or check your internet connection.
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Noteerr installed successfully!
echo.

REM Fix PATH automatically
echo Setting up PATH...
echo.

REM Get Python Scripts directory
for /f "delims=" %%i in ('python -c "import sys, os; print(os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Python', 'Python' + str(sys.version_info.major) + str(sys.version_info.minor), 'Scripts'))"') do set SCRIPTS_DIR=%%i

REM Check if noteerr.exe exists
if not exist "%SCRIPTS_DIR%\noteerr.exe" (
    REM Try alternate location
    for /f "delims=" %%i in ('python -c "import sys, os; print(os.path.join(sys.prefix, 'Scripts'))"') do set SCRIPTS_DIR=%%i
)

if exist "%SCRIPTS_DIR%\noteerr.exe" (
    echo Found noteerr at: %SCRIPTS_DIR%
    echo.
    
    REM Add to PATH using PowerShell
    powershell -NoProfile -Command "$currentPath = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($currentPath -notlike '*%SCRIPTS_DIR%*') { [Environment]::SetEnvironmentVariable('Path', $currentPath + ';%SCRIPTS_DIR%', 'User'); Write-Output 'PATH_UPDATED' } else { Write-Output 'PATH_EXISTS' }" > %TEMP%\noteerr_path.txt
    
    findstr /C:"PATH_UPDATED" %TEMP%\noteerr_path.txt >nul
    if not errorlevel 1 (
        echo [OK] Added to PATH successfully!
    ) else (
        echo [OK] Already in PATH
    )
    
    del %TEMP%\noteerr_path.txt >nul 2>&1
) else (
    color 0E
    echo [WARNING] Could not locate noteerr.exe
)

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
color 0A
echo SUCCESS! Noteerr is now installed.
echo.
echo IMPORTANT: Close this window and open a NEW terminal window
echo.
echo Then try:
echo   noteerr --version
echo   noteerr --help
echo.
echo Quick start:
echo   noteerr save "your note"
echo   noteerr list
echo   noteerr copy error latest
echo.
echo For shell integration:
echo   noteerr install --shell powershell
echo.
echo Read README.md for more examples!
echo.
pause
