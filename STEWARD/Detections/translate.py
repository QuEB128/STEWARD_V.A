import tempfile
import subprocess
from gtts import gTTS
from googletrans import Translator

def read_text(text, lang= 'sw'):
    """
    Convert text to speech using gTTS and play it using mpg123.
    """
    try:
        # Create a temporary MP3 file
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang=lang)
            tts.save(fp.name)
            # Play using mpg123 (already installed)
            subprocess.run(["mpg123", "-q", fp.name], check=True)
    except Exception as e:
        print(f"? Failed to speak: {e}")

def translate_to_swahili(text):
    translator = Translator()
    result = translator.translate(text, src='en', dest='sw')
    return result.text

if __name__ == "__main__":
    user_input = input("Enter text to translate to Swahili: ")
    translated = translate_to_swahili(user_input)
    print("Swahili:", translated)
    read_text(translated)
