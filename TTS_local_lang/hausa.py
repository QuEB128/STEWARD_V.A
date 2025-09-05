from gtts import gTTS

text = "Sannu! Yaya kake?"
tts = gTTS(text=text, lang="ha")
tts.save("hausa.mp3")
print("✅ Hausa audio saved as hausa.mp3")
