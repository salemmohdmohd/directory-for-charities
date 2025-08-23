#!/bin/bash
# Script to activate venv and run the Flask backend

# Activate virtual environment
if [ -d "../.venv" ]; then
    source ../.venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Virtual environment not found. Please create one in .venv."
    exit 1
fi

# Run Flask app using Flask CLI
export FLASK_APP=backend/app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=3000
