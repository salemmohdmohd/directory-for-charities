#!/bin/bash
# Simple Database Migration Script
# Usage: ./migrate.sh [init|migrate|upgrade|downgrade|reset]

# Detect OS and set appropriate commands
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PYTHON_CMD="python3"
    echo "Using python3 for macOS/Linux"
else
    PYTHON_CMD="python"
    echo "Using python for Windows"
fi

# Activate virtual environment
if [ -d "../.venv" ]; then
    echo "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        source ../.venv/Scripts/activate
    else
        source ../.venv/bin/activate
    fi
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi
else
    echo "Warning: Virtual environment not found"
fi

# Set Flask app
export FLASK_APP=app

# Function to show usage
show_usage() {
    echo "Usage: ./migrate.sh [command]"
    echo ""
    echo "Commands:"
    echo "  init      - Initialize migration repository"
    echo "  migrate   - Create new migration"
    echo "  upgrade   - Apply migrations to database"
    echo "  downgrade - Rollback last migration"
    echo "  reset     - Reset database (WARNING: deletes all data)"
    echo "  status    - Show migration status"
    echo ""
    echo "Examples:"
    echo "  ./migrate.sh init"
    echo "  ./migrate.sh migrate"
    echo "  ./migrate.sh upgrade"
}

# Check if Flask-Migrate is available
check_flask_migrate() {
    if ! $PYTHON_CMD -c "import flask_migrate" &> /dev/null; then
        echo "Error: Flask-Migrate not installed"
        echo "Install with: pip install Flask-Migrate"
        exit 1
    fi
}

# Main script logic
case "$1" in
    "init")
        echo "🚀 Initializing migration repository..."
        check_flask_migrate
        flask db init
        echo "✅ Migration repository initialized"
        ;;

    "migrate")
        echo "📝 Creating new migration..."
        check_flask_migrate

        # Ask for migration message
        if [ -z "$2" ]; then
            read -p "Enter migration message (or press Enter for auto): " message
        else
            message="$2"
        fi

        if [ -z "$message" ]; then
            flask db migrate
        else
            flask db migrate -m "$message"
        fi
        echo "✅ Migration created"
        ;;

    "upgrade")
        echo "⬆️  Applying migrations to database..."
        check_flask_migrate
        flask db upgrade
        echo "✅ Database upgraded"
        ;;

    "downgrade")
        echo "⬇️  Rolling back last migration..."
        check_flask_migrate
        read -p "Are you sure you want to rollback? (y/N): " confirm
        if [[ $confirm == [yY] ]]; then
            flask db downgrade
            echo "✅ Migration rolled back"
        else
            echo "❌ Rollback cancelled"
        fi
        ;;

    "reset")
        echo "🔥 DANGER: This will delete ALL data!"
        read -p "Type 'DELETE' to confirm database reset: " confirm
        if [[ $confirm == "DELETE" ]]; then
            echo "Removing database..."
            rm -f instance/example.db
            echo "Removing migrations..."
            rm -rf migrations/
            echo "Reinitializing..."
            flask db init
            flask db migrate -m "Initial migration"
            flask db upgrade
            echo "✅ Database reset complete"
        else
            echo "❌ Reset cancelled"
        fi
        ;;

    "status")
        echo "📊 Migration status..."
        check_flask_migrate
        flask db current
        flask db history
        ;;

    *)
        show_usage
        exit 1
        ;;
esac
