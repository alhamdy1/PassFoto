#!/bin/bash
# PassFoto - Linux/Mac Startup Script

echo "========================================"
echo "   PassFoto - Passport Photo Enhancer"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.7+ from https://www.python.org/downloads/"
    exit 1
fi

echo "Checking dependencies..."

# Check if dependencies are installed
python3 -c "import cv2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies."
        exit 1
    fi
fi

echo "Starting PassFoto..."
echo

python3 main.py
