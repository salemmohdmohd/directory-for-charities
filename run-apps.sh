
#!/bin/bash
# Script to run both backend (Flask) and frontend (React/Vite) servers
# Supports macOS and Windows (via Git Bash or WSL)

detect_os() {
	case "$(uname -s)" in
		Darwin)
			echo "macos"
			;;
		MINGW*|MSYS*|CYGWIN*)
			echo "windows"
			;;
		*)
			echo "unsupported"
			;;
	esac
}

OS=$(detect_os)

if [ "$OS" = "macos" ]; then
	echo "Running on macOS..."

	# Activate root virtual environment first
	if [ -f ".venv/bin/activate" ]; then
		source .venv/bin/activate
	else
		echo "Virtual environment not found at .venv/bin/activate in root folder."
		exit 1
	fi

	# Start backend using Flask CLI
	export FLASK_APP=backend/app
	export FLASK_ENV=development
	flask run --host=0.0.0.0 --port=3000 &
	BACKEND_PID=$!

	# Start frontend
	cd frontend
	npm run dev &
	FRONTEND_PID=$!
	cd ..

	trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
	wait $BACKEND_PID $FRONTEND_PID
elif [ "$OS" = "windows" ]; then
	echo "Running on Windows..."
	start "Backend" bash -c "cd backend && source .venv/Scripts/activate && python app.py"
	start "Frontend" bash -c "cd frontend && npm run dev"
	echo "Servers started in separate windows. Press Ctrl+C to exit."
else
	echo "Unsupported OS. This script only supports macOS and Windows."
	exit 1
fi
