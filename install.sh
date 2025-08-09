#!/bin/bash

# VibeTrack Installation Script
# This script installs VibeTrack CLI tool

set -e

echo "🎯 Installing VibeTrack..."

# Check if Python 3.8+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install VibeTrack in development mode
echo "🚀 Installing VibeTrack..."
pip install -e .

echo ""
echo "✅ VibeTrack installed successfully!"
echo ""
echo "🎉 You can now use VibeTrack with the following commands:"
echo "   vibetrack --help          # Show help"
echo "   vibetrack about           # Show project info"
echo "   vibetrack check           # Analyze current changes"
echo "   vibetrack status          # Show Git status"
echo ""
echo "💡 Make sure to activate the virtual environment before using:"
echo "   source venv/bin/activate"
echo ""
echo "🚀 Happy coding with VibeTrack!"