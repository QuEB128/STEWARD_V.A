import os
import sys
import subprocess

def check_for_updates():
    try:
        print("🔍 Checking for updates...")
        
        # Fetch changes from GitHub
        subprocess.run(['git', 'fetch', 'origin'], check=True)
        
        # Compare local and remote versions
        current_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        latest_hash = subprocess.check_output(
            ['git', 'rev-parse', 'origin/main']).decode('utf-8').strip()
        
        print(f"🔄 Current version: {current_hash[:7]}")
        print(f"🆕 Latest version: {latest_hash[:7]}")
        
        if current_hash != latest_hash:
            print("📥 Update available! Pulling changes...")
            subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
            print("✅ Update complete. Restarting...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("✅ Already up to date!")
            
    except Exception as e:
        print(f"❌ Update check failed: {str(e)}")

def main():
    print("\n===== STEWARD V.A Starting =====")
    check_for_updates()
    
    # Your normal application code here
    print("\nRunning main application...")
    print("Version: 1.0 - Initial release")
    
    print("\n===== STEWARD V.A Running =====")

if __name__ == "__main__":
    main()
print("\n✨ New feature added in v1.1!")
