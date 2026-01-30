import os
import time
import io

import pyttsx3
import speech_recognition as sr
from gpiozero import Button, LED

from PIL import Image
import cv2
import numpy as np
from picamera2 import Picamera2

from google import genai
from deep_translator import GoogleTranslator
from gtts import gTTS
import subprocess
import tempfile


# =========================
# HARDWARE SETUP
# =========================
led = LED(17)
button1 = Button(5)
button2 = Button(4)
exit_button = Button(2)

# =========================
# SPEECH SETUP
# =========================
recognizer = sr.Recognizer()

IMAGE_PATH = "image_to_examine/image.jpg"
'''def read_text(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()'''
    

'''      
def read_text(text, lang='en'):
    
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang=lang)
            tts.save(fp.name)

            # Start audio playback
            process = subprocess.Popen(
                ["mpg123", "-q", fp.name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Monitor button while audio is playing
            while process.poll() is None:
                if exit_button.is_pressed:
                    print("Button pressed stopping speech")
                    process.terminate()
                    break
                time.sleep(0.05)

    except Exception as e:
        print(f"? Failed to speak: {e}") '''

def read_text(text):
    try:
        # =========================
        # READ LANGUAGE CODE
        # =========================
        lang_file = os.path.join(os.path.dirname(__file__), "lang.txt")
        lang_code = None

        if os.path.exists(lang_file):
            with open(lang_file, "r") as f:
                code = f.read().strip().lower()
                if code:
                    lang_code = code

        # =========================
        # TRANSLATE (IF NEEDED)
        # =========================
        if lang_code:
            try:
                spoken_text = GoogleTranslator(source='en', target=lang_code).translate(text)
                tts_lang = lang_code
                print(f"Translated ({lang_code}): {spoken_text}")
            except Exception as e:
                print(f"? Translation failed, speaking English: {e}")
                spoken_text = text
                tts_lang = "en"
        else:
            spoken_text = text
            tts_lang = "en"
            print("No language set speaking English")

        # =========================
        # TEXT TO SPEECH
        # =========================
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
            tts = gTTS(text=spoken_text, lang=tts_lang)
            tts.save(fp.name)

            process = subprocess.Popen(
                ["mpg123", "-q", fp.name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # =========================
            # BUTTON INTERRUPT
            # =========================
            while process.poll() is None:
                if exit_button.is_pressed:
                    print("?? Button pressed stopping speech")
                    process.terminate()
                    break
                time.sleep(0.05)

    except Exception as e:
        print("? Error:", e)



def speech_to_text():
    with sr.Microphone() as source:
        read_text("Please say your command")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        read_text("Sorry, I did not understand")
        return ""
    except sr.RequestError:
        read_text("Network error")
        return ""

def wait_with_button2_check(duration):
    start = time.time()
    while time.time() - start < duration:
        if button2.is_pressed:
            return True
        if exit_button.is_pressed:
            return "exit"
        time.sleep(0.1)
    return False

# =========================
# STEWARD CLASS
# =========================
class STEWARD:
    def __init__(self):
        # Gemini client (NEW SDK)
        self.client = genai.Client(
            api_key= "AIzaSyDxoA34W61H363zaYzASrkIedgByeGEsCU"  #os.getenv("GEMINI_API_KEY")
        )

        self.model_name = "gemini-2.5-flash"

        self.image_dir = "image_to_examine"
        os.makedirs(self.image_dir, exist_ok=True)

    # -------------------------
    # CAMERA
    # -------------------------
    def delete_existing_files(self):
        for f in os.listdir(self.image_dir):
            os.remove(os.path.join(self.image_dir, f))

    #IMAGE_PATH = "image_to_examine/image.jpg"

    def capture_image_rpicam(self):
        os.makedirs("image_to_examine", exist_ok=True)

        # Small delay to allow camera auto-exposure
        time.sleep(1)

        cmd = [
            "rpicam-still",
            "-o", IMAGE_PATH,
            "--timeout", "1",
            "--nopreview",
            "--immediate"
        ]

        subprocess.run(cmd, check=True)
        return IMAGE_PATH

    def capture_image(self):
        read_text("CAMERA READY")
        '''filename = None

        picam2 = Picamera2()
        picam2.configure(
            picam2.create_still_configuration(main={"size": (640, 480)})
        )
        picam2.start()
        time.sleep(2)'''

        try:
            while True:
                #frame = picam2.capture_array()

                if button2.is_pressed:
                    #read_text("Capturing image")
                    self.delete_existing_files()
                    #filename = os.path.join(self.image_dir, "image.jpg")
                    #cv2.imwrite(filename, frame)
                    filename = self.capture_image_rpicam()
                    read_text("Analyzing image")
                    #break
                    return filename

                if exit_button.is_pressed:
                    return None

                time.sleep(0.05)

        finally:
            print("done")
            '''picam2.stop()
            picam2.close()'''

        #return None #filename

    def load_image(self):
        path = os.path.join(self.image_dir, "image.jpg")
        return Image.open(path).convert("RGB")

    # -------------------------
    # GEMINI HELPERS
    # -------------------------
    def gemini_image_prompt(self, image, prompt):
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt, image]
        )
        return response.text.replace("*", "")

    # -------------------------
    # FEATURES
    # -------------------------
    def describe_image(self):
        led.on()
        if not self.capture_image():
            led.off()
            return

        image = self.load_image()
        text = self.gemini_image_prompt(
            image,
            "Describe this image clearly for a visually impaired person.(in less than 50 words)"
        )
        read_text(text)
        led.off()

    def start_chat(self):
        led.on()
        if not self.capture_image():
            led.off()
            return

        image = self.load_image()
        short_desc = self.gemini_image_prompt(
            image,
            "Describe this image in less than 30 words."
        )

        read_text(short_desc)
        read_text("Press the button for more details.")

        if wait_with_button2_check(2):
            detailed = self.gemini_image_prompt(
                image,
                "Describe this image in detail as a vision assistant. (in less than 100 words)"
            )
            read_text(detailed)

        led.off()


    def detect_currency(self):
        led.on()
        if not self.capture_image():
            led.off()
            return

        image = self.load_image()
        text = self.gemini_image_prompt(
            image,
            "Detect currency and amount(example: 20 ghana cedis). If none, say 'No money detected'."
        )
        read_text(text)
        led.off()

    def translate_language(self):
        led.on()
        if not self.capture_image():
            led.off()
            return

        image = self.load_image()
        text = self.gemini_image_prompt(
            image,
            "Translate any visible text to English. If none, say 'No visible text detected'."
        )
        read_text(text)
        led.off()

    def extract_text_exact(self):
        led.on()
        if not self.capture_image():
            led.off()
            return

        image = self.load_image()
        text = self.gemini_image_prompt(
            image,
            "Extract the exact text in this image. Do not add words."
        )
        read_text(text)
        led.off()
    def summarize_text(self):
        led.on()
        if not self.capture_image():
            led.off()
            return

        image = self.load_image()
        text = self.gemini_image_prompt(
            image,
            "summarize the exact text in this image as brief as possible."
        )
        read_text(text)
        led.off()
        
    

    def chat_mode(self):
        led.on()
        read_text("AI mode activated")

        while True:
            #user_text = speech_to_text().lower()
            user_text = input(">> ").lower()

            if any(k in user_text for k in ["exit", "quit", "back"]):
                break

            if any(k in user_text for k in ["describe", "image", "see"]):
                self.start_chat()
            else:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_text
                )
                read_text(response.text.replace("*", ""))

        led.off()

    def ai_extract_text(self):
        led.on()
        status = self.captureImg()
        if status == 1:
            read_text("exiting...")
            led.off()
            return 
        image = self.load_image()
        self.chat_session.send_message("extract all text")
        response = self.chat_session.send_message(image)
        read_text(response.text.replace("*", ""))
        read_text("You can ask for more details or say return to exit")
        while True:
            text = speech_to_text()
            if any(k in text.lower() for k in ["exit", "back", "return"]):
                break
            response = self.chat_session.send_message(text)
            read_text(response.text.replace("*", ""))
        led.off()

# =========================
# ENTRY POINTS
# =========================
def start_chat():
    STEWARD().start_chat()

def start_plus_chat():
    STEWARD().describe_image()

def detect_currency():
    STEWARD().detect_currency()

def translate_language():
    STEWARD().translate_language()

def chatmain():
    STEWARD().chat_mode()

def ai_extract_text():
    STEWARD().ai_extract_text()

def text_extraction():
    STEWARD().extract_text_exact()
    
def summarize_text():
    STEWARD().summarize_text()

# =========================
# RUN
# =========================
#if __name__ == "__main__":
#    chat()

