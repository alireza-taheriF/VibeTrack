import subprocess
from vibetrack.local_client import send_to_local_model
from rich.console import Console
from rich.panel import Panel

console = Console()

def get_commit_message(commit_hash="HEAD"):
    """Get commit message for a specific commit"""
    try:
        message = subprocess.check_output(
            ['git', 'log', '--format=%B', '-n', '1', commit_hash],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip()
        return message
    except subprocess.CalledProcessError:
        return None

def analyze_commit_message_vs_changes(commit_hash="HEAD", persian_mode=False):
    """Analyze if commit message matches the actual changes"""
    
    if persian_mode:
        console.print(f"[bold blue]🔍 دارم پیام کامیت {commit_hash} رو با تغییرات مقایسه میکنم...[/bold blue]")
    else:
        console.print(f"[bold blue]🔍 Analyzing commit message vs changes for {commit_hash}...[/bold blue]")
    
    # Get commit message
    commit_message = get_commit_message(commit_hash)
    if not commit_message:
        if persian_mode:
            console.print("❌ [red]نتونستم پیام کامیت رو پیدا کنم[/red]")
        else:
            console.print("❌ [red]Could not find commit message[/red]")
        return
    
    # Get changes for this commit
    try:
        from vibetrack.diff_utils import generate_git_diff
        if commit_hash == "HEAD":
            diff = generate_git_diff("HEAD~1", "HEAD")
        else:
            diff = generate_git_diff(f"{commit_hash}~1", commit_hash)
    except Exception as e:
        if persian_mode:
            console.print(f"❌ [red]خطا در دریافت تغییرات: {e}[/red]")
        else:
            console.print(f"❌ [red]Error getting changes: {e}[/red]")
        return
    
    if not diff.strip():
        if persian_mode:
            console.print("ℹ️  [yellow]هیچ تغییری در این کامیت پیدا نشد[/yellow]")
        else:
            console.print("ℹ️  [yellow]No changes found in this commit[/yellow]")
        return
    
    # Display commit message
    title = "[bold cyan]📝 پیام کامیت[/bold cyan]" if persian_mode else "[bold cyan]📝 Commit Message[/bold cyan]"
    message_panel = Panel(
        commit_message,
        title=title,
        border_style="cyan",
        expand=False
    )
    console.print(message_panel)
    
    # Analyze with AI
    if persian_mode:
        prompt = f"""پیام کامیت:
{commit_message}

تغییرات واقعی کد:
{diff}

لطفاً تحلیل کن:
1. آیا پیام کامیت با تغییرات واقعی مطابقت داره؟
2. اگه تضاد وجود داره، کجاها؟
3. پیام کامیت چقدر دقیق و کامله؟
4. پیشنهاد برای بهتر کردن پیام کامیت چیه؟

جواب رو به فارسی و قابل فهم بده."""
    else:
        prompt = f"""Commit message:
{commit_message}

Actual code changes:
{diff}

Please analyze:
1. Does the commit message match the actual changes?
2. If there are discrepancies, where are they?
3. How accurate and complete is the commit message?
4. What would be a better commit message?

Provide a clear and understandable analysis."""
    
    if persian_mode:
        console.print("\n[bold blue]🤖 دارم تطابق پیام و تغییرات رو بررسی میکنم...[/bold blue]")
    else:
        console.print("\n[bold blue]🤖 Analyzing message vs changes consistency...[/bold blue]")
    
    analysis = send_to_local_model(prompt, persian_mode=persian_mode)
    
    # Display analysis
    title = "[bold yellow]�� تحلیل تطابق[/bold yellow]" if persian_mode else "[bold yellow]🧠 Consistency Analysis[/bold yellow]"
    analysis_panel = Panel(
        analysis,
        title=title,
        border_style="yellow",
        expand=False
    )
    console.print(analysis_panel)
    
    return {
        'commit_hash': commit_hash,
        'commit_message': commit_message,
        'diff': diff,
        'analysis': analysis
    }

def suggest_better_commit_message(diff, persian_mode=False):
    """Suggest a better commit message based on changes"""
    
    if persian_mode:
        prompt = f"""بر اساس این تغییرات کد:

{diff}

لطفاً یک پیام کامیت مناسب پیشنهاد بده که:
1. دقیق و واضح باشه
2. تغییرات اصلی رو خلاصه کنه
3. از قوانین conventional commits پیروی کنه
4. به فارسی باشه

فقط پیام کامیت رو بنویس، توضیح اضافی نده."""
    else:
        prompt = f"""Based on these code changes:

{diff}

Please suggest a good commit message that:
1. Is accurate and clear
2. Summarizes the main changes
3. Follows conventional commits format
4. Is concise but descriptive

Just provide the commit message, no extra explanation."""
    
    suggestion = send_to_local_model(prompt, persian_mode=persian_mode)
    
    title = "[bold green]💡 پیشنهاد پیام کامیت[/bold green]" if persian_mode else "[bold green]💡 Suggested Commit Message[/bold green]"
    suggestion_panel = Panel(
        suggestion,
        title=title,
        border_style="green",
        expand=False
    )
    console.print(suggestion_panel)
    
    return suggestion