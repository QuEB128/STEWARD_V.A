Perfect! Here’s a **full, corrected, production-ready STEWARD V.A installation and setup guide** including all the fixes, changes, and lessons learned from our chat. I’ve structured it step-by-step from OS installation to a fully functional device ready for scaling.  

---

# **STEWARD V.A – Complete Installation & Setup Guide**

## **1️⃣ Raspberry Pi OS Preparation**

1. **Flash Raspberry Pi OS** (64-bit Debian Bookworm recommended) to SD card using **Raspberry Pi Imager**.
2. Boot the Raspberry Pi with keyboard, mouse, and monitor, or headless with SSH.
3. **Enable SSH** (for remote terminal access):
   ```bash
   sudo raspi-config
   ```
   - Go to **Interface Options → SSH → Enable**
4. **Enable VNC** (for remote GUI access):
   ```bash
   sudo raspi-config
   ```
   - Go to **Interface Options → VNC → Enable**
   - This installs `realvnc-vnc-server`.
5. **Update the system packages:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y git vim wget curl
   ```
6. **Optional: Set hostname** for easy identification on network:
   ```bash
   sudo raspi-config
   ```
   - System Options → Hostname → set `STEWARD_VA`

---

## **2️⃣ Audio Setup**

1. Install audio playback tools:
   ```bash
   sudo apt install -y espeak-ng espeak-ng-data libespeak-ng1 alsa-utils mpg123
   ```
2. Test audio output:
   ```bash
   amixer cset numid=3 1    # Sets audio to HDMI (1) or 2 for 3.5mm jack
   espeak-ng "Hello, STEWARD V.A is alive"
   ```
3. Ensure system volume is not 0%:
   ```bash
   alsamixer
   ```
   - Adjust **Master** volume above 50%
4. **Python TTS options:**  
   - `pyttsx3` defaults to `espeak` on Linux
   - Alternatively, `gTTS` for cloud TTS (requires internet)

---

## **3️⃣ Camera Setup**

1. Install required camera libraries:
   ```bash
   sudo apt install -y libcamera-apps python3-picamera2
   ```
2. Test Picamera2:
   ```bash
   python3 - <<EOF
   from picamera2 import Picamera2
   picam2 = Picamera2()
   picam2.configure(picam2.create_still_configuration())
   picam2.start()
   img = picam2.capture_array()
   print("Camera OK")
   EOF
   ```
3. Fix **numpy incompatibility**:  
   ```bash
   pip install --upgrade numpy
   pip install opencv-python
   ```
4. Use **still capture mode** for images (no GUI needed):
   ```python
   picam2.configure(picam2.create_still_configuration(main={"size": (640,480)}))
   ```

---

## **4️⃣ Python Virtual Environment**

1. Create venv for STEWARD V.A:
   ```bash
   cd ~/STEWARD_V.A
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install required Python libraries (updated versions):
   ```bash
   pip install numpy opencv-python pillow pyttsx3 gtts playsound speechrecognition gpiozero google-genai
   ```
3. Optional: test TTS:
   ```python
   from gtts import gTTS
   import os
   tts = gTTS("Hello, STEWARD V.A is alive")
   tts.save("test.mp3")
   os.system("mpg123 test.mp3")
   ```

---

## **5️⃣ Gemini AI SDK Configuration**

1. Set the Gemini API key in `.bashrc` for persistent access:
   ```bash
   nano ~/.bashrc
   ```
   Add:
   ```bash
   export GEMINI_API_KEY="YOUR_API_KEY_HERE"
   ```
   - Replace `YOUR_API_KEY_HERE` with your actual key.
   ```bash
   source ~/.bashrc
   ```
2. Test Gemini SDK:
   ```python
   import google.genai as genai
   genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
   print("Gemini API configured successfully")
   ```

---

## **6️⃣ STEWARD V.A Software Setup**

1. Clone or update the repository:
   ```bash
   git clone https://github.com/QuEB128/STEWARD_V.A.git
   cd STEWARD_V.A
   source venv/bin/activate
   ```
2. Ensure correct Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Test basic script:
   ```bash
   python test1.py
   ```
   - Check: TTS, camera capture, buttons, and Gemini API

---

## **7️⃣ Button & GPIO Configuration**

1. Buttons wired to GPIO pins:
   - Button1: GPIO5
   - Button2: GPIO4
   - Exit button: GPIO2
2. LED indicator: GPIO17
3. Python library: `gpiozero` handles debouncing and state checking.

---

## **8️⃣ Systemd Service (Optional, Auto-start)**

1. Create service file for STEWARD V.A:
   ```bash
   sudo nano /etc/systemd/system/stewardva.service
   ```
   ```ini
   [Unit]
   Description=STEWARD V.A AI Assistant
   After=network.target

   [Service]
   ExecStart=/home/pi/STEWARD_V.A/venv/bin/python /home/pi/STEWARD_V.A/STEWARD/Detections/test1.py
   WorkingDirectory=/home/pi/STEWARD_V.A
   StandardOutput=inherit
   StandardError=inherit
   Restart=always
   User=pi

   [Install]
   WantedBy=multi-user.target
   ```
2. Enable and start service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable stewardva.service
   sudo systemctl start stewardva.service
   sudo systemctl status stewardva.service
   ```

---

## **9️⃣ Final Testing Checklist**

- [ ] Audio TTS works (espeak-ng / gTTS)
- [ ] Camera captures images correctly
- [ ] Buttons respond (Button1, Button2, Exit)
- [ ] LED indicators work
- [ ] Gemini AI chat responds correctly
- [ ] Python scripts run inside virtual environment
- [ ] VNC allows remote GUI access
- [ ] Optional systemd service auto-starts on boot

---

✅ **Ready for Market Deployment**

This flow includes all fixes we encountered:  

- numpy / Picamera2 incompatibility resolved  
- pyttsx3 espeak vs gTTS TTS workaround  
- Audio volume & playback fixes  
- Gemini API new SDK & API key environment variable  
- VNC for GUI remote access  
- Systemd service for automatic startup  

---

If you want, I can **also make a diagram/flowchart of this process** for training manuals or investor documentation — that usually helps production teams understand the ex