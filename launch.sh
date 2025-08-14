#!/bin/bash

# Seq80x25 Launcher Script
# This script launches the retro music sequencer

echo "Seq80x25 - Retro Music Sequencer"
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python $REQUIRED_VERSION or higher is required"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Check if dependencies are installed
echo "Checking dependencies..."

# Check if virtual environment exists
if [ -d "venv" ] || [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        source .venv/bin/activate
    fi
fi

# Check required packages
MISSING_DEPS=()
for package in textual pygame numpy; do
    if ! python3 -c "import $package" &> /dev/null; then
        MISSING_DEPS+=("$package")
    fi
done

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "Missing dependencies: ${MISSING_DEPS[*]}"
    echo "Installing dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
    else
        pip3 install textual pygame numpy
    fi
    
    # Check again
    for package in "${MISSING_DEPS[@]}"; do
        if ! python3 -c "import $package" &> /dev/null; then
            echo "Error: Failed to install $package"
            exit 1
        fi
    done
fi

echo "Dependencies OK"
echo "Launching Seq80x25..."

# Launch the sequencer
python3 seq80x25.py

echo "Seq80x25 closed"
