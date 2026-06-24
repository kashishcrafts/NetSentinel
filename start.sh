#!/bin/bash
# NetSentinel Setup and Run Script

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║    NetSentinel - Setup and Launch                 ║"
echo "╚════════════════════════════════════════════════════╝"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ .env created (please update with your configuration)"
fi

# Initialize database
echo "🗄️  Initializing database..."
python init_db.py
echo "✓ Database initialized"

# Start the application
echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║    Starting NetSentinel API Server                ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

python run.py
