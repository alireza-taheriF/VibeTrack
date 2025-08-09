# 🎯 VibeTrack Usage Guide

This guide shows you how to use VibeTrack to analyze your Git changes before pushing to GitHub.

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/alireza-taheriF/vibetrack.git
cd vibetrack

# Run the installation script
./install.sh

# Or install manually
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 2. Basic Usage

```bash
# Activate the virtual environment (if not already active)
source venv/bin/activate

# Show help
vibetrack --help

# Show project information
vibetrack about
```

## 📋 Main Commands

### `vibetrack check` - Analyze Current Changes

This is the main command you'll use before pushing to GitHub:

```bash
# Analyze all uncommitted changes (default behavior)
vibetrack check

# Analyze only staged changes (ready for commit)
vibetrack check --staged

# Analyze all changes including unstaged files
vibetrack check --all

# Compare with a specific commit
vibetrack check --commit abc123

# Don't save the analysis to a file
vibetrack check --no-save
```

### `vibetrack compare` - Compare Commits/Branches

Compare any two commits, branches, or Git references:

```bash
# Compare two specific commits
vibetrack compare abc123 def456

# Compare with HEAD (default second argument)
vibetrack compare abc123

# Compare branches
vibetrack compare main feature-branch

# Compare with previous commits
vibetrack compare HEAD~1 HEAD
vibetrack compare HEAD~3 HEAD~1

# Don't save the analysis
vibetrack compare main feature-branch --no-save
```

### `vibetrack status` - Enhanced Git Status

Show current Git status with VibeTrack insights:

```bash
vibetrack status
```

### `vibetrack about` - Project Information

Show information about VibeTrack and usage examples:

```bash
vibetrack about
```

## 🎯 Real-World Workflow Examples

### Before Committing Changes

```bash
# 1. Make your code changes
echo "print('Hello, VibeTrack!')" > hello.py

# 2. Stage your changes
git add hello.py

# 3. Analyze staged changes before committing
vibetrack check --staged

# 4. Review the AI analysis, then commit
git commit -m "Add hello world script"
```

### Before Pushing to GitHub

```bash
# 1. Check what you're about to push
vibetrack compare origin/main HEAD

# 2. Review the analysis
# 3. Push with confidence
git push origin main
```

### Reviewing a Pull Request

```bash
# Compare your feature branch with main
vibetrack compare main feature/new-feature

# Or compare specific commits
vibetrack compare abc123 def456
```

### Understanding Recent Changes

```bash
# What changed in the last commit?
vibetrack compare HEAD~1 HEAD

# What's different from 3 commits ago?
vibetrack compare HEAD~3 HEAD

# Compare with a specific tag
vibetrack compare v1.0.0 HEAD
```

## 🎨 Output Examples

### Beautiful Terminal Output

VibeTrack provides rich, colorful output:

- **🎯 Banner**: Shows project info and author details
- **📋 Syntax Highlighted Diffs**: Easy-to-read code differences
- **🧠 AI Analysis Panels**: Clear explanations in bordered panels
- **🔍 Progress Indicators**: Spinners while analyzing
- **✅ Status Messages**: Color-coded success/error messages

### Saved Analysis Files

VibeTrack automatically saves analysis to markdown files in the `history/` directory:

```
history/
├── analysis_2024-01-15_14-30-25.md
├── analysis_2024-01-15_15-45-10.md
└── analysis_2024-01-15_16-20-33.md
```

Each file contains:
- Original diff
- AI analysis and explanation
- Timestamp and commit information
- Formatted for easy reading

## 🔧 Configuration

### Supported File Types

VibeTrack automatically analyzes these file types:

**Programming Languages:**
- Python (`.py`)
- JavaScript (`.js`, `.jsx`)
- TypeScript (`.ts`, `.tsx`)
- Java (`.java`)
- C/C++ (`.c`, `.cpp`, `.h`)
- C# (`.cs`)
- PHP (`.php`)
- Ruby (`.rb`)
- Go (`.go`)
- Rust (`.rs`)
- Swift (`.swift`)
- Kotlin (`.kt`)
- Scala (`.scala`)

**Configuration & Data:**
- JSON (`.json`)
- YAML (`.yaml`, `.yml`)
- XML (`.xml`)

**Web Technologies:**
- HTML (`.html`)
- CSS (`.css`)
- SCSS (`.scss`)
- Sass (`.sass`)
- Less (`.less`)

**Documentation:**
- Markdown (`.md`)
- Text (`.txt`)

### AI Backend Configuration

VibeTrack uses a local LLM backend. Make sure you have your AI service configured in `vibetrack/local_client.py`.

## 🚨 Troubleshooting

### Common Issues

**"Not a Git repository" error:**
```bash
# Make sure you're in a Git repository
git init  # If starting a new project
cd /path/to/your/git/repo  # Or navigate to existing repo
```

**"No changes found" message:**
```bash
# Make sure you have uncommitted changes
git status  # Check current status
echo "test" > test.txt  # Make a test change
git add test.txt  # Stage the change
vibetrack check --staged  # Analyze staged changes
```

**Virtual environment issues:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall if needed
pip install -e .
```

### Getting Help

```bash
# Show general help
vibetrack --help

# Show help for specific commands
vibetrack check --help
vibetrack compare --help
```

## 🎉 Tips for Best Results

1. **Use before every push**: Make it a habit to run `vibetrack check` before pushing to GitHub
2. **Review staged changes**: Use `--staged` flag to analyze only what you're about to commit
3. **Compare branches**: Use `compare` to understand differences between branches
4. **Save analyses**: Keep the auto-saved markdown files for future reference
5. **Read AI explanations**: The AI provides valuable insights about your changes

## 🤝 Contributing

Want to improve VibeTrack? Check out our [Contributing Guide](README.md#contributing) in the main README.

---

**Happy coding with VibeTrack! 🚀**