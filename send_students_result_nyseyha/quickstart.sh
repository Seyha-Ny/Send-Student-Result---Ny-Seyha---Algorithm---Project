#!/bin/bash

# Quick Start Script for Send Student Result System (macOS/Linux)

echo ""
echo "========================================"
echo "Send Student Result System - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo ""
echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[3/5] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[4/5] Checking for .env file..."
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env file with your email configuration!"
    echo "Open .env and update:"
    echo "  - MAIL_USERNAME"
    echo "  - MAIL_PASSWORD"
    echo "  - MAIL_DEFAULT_SENDER"
    echo ""
    read -p "Press Enter to continue..."
fi

echo ""
echo "[5/5] Starting application..."
echo ""
echo "========================================"
echo "Application is starting..."
echo "Open your browser to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

python app.py

