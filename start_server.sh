#!/bin/bash
set -e  # Exit immediately if any command fails

echo "🚀 Starting Flask application with Gunicorn..."

# Ensure virtual environment is activated
source venv/bin/activate

# Check if port 5000 is already in use and kill the existing process
PORT=5000
PID=$(lsof -ti :$PORT)
if [ ! -z "$PID" ]; then
    echo "⚠️ Port $PORT is already in use. Killing process $PID..."
    kill -9 $PID
fi

# Start Gunicorn with 4 workers
gunicorn --reload -w 4 -b 0.0.0.0:5000 run:app

echo "✅ Flask app is running on http://127.0.0.1:5000/"
