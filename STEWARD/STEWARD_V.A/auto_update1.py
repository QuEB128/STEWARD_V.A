import os
import sys
import subprocess

def check_for_updates():
    try:
        print("🔍 Checking for updates...")

        # First check if we're in a merge state
        merge_state = subprocess.run(['git', 'rev-parse', '--verify', 'MERGE_HEAD'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        
        if merge_state.returncode == 0:
            print("⚠️ Merge in progress detected. Attempting to complete...")
            try:
                # Try to commit the merge automatically
                subprocess.run(['git', 'commit', '--no-edit'], check=True)
                print("✅ Merge completed automatically.")
            except subprocess.CalledProcessError as e:
                print("❌ Could not auto-commit merge. Please resolve conflicts manually.")
                return False

        # Fetch changes from GitHub
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
                print("✅ Update complete. Restarting...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
            except subprocess.CalledProcessError as e:
                print("⚠️ Merge required. Attempting automatic resolution...")
                subprocess.run(['git', 'merge', '--no-edit', 'origin/main'], check=True)
                print("✅ Merge completed. Restarting...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("✅ Already up to date!")
        return True

    except Exception as e:
        print(f"❌ Update check failed: {str(e)}")
        return False

def main():
    print("\n===== STEWARD V.A Starting =====")
    if not check_for_updates():
        print("⚠️ Continuing with existing version (update not applied)")

    # Your normal application code here
    print("\nRunning main application...")
    print("Version: 1.0 - Initial release")

    print("\n===== STEWARD V.A Running =====")
    print("\n✨ New feature added in v1.1!")

if __name__ == "__main__":
    main()
