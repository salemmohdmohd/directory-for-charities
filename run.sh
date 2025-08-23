#!/bin/bash
# Cross-platform run script for Flask app

# Detect OS and activate virtual environment
if [[ "$OSTYPE" == "darwin"* ]]; then
    source .venv/bin/activate
elif [[ "$OSTYPE" == "linux"* ]]; then
    source .venv/bin/activate
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* ]]; then
    source .venv/Scripts/activate
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

# Run the Flask app
python src/app.py
