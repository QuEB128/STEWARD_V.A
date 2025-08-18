import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuration
REPO_URL = "https://github.com/QuEB128/STEWARD_V.A"
DEFAULT_REPO_NAME = "STEWARD_V.A"
UPDATE_SCRIPT = "auto_update.py"

def get_script_dir():
    """Get the directory where this script is located"""
    return Path(os.path.dirname(os.path.abspath(__file__)))

def is_git_repo(path):
    """Check if a directory is a git repository"""
    try:
        return subprocess.run(['git', '-C', str(path), 'rev-parse', '--is-inside-work-tree'],
                            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
    except subprocess.CalledProcessError:
        return False

def clone_repository():
    """Clone the repository if it doesn't exist"""
    script_dir = get_script_dir()
    repo_path = script_dir / DEFAULT_REPO_NAME
    
    print(f"🔍 Repository not found. Cloning {REPO_URL}...")
    try:
        subprocess.run(['git', 'clone', REPO_URL, str(repo_path)], check=True)
        print(f"✅ Successfully cloned repository to {repo_path}")
        return repo_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone repository: {e}")
        return None

def ensure_repository():
    """Ensure we're working in the correct repository"""
    script_dir = get_script_dir()
    
    # Case 1: Already in the repository
    if is_git_repo(script_dir):
        return script_dir
    
    # Case 2: Repository exists as subdirectory
    repo_path = script_dir / DEFAULT_REPO_NAME
    if repo_path.exists() and is_git_repo(repo_path):
        return repo_path
    
    # Case 3: Need to clone repository
    cloned_path = clone_repository()
    if cloned_path:
        return cloned_path
    
    # Fallback: Use current directory without git functionality
    print("⚠️ Continuing in standalone mode without update capabilities")
    return script_dir

def check_for_updates(repo_path):
    """Check for and apply updates"""
    try:
        print("🔍 Checking for updates...")
        
        # Change to repository directory
        os.chdir(str(repo_path))
        
        # Fetch updates
        subprocess.run(['git', 'fetch', 'origin'], check=True)
        
        # Compare versions
        current_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        latest_hash = subprocess.check_output(['git', 'rev-parse', 'origin/main']).decode('utf-8').strip()

        print(f"🔄 Current version: {current_hash[:7]}")
        print(f"🆕 Latest version: {latest_hash[:7]}")

        if current_hash != latest_hash:
            print("📥 Update available! Pulling changes...")
            try:
                subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
                print("✅ Update complete.")
                return True
            except subprocess.CalledProcessError:
                print("⚠️ Merge required. Attempting automatic resolution...")
                subprocess.run(['git', 'merge', '--no-edit', 'origin/main'], check=True)
                print("✅ Merge completed.")
                return True
        else:
            print("✅ Already up to date!")
            return False

    except Exception as e:
        print(f"❌ Update check failed: {str(e)}")
        return False

def restart_application():
    """Restart the application after update"""
    python = sys.executable
    os.execl(python, python, *sys.argv)

def main():
    print("\n===== STEWARD V.A Starting =====")
    
    # Ensure we have the repository
    repo_path = ensure_repository()
    
    # Check for updates if in a git repo
    if is_git_repo(repo_path):
        if check_for_updates(repo_path):
            print("🔄 Restarting to apply updates...")
            restart_application()
    
    # Your normal application code here
    print("\nRunning main application...")
    print("Version: 1.0 - Initial release")
    print("\n===== STEWARD V.A Running =====")
    print("\n✨ New feature added in v1.1!")

if __name__ == "__main__":
    main()
