#!/bin/bash

echo "============================================"
echo "  Headline AI - Web Interface"
echo "============================================"
echo ""

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

# Create necessary directories
mkdir -p output temp_images static/css static/js templates

echo ""
echo "============================================"
echo "  Starting Web Server..."
echo "============================================"
echo ""
echo "  Open your browser and go to:"
echo "  http://localhost:5000"
echo ""
echo "  Press Ctrl+C to stop the server"
echo ""

# Run the app
python app.py
