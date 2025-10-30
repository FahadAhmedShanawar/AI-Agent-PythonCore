#!/bin/bash

# Event Planner Agent Local Runner

echo "Setting up Event Planner Agent..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Copy .env.example and configure API keys."
fi

# Run the application
echo "Starting Event Planner Agent..."
python -m app.main
