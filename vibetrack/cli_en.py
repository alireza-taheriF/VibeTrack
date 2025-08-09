import typer
import os
from typing import Optional
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from vibetrack.main import analyze_git_diff, analyze_pending_changes, analyze_staged_changes

__app_name__ = "VibeTrack"
__version__ = "0.1.0"
__author__ = "Alireza Taheri Fakhr"
__linkedin__ = "https://www.linkedin.com/in/alireza-taheri-a34179164/"
__github__ = "https://github.com/alireza-taheriF"

app = typer.Typer(
    add_completion=False,
    help="🎯 VibeTrack - AI-powered Git change analyzer",
    rich_markup_mode="rich"
)
console = Console()

def show_banner():
    """Display beautiful banner with project info"""
    banner_content = f"""[bold cyan]🎯 {__app_name__}[/bold cyan] [dim cyan]v{__version__}[/dim cyan]
[bold magenta]👨‍💻 AI-powered Git change analyzer[/bold magenta]

[dim blue]🔗 GitHub:[/dim blue] [blue]{__github__}[/blue]
[dim blue]💼 LinkedIn:[/dim blue] [blue]{__linkedin__}[/blue]"""
    
    panel = Panel(
        banner_content,
        border_style="cyan",
        title="[bold cyan]Welcome to VibeTrack![/bold cyan]",
        subtitle="[dim]Understand your code changes before pushing![/dim]",
        expand=False
    )
    console.print(panel)
    console.print()

def check_git_repo():
    """Check if current directory is a git repository"""
    if not os.path.exists('.git'):
        console.print("❌ [bold red]Error:[/bold red] This is not a Git repository!", style="red")
        console.print("💡 [dim]Navigate to a directory that contains a Git repository[/dim]")
        
        # Show current directory
        current_dir = os.getcwd()
        console.print(f"📁 [dim]Current directory:[/dim] [cyan]{current_dir}[/cyan]")
        
        # Suggest git init
        console.print("\n🚀 [bold yellow]Solutions:[/bold yellow]")
        console.print("1. [cyan]git init[/cyan] - Initialize Git in this directory")
        console.print("2. [cyan]cd /path/to/your/project[/cyan] - Navigate to a Git repository")
        
        raise typer.Exit(1)

@app.callback()
def main_callback():
    """Main callback"""
    pass

@app.command("check", help="🔍 Analyze current changes")
def check_changes(
    staged: bool = typer.Option(False, "--staged", "-s", help="🎭 Analyze only staged files"),
    all_changes: bool = typer.Option(False, "--all", "-a", help="📋 Analyze all changes"),
    commit: Optional[str] = typer.Option(None, "--commit", "-c", help="Compare with specific commit"),
    no_save: bool = typer.Option(False, "--no-save", help="Don't save analysis to file"),
):
    """
    🔍 Analyze current changes - Main command for understanding your modifications
    
    This is the primary command you'll use before pushing to GitHub.
    It analyzes your changes and explains what was modified and why.
    """
    check_git_repo()
    
    console.print("🔍 [bold blue]Analyzing your changes...[/bold blue]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("🔍 Analyzing changes...", total=None)
        
        try:
            # Show current status first
            from vibetrack.diff_utils import get_git_status, get_current_branch
            
            current_branch = get_current_branch()
            console.print(f"📍 [bold cyan]Current branch:[/bold cyan] [yellow]{current_branch}[/yellow]")
            
            status_info = get_git_status()
            if status_info:
                console.print(Panel(status_info, title="[bold cyan]📊 Current Status[/bold cyan]", border_style="cyan"))
            
            # Analyze changes based on options
            if staged:
                analyze_staged_changes(save_to_file=not no_save, persian_mode=False)
            elif commit:
                analyze_git_diff(commit, "HEAD", save_to_file=not no_save, persian_mode=False)
            else:
                analyze_pending_changes(save_to_file=not no_save, persian_mode=False)
            
        except Exception as e:
            progress.stop()
            console.print(f"❌ [bold red]Error:[/bold red] {str(e)}", style="red")
            raise typer.Exit(1)

@app.command("compare", help="📖 Compare commits or branches")
def compare_commits(
    commit1: str = typer.Argument(..., help="First commit/branch"),
    commit2: str = typer.Argument("HEAD", help="Second commit/branch (default: HEAD)"),
    no_save: bool = typer.Option(False, "--no-save", help="Don't save analysis to file"),
):
    """
    📖 Compare two commits or branches
    
    Examples:
      vibetrack compare HEAD~1 HEAD     # What changed in the last commit?
      vibetrack compare main feature    # Difference between main and feature
      vibetrack compare abc123 def456   # Compare two specific commits
    """
    check_git_repo()
    
    console.print(f"📖 [bold blue]Comparing {commit1} with {commit2}...[/bold blue]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task(f"📚 Analyzing differences...", total=None)
        
        try:
            analyze_git_diff(commit1, commit2, save_to_file=not no_save, persian_mode=False)
        except Exception as e:
            progress.stop()
            console.print(f"❌ [bold red]Error:[/bold red] {str(e)}", style="red")
            raise typer.Exit(1)

@app.command("status", help="📊 Show project status")
def project_status():
    """
    📊 Show current project status with Git insights
    """
    check_git_repo()
    
    from vibetrack.diff_utils import get_git_status, get_current_branch, get_recent_commits
    
    # Current branch
    current_branch = get_current_branch()
    console.print(f"📍 [bold cyan]Current branch:[/bold cyan] [yellow]{current_branch}[/yellow]")
    
    # Git status
    status_info = get_git_status()
    if status_info:
        console.print(Panel(status_info, title="[bold cyan]📊 File Status[/bold cyan]", border_style="cyan"))
    else:
        console.print("✅ [bold green]Everything is clean! No changes detected[/bold green]")
    
    # Recent commits
    recent_commits = get_recent_commits(5)
    if recent_commits:
        console.print(Panel(recent_commits, title="[bold yellow]📝 Recent Commits[/bold yellow]", border_style="yellow"))

@app.command("about", help="ℹ️ About VibeTrack")
def show_about():
    """
    ℹ️ Show information about VibeTrack and usage examples
    """
    show_banner()
    
    # Features table
    features_table = Table(title="✨ Key Features", border_style="cyan")
    features_table.add_column("Feature", style="bold cyan")
    features_table.add_column("Description", style="white")
    
    features_table.add_row("🔍 Smart Analysis", "AI-powered change detection and explanation")
    features_table.add_row("🎭 Staged Changes", "Analyze only staged changes ready for commit")
    features_table.add_row("📋 All Changes", "Analyze all uncommitted modifications")
    features_table.add_row("🔄 Commit Comparison", "Compare any two commits or branches")
    features_table.add_row("💾 Auto Save", "Automatically save analysis reports")
    features_table.add_row("🎨 Beautiful Output", "Rich, colorful terminal interface")
    
    console.print(features_table)
    console.print()
    
    # Usage examples
    examples_panel = Panel(
        """[bold cyan]🎯 Common Usage Scenarios:[/bold cyan]

[bold yellow]🔍 Before committing:[/bold yellow]
• [cyan]vibetrack check --staged[/cyan] - Check what you're about to commit
• [cyan]vibetrack check[/cyan] - Analyze all current changes

[bold yellow]📖 Understanding history:[/bold yellow]  
• [cyan]vibetrack compare HEAD~1 HEAD[/cyan] - What changed in the last commit?
• [cyan]vibetrack compare main feature[/cyan] - Difference between branches

[bold yellow]📊 Project overview:[/bold yellow]
• [cyan]vibetrack status[/cyan] - Current project status

[bold yellow]🚀 Before pushing to GitHub:[/bold yellow]
• [cyan]vibetrack check[/cyan] - Understand what you're about to push

[dim]💡 Tip: Use VibeTrack from any Git repository directory[/dim]""",
        title="[bold green]🚀 Usage Guide[/bold green]",
        border_style="green"
    )
    console.print(examples_panel)

@app.command("help", help="❓ Show help and examples")
def show_help():
    """
    ❓ Complete VibeTrack help guide
    """
    show_banner()
    
    # Commands table
    commands_table = Table(title="🎯 Main Commands", border_style="cyan")
    commands_table.add_column("Command", style="bold cyan")
    commands_table.add_column("Purpose", style="white")
    commands_table.add_column("Example", style="dim yellow")
    
    commands_table.add_row("vibetrack check", "🔍 Analyze current changes", "vibetrack check --staged")
    commands_table.add_row("vibetrack compare", "📖 Compare commits/branches", "vibetrack compare HEAD~1 HEAD")
    commands_table.add_row("vibetrack status", "📊 Project status", "vibetrack status")
    commands_table.add_row("vibetrack about", "ℹ️ About VibeTrack", "vibetrack about")
    
    console.print(commands_table)
    console.print()
    
    # Workflow panel
    workflow_panel = Panel(
        """[bold cyan]🔄 Recommended Workflow:[/bold cyan]

[bold yellow]1. Before committing:[/bold yellow]
[cyan]git add .[/cyan]
[cyan]vibetrack check --staged[/cyan]
[cyan]git commit -m "Your message based on analysis"[/cyan]

[bold yellow]2. Before pushing:[/bold yellow]
[cyan]vibetrack check[/cyan]
[cyan]git push origin main[/cyan]

[bold yellow]3. Understanding changes:[/bold yellow]
[cyan]vibetrack compare HEAD~1 HEAD[/cyan]
[cyan]vibetrack status[/cyan]

[dim]💡 Make VibeTrack part of your daily Git workflow![/dim]""",
        title="[bold green]🚀 Best Practices[/bold green]",
        border_style="green"
    )
    console.print(workflow_panel)

if __name__ == "__main__":
    app()