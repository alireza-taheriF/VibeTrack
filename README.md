# 🎯 VibeTrack

**AI-powered Git change analyzer** - Understand your code changes before pushing to GitHub!

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)

## ✨ Features

- 🔍 **Smart Analysis**: AI-powered change detection and explanation
- 🎭 **Staged Changes**: Analyze only staged changes ready for commit
- 📋 **All Changes**: Analyze all uncommitted modifications
- 🔄 **Commit Comparison**: Compare any two commits or branches
- 💾 **Auto Save**: Automatically save analysis reports
- 🎨 **Beautiful Output**: Rich, colorful terminal interface
- 🌍 **Multi-language**: Supports Python, JavaScript, TypeScript, Java, C++, and more

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/alireza-taheriF/VibeTrack.git
cd VibeTrack

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .

# Or install from PyPI (when available)
pip install vibetrack
```

### Basic Usage

```bash
# Analyze current changes before pushing
vibetrack check

# Analyze only staged changes
vibetrack check --staged

# Compare two commits
vibetrack compare HEAD~1 HEAD

# Compare branches
vibetrack compare main feature-branch

# Show Git status with insights
vibetrack status

# Get help
vibetrack --help
```

## 📖 Detailed Usage

### Main Commands

#### `vibetrack check` - Analyze Current Changes
This is the main command you'll use before pushing to GitHub. It analyzes your changes and explains what was modified and why.

```bash
# Analyze all uncommitted changes (default)
vibetrack check

# Analyze only staged changes
vibetrack check --staged

# Analyze all changes including unstaged
vibetrack check --all

# Compare with a specific commit
vibetrack check --commit abc123

# Don't save analysis to file
vibetrack check --no-save
```

#### `vibetrack compare` - Compare Commits/Branches
Compare any two commits, branches, or references.

```bash
# Compare two commits
vibetrack compare abc123 def456

# Compare with HEAD (default)
vibetrack compare abc123

# Compare branches
vibetrack compare main feature-branch

# Compare with previous commit
vibetrack compare HEAD~1 HEAD
```

#### `vibetrack status` - Enhanced Git Status
Show current Git status with VibeTrack insights.

```bash
vibetrack status
```

#### `vibetrack about` - Project Information
Show information about VibeTrack and usage examples.

```bash
vibetrack about
```

## 🛠️ Configuration

### AI Backend
VibeTrack uses a local LLM backend for analysis. Configure your AI service in the `vibetrack/local_client.py` file:

```python
API_URL = "http://your-ai-server:1234/v1/chat/completions"
```

### Supported File Types
VibeTrack automatically analyzes these file types:
- **Programming Languages**: `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.java`, `.cpp`, `.c`, `.h`, `.cs`, `.php`, `.rb`, `.go`, `.rs`, `.swift`, `.kt`, `.scala`
- **Configuration**: `.json`, `.yaml`, `.yml`, `.xml`
- **Web**: `.html`, `.css`, `.scss`, `.sass`, `.less`
- **Documentation**: `.md`, `.txt`

## 📁 Project Structure

```
VibeTrack/
├── vibetrack/
│   ├── __init__.py
│   ├── __main__.py          # Module entry point
│   ├── cli_en.py            # English CLI interface
│   ├── main.py              # Core analysis functions
│   ├── diff_utils.py        # Git diff utilities
│   ├── local_client.py      # AI backend client
│   ├── save_result.py       # Save analysis results
│   └── llm_analyzer.py      # LLM analysis logic
├── examples/                # Example files
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🎨 Beautiful Output

VibeTrack provides a rich, colorful terminal experience:

- 🎯 **Beautiful Banner**: Shows project info and author details
- 📋 **Syntax Highlighted Diffs**: Easy-to-read code differences
- 🧠 **AI Analysis Panels**: Clear explanations in bordered panels
- 🔍 **Progress Indicators**: Spinners and progress bars
- ✅ **Status Messages**: Color-coded success/error messages
- 💾 **File Saving**: Automatic markdown report generation

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/VibeTrack.git
cd VibeTrack

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 📝 Examples

### Before Pushing to GitHub

```bash
# Check what you're about to commit
git add .
vibetrack check --staged

# Review the AI analysis
# Make any necessary adjustments
# Then commit and push
git commit -m "Your commit message"
git push origin main
```

### Reviewing a Feature Branch

```bash
# Compare your feature branch with main
vibetrack compare main feature-branch

# Or compare with the last few commits
vibetrack compare HEAD~3 HEAD
```

### Understanding Recent Changes

```bash
# What changed in the last commit?
vibetrack compare HEAD~1 HEAD

# What's different from 2 commits ago?
vibetrack compare HEAD~2 HEAD
```

## 🔧 Requirements

- Python 3.8 or higher
- Git (for Git operations)
- Rich (for beautiful terminal output)
- Typer (for CLI interface)
- Requests (for AI backend communication)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Alireza Taheri Fakhr**
- 🔗 GitHub: [@alireza-taheriF](https://github.com/alireza-taheriF)
- 💼 LinkedIn: [Alireza Taheri](https://www.linkedin.com/in/alireza-taheri-a34179164/)

## 🙏 Acknowledgments

- Thanks to the open-source community for inspiration
- Built with ❤️ for developers who want to understand their code changes
- Special thanks to the Rich and Typer libraries for making beautiful CLIs possible

## 🚀 Future Plans

- [ ] Integration with popular Git hosting services
- [ ] Support for more file types
- [ ] Custom AI prompts and templates
- [ ] Team collaboration features
- [ ] VS Code extension
- [ ] GitHub Actions integration
- [ ] Commit message suggestions
- [ ] Code quality insights

---

**Made with ❤️ by developers, for developers**

*Use VibeTrack before every push to GitHub and never wonder "what did I change?" again!*