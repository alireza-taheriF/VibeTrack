#!/usr/bin/env python3
"""
Demo script for VibeTrack CLI - Vibe Coding Edition
نمایش قابلیت‌های VibeTrack برای vibe coders
"""

import subprocess
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()

def run_command(cmd, description, persian_desc=""):
    """Run a command and display the result"""
    desc = f"{description} | {persian_desc}" if persian_desc else description
    console.print(f"\n[bold cyan]🚀 {desc}[/bold cyan]")
    console.print(f"[dim]دستور: {cmd}[/dim]")
    console.print("─" * 60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            console.print(result.stdout)
        else:
            console.print(f"[red]خطا: {result.stderr}[/red]")
    except Exception as e:
        console.print(f"[red]خطا در اجرای دستور: {e}[/red]")

def main():
    """Main demo function"""
    
    # Welcome banner
    welcome_text = Text.assemble(
        ("🎯 ", "bold cyan"),
        ("VibeTrack Demo - Vibe Coding Edition", "bold cyan"),
        ("\n\n", ""),
        ("این demo نشون میده که VibeTrack چطور کار میکنه", "white"),
        ("\n", ""),
        ("مخصوص کسایی که vibe coding میکنن! 😎", "bold magenta"),
        ("\n\n", ""),
        ("⚠️  ", "bold yellow"),
        ("برای دیدن همه قابلیت‌ها، توی یک Git repository باش", "yellow")
    )
    
    welcome_panel = Panel(
        welcome_text,
        title="[bold green]به VibeTrack خوش اومدی![/bold green]",
        border_style="cyan",
        expand=False
    )
    console.print(welcome_panel)
    
    # Check if we're in a git repo
    current_dir = os.getcwd()
    console.print(f"📁 [dim]الان توی این پوشه هستی:[/dim] [cyan]{current_dir}[/cyan]")
    
    if os.path.exists('.git'):
        console.print("✅ [green]��الی! اینجا یک Git repository هست[/green]")
        git_repo = True
    else:
        console.print("⚠️  [yellow]اینجا Git repository نیست، ولی بازم demo رو نشونت میدم[/yellow]")
        git_repo = False
    
    # Demo commands
    commands = [
        ("vt help", "نمایش راهنما", "راهنمای کامل VibeTrack"),
    ]
    
    if git_repo:
        commands.extend([
            ("vt status", "وضعیت پروژه", "ببین پروژه‌ت چه وضعیه"),
            ("vt wtf", "چی شده؟!", "تحلیل سریع تغییرات"),
        ])
    else:
        commands.extend([
            ("vt status", "تست وضعیت", "چون Git repository نیست، خطا میده"),
        ])
    
    for cmd, desc, persian_desc in commands:
        run_command(cmd, desc, persian_desc)
    
    # Usage scenarios
    scenarios_table = Table(title="🎯 سناریوهای مختلف استفاده", border_style="cyan")
    scenarios_table.add_column("وضعیت", style="bold yellow")
    scenarios_table.add_column("دستور", style="bold cyan")
    scenarios_table.add_column("توض��ح", style="white")
    
    scenarios_table.add_row("😵 گیج شدم!", "vt wtf", "تحلیل سریع همه تغییرات")
    scenarios_table.add_row("🎵 وقت دارم", "vt vibe", "تحلیل کامل و آروم")
    scenarios_table.add_row("📋 قبل از کامیت", "vt vibe --staged", "فقط فایلهای staged")
    scenarios_table.add_row("📖 مقایسه کامیت‌ها", "vt story HEAD~1 HEAD", "آخرین کامیت چی بود؟")
    scenarios_table.add_row("📊 چک وضعیت", "vt status", "وضعیت فعلی پروژه")
    
    console.print(scenarios_table)
    
    # Installation guide
    install_panel = Panel(
        """[bold cyan]🚀 نصب Global:[/bold cyan]

[bold yellow]1. کلون کن:[/bold yellow]
[cyan]git clone https://github.com/alireza-taheriF/vibetrack.git[/cyan]
[cyan]cd vibetrack[/cyan]

[bold yellow]2. نصب global:[/bold yellow]
[cyan]./install_global.sh[/cyan]

[bold yellow]3. استفاده از هر پوشه‌ای:[/bold yellow]
[cyan]cd /path/to/your/project[/cyan]
[cyan]vt wtf[/cyan]

[dim]💡 بعد از نصب global، دیگه نیازی نیست توی پوشه VibeTrack باشی![/dim]""",
        title="[bold green]📦 راهنمای نصب[/bold green]",
        border_style="green"
    )
    console.print(install_panel)
    
    # Final message
    final_text = Text.assemble(
        ("🎉 ", "bold yellow"),
        ("Demo تموم شد!", "bold green"),
        ("\n\n", ""),
        ("حالا میتونی:", "white"),
        ("\n", ""),
        ("1. ", "bold cyan"), ("VibeTrack رو global نصب کنی", "cyan"),
        ("\n", ""),
        ("2. ", "bold cyan"), ("از هر پوشه‌ای که Git repository باشه استفاده کنی", "cyan"),
        ("\n", ""),
        ("3. ", "bold cyan"), ("دیگه هیچ وقت گیج نشی که چی عوض شده!", "cyan"),
        ("\n\n", ""),
        ("موفق باشی! 🚀", "bold magenta")
    )
    
    final_panel = Panel(
        final_text,
        title="[bold green]🎯 مرحله بعدی[/bold green]",
        border_style="green",
        expand=False
    )
    console.print(final_panel)

if __name__ == "__main__":
    main()