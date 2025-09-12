import subprocess
import time

# Replace with your Bluetooth device's MAC address
DEVICE_MAC = "XX:XX:XX:XX:XX:XX"

def bt_run(cmd):
    """Helper to run bluetoothctl command"""
    return subprocess.run(
        f"echo '{cmd}' | bluetoothctl", 
        shell=True, capture_output=True, text=True
    )

def connect_device(mac):
    print("🔵 Starting Bluetooth setup...")

    # Turn on Bluetooth
    bt_run("power on")
    bt_run("agent on")
    bt_run("default-agent")

    # Start scanning
    print("🔍 Scanning for devices...")
    bt_run("scan on")
    time.sleep(5)  # wait a bit for device to show up
    bt_run("scan off")

    # Pair device
    print(f"🔗 Pairing with {mac}...")
    result = bt_run(f"pair {mac}")
    if "Failed" in result.stdout:
        print("❌ Pairing failed:", result.stdout)
        return

    # Trust device (so we don’t need to confirm again later)
    bt_run(f"trust {mac}")

    # Connect device
    print(f"📡 Connecting to {mac}...")
    result = bt_run(f"connect {mac}")
    if "Failed" in result.stdout:
        print("❌ Connection failed:", result.stdout)
    else:
        print(f"✅ Connected to {mac}")

if __name__ == "__main__":
    connect_device(DEVICE_MAC)
