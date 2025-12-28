#!/bin/bash

# RansomSim Setup Script
# This script sets up the RansomSim application

echo "================================"
echo "RansomSim Setup"
echo "================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p uploads
mkdir -p generated_files
mkdir -p templates
mkdir -p static/css
mkdir -p static/js

echo ""
echo "================================"
echo "✓ Setup Complete!"
echo "================================"
echo ""
echo "To start the application, run:"
echo "  source venv/bin/activate"
echo "  python3 app.py"
echo ""
echo "Then open http://localhost:5000 in your browser"
echo ""
