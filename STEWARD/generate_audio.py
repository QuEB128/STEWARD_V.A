"""from gtts import gTTS

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
    "no_internet": "Please connect to the internet to use this feature",
    "sys_ready": "Steward vision assistant is ready"
}

for name, text in phrases.items():
    tts = gTTS(text=text, lang="en")
    tts.save(f"audio/{name}.mp3")
"""


from gtts import gTTS
import subprocess
import os

phrases = {
    "time": "time",
    "detection": "detection",
    "currency": "currency detection",
    "describe": "describe environment",
    "object": "object detection",
    "text": "text extraction",
    "summarize": "summarize text",
    "read": "Instant read",
    "docs": "Documents",
    "language": "language selection",

    "ready": "camera ready",
    "reader": "activated",
    "no_doc": "No documents found.",
    "no_text": "No text documents available.",
    "selected": "selected",
    "analyze": "analyzing",
    "details": "select for more details",
    "no_internet": "Please connect to the internet to use this feature",
    "sys_ready": "Steward vision assistant is ready"
}

# Make sure the audio folder exists
os.makedirs("audio", exist_ok=True)

# Playback speed
SPEED = "1.35"      # Try 1.2, 1.3, 1.4 or 1.5

for name, text in phrases.items():
    print(f"Generating {name}.mp3...")

    temp_file = f"audio/{name}_temp.mp3"
    final_file = f"audio/{name}.mp3"

    # Generate normal speech
    tts = gTTS(text=text, lang="en")
    tts.save(temp_file)

    # Speed it up using ffmpeg
    subprocess.run(
        [
            "ffmpeg",
            "-loglevel", "quiet",
            "-y",
            "-i", temp_file,
            "-filter:a", f"atempo={SPEED}",
            final_file
        ],
        check=True
    )

    # Remove temporary file
    os.remove(temp_file)

print("All audio files generated successfully!")
