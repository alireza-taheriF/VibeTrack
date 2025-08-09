import os
import json
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet
from rich.console import Console

console = Console()

class PrivacyManager:
    """Manage private/encrypted storage of analysis results"""
    
    def __init__(self):
        self.private_dir = os.path.expanduser("~/.vibetrack_private")
        self.key_file = os.path.join(self.private_dir, ".encryption_key")
        self.config_file = os.path.join(self.private_dir, "config.json")
        self._ensure_private_dir()
        self._load_or_create_key()
    
    def _ensure_private_dir(self):
        """Create private directory with proper permissions"""
        if not os.path.exists(self.private_dir):
            os.makedirs(self.private_dir, mode=0o700)  # Only owner can read/write/execute
    
    def _load_or_create_key(self):
        """Load existing encryption key or create new one"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
            os.chmod(self.key_file, 0o600)  # Only owner can read/write
        
        self.cipher = Fernet(self.key)
    
    def _get_project_hash(self, project_path):
        """Generate unique hash for project path"""
        return hashlib.sha256(project_path.encode()).hexdigest()[:16]
    
    def save_private_analysis(self, diff, explanation, project_path, analysis_type="diff", extra_data=None):
        """Save analysis in encrypted format"""
        project_hash = self._get_project_hash(project_path)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Create analysis data
        analysis_data = {
            "timestamp": datetime.now().isoformat(),
            "project_path": project_path,  # This will be encrypted
            "analysis_type": analysis_type,
            "diff": diff,
            "explanation": explanation,
            "extra_data": extra_data or {}
        }
        
        # Encrypt the data
        encrypted_data = self.cipher.encrypt(json.dumps(analysis_data).encode())
        
        # Save to private directory
        filename = f"analysis_{project_hash}_{timestamp}.enc"
        filepath = os.path.join(self.private_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(encrypted_data)
        
        os.chmod(filepath, 0o600)  # Only owner can read/write
        
        return filepath
    
    def load_private_analysis(self, filename):
        """Load and decrypt analysis"""
        filepath = os.path.join(self.private_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            console.print(f"[red]خطا در بازیابی تحلیل رمزگذاری شده: {e}[/red]")
            return None
    
    def list_private_analyses(self, project_path=None):
        """List all private analyses, optionally filtered by project"""
        analyses = []
        
        if not os.path.exists(self.private_dir):
            return analyses
        
        project_hash = self._get_project_hash(project_path) if project_path else None
        
        for filename in os.listdir(self.private_dir):
            if filename.endswith('.enc'):
                if project_hash and not filename.startswith(f"analysis_{project_hash}_"):
                    continue
                
                analysis = self.load_private_analysis(filename)
                if analysis:
                    analyses.append({
                        'filename': filename,
                        'timestamp': analysis['timestamp'],
                        'analysis_type': analysis['analysis_type'],
                        'project_path': analysis['project_path']
                    })
        
        return sorted(analyses, key=lambda x: x['timestamp'], reverse=True)
    
    def cleanup_old_analyses(self, days_old=30):
        """Remove analyses older than specified days"""
        if not os.path.exists(self.private_dir):
            return 0
        
        cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        removed_count = 0
        
        for filename in os.listdir(self.private_dir):
            if filename.endswith('.enc'):
                filepath = os.path.join(self.private_dir, filename)
                if os.path.getmtime(filepath) < cutoff_date:
                    os.remove(filepath)
                    removed_count += 1
        
        return removed_count
    
    def export_private_analysis(self, filename, export_format='markdown'):
        """Export private analysis to readable format"""
        analysis = self.load_private_analysis(filename)
        if not analysis:
            return None
        
        if export_format == 'markdown':
            return self._export_to_markdown(analysis)
        elif export_format == 'json':
            return json.dumps(analysis, indent=2, ensure_ascii=False)
        else:
            return str(analysis)
    
    def _export_to_markdown(self, analysis):
        """Convert analysis to markdown format"""
        return f"""# 🔒 VibeTrack Private Analysis

**Generated:** {analysis['timestamp']}
**Project:** {analysis['project_path']}
**Type:** {analysis['analysis_type']}

## 🔍 Changes

```diff
{analysis['diff']}
```

## 🧠 Analysis

{analysis['explanation']}

---
*Private analysis - stored encrypted locally*
"""

class SilentMode:
    """Handle silent mode operations for CI/CD"""
    
    @staticmethod
    def analyze_silent(diff, analysis_type="ci-analysis"):
        """Perform analysis in silent mode (no interactive output)"""
        from vibetrack.local_client import send_to_local_model
        
        try:
            # Use English for CI/CD environments
            analysis = send_to_local_model(diff, persian_mode=False)
            
            return {
                "success": True,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "type": analysis_type
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "type": analysis_type
            }
    
    @staticmethod
    def generate_ci_report(analysis_result, output_format="json"):
        """Generate CI-friendly report"""
        if output_format == "json":
            return json.dumps(analysis_result, indent=2)
        elif output_format == "text":
            if analysis_result["success"]:
                return f"✅ Analysis completed successfully\n\n{analysis_result['analysis']}"
            else:
                return f"❌ Analysis failed: {analysis_result['error']}"
        else:
            return str(analysis_result)
    
    @staticmethod
    def check_commit_quality(commit_hash="HEAD"):
        """Check commit quality in silent mode"""
        import subprocess
        
        try:
            # Get commit message
            commit_msg = subprocess.check_output(
                ['git', 'log', '--format=%B', '-n', '1', commit_hash],
                stderr=subprocess.STDOUT
            ).decode('utf-8').strip()
            
            # Get commit diff
            commit_diff = subprocess.check_output(
                ['git', 'show', commit_hash, '--format=""'],
                stderr=subprocess.STDOUT
            ).decode('utf-8')
            
            # Analyze
            prompt = f"""Commit message: {commit_msg}
            
Changes: {commit_diff}

Rate this commit quality (1-10) and provide brief feedback:
1. Message clarity
2. Change consistency
3. Overall quality

Provide JSON response with: {{"score": X, "feedback": "brief feedback"}}"""
            
            from vibetrack.local_client import send_to_local_model
            analysis = send_to_local_model(prompt, persian_mode=False)
            
            return {
                "success": True,
                "commit_hash": commit_hash,
                "commit_message": commit_msg,
                "quality_analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "commit_hash": commit_hash,
                "timestamp": datetime.now().isoformat()
            }