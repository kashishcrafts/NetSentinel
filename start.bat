@echo off
REM NetSentinel Setup and Run Script for Windows

echo ╔════════════════════════════════════════════════════╗
echo ║    NetSentinel - Setup and Launch                 ║
echo ╚════════════════════════════════════════════════════╝

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

echo ✓ Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt
echo ✓ Dependencies installed

REM Check if .env exists
if not exist ".env" (
    echo ⚙️  Creating .env from .env.example...
    copy .env.example .env
    echo ✓ .env created (please update with your configuration)
)

REM Initialize database
echo 🗄️  Initializing database...
python init_db.py
echo ✓ Database initialized

REM Start the application
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║    Starting NetSentinel API Server                ║
echo ╚════════════════════════════════════════════════════╝
echo.

python run.py

pause
