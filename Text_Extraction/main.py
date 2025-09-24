import cv2
import pytesseract
import numpy as np
import time
import pyttsx3
from threading import Thread
import enchant
import re

# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Emmanuel Quartey\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Camera setup
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
cap.set(cv2.CAP_PROP_FPS, 30)

# Window setup
cv2.namedWindow('Text Capture', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Text Capture', 800, 600)

# Global variables
last_capture_time = 0
cooldown_period = 3  # seconds
processing = False

# Crop margin (90% center area)
CROP_MARGIN = 0.05  # 5% margin on all sides

def draw_crop_guidelines(frame):
    """Draw visual guidelines showing the crop area"""
    h, w = frame.shape[:2]
    x1 = int(w * CROP_MARGIN)
    x2 = int(w * (1 - CROP_MARGIN))
    y1 = int(h * CROP_MARGIN)
    y2 = int(h * (1 - CROP_MARGIN))
    
    # Draw rectangle
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Draw crosshairs
    center_x, center_y = w//2, h//2
    cv2.line(frame, (center_x, y1), (center_x, y2), (0, 255, 0), 1)
    cv2.line(frame, (x1, center_y), (x2, center_y), (0, 255, 0), 1)
    
    return frame

def filter_text(text):
    """Basic cleanup of OCR output"""
    if not text:
        return ""
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    # Keep letters, numbers, punctuation, file paths
    text = re.sub(r'[^a-zA-Z0-9\s\-\.\',:@/]', '', text)
    
    return text

def speak(text):
    """Threaded text-to-speech"""
    print("\nSpeaking:", text)
    def _speak():
        engine.say(text)
        engine.runAndWait()
    Thread(target=_speak).start()

def preprocess_image(img):
    """Image preprocessing for OCR"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Otsu thresholding (black text on white background)
    _, thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Reduce salt-and-pepper noise
    thresh = cv2.medianBlur(thresh, 3)

    # Save debug image
    cv2.imwrite('debug_preprocessed.jpg', thresh)

    return thresh

def extract_text(img):
    """OCR text extraction"""
    processed_img = preprocess_image(img)
    
    configs = [
        r'--psm 6 --oem 3 -l eng',
        r'--psm 4 --oem 3 -l eng',
        r'--psm 11 --oem 3 -l eng',
        r'--psm 6 --oem 1 -l eng'
    ]
    
    best_text = ""
    for config in configs:
        try:
            text = pytesseract.image_to_string(processed_img, config=config)
            text = filter_text(text)
            if len(text.split()) > len(best_text.split()):
                best_text = text
        except Exception as e:
            print(f"OCR Error with config {config}: {e}")
    
    return best_text.strip()

def filter_english_words(sentence):
    d = enchant.Dict("en_US")
    words = re.findall(r"\b\w+\b", sentence)
    filtered = [
        word for word in words
        if d.check(word) and (len(word) > 1 or word.lower() in ['a', 'i'])
    ]
    return " ".join(filtered)

def capture_and_process(frame):
    global processing, last_capture_time
    
    if processing:
        return
    
    current_time = time.time()
    if current_time - last_capture_time < cooldown_period:
        speak("Please wait before capturing again")
        return
    
    processing = True
    
    # Crop center area (90%)
    h, w = frame.shape[:2]
    cropped = frame[int(h*CROP_MARGIN):int(h*(1-CROP_MARGIN)), 
                    int(w*CROP_MARGIN):int(w*(1-CROP_MARGIN))]
    
    raw_text = extract_text(cropped)
    
    if raw_text:
        print("\n" + "="*40)
        #print("RAW TEXT:\n", raw_text)print("\n\nFiltered TEXT:\n", filter_english_words(raw_text))
        print("="*40)
        speak(raw_text)
    else:
        speak("No readable text detected.")
    
    cv2.imwrite('last_capture.jpg', cropped)
    processing = False
    last_capture_time = current_time

def main():
    speak("Text capture ready. Press space to capture text within the green guide.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Camera error occurred")
            break
        
        frame_with_guides = draw_crop_guidelines(frame.copy())
        cv2.imshow('Text Capture', frame_with_guides)
        
        key = cv2.waitKey(1)
        if key == 32:  # Space
            capture_and_process(frame)
        elif key == ord('q'):
            speak("Exiting application")
            break
        elif key == ord('h'):
            help_msg = "Help: Center text in green area, SPACE to capture, Q to quit"
            print(help_msg)
            speak(help_msg)
    
    cap.release()
    cv2.destroyAllWindows()
    engine.stop()

if __name__ == "__main__":
    main()
