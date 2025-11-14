#!/bin/bash

# Roamy - AI Travel Planner Runner Script

echo "✈️  Roamy - AI Travel Planner"
echo "============================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your OPENAI_API_KEY"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the app
echo ""
echo "🚀 Starting Roamy..."
echo "Open your browser to the URL shown below"
echo ""
streamlit run app.py

