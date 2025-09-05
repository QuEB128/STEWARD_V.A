from gtts import gTTS
import os

# French text
text = "Bonjour, je suis un programme Python qui parle français."

# Convert text to speech
tts = gTTS(text=text, lang='fr')

# Save as mp3
tts.save("output.mp3")

# Play the audio (Windows)
os.system("start output.mp3")

# For Linux/macOS, replace with:
# os.system("xdg-open output.mp3")
