#!/bin/bash
# Noteerr Quick Installer for macOS/Linux
# Run: bash install.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo "========================================"
echo "  Noteerr Quick Installer"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}[ERROR] Python is not installed!${NC}"
    echo ""
    echo "Please install Python 3.8+ from:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo ""
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "${GREEN}[OK] Found $PYTHON_VERSION${NC}"
echo ""

# Check if pip is available
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${RED}[ERROR] pip is not installed${NC}"
    echo "Install with: $PYTHON_CMD -m ensurepip --upgrade"
    exit 1
fi

echo -e "${GREEN}[OK] pip is available${NC}"
echo ""

# Install Noteerr
echo "Installing Noteerr..."
echo ""

$PYTHON_CMD -m pip install --user -e . --quiet --disable-pip-version-check

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERROR] Installation failed!${NC}"
    echo ""
    exit 1
fi

echo ""
echo -e "${GREEN}[OK] Noteerr installed successfully!${NC}"
echo ""

# Set up PATH
LOCAL_BIN="$HOME/.local/bin"

if [ -f "$LOCAL_BIN/noteerr" ]; then
    echo -e "${GREEN}[OK] Found noteerr at: $LOCAL_BIN/noteerr${NC}"
    echo ""
    
    # Check if already in PATH
    if [[ ":$PATH:" == *":$LOCAL_BIN:"* ]]; then
        echo -e "${GREEN}[OK] $LOCAL_BIN is already in PATH${NC}"
    else
        echo -e "${YELLOW}[INFO] Adding $LOCAL_BIN to PATH${NC}"
        echo ""
        
        # Detect shell
        if [ -n "$BASH_VERSION" ]; then
            SHELL_RC="$HOME/.bashrc"
        elif [ -n "$ZSH_VERSION" ]; then
            SHELL_RC="$HOME/.zshrc"
        else
            # Try to detect from SHELL env var
            case "$SHELL" in
                */bash)
                    SHELL_RC="$HOME/.bashrc"
                    ;;
                */zsh)
                    SHELL_RC="$HOME/.zshrc"
                    ;;
                *)
                    SHELL_RC="$HOME/.profile"
                    ;;
            esac
        fi
        
        # Add to shell config if not already there
        if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$SHELL_RC" 2>/dev/null; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
            echo -e "${GREEN}[OK] Added to $SHELL_RC${NC}"
            echo ""
            echo -e "${YELLOW}Run: source $SHELL_RC${NC}"
            echo "Or close and reopen your terminal"
        fi
    fi
else
    echo -e "${YELLOW}[WARNING] Could not locate noteerr binary${NC}"
    echo "It might be installed at a different location"
fi

echo ""
echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo -e "${GREEN}SUCCESS! Noteerr is now installed.${NC}"
echo ""
echo "IMPORTANT: Close and reopen your terminal (or run: source $SHELL_RC)"
echo ""
echo "Then try:"
echo -e "  ${CYAN}noteerr --version${NC}"
echo -e "  ${CYAN}noteerr --help${NC}"
echo ""
echo "Quick start:"
echo -e "  ${CYAN}noteerr save \"your note\"${NC}"
echo -e "  ${CYAN}noteerr list${NC}"
echo -e "  ${CYAN}noteerr copy error latest${NC}"
echo ""
echo "For shell integration:"
echo -e "  ${CYAN}noteerr install --shell bash${NC}   # or zsh"
echo ""
echo "Read README.md for more examples!"
echo ""
