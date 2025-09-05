from gtts import gTTS

text = "Habari yako rafiki?"
tts = gTTS(text=text, lang="sw")
tts.save("swahili.mp3")
print("✅ Swahili audio saved as swahili.mp3")
