# VibeTrack 🎵

VibeTrack is a powerful CLI tool and VS Code extension that provides AI-powered code diff analysis. It helps developers understand code changes more easily by generating human-readable explanations of git diffs.

## Features 🚀

- Analyze git diffs between any two commits
- Generate human-readable explanations using AI
- Save analysis results in markdown format
- Beautiful CLI interface with rich formatting
- VS Code extension integration
- Git hook support for automatic analysis

## Installation 📦

```bash
# Install from PyPI
pip install vibetrack

# Or install from source
git clone https://github.com/alireza-taheriF/vibetrack
cd vibetrack
pip install -e .
```

## Usage 💻

### CLI Usage

```bash
# Analyze diff between two git commits
vibetrack analyze abc123 def456

# Analyze diff between previous commit and HEAD
vibetrack analyze HEAD~1 HEAD
```

### Git Hook Integration

To automatically analyze diffs after each commit:

```bash
python install_hook.py
```

This will install a post-commit hook that runs VibeTrack analysis automatically.

## How It Works 🔧

1. VibeTrack generates a diff between two code versions using either:
   - Git diff between commits
   - Direct file comparison
2. The diff is sent to an AI model for analysis
3. The AI provides a human-readable explanation of:
   - What exactly changed
   - Why it was changed
   - The difference in behavior
4. Results are saved as markdown files in the `history/` directory

## Configuration ⚙️

The tool supports various file extensions for analysis:
- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- JSX/TSX (.jsx, .tsx)

## Dependencies 📚

- typer: CLI interface
- requests: API communication
- rich: Terminal formatting

## Development 🛠️

```bash
# Clone the repository
git clone https://github.com/alireza-taheriF/vibetrack

# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## Author ✍️

**Alireza Taheri Fakhr**
- GitHub: [alireza-taheriF](https://github.com/alireza-taheriF)
- LinkedIn: [Alireza Taheri](https://www.linkedin.com/in/alireza-taheri-a34179164/)

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Version 📌

Current version: 0.1.0