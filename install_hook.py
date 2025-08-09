import os

# Directions (you already gave)
project_path = "/Users/alireza/Documents/reddit_fetcher"
vibetrack_path = "/Users/alireza/VibeTrack"

# Hook file path
hook_path = os.path.join(project_path, ".git", "hooks", "post-commit")

# کدی که داخل فایل hook می‌نویسیم
hook_code = f"""#!/bin/bash

echo "[VibeTrack] Auto-analyzing code diff after commit..."

python3 {vibetrack_path}/main.py --git HEAD~1 HEAD
"""

# ساخت فایل
with open(hook_path, "w") as f:
    f.write(hook_code)

# اجرای chmod +x
os.chmod(hook_path, 0o755)

print(f"✅ Hook installed at: {hook_path}")
