import subprocess
import keyboard
import threading
import time

# Global variable for the espeak process
espeak_process = None

def speak_text(text):
    global espeak_process
    # Start espeak as a subprocess
    espeak_process = subprocess.Popen(['espeak', text])

def monitor_escape():
    global espeak_process
    while True:
        if keyboard.is_pressed("esc"):
            if espeak_process:
                espeak_process.terminate()  # stop espeak
                print("Stopped reading (ESC pressed).")
                break
        time.sleep(0.1)

if __name__ == "__main__":
    text = """This is a test of the espeak TTS system.
    Press the Escape key anytime to stop reading immediately."""

    # Start monitoring Esc in background
    monitor_thread = threading.Thread(target=monitor_escape, daemon=True)
    monitor_thread.start()

    # Start espeak reading
    speak_text(text)

    # Wait for espeak to finish (unless stopped)
    if espeak_process:
        espeak_process.wait()
