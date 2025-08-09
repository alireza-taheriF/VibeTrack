# 🎯 VibeTrack Installation Guide

## 📋 Prerequisites

- **Python 3.8+** (required)
- **Git** (for Git operations)
- **Terminal/Command Line** access

## 🚀 Quick Installation

### Option 1: Automatic Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/alireza-taheriF/vibetrack.git
cd vibetrack

# Run the installation script
./install.sh
```

### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/alireza-taheriF/vibetrack.git
cd vibetrack

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install VibeTrack
pip install -e .
```

### Option 3: From PyPI (Future)

```bash
# This will be available once published to PyPI
pip install vibetrack
```

## ✅ Verify Installation

```bash
# Activate virtual environment (if using manual installation)
source venv/bin/activate

# Test the installation
vibetrack --help
vibetrack about

# Run the demo
python3 demo.py
```

## 🎯 First Usage

```bash
# Navigate to any Git repository
cd /path/to/your/git/project

# Activate VibeTrack environment
source /path/to/vibetrack/venv/bin/activate

# Use VibeTrack
vibetrack check          # Analyze current changes
vibetrack status         # Show Git status
vibetrack about          # Show help and examples
```

## 🔧 Configuration

### AI Backend Setup

VibeTrack requires an AI backend for analysis. Configure your AI service in:
```
vibetrack/local_client.py
```

Supported backends:
- Local LLM servers (Ollama, LM Studio, etc.)
- OpenAI API
- Custom AI endpoints

### Environment Variables (Optional)

```bash
# Set custom AI endpoint
export VIBETRACK_AI_ENDPOINT="http://localhost:11434"

# Set API key (if needed)
export VIBETRACK_API_KEY="your-api-key"
```

## 🚨 Troubleshooting

### Common Issues

**Python version error:**
```bash
# Check Python version
python3 --version

# Install Python 3.8+ if needed
# macOS: brew install python@3.9
# Ubuntu: sudo apt install python3.9
# Windows: Download from python.org
```

**Permission denied on install.sh:**
```bash
chmod +x install.sh
./install.sh
```

**Virtual environment issues:**
```bash
# Remove and recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

**Git not found:**
```bash
# Install Git
# macOS: brew install git
# Ubuntu: sudo apt install git
# Windows: Download from git-scm.com
```

### Getting Help

```bash
# Show help
vibetrack --help

# Show command-specific help
vibetrack check --help
vibetrack compare --help

# Run demo to test functionality
python3 demo.py
```

## 🔄 Updating VibeTrack

```bash
# Navigate to VibeTrack directory
cd /path/to/vibetrack

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install --upgrade -r requirements.txt

# Reinstall VibeTrack
pip install -e .
```

## 🗑️ Uninstallation

```bash
# Remove the VibeTrack directory
rm -rf /path/to/vibetrack

# Or if installed via pip
pip uninstall vibetrack
```

## 🌍 Global Installation (Advanced)

To use VibeTrack from anywhere without activating virtual environment:

```bash
# Install globally (not recommended for development)
pip install --user -e .

# Or create a symlink
ln -s /path/to/vibetrack/venv/bin/vibetrack /usr/local/bin/vibetrack
```

## 📱 IDE Integration

### VS Code

Add to your VS Code settings:
```json
{
    "terminal.integrated.shellArgs.osx": [
        "-c",
        "source /path/to/vibetrack/venv/bin/activate && exec zsh"
    ]
}
```

### Terminal Aliases

Add to your shell profile (`.bashrc`, `.zshrc`, etc.):
```bash
alias vt="source /path/to/vibetrack/venv/bin/activate && vibetrack"
alias vibetrack-check="source /path/to/vibetrack/venv/bin/activate && vibetrack check"
```

## 🎉 You're Ready!

VibeTrack is now installed and ready to use. Check out the [Usage Guide](USAGE.md) for detailed examples and workflows.

**Happy coding with VibeTrack! 🚀**