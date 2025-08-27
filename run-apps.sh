
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
		Linux*)
			echo "linux"
			;;
		*)
			echo "unsupported"
			;;
	esac
}

OS=$(detect_os)

if [ "$OS" = "macos" ] || [ "$OS" = "linux" ]; then
	echo "Running on $OS..."

	# Activate root virtual environment first
	if [ -f ".venv/bin/activate" ]; then
		source .venv/bin/activate
		echo " Virtual environment activated"
	else
		echo " Virtual environment not found at .venv/bin/activate in root folder."
		echo "Please run: python3 -m venv .venv"
		exit 1
	fi

	# Start backend using Python module (more reliable)
	echo " Starting Flask backend on port 5000..."
	cd backend
	export FLASK_APP=app
	export FLASK_ENV=development

	# Try Flask CLI first, fallback to Python module
	if command -v flask &> /dev/null; then
		flask run --host=0.0.0.0 --port=5000 &
	else
		python3 -m app.wsgi &
	fi
	BACKEND_PID=$!
	cd ..

	# Wait a moment for backend to start
	sleep 2

	# Start frontend
	echo "Starting React frontend..."
	cd frontend
	npm run dev &
	FRONTEND_PID=$!
	cd ..

	echo " Both servers started successfully!"
	echo " Frontend: http://localhost:5173"
	echo " Backend:  http://localhost:5000"
	echo " Admin:    http://localhost:5000/admin/"
	echo ""
	echo "Press Ctrl+C to stop both servers"

	# Handle cleanup on exit
	trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" EXIT INT TERM
	wait $BACKEND_PID $FRONTEND_PID

elif [ "$OS" = "windows" ]; then
	echo "Running on Windows..."

	# Start backend
	echo " Starting Flask backend..."
	start "Flask Backend" bash -c "cd backend && source .venv/Scripts/activate && export FLASK_APP=app && export FLASK_ENV=development && python -m app.wsgi"

	# Start frontend
	echo " Starting React frontend..."
	start "React Frontend" bash -c "cd frontend && npm run dev"

	echo " Servers started in separate windows!"
	echo " Frontend: http://localhost:5173"
	echo " Backend:  http://localhost:5000"
	echo " Admin:    http://localhost:5000/admin/"
	echo ""
	echo "Press Ctrl+C to exit this script (servers will continue running)."
	echo "Press Ctrl+C to exit this script (servers will continue running)."

	# Keep script running
	read -p "Press Enter to exit..."

else
	echo " Unsupported OS. This script supports macOS, Linux, and Windows."
	exit 1
fi
