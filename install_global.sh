#!/bin/bash

# VibeTrack Global Installation Script
# This script installs VibeTrack globally so you can use it from any directory

set -e

echo "🎯 نصب Global VibeTrack..."
echo "این اسکریپت VibeTrack رو به صورت global نصب میکنه تا از هر پوشه‌ای استفاده کنی"

# Check if Python 3.8+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 لازمه ولی نصب نیست."
    echo "لطفاً Python 3.8 یا بالاتر رو نصب کن و دوباره امتحان کن."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version یا بالاتر لازمه. پیدا شده: $python_version"
    exit 1
fi

echo "✅ Python $python_version پیدا شد"

# Get the current directory (where VibeTrack is)
VIBETRACK_DIR=$(pwd)
echo "📁 VibeTrack directory: $VIBETRACK_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 ساخت virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 فعال‌سازی virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 نصب dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install VibeTrack in development mode
echo "🚀 نصب VibeTrack..."
pip install -e .

# Create a global wrapper script
GLOBAL_SCRIPT="/usr/local/bin/vt"
echo "📝 ساخت اسکریپت global در $GLOBAL_SCRIPT..."

# Create the wrapper script
sudo tee $GLOBAL_SCRIPT > /dev/null << EOF
#!/bin/bash
# VibeTrack Global Wrapper Script
# This script allows you to use VibeTrack from any directory

# Activate VibeTrack virtual environment and run the command
source "$VIBETRACK_DIR/venv/bin/activate" && vibetrack "\$@"
EOF

# Make it executable
sudo chmod +x $GLOBAL_SCRIPT

# Also create vibetrack command
GLOBAL_SCRIPT_FULL="/usr/local/bin/vibetrack"
sudo tee $GLOBAL_SCRIPT_FULL > /dev/null << EOF
#!/bin/bash
# VibeTrack Global Wrapper Script
# This script allows you to use VibeTrack from any directory

# Activate VibeTrack virtual environment and run the command
source "$VIBETRACK_DIR/venv/bin/activate" && vibetrack "\$@"
EOF

sudo chmod +x $GLOBAL_SCRIPT_FULL

echo ""
echo "✅ VibeTrack به صورت global نصب شد!"
echo ""
echo "🎉 حالا میتونی از هر پوشه‌ای استفاده کنی:"
echo "   vt wtf              # چی شده؟!"
echo "   vt vibe             # تحلیل کامل"
echo "   vt story HEAD~1     # داستان تغییرات"
echo "   vt status           # وضعیت پروژه"
echo "   vt help             # راهنما"
echo ""
echo "   vibetrack wtf       # همین دستورات با نام کامل"
echo ""
echo "💡 نکته: حتماً توی یک Git repository باش تا کار کنه"
echo ""
echo "🚀 موفق باشی با VibeTrack!"

# Test the installation
echo ""
echo "🧪 تست نصب..."
if command -v vt &> /dev/null; then
    echo "✅ دستور 'vt' آماده استفاده است"
    vt help
else
    echo "❌ مشکلی در نصب پیش اومده"
    echo "💡 ممکنه نیاز باشه terminal رو restart کنی"
fi