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
    help="🎯 VibeTrack - دستیار شخصی برای Vibe Coders",
    rich_markup_mode="rich"
)
console = Console()

def show_banner():
    """Display beautiful banner with project info"""
    banner_content = f"""[bold cyan]🎯 {__app_name__}[/bold cyan] [dim cyan]v{__version__}[/dim cyan]
[bold magenta]👨‍💻 دستیار شخصی برای Vibe Coders[/bold magenta]

[dim blue]🔗 GitHub:[/dim blue] [blue]{__github__}[/blue]
[dim blue]💼 LinkedIn:[/dim blue] [blue]{__linkedin__}[/blue]"""
    
    panel = Panel(
        banner_content,
        border_style="cyan",
        title="[bold cyan]به VibeTrack خوش اومدی![/bold cyan]",
        subtitle="[dim]بفهم چی عوض شده و چرا![/dim]",
        expand=False
    )
    console.print(panel)
    console.print()

def check_git_repo():
    """Check if current directory is a git repository"""
    if not os.path.exists('.git'):
        console.print("❌ [bold red]خطا:[/bold red] اینجا یک Git repository نیست!", style="red")
        console.print("💡 [dim]برو توی یک پوشه که Git repository باشه[/dim]")
        
        # Show current directory
        current_dir = os.getcwd()
        console.print(f"📁 [dim]الان توی این پوشه هستی:[/dim] [cyan]{current_dir}[/cyan]")
        
        # Suggest git init
        console.print("\n🚀 [bold yellow]راه حل:[/bold yellow]")
        console.print("1. [cyan]git init[/cyan] - اگه میخوای اینجا Git ش��وع کنی")
        console.print("2. [cyan]cd /path/to/your/project[/cyan] - برو توی پروژه‌ای که Git داره")
        
        raise typer.Exit(1)

@app.callback()
def main_callback():
    """Main callback"""
    pass

@app.command("wtf", help="😵 چی شده؟! - تحلیل سریع تغییرات")
def what_the_hell():
    """
    😵 چی شده؟! - برای وقتی که کلاً گیج شدی
    
    این دستور بهت میگه:
    - چه فایلهایی عوض شدن
    - چه تغییراتی داده شدن  
    - چرا این تغییرات انجام شدن
    - چطور میتونی ادامه بدی
    """
    check_git_repo()
    
    console.print("😵 [bold yellow]بذار ببینم چی شده...[/bold yellow]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("🔍 دارم چک میکنم...", total=None)
        
        try:
            # Show current status first
            from vibetrack.diff_utils import get_git_status, get_current_branch
            
            current_branch = get_current_branch()
            console.print(f"📍 [bold cyan]الان روی branch:[/bold cyan] [yellow]{current_branch}[/yellow]")
            
            status_info = get_git_status()
            if status_info:
                console.print(Panel(status_info, title="[bold cyan]📊 وضعیت فعلی[/bold cyan]", border_style="cyan"))
            
            # Analyze changes
            analyze_pending_changes(save_to_file=True, persian_mode=True)
            
        except Exception as e:
            progress.stop()
            console.print(f"❌ [bold red]خطا:[/bold red] {str(e)}", style="red")
            raise typer.Exit(1)

@app.command("vibe", help="🎵 حالت vibe - تحلیل آروم و کامل")
def vibe_mode(
    staged: bool = typer.Option(False, "--staged", "-s", help="🎭 فقط فایلهای staged"),
    all_changes: bool = typer.Option(False, "--all", "-a", help="📋 همه تغییرات"),
):
    """
    🎵 حالت vibe - تحلیل کامل و آروم
    
    برای وقتی که وقت داری و می��وای همه چیز رو کامل بفهمی
    """
    check_git_repo()
    
    console.print("🎵 [bold magenta]حالت vibe فعال شد...[/bold magenta]")
    console.print("☕ [dim]یه چای بریز و بشین ببین چی شده[/dim]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("🎵 دارم با حوصله تحلیل میکنم...", total=None)
        
        try:
            if staged:
                analyze_staged_changes(save_to_file=True, persian_mode=True)
            elif all_changes:
                analyze_pending_changes(save_to_file=True, persian_mode=True)
            else:
                analyze_pending_changes(save_to_file=True, persian_mode=True)
        except Exception as e:
            progress.stop()
            console.print(f"❌ [bold red]خطا:[/bold red] {str(e)}", style="red")
            raise typer.Exit(1)

@app.command("story", help="📖 داستان تغییرات - مقایسه کامیت‌ها")
def tell_story(
    commit1: str = typer.Argument(..., help="کامیت اول"),
    commit2: str = typer.Argument("HEAD", help="کامیت دوم (پیش‌فرض: HEAD)"),
):
    """
    📖 داستان تغییرات - مقایسه دو کامیت
    
    مثال‌ها:
      vt story HEAD~1 HEAD     # آخرین کامیت چی بود؟
      vt story main feature    # تفاوت main و feature
      vt story abc123 def456   # مقایسه دو کامیت خاص
    """
    check_git_repo()
    
    console.print(f"📖 [bold blue]دارم داستان تغییرات از {commit1} تا {commit2} رو میگم...[/bold blue]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task(f"📚 دارم داستان رو می‌خونم...", total=None)
        
        try:
            analyze_git_diff(commit1, commit2, save_to_file=True, persian_mode=True)
        except Exception as e:
            progress.stop()
            console.print(f"❌ [bold red]خطا:[/bold red] {str(e)}", style="red")
            raise typer.Exit(1)

@app.command("status", help="📊 وضعیت پروژه")
def project_status():
    """
    📊 وضعیت فعلی پروژه
    """
    check_git_repo()
    
    from vibetrack.diff_utils import get_git_status, get_current_branch, get_recent_commits
    
    # Current branch
    current_branch = get_current_branch()
    console.print(f"📍 [bold cyan]Branch فعلی:[/bold cyan] [yellow]{current_branch}[/yellow]")
    
    # Git status
    status_info = get_git_status()
    if status_info:
        console.print(Panel(status_info, title="[bold cyan]📊 وضعیت فایل‌ها[/bold cyan]", border_style="cyan"))
    else:
        console.print("✅ [bold green]همه چیز تمیزه! هیچ تغییری نداری[/bold green]")
    
    # Recent commits
    recent_commits = get_recent_commits(5)
    if recent_commits:
        console.print(Panel(recent_commits, title="[bold yellow]📝 آخرین کامیت‌ها[/bold yellow]", border_style="yellow"))

@app.command("check-commit", help="📝 تحلیل پیام کامیت")
def check_commit_message(
    commit: str = typer.Argument("HEAD", help="کامیت مورد نظر"),
    suggest: bool = typer.Option(False, "--suggest", help="پیشنهاد پیام بهتر"),
):
    """
    📝 تحلیل تطابق پیام کامیت با تغییرات
    
    بررسی میکنه که آیا پیام کامیت با تغییرات واقعی مطابقت داره یا نه
    """
    check_git_repo()
    
    console.print(f"📝 [bold blue]دارم پیام کامیت {commit} رو بررسی میکنم...[/bold blue]")
    
    try:
        from vibetrack.commit_analyzer import analyze_commit_message_vs_changes, suggest_better_commit_message
        from vibetrack.diff_utils import generate_git_diff
        
        # Analyze commit message vs changes
        result = analyze_commit_message_vs_changes(commit, persian_mode=True)
        
        if suggest and result:
            console.print("\n[bold green]💡 پیشنهاد پیام بهتر:[/bold green]")
            suggest_better_commit_message(result['diff'], persian_mode=True)
            
    except Exception as e:
        console.print(f"❌ [bold red]خطا:[/bold red] {str(e)}", style="red")
        raise typer.Exit(1)

@app.command("private", help="🔒 حالت خصوصی")
def private_mode(
    action: str = typer.Argument(..., help="عمل: save, list, export, cleanup"),
    target: Optional[str] = typer.Argument(None, help="هدف (برای export یا cleanup)"),
):
    """
    🔒 مدیریت تحلیل‌های خصوصی و رمزگذاری شده
    
    Actions:
    - save: ذخیره تحلیل فعلی به صورت رمزگذاری شده
    - list: لیست تحلیل‌های خصوصی
    - export: خروجی گرفتن از تحلیل خصوصی
    - cleanup: پاک کردن تحلیل‌های قدیمی
    """
    check_git_repo()
    
    from vibetrack.privacy_manager import PrivacyManager
    
    privacy_manager = PrivacyManager()
    current_dir = os.getcwd()
    
    if action == "save":
        console.print("🔒 [bold blue]دارم تحلیل رو به صورت خصوصی ذخیره میکنم...[/bold blue]")
        
        try:
            from vibetrack.diff_utils import get_pending_changes
            from vibetrack.local_client import send_to_local_model
            
            diff = get_pending_changes()
            if not diff.strip():
                console.print("ℹ️  [yellow]هیچ تغییری برای ذخیره پیدا نشد[/yellow]")
                return
            
            explanation = send_to_local_model(diff, persian_mode=True)
            filepath = privacy_manager.save_private_analysis(
                diff, explanation, current_dir, "private-analysis"
            )
            
            console.print(f"✅ [bold green]تحلیل خصوصی ذخیره شد:[/bold green] [dim]{os.path.basename(filepath)}[/dim]")
            
        except Exception as e:
            console.print(f"❌ [bold red]خطا:[/bold red] {str(e)}", style="red")
    
    elif action == "list":
        console.print("📋 [bold blue]لیست تحلیل‌های خصوصی:[/bold blue]")
        
        analyses = privacy_manager.list_private_analyses(current_dir)
        if not analyses:
            console.print("ℹ️  [yellow]هیچ تحلیل خصوصی پیدا نشد[/yellow]")
            return
        
        table = Table(title="🔒 تحلیل‌های خصوصی", border_style="cyan")
        table.add_column("فایل", style="cyan")
        table.add_column("تاریخ", style="yellow")
        table.add_column("نوع", style="green")
        
        for analysis in analyses:
            table.add_row(
                analysis['filename'],
                analysis['timestamp'][:19],
                analysis['analysis_type']
            )
        
        console.print(table)
    
    elif action == "export":
        if not target:
            console.print("❌ [red]نام فایل برای export لازمه[/red]")
            return
        
        console.print(f"📤 [bold blue]دارم {target} رو export میکنم...[/bold blue]")
        
        exported = privacy_manager.export_private_analysis(target, 'markdown')
        if exported:
            export_file = f"exported_{target.replace('.enc', '.md')}"
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(exported)
            console.print(f"✅ [bold green]Export شد:[/bold green] {export_file}")
        else:
            console.print("❌ [red]فایل پیدا نشد یا خطا در export[/red]")
    
    elif action == "cleanup":
        days = int(target) if target else 30
        console.print(f"🧹 [bold blue]دارم تحلیل‌های قدیمی‌تر از {days} روز رو پاک میکنم...[/bold blue]")
        
        removed = privacy_manager.cleanup_old_analyses(days)
        console.print(f"✅ [bold green]{removed} فایل پاک شد[/bold green]")

@app.command("silent", help="🤫 حالت ساکت برای CI/CD")
def silent_mode(
    action: str = typer.Argument("analyze", help="عمل: analyze, check-commit"),
    output_format: str = typer.Option("json", help="فرمت خروجی: json, text"),
    commit: str = typer.Option("HEAD", help="کامیت مورد نظر"),
):
    """
    🤫 حالت ساکت برای استفاده در CI/CD
    
    خروجی ساده و قابل پردازش برای اسکریپت‌ها
    """
    from vibetrack.privacy_manager import SilentMode
    
    if action == "analyze":
        try:
            from vibetrack.diff_utils import get_pending_changes
            diff = get_pending_changes()
            
            if not diff.strip():
                result = {
                    "success": False,
                    "error": "No changes found",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                result = SilentMode.analyze_silent(diff)
            
            print(SilentMode.generate_ci_report(result, output_format))
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            print(SilentMode.generate_ci_report(result, output_format))
    
    elif action == "check-commit":
        result = SilentMode.check_commit_quality(commit)
        print(SilentMode.generate_ci_report(result, output_format))

@app.command("export", help="📤 Export گزارش‌ها")
def export_reports(
    format: str = typer.Argument("markdown", help="فرمت: markdown, json, html"),
    target: Optional[str] = typer.Option(None, help="فایل یا پوشه مقصد"),
):
    """
    📤 Export گزارش‌های تحلیل به فرمت‌های مختلف
    """
    check_git_repo()
    
    console.print(f"📤 [bold blue]دارم گزارش رو به فرمت {format} export میکنم...[/bold blue]")
    
    try:
        from vibetrack.diff_utils import get_pending_changes
        from vibetrack.local_client import send_to_local_model
        from vibetrack.save_result import save_json_report, save_html_report, save_markdown
        
        diff = get_pending_changes()
        if not diff.strip():
            console.print("ℹ️  [yellow]هیچ تغییری برای export پیدا نشد[/yellow]")
            return
        
        explanation = send_to_local_model(diff, persian_mode=True)
        old_file = "Working Directory (before)"
        new_file = "Working Directory (current)"
        
        if format == "json":
            filename = save_json_report(diff, explanation, old_file, new_file, "export")
        elif format == "html":
            filename = save_html_report(diff, explanation, old_file, new_file, "export")
        else:  # markdown
            filename = save_markdown(diff, explanation, old_file, new_file, "export")
        
        console.print(f"✅ [bold green]Export شد:[/bold green] [cyan]{filename}[/cyan]")
        
    except Exception as e:
        console.print(f"❌ [bold red]خطا:[/bold red] {str(e)}", style="red")

@app.command("help", help="❓ راهنما و مثال‌ها")
def show_help():
    """
    ❓ راهنمای کامل VibeTrack
    """
    show_banner()
    
    # Commands table
    commands_table = Table(title="🎯 دستورات اصلی", border_style="cyan")
    commands_table.add_column("دستور", style="bold cyan")
    commands_table.add_column("کاربرد", style="white")
    commands_table.add_column("مثال", style="dim yellow")
    
    commands_table.add_row("vt wtf", "😵 چی شده؟! تحلیل سریع", "vt wtf")
    commands_table.add_row("vt vibe", "🎵 تحلیل کامل و آروم", "vt vibe --staged")
    commands_table.add_row("vt story", "📖 داستان تغییرات", "vt story HEAD~1 HEAD")
    commands_table.add_row("vt status", "📊 وضعیت پروژه", "vt status")
    commands_table.add_row("vt check-commit", "📝 تحلیل پیام کامیت", "vt check-commit HEAD")
    commands_table.add_row("vt private", "🔒 حالت خصوصی", "vt private save")
    commands_table.add_row("vt export", "📤 Export گزارش", "vt export html")
    commands_table.add_row("vt silent", "🤫 حالت ساکت", "vt silent analyze")
    
    console.print(commands_table)
    console.print()
    
    # New features
    features_panel = Panel(
        """[bold cyan]✨ قابلیت‌های جدید:[/bold cyan]

[bold yellow]📝 تحلیل پیام کامیت:[/bold yellow]
• [cyan]vt check-commit[/cyan] - بررسی تطابق پیام با تغییرات
• [cyan]vt check-commit --suggest[/cyan] - پیشنهاد پیام بهتر

[bold yellow]🔒 حالت خصوصی:[/bold yellow]
• [cyan]vt private save[/cyan] - ذخیره رمزگذاری شده
• [cyan]vt private list[/cyan] - لیست تحلیل‌های خصوصی
• [cyan]vt private export filename.enc[/cyan] - خروجی گرفتن

[bold yellow]📤 Export پیشرفته:[/bold yellow]
• [cyan]vt export markdown[/cyan] - گزارش Markdown کامل
• [cyan]vt export json[/cyan] - فرمت JSON برای برنامه‌ها
• [cyan]vt export html[/cyan] - گزارش وب زیبا

[bold yellow]🤫 حالت ساکت (CI/CD):[/bold yellow]
• [cyan]vt silent analyze[/cyan] - تحلیل بدون تعامل
• [cyan]vt silent check-commit[/cyan] - بررسی کیفیت کامیت

[dim]💡 همه قابلیت‌ها از هر پوشه Git repository قابل استفاده‌اند[/dim]""",
        title="[bold green]🚀 قابلیت‌های پیشرفته[/bold green]",
        border_style="green"
    )
    console.print(features_panel)
    
    # Original scenarios
    scenarios_panel = Panel(
        """[bold cyan]🎯 سناریوهای مختلف:[/bold cyan]

[bold yellow]😵 وقتی کلاً گیج شدی:[/bold yellow]
• [cyan]vt wtf[/cyan] - بزن ببین چی شده

[bold yellow]🎵 وقتی وقت داری:[/bold yellow]  
• [cyan]vt vibe[/cyan] - تحلیل کامل همه چیز
• [cyan]vt vibe --staged[/cyan] - فقط فایلهای آماده کامیت

[bold yellow]📖 وقتی میخوای بفهمی چی عوض شده:[/bold yellow]
• [cyan]vt story HEAD~1 HEAD[/cyan] - آخرین کامیت چی بود؟
• [cyan]vt story main feature[/cyan] - تفاوت دو branch

[bold yellow]��� چک کردن وضعیت:[/bold yellow]
• [cyan]vt status[/cyan] - وضعیت فعلی پروژه

[dim]💡 نکته: همه دستورات رو میتونی از هر پوشه‌ای که Git repository باشه اجرا کنی[/dim]""",
        title="[bold green]🚀 راهنمای استفاده[/bold green]",
        border_style="green"
    )
    console.print(scenarios_panel)

# Add short aliases
app.command("w", hidden=True)(what_the_hell)  # vt w
app.command("v", hidden=True)(vibe_mode)      # vt v  
app.command("s", hidden=True)(tell_story)     # vt s

if __name__ == "__main__":
    app()