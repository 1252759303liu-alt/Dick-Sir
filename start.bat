@echo off
REM Quick start script for Textbook Reading Assistant (Windows)

echo ==========================================
echo 教科书阅读助手 - Textbook Reading Assistant
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Check if in correct directory
if not exist "backend\app.py" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check for .env file
if not exist "backend\.env" (
    echo.
    echo ⚠️  WARNING: .env file not found!
    echo Creating .env file from .env.example...
    copy backend\.env.example backend\.env
    echo.
    echo 📝 Please edit backend\.env and add your DeepSeek API key:
    echo    DEEPSEEK_API_KEY=your_api_key_here
    echo.
    pause
)

REM Install dependencies
echo.
echo 📦 Installing dependencies...
cd backend
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
cd ..

echo ✅ Dependencies installed

echo.
echo 🚀 Starting application...
echo 📍 Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
echo ==========================================
echo.

REM Start the application
cd backend
python -m backend.app
