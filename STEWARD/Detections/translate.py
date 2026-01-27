import tempfile
import subprocess
import time
from gtts import gTTS
from googletrans import Translator
from gpiozero import Button

# =========================
# GPIO SETUP
# =========================
exit_button = Button(2, pull_up=True)

# =========================
# TRANSLATE + SPEAK
# =========================
def translate_and_read(text, lang_code):
    """
    Translates English text to the given language code
    and speaks it using gTTS.
    Reading stops if GPIO 2 button is pressed.
    """
    try:
        # Translate
        translator = Translator()
        translated = translator.translate(text, src='en', dest=lang_code).text
        print(f"Translated ({lang_code}):", translated)

        # Text-to-speech
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
            tts = gTTS(text=translated, lang=lang_code)
            tts.save(fp.name)

            process = subprocess.Popen(
                ["mpg123", "-q", fp.name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Monitor button while speaking
            while process.poll() is None:
                if exit_button.is_pressed:
                    print("?? Button pressed stopping speech")
                    process.terminate()
                    break
                time.sleep(0.05)

    except Exception as e:
        print("? Error:", e)

# =========================
# TEST
# =========================
if __name__ == "__main__":
    user_input = input("Enter English text: ")
    translate_and_read(user_input, "sw")  # sw = Swahili
