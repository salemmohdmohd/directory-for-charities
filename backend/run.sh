#!/bin/bash
# Script to activate venv and run the Flask backend
# Compatible with macOS/Linux (flask) and Windows (flask)

# Detect OS and set appropriate commands
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # macOS or Linux
    FLASK_CMD="flask"
    PYTHON_CMD="python3"
    echo "Detected macOS/Linux - using flask and python3"
else
    # Windows
    FLASK_CMD="flask"
    PYTHON_CMD="python"
    echo "Detected Windows - using flask and python"
fi

# Check if Flask is available
if ! command -v $FLASK_CMD &> /dev/null; then
    echo "Flask not found. Will use Python module instead."
    USE_PYTHON_MODULE=true
else
    USE_PYTHON_MODULE=false
fi

# Activate virtual environment
if [ -d "../.venv" ]; then
    echo "Activating virtual environment from ../.venv"
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        source ../.venv/Scripts/activate
    else
        source ../.venv/bin/activate
    fi
elif [ -d ".venv" ]; then
    echo "Activating virtual environment from .venv"
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi
else
    echo "Virtual environment not found. Please create one in .venv."
    exit 1
fi

# Run Flask app
echo "Starting Flask backend server..."

if [ "$USE_PYTHON_MODULE" = true ]; then
    # Use Python module approach
    echo "Using Python module to start Flask app"
    export FLASK_APP=app
    export FLASK_ENV=development
    $PYTHON_CMD -m app.wsgi
else
    # Use Flask CLI
    echo "Using Flask CLI to start app"
    export FLASK_APP=app
    export FLASK_ENV=development
    $FLASK_CMD run --host=0.0.0.0 --port=5000
fi
