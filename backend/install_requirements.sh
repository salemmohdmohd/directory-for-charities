#!/bin/bash
# Script to install Python packages from requirements.txt
# Compatible with macOS/Linux (pip3) and Windows (pip)

# Detect OS and set appropriate commands
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # macOS or Linux - use pip3 and python3
    PIP_CMD="pip3"
    PYTHON_CMD="python3"
    echo "Detected macOS/Linux - using pip3 and python3"
else
    # Windows or other - use pip and python
    PIP_CMD="pip"
    PYTHON_CMD="python"
    echo "Detected Windows/Other - using pip and python"
fi

# Check if commands exist
if ! command -v $PIP_CMD &> /dev/null; then
    echo "Error: $PIP_CMD not found. Please install Python first."
    exit 1
fi

if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "Error: $PYTHON_CMD not found. Please install Python first."
    exit 1
fi

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "../.venv" ]; then
        echo "Activating virtual environment from ../.venv"
        source ../.venv/bin/activate
    elif [ -d ".venv" ]; then
        echo "Activating virtual environment from .venv"
        source .venv/bin/activate
    else
        echo "Virtual environment not found. Creating one..."
        $PYTHON_CMD -m venv .venv
        if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
            # Windows
            source .venv/Scripts/activate
        else
            # macOS/Linux
            source .venv/bin/activate
        fi
    fi
fi

# Install requirements
echo "Upgrading pip..."
$PIP_CMD install --upgrade pip

echo "Installing requirements from requirements.txt..."
if [ -f "requirements.txt" ]; then
    $PIP_CMD install -r requirements.txt
elif [ -f "backend/requirements.txt" ]; then
    $PIP_CMD install -r backend/requirements.txt
else
    echo "Error: requirements.txt not found in current directory or backend/ directory"
    exit 1
fi

echo "✅ Requirements installed successfully!"
