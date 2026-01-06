#!/bin/bash
# Quick start script for Textbook Reading Assistant

echo "=========================================="
echo "教科书阅读助手 - Textbook Reading Assistant"
echo "=========================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $PYTHON_VERSION"

# Check if in correct directory
if [ ! -f "backend/app.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check for .env file
if [ ! -f "backend/.env" ]; then
    echo ""
    echo "⚠️  WARNING: .env file not found!"
    echo "Creating .env file from .env.example..."
    cp backend/.env.example backend/.env
    echo ""
    echo "📝 Please edit backend/.env and add your DeepSeek API key:"
    echo "   DEEPSEEK_API_KEY=your_api_key_here"
    echo ""
    read -p "Press Enter to continue (or Ctrl+C to exit and configure .env first)..."
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
cd backend
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
cd ..

echo "✅ Dependencies installed"

# Check for Tesseract (optional)
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract OCR is installed"
else
    echo "⚠️  Tesseract OCR not found (optional - needed for image text extraction)"
    echo "   Install on Ubuntu: sudo apt-get install tesseract-ocr"
    echo "   Install on macOS: brew install tesseract"
fi

echo ""
echo "🚀 Starting application..."
echo "📍 Server will be available at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

# Start the application
cd backend
python3 -m backend.app
