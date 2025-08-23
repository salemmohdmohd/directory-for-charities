#!/bin/bash
# Script to install Python packages from requirements.txt

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "../.venv" ]; then
        source ../.venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        echo "Virtual environment not found. Please create one in .venv."
        exit 1
    fi
fi

# Install requirements
pip install --upgrade pip
pip install -r backend/requirements.txt
