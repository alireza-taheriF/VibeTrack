import difflib
import subprocess
from rich.text import Text

# Normal mode: Compare two files
def generate_diff(file_path_old, file_path_new):
    with open(file_path_old, 'r') as f_old:
        old_lines = f_old.readlines()

    with open(file_path_new, 'r') as f_new:
        new_lines = f_new.readlines()

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=file_path_old,
        tofile=file_path_new,
        lineterm=''
    )

    return '\n'.join(diff)

# Git mode: Compare two commits
def generate_git_diff(commit1="HEAD~1", commit2="HEAD", allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.html', '.css', '.scss', '.sass', '.less']

    try:
        diff_output = subprocess.check_output(
            ['git', 'diff', commit1, commit2],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(e.returncode, e.cmd, e.output.decode() if e.output else str(e))

    # Filter only relevant files
    filtered_diff = []
    capture = False

    for line in diff_output.splitlines():
        if line.startswith('diff --git'):
            capture = False
            for ext in allowed_extensions:
                if line.endswith(ext) or (ext + ' ') in line:
                    capture = True
                    break
        if capture:
            filtered_diff.append(line)

    return '\n'.join(filtered_diff)

def get_pending_changes(allowed_extensions=None):
    """Get all uncommitted changes (both staged and unstaged)"""
    if allowed_extensions is None:
        allowed_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.html', '.css', '.scss', '.sass', '.less']

    try:
        # Get diff of all changes (staged + unstaged)
        diff_output = subprocess.check_output(
            ['git', 'diff', 'HEAD'],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(e.returncode, e.cmd, e.output.decode() if e.output else str(e))

    # Filter only relevant files
    filtered_diff = []
    capture = False

    for line in diff_output.splitlines():
        if line.startswith('diff --git'):
            capture = False
            for ext in allowed_extensions:
                if line.endswith(ext) or (ext + ' ') in line:
                    capture = True
                    break
        if capture:
            filtered_diff.append(line)

    return '\n'.join(filtered_diff)

def get_staged_changes(allowed_extensions=None):
    """Get only staged changes"""
    if allowed_extensions is None:
        allowed_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.html', '.css', '.scss', '.sass', '.less']

    try:
        # Get diff of staged changes only
        diff_output = subprocess.check_output(
            ['git', 'diff', '--cached'],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(e.returncode, e.cmd, e.output.decode() if e.output else str(e))

    # Filter only relevant files
    filtered_diff = []
    capture = False

    for line in diff_output.splitlines():
        if line.startswith('diff --git'):
            capture = False
            for ext in allowed_extensions:
                if line.endswith(ext) or (ext + ' ') in line:
                    capture = True
                    break
        if capture:
            filtered_diff.append(line)

    return '\n'.join(filtered_diff)

def get_git_status():
    """Get current Git status"""
    try:
        status_output = subprocess.check_output(
            ['git', 'status', '--porcelain'],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
        
        if not status_output.strip():
            return None
            
        # Parse status output
        status_lines = []
        for line in status_output.strip().split('\n'):
            if line:
                status = line[:2]
                filename = line[3:]
                
                if status == '??':
                    status_lines.append(f"🆕 [red]فایل جدید:[/red] {filename}")
                elif status[0] == 'M':
                    status_lines.append(f"📝 [yellow]تغییر یافته (staged):[/yellow] {filename}")
                elif status[1] == 'M':
                    status_lines.append(f"📝 [blue]تغییر یافته (unstaged):[/blue] {filename}")
                elif status[0] == 'A':
                    status_lines.append(f"➕ [green]اضافه شده:[/green] {filename}")
                elif status[0] == 'D':
                    status_lines.append(f"❌ [red]حذف شده:[/red] {filename}")
                elif status[0] == 'R':
                    status_lines.append(f"🔄 [cyan]تغییر نام:[/cyan] {filename}")
                else:
                    status_lines.append(f"❓ [dim]وضعیت نامشخص ({status}):[/dim] {filename}")
        
        return '\n'.join(status_lines)
        
    except subprocess.CalledProcessError:
        return "❌ خطا در دریافت وضعیت Git"

def get_current_branch():
    """Get current Git branch"""
    try:
        branch_output = subprocess.check_output(
            ['git', 'branch', '--show-current'],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip()
        
        return branch_output if branch_output else "unknown"
        
    except subprocess.CalledProcessError:
        return "unknown"

def get_recent_commits(count=5):
    """Get recent commits"""
    try:
        commits_output = subprocess.check_output(
            ['git', 'log', f'--oneline', f'-{count}'],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
        
        if not commits_output.strip():
            return None
            
        # Format commits
        commit_lines = []
        for line in commits_output.strip().split('\n'):
            if line:
                parts = line.split(' ', 1)
                if len(parts) >= 2:
                    commit_hash = parts[0]
                    commit_message = parts[1]
                    commit_lines.append(f"📝 [cyan]{commit_hash}[/cyan] {commit_message}")
        
        return '\n'.join(commit_lines)
        
    except subprocess.CalledProcessError:
        return "❌ خطا در دریافت کامیت‌ها"
