#!/usr/bin/env python3
"""
Demo script for VibeTrack CLI
This script demonstrates the main features of VibeTrack
"""

import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def run_command(cmd, description):
    """Run a command and display the result"""
    console.print(f"\n[bold cyan]🚀 {description}[/bold cyan]")
    console.print(f"[dim]Command: {cmd}[/dim]")
    console.print("─" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            console.print(result.stdout)
        else:
            console.print(f"[red]Error: {result.stderr}[/red]")
    except Exception as e:
        console.print(f"[red]Error running command: {e}[/red]")

def main():
    """Main demo function"""
    
    # Welcome banner
    welcome_text = Text.assemble(
        ("🎯 ", "bold cyan"),
        ("VibeTrack Demo", "bold cyan"),
        ("\n\n", ""),
        ("This demo shows the main features of VibeTrack CLI", "white"),
        ("\n", ""),
        ("Make sure you're in a Git repository to see all features!", "dim yellow")
    )
    
    welcome_panel = Panel(
        welcome_text,
        title="[bold green]Welcome to VibeTrack![/bold green]",
        border_style="cyan",
        expand=False
    )
    console.print(welcome_panel)
    
    # Demo commands
    commands = [
        ("vibetrack about", "Show project information and features"),
        ("vibetrack status", "Show current Git status with insights"),
        ("vibetrack check --help", "Show help for the main check command"),
        ("vibetrack compare --help", "Show help for the compare command"),
    ]
    
    for cmd, desc in commands:
        run_command(cmd, desc)
    
    # Final message
    final_text = Text.assemble(
        ("✨ ", "bold yellow"),
        ("Demo Complete!", "bold green"),
        ("\n\n", ""),
        ("To use VibeTrack in a real Git repository:", "white"),
        ("\n", ""),
        ("1. ", "bold cyan"), ("cd /path/to/your/git/repo", "cyan"),
        ("\n", ""),
        ("2. ", "bold cyan"), ("vibetrack check", "cyan"), (" - Analyze your changes", "white"),
        ("\n", ""),
        ("3. ", "bold cyan"), ("vibetrack compare HEAD~1 HEAD", "cyan"), (" - Compare commits", "white"),
        ("\n\n", ""),
        ("Happy coding! 🚀", "bold magenta")
    )
    
    final_panel = Panel(
        final_text,
        title="[bold green]🎉 Next Steps[/bold green]",
        border_style="green",
        expand=False
    )
    console.print(final_panel)

if __name__ == "__main__":
    main()