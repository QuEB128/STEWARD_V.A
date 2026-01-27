import tempfile
import subprocess
import time
import os
from gtts import gTTS
from googletrans import Translator
from gpiozero import Button

# =========================
# GPIO SETUP
# =========================
exit_button = Button(2, pull_up=True)

# =========================
# READ LANGUAGE CODE
# =========================

def translate_and_read(text):
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
            translator = Translator()
            spoken_text = translator.translate(
                text, src="en", dest=lang_code
            ).text
            tts_lang = lang_code
            print(f"Translated ({lang_code}): {spoken_text}")
        else:
            spoken_text = text
            tts_lang = "en"
            print("No language set ? Speaking English")

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

if __name__ == "__main__":
    user_input = input("Enter English text: ")
    translate_and_read(user_input)
