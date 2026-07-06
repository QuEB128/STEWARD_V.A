import os
import requests

# ============================================
# GitHub Configuration
# ============================================

OWNER = "QuEB128"
REPO = "mobile-file-storage"
BRANCH = "main"

# Folder inside the GitHub repository
REMOTE_FOLDER = "uploads"

# Folder on the Raspberry Pi
LOCAL_FOLDER = "Docs"

# ============================================
# Download Function
# ============================================

def download_repo_folder():

    print("===================================")
    print(" STEWARD Cloud Synchronization")
    print("===================================")

    os.makedirs(LOCAL_FOLDER, exist_ok=True)

    api_url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/contents/{REMOTE_FOLDER}?ref={BRANCH}"
    )

    try:
        response = requests.get(api_url, timeout=15)

    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return

    if response.status_code != 200:
        print(f"GitHub Error ({response.status_code})")
        print(response.text)
        return

    files = response.json()

    if not files:
        print("No files found.")
        return

    downloaded = 0
    skipped = 0

    for item in files:

        if item["type"] != "file":
            continue

        filename = item["name"]
        download_url = item["download_url"]

        local_path = os.path.join(LOCAL_FOLDER, filename)

        # Skip existing files
        if os.path.exists(local_path):
            print(f"Skipping: {filename} (already exists)")
            skipped += 1
            continue

        print(f"Downloading: {filename}")

        try:
            file_response = requests.get(download_url, timeout=30)

            if file_response.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(file_response.content)

                downloaded += 1
                print("Done.")

            else:
                print(f"Failed ({file_response.status_code})")

        except requests.exceptions.RequestException as e:
            print(f"Download failed: {e}")

    print("\n===================================")
    print("Synchronization Complete")
    print(f"Downloaded : {downloaded}")
    print(f"Skipped    : {skipped}")
    print("===================================")


# ============================================
# Run
# ============================================

if __name__ == "__main__":
    download_repo_folder()
