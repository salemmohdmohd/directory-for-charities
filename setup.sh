#!/usr/bin/env sh
set -e

# Cross-platform POSIX setup for local dev (macOS / Linux)
# - creates a virtualenv in .venv (if not present)
# - installs pinned requirements from requirements.txt
# - runs migrations (if Flask-Migrate is configured)
# - starts the Flask dev server on 0.0.0.0:3000

if [ -z "${VIRTUAL_ENV}" ]; then
	if [ ! -d ".venv" ]; then
		echo "Creating virtualenv in .venv..."
		if command -v python3 >/dev/null 2>&1; then
			python3 -m venv .venv
		else
			python -m venv .venv
		fi
	fi
	# shellcheck disable=SC1091
	. .venv/bin/activate
fi

export FLASK_APP=${FLASK_APP:-src/app.py}
export FLASK_ENV=${FLASK_ENV:-development}

echo "Upgrading pip and installing requirements..."
pip install --upgrade pip
if [ -f requirements.txt ]; then
	pip install --no-cache-dir -r requirements.txt
else
	echo "requirements.txt not found — falling back to install editable project (may fail)"
fi

echo "Running database migrations (if any)..."
# run migrations but don't fail if there are no changes
if command -v flask >/dev/null 2>&1; then
	flask db migrate || true
	flask db upgrade || true
else
	echo "flask CLI not available; ensure Flask is installed in the venv"
fi

echo "Starting Flask development server at http://0.0.0.0:3000"
flask run --host=0.0.0.0 --port=3000
