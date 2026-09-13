#!/bin/bash

# ebot Flask API Startup Script

echo "Starting ebot Flask API..."
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create logs directory if it doesn't exist
if [ ! -d "logs" ]; then
    mkdir logs
fi

# Start the Flask app
echo "Starting Flask application..."
echo "API will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "================================"

cd ebot_app
python app.py
