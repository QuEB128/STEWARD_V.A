import pyttsx3
import keyboard
import threading
import time

# Initialize TTS engine
engine = pyttsx3.init()

# Global flag to stop reading
stop_reading = False

def on_word(name, location, length):
    global stop_reading
    if stop_reading:
        engine.stop()

def read_text(text):
    global stop_reading
    stop_reading = False
    engine.connect('started-word', on_word)  # Check at each word
    engine.say(text)
    engine.runAndWait()

def monitor_escape():
    global stop_reading
    while True:
        if keyboard.is_pressed("esc"):
            stop_reading = True
            break
        time.sleep(0.1)

if __name__ == "__main__":
    text = """This is a test. The program will read this text aloud.
    Press the Escape key anytime to stop the reading immediately. Do you want me to extend this so it reads line by line from a text file (like a book) and lets you stop anytime with Esc?"""

    # Start monitoring Escape key in a thread
    monitor_thread = threading.Thread(target=monitor_escape, daemon=True)
    monitor_thread.start()

    # Start TTS reading
    read_text(text)

    print("Reading stopped.")
