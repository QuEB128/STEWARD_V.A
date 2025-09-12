from gtts import gTTS
import tempfile
import os
from playsound import playsound

# Hausa text
text = '''Sannu! Yaya kake?
	hello wannan gwaji ne na "mataimakin hangen nesa" ko za ku iya gaya mani game da abin da kuke bukata in yi?'''
# Convert text to speech
tts = gTTS(text=text, lang="ha")

# Save to a temporary file and play
with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
    temp_path = fp.name
    tts.save(temp_path)

# Play the audio
playsound(temp_path)

# Clean up temp file
os.remove(temp_path)
