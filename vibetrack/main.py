import sys
import subprocess
from vibetrack.diff_utils import generate_diff, generate_git_diff, get_pending_changes, get_staged_changes
from vibetrack.local_client import send_to_local_model as analyze_diff
from vibetrack.save_result import save_markdown
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

console = Console()

def analyze_git_diff(commit1: str, commit2: str = "HEAD", save_to_file: bool = True, persian_mode: bool = False):
    """Analyze diff between two commits"""
    if persian_mode:
        console.print(f"[bold blue]🔍 دارم تفاوت بین {commit1} و {commit2} رو چک میکنم...[/bold blue]")
    else:
        console.print(f"[bold blue]🔍 Generating git diff between {commit1} and {commit2}...[/bold blue]")
    
    try:
        diff = generate_git_diff(commit1, commit2)
        if not diff.strip():
            if persian_mode:
                console.print("ℹ️  [yellow]هیچ تفاوتی بین این دو کامیت پیدا نشد[/yellow]")
            else:
                console.print("ℹ️  [yellow]No differences found between the specified commits[/yellow]")
            return
            
        old_file = f"Git: {commit1}"
        new_file = f"Git: {commit2}"

        # Display diff in a beautiful panel
        title = "[bold green]📋 تفاوت‌ها[/bold green]" if persian_mode else "[bold green]📋 Git Diff[/bold green]"
        diff_panel = Panel(
            Syntax(diff, "diff", theme="monokai", line_numbers=False),
            title=title,
            border_style="green",
            expand=False
        )
        console.print(diff_panel)

        if persian_mode:
            console.print("\n[bold blue]🤖 دارم از هوش مصنوعی میپرسم چی شده...[/bold blue]")
        else:
            console.print("\n[bold blue]🤖 Asking AI to analyze the diff...[/bold blue]")
            
        explanation = analyze_diff(diff, persian_mode=persian_mode)

        # Display AI explanation in a beautiful panel
        title = "[bold yellow]🧠 تحلیل هوش مصنوعی[/bold yellow]" if persian_mode else "[bold yellow]🧠 AI Analysis[/bold yellow]"
        explanation_panel = Panel(
            explanation,
            title=title,
            border_style="yellow",
            expand=False
        )
        console.print(explanation_panel)

        if save_to_file:
            filename = save_markdown(diff, explanation, old_file, new_file)
            if persian_mode:
                console.print(f"\n[bold green]✅ تحلیل ذخیره شد در:[/bold green] [cyan]{filename}[/cyan]")
            else:
                console.print(f"\n[bold green]✅ Analysis saved to:[/bold green] [cyan]{filename}[/cyan]")
            
    except subprocess.CalledProcessError as e:
        error_msg = "[bold red]❌ خطای Git:[/bold red]" if persian_mode else "[bold red]❌ Git error:[/bold red]"
        console.print(f"{error_msg} {e}")
        raise
    except Exception as e:
        error_msg = "[bold red]❌ خطا:[/bold red]" if persian_mode else "[bold red]❌ Error:[/bold red]"
        console.print(f"{error_msg} {e}")
        raise

def analyze_pending_changes(save_to_file: bool = True, persian_mode: bool = False):
    """Analyze all uncommitted changes"""
    if persian_mode:
        console.print("[bold blue]🔍 دارم همه تغییرات uncommitted رو چک میکنم...[/bold blue]")
    else:
        console.print("[bold blue]🔍 Analyzing all uncommitted changes...[/bold blue]")
    
    try:
        diff = get_pending_changes()
        if not diff.strip():
            if persian_mode:
                console.print("✅ [green]هیچ ت��ییر uncommitted پیدا نشد[/green]")
                console.print("🎉 [dim]همه چیز تمیزه! کارت تموم شده[/dim]")
            else:
                console.print("✅ [green]No uncommitted changes found[/green]")
            return
            
        old_file = "Working Directory (before changes)"
        new_file = "Working Directory (current)"

        # Display diff in a beautiful panel
        title = "[bold green]📋 تغییرات Uncommitted[/bold green]" if persian_mode else "[bold green]📋 Uncommitted Changes[/bold green]"
        diff_panel = Panel(
            Syntax(diff, "diff", theme="monokai", line_numbers=False),
            title=title,
            border_style="green",
            expand=False
        )
        console.print(diff_panel)

        if persian_mode:
            console.print("\n[bold blue]🤖 دارم از هوش مصنوعی میپرسم چی شده...[/bold blue]")
        else:
            console.print("\n[bold blue]🤖 Asking AI to analyze the changes...[/bold blue]")
            
        explanation = analyze_diff(diff, persian_mode=persian_mode)

        # Display AI explanation in a beautiful panel
        title = "[bold yellow]🧠 تحلیل هوش مصنوعی[/bold yellow]" if persian_mode else "[bold yellow]🧠 AI Analysis[/bold yellow]"
        explanation_panel = Panel(
            explanation,
            title=title,
            border_style="yellow",
            expand=False
        )
        console.print(explanation_panel)

        if save_to_file:
            filename = save_markdown(diff, explanation, old_file, new_file)
            if persian_mode:
                console.print(f"\n[bold green]✅ تحلیل ذخیره شد در:[/bold green] [cyan]{filename}[/cyan]")
            else:
                console.print(f"\n[bold green]✅ Analysis saved to:[/bold green] [cyan]{filename}[/cyan]")
            
    except Exception as e:
        error_msg = "[bold red]❌ خطا:[/bold red]" if persian_mode else "[bold red]❌ Error:[/bold red]"
        console.print(f"{error_msg} {e}")
        raise

def analyze_staged_changes(save_to_file: bool = True, persian_mode: bool = False):
    """Analyze only staged changes"""
    if persian_mode:
        console.print("[bold blue]🔍 دارم فایل‌های staged رو تحلیل میکنم...[/bold blue]")
    else:
        console.print("[bold blue]🔍 Analyzing staged changes...[/bold blue]")
    
    try:
        diff = get_staged_changes()
        if not diff.strip():
            if persian_mode:
                console.print("ℹ️  [yellow]هیچ فایل staged پیدا نشد[/yellow]")
                console.print("💡 [dim]از 'git add' استفاده کن تا فایل‌ها رو stage کنی[/dim]")
            else:
                console.print("ℹ️  [yellow]No staged changes found[/yellow]")
                console.print("💡 [dim]Use 'git add' to stage files for commit[/dim]")
            return
            
        old_file = "Repository (HEAD)"
        new_file = "Staged Changes"

        # Display diff in a beautiful panel
        title = "[bold green]📋 فایل‌های Staged[/bold green]" if persian_mode else "[bold green]📋 Staged Changes[/bold green]"
        diff_panel = Panel(
            Syntax(diff, "diff", theme="monokai", line_numbers=False),
            title=title,
            border_style="green",
            expand=False
        )
        console.print(diff_panel)

        if persian_mode:
            console.print("\n[bold blue]🤖 دارم از هوش مصنوعی میپرسم چی شده...[/bold blue]")
        else:
            console.print("\n[bold blue]🤖 Asking AI to analyze the staged changes...[/bold blue]")
            
        explanation = analyze_diff(diff, persian_mode=persian_mode)

        # Display AI explanation in a beautiful panel
        title = "[bold yellow]🧠 تحلیل هوش مصنوعی[/bold yellow]" if persian_mode else "[bold yellow]🧠 AI Analysis[/bold yellow]"
        explanation_panel = Panel(
            explanation,
            title=title,
            border_style="yellow",
            expand=False
        )
        console.print(explanation_panel)

        if save_to_file:
            filename = save_markdown(diff, explanation, old_file, new_file)
            if persian_mode:
                console.print(f"\n[bold green]✅ تحلیل ذخیره شد در:[/bold green] [cyan]{filename}[/cyan]")
            else:
                console.print(f"\n[bold green]✅ Analysis saved to:[/bold green] [cyan]{filename}[/cyan]")
            
    except Exception as e:
        error_msg = "[bold red]❌ خطا:[/bold red]" if persian_mode else "[bold red]❌ Error:[/bold red]"
        console.print(f"{error_msg} {e}")
        raise

def analyze_file_diff(old_file: str, new_file: str, save_to_file: bool = True):
    """Analyze diff between two files"""
    console.print(f"[bold blue]🔍 Generating diff between {old_file} and {new_file}...[/bold blue]")
    
    try:
        diff = generate_diff(old_file, new_file)
        if not diff.strip():
            console.print("ℹ️  [yellow]No differences found between the files[/yellow]")
            return

        # Display diff in a beautiful panel
        diff_panel = Panel(
            Syntax(diff, "diff", theme="monokai", line_numbers=False),
            title="[bold green]📋 File Diff[/bold green]",
            border_style="green",
            expand=False
        )
        console.print(diff_panel)

        console.print("\n[bold blue]🤖 Asking AI to analyze the diff...[/bold blue]")
        explanation = analyze_diff(diff)

        # Display AI explanation in a beautiful panel
        explanation_panel = Panel(
            explanation,
            title="[bold yellow]🧠 AI Analysis[/bold yellow]",
            border_style="yellow",
            expand=False
        )
        console.print(explanation_panel)

        if save_to_file:
            filename = save_markdown(diff, explanation, old_file, new_file)
            console.print(f"\n[bold green]✅ Analysis saved to:[/bold green] [cyan]{filename}[/cyan]")
            
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        raise

def main():
    """Legacy main function for backward compatibility"""
    args = sys.argv[1:]

    if len(args) >= 2 and args[0] == "--git":
        commit1 = args[1]
        commit2 = args[2] if len(args) >= 3 else "HEAD"
        analyze_git_diff(commit1, commit2)

    elif len(args) == 2:
        old_file, new_file = args
        analyze_file_diff(old_file, new_file)

    else:
        console.print("[bold red]Usage:[/bold red] python main.py <old_file> <new_file>")
        console.print("[bold red]Or:[/bold red]  python main.py --git <commit1> [<commit2>]")
        console.print("\n[bold cyan]💡 Tip:[/bold cyan] Use 'vibetrack --help' for the new CLI interface!")
        sys.exit(1)

if __name__ == "__main__":
    main()
