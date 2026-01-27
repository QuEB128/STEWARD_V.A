"""
STEWARD VISION ASSISTANT 1.5
Main Controller Module
Clean, optimized, and professional rewrite.
"""

import io
import os
import time
import pygame
import speech_recognition as sr
from gtts import gTTS, gTTSError
import pyttsx3

import lib
from gpiozero import Button
from datetime import datetime

# ---------------------------
# HARDWARE CONFIG
# ---------------------------
led = lib.test.led
button1 = lib.test.button1     # Voice-select mode
button2 = lib.test.button2     # Button-select mode
exit_button = lib.test.exit_button
# ---------------------------
# TTS ENGINE SETUP
# ---------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# ---------------------------
# SPEAK FUNCTION (core)
# ---------------------------
def speak(text: str):
    """Text-to-speech wrapper"""
    engine.say(text)
    engine.runAndWait()

from datetime import datetime

def tell_time():
    now = datetime.now()
    speak(f"it is {now.hour} : {now.minute:02d}")


# ---------------------------
# GOOGLE TTS (online voice)
# ---------------------------
def text_to_speech():
    """Play a demo sentence using Google TTS with pygame controls."""
    text = "This is a sample of Steward Vision Assistant voice for online features."
    if not text.strip():
        print("Empty TTS text.")
        return

    try:
        # Generate audio in memory
        tts = gTTS(text=text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Hidden window
        pygame.display.set_mode((1, 1), pygame.NOFRAME)
        pygame.display.set_caption("TTS Player")

        pygame.mixer.music.load(mp3_fp, "mp3")
        pygame.mixer.music.play()

        paused = False
        running = True
        print("Playing audio... SPACE = pause/unpause | ESC = stop")

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                        pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()
                        print("Paused" if paused else "Resumed")

                    elif event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        running = False

            if not pygame.mixer.music.get_busy() and not paused:
                running = False

            time.sleep(0.05)

        pygame.quit()
        print("TTS playback finished.")

    except gTTSError:
        speak("Sorry, please check your internet connection.")
    except Exception as e:
        print(f"TTS Error: {e}")
        pygame.quit()



# ---------------------------
# SPEECH RECOGNITION
# ---------------------------
def speech_to_text() -> str:
    """Convert microphone speech to text using Google"""
    with sr.Microphone() as source:
        speak("Please say your command.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        speak("Analyzing.")
        return recognizer.recognize_google(audio)

    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""

    except sr.RequestError:
        speak("Please make sure you are online.")
        return ""

LANGUAGES = {
    "English": "en",
    "French": "fr",
    "Swahili": "sw",
    "Hausa": "ha"
}

def select_language():
    """Allow user to select language via buttons."""
    languages = [
        ("English", "en"),
        ("French", "fr"),
        ("Swahili", "sw"),
        ("Hausa", "ha")
    ]

    speak("Language selection mode activated:")

    for lang_name, lang_code in languages:
        speak(lang_name)
        result = wait_for_button(button2, 1.5)  # Wait 1.5s for button2 press
        if result:
            # Confirm selection
            speak(f"You selected {lang_name}. Press again to confirm.")
            confirm = wait_for_button(button2, 2.0)  # Wait 2s for confirmation
            if confirm:
                # Save selected language
                with open(os.path.join(os.path.dirname(__file__), "Detections/lang.txt"), "w") as f:
                    f.write(lang_code)
                speak(f"{lang_name} set as your preferred language.")
                return lang_code
        # Optional small pause before moving to next language
        time.sleep(0.2)

    # If no selection made
    speak("No language selected. Defaulting to English.")
    with open(os.path.join(os.path.dirname(__file__), "Detections/lang.txt"), "w") as f:
        f.write("en")
    return "en"



# ---------------------------
# TASK FUNCTIONS
# ---------------------------
'''def update_reminder():
    lib.Reminder_Update.reminder_options()

def check_schedule():
    lib.Reminder.main()

def extract_text():
    speak("Keep camera steady before pressing the button.")
    lib.Main.TextExtractor().main()

def img_extractor():
    speak("Extracting text from image. Please wait.")
    lib.Image_txt_extract.ImgTextExtractor().main()

def detect_motion():
    speak("Detecting motion.")
    lib.Motion_Detection.LiveImageDetector().detect_live_images()

def detect_color():
    speak("Detecting colors.")
    lib.Colour_Detection.ColorDetector().detect_colors()

def detect_object():
    speak("Detecting objects.")
    lib.object_ident().main()

def shot_detect_obj():
    speak("Analyzing image for objects.")
    lib.detectObjFromImg.detectImg()
'''

def gemini_ai():
    lib.test.start_chat()

def gemini_ai_voice():
    lib.test.start_plus_chat()

def gemini_Chat():
    lib.test.chatmain()

def translate_text():
    lib.test.translate_language()

def currency_detect():
    lib.test.detect_currency()

def ai_extract_text():
    lib.test.text_extraction()

def ai_extract_text_voice():
    lib.test.ai_extract_text()

# --------------------------
# HELPER FUNCTIONS
# ---------------------------
def wait_with_button_check(duration: float):
    """Wait some seconds and return which button was pressed."""
    start = time.time()
    while time.time() - start < duration:
        if button1.is_pressed: return "v_select"
        if button2.is_pressed: return "b_select"
        if exit_button.is_pressed: return "exit"
        time.sleep(0.1)
    return False


def wait_for_button(button, duration: float):
    """Wait for a specific button press."""
    start = time.time()
    while time.time() - start < duration:
        if button.is_pressed: return True
        if exit_button.is_pressed: return "exit"
        time.sleep(0.1)
    return False


# ---------------------------
# BUTTON MODE LOGIC
# ---------------------------
'''def button_selection_mode():
    """Main menu navigation via button mode."""
    speak("Button select mode activated.")

    while True:
        led.off()
        speak("Options.")

        # Time
        speak("Tell time.")
        if wait_for_button(button2, 1.5):  
            tell_time()

        # Detection features
        speak("Detection features.")
        if wait_for_button(button2, 1.5):

            speak("Detect currency.")
            if wait_for_button(button2, 1.5):
                currency_detect()

            speak("Describe environment.")
            if wait_for_button(button2, 1.5):
                gemini_ai()

            speak("Object detection.")
            if wait_for_button(button2, 1.5):
                shot_detect_obj()

        # Text extraction
        speak("Text extraction.")
        if wait_for_button(button2, 1.5):

            speak("Online read.")
            if wait_for_button(button2, 1.5):
                text_to_speech()

            speak("Instant read.")
            if wait_for_button(button2, 1.5):
                ai_extract_text()
'''

def button_selection_mode():
    speak("...button select mode activated...")

    while True:
        led.off()
        speak("...options...")

        # === OPTION 1 ===
        speak("...tell time...")
        if wait_for_button(button2, 1.5):
            tell_time()

        # === GROUP 2 ===
        speak("...detection features...")
        result = wait_for_button(button2, 1.5)
        if result:
            speak("...detect currency...")
            if wait_for_button(button2, 1.5):
                currency_detect()

            speak("...describe environment...")
            if wait_for_button(button2, 1.5):
                gemini_ai()

            speak("...object detection...")
            if wait_for_button(button2, 1.5):
                #shot_detect_obj() 
                print("detect object")

        # === GROUP 3 ===
        speak("...Text extraction...")
        result = wait_for_button(button2, 1.5)
        if result:
            speak("...Online read...")
            if wait_for_button(button2, 1.5):
                text_to_speech()

            speak("...instant read...")
            if wait_for_button(button2, 1.5):
                ai_extract_text()

        # === LANGUAGE SELECTION ===
        speak("Select language for assistant.")
        if wait_for_button(button2, 1.5):
            select_language()

        # ------------------------------------
        # ? AFTER ALL OPTIONS: WAIT HERE
        # ------------------------------------
        speak("Press the select button to hear options again.")
        while True:
            if button2.is_pressed:
                break
            if exit_button.is_pressed:
                speak("Exiting button selection mode.")
                return
            time.sleep(0.1)



# ---------------------------
# MAIN PROGRAM LOOP (OPTIONAL)
# ---------------------------
def main():
    speak("Steward Vision Assistant is ready.")

    while True:
        press = wait_with_button_check(0.5)

        if press == "v_select":
            speak("Voice mode activated.")
            cmd = speech_to_text()
            print("VOICE CMD:", cmd)

        elif press == "b_select":
            button_selection_mode()

        elif press == "exit":
            speak("Steward vision assistant on standby....")


if __name__ == "__main__":
    main()

led.close()
button1.close()
button2.close()
exit_button.close()
