#!/bin/bash

# ContextKangz dependency installer 🦘
# Installs Tkinter system packages. Run with: bash install_deps.sh
# Note: Requires sudo for apt. On Windows, install Python with Tkinter option checked.

OS=$(uname -s)

if [ "$OS" = "Darwin" ]; then
    # macOS
    echo "Detected macOS. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Install it first: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    brew install python-tk
    echo "Done! Tkinter should be good. Run python ContextKang.py to test."
elif [ "$OS" = "Linux" ]; then
    # Linux (assuming Debian/Ubuntu; adjust for others)
    echo "Detected Linux. Installing via apt..."
    sudo apt update
    sudo apt install python3-tk -y
    echo "Done! Tkinter installed. Run python3 ContextKang.py to test."
else
    echo "Unsupported OS: $OS. For Windows, ensure Tkinter is included in your Python install."
    exit 1
fi