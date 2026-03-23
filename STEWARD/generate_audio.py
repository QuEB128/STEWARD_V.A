from gtts import gTTS

phrases = {
    "time": "time",
    "detection": "detection",
    "currency": "currency detection",
    "describe": "describe environment",
    "object": "object detection",
    "text": "text extraction",
    "summarize": "summarize text",
    "read": "Instant read",
    "language": "language selection",
        
    "ready": "camera ready",
    "analyze": "analyzing",
    "details": "select for more details",
}

for name, text in phrases.items():
    tts = gTTS(text=text, lang="en")
    tts.save(f"audio/{name}.mp3")
