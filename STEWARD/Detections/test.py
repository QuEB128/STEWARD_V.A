import os
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
from PIL import Image
import io
import cv2
import time
import gpiozero
from gpiozero import Button
from picamera2 import Picamera2
import numpy as np

# Initialize the recognizer
recognizer = sr.Recognizer()

led = gpiozero.LED(17)
button1 = Button(5)
button2 = Button(4)
exit_button = Button(2)
status = 0

def read_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
"""

def read_text(text):
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')

    # Try to find a female voice, else default to the first available voice
    female_voice = None
    for voice in voices:
        if "female" in voice.name.lower() or "Zira" in voice.name or "Samantha" in voice.name:
            female_voice = voice.id
            break

    if female_voice:
        engine.setProperty('voice', female_voice)
    else:
        engine.setProperty('voice', voices[0].id)  # Default to first voice if no female voice is found

    engine.setProperty('rate', 150)  # Set speech rate
    engine.say(text)
    engine.runAndWait()
"""

def recognize_speech():
    with sr.Microphone() as source:
        read_text("Please say your command.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        return command
    except sr.UnknownValueError:
        return "hi"
    except sr.RequestError:
        read_text("Sorry, I'm having trouble accessing the Google API.")

def speech_to_text():
    with sr.Microphone() as source:
        read_text("...please say your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        read_text("...analyzing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        read_text("...Sorry, I do not understand you")
        return speech_to_text()
    except sr.RequestError:
        read_text("please make sure you are online")

def wait_with_button_check(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        if button1.is_pressed:
            return "v_select"
        if button2.is_pressed:
            return "b_select"
        if exit_button.is_pressed:
            return "exit"
        time.sleep(0.1)
    return False

def wait_with_button2_check(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        if button2.is_pressed:
            return True
        if exit_button.is_pressed:
            return "exit"
        time.sleep(0.1)
    return False

class STEWARD:
    def __init__(self):
        genai.configure(api_key= "AIzaSyAZqQZuWUhFds_v8rpQhyFneKuHeuoWUdk")  #"AIzaSyAjeGmI6f4vY_QAZX-fdTeYrX00_V2bWBk")  # Replace with your actual API key
        self.directory = 'image_to_examine'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
            ],
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain"
            }
        )
        self.chat_session = self.model.start_chat(history=[])

    def delete_existing_files(self):
        for filename in os.listdir(self.directory):
            os.remove(os.path.join(self.directory, filename))

    '''def captureImg(self):
        status = 0
        read_text("Keep the camera steady before clicking the button...")
        filename = None
        try:
            picam2 = Picamera2()
            #picam2.configure(picam2.create_still_configuration(main={"size": (640, 480)}))
            picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
            picam2.start()
            time.sleep(2)
            while True:
                frame = picam2.capture_array()
                #cv2.imshow("Camera Feed", frame)

                if button2.is_pressed:
                    read_text("...analyzing")
                    self.delete_existing_files()
                    filename = os.path.join(self.directory, 'image.jpg')
                    cv2.imwrite(filename, frame)
                    break
                elif exit_button.is_pressed:
                    return (1)
                    break

                if cv2.waitKey(1) == 27:
                    break
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            picam2.stop()
            picam2.close()

        return filename'''
    def captureImg(self):
        status = 0
        read_text("Keep the camera steady before clicking the button...")
        filename = None
        try:
            picam2 = Picamera2()
            picam2.configure(picam2.create_still_configuration(main={"size": (640, 480)}))
            picam2.start()
            time.sleep(2)
            while True:
                frame = picam2.capture_array()

                if button2.is_pressed:
                    read_text("...analyzing")
                    self.delete_existing_files()
                    filename = os.path.join(self.directory, 'image.jpg')
                    cv2.imwrite(filename, frame)
                    break
                elif exit_button.is_pressed:
                    return 1
                    break

                time.sleep(0.05)  # replaces cv2.waitKey

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            picam2.stop()
            picam2.close()

        return filename


    def load_image(self):
        image_path = os.path.join(self.directory, "image.jpg")
        image = Image.open(image_path).convert("RGB")
        return image

    def describe_image(self):
        led.on()
        status = self.captureImg()
        if status == 1:
            read_text("exiting...")
            led.off()
            return 
        image = self.load_image()
        response = self.chat_session.send_message(image)

        read_text(response.text.replace("*", ""))
        led.off()

    def start_chat(self):
        led.on()
        status = self.captureImg()
        if status == 1:
            read_text("exiting...")
            led.off()
            return 
        image = self.load_image()
        response = self.chat_session.send_message(image)
        response = self.chat_session.send_message("Describe this image briefly and detailed in less than 30 words.")
        resp = response.text.replace("*", "")
        print(resp)
        read_text(resp)
        read_text("click for detailed description.")
        result = wait_with_button2_check(1)
        if result:
            response = self.chat_session.send_message("describe this as though you are a vision assistant to a in less than 100 words")
            resp = response.text.replace("*", "")
            print(resp)
            read_text(resp)
        led.off()
        return True

    def detect_currency(self):
        led.on()
        status = self.captureImg()
        if status == 1:
            read_text("exiting...")
            led.off()
            return 
        image = self.load_image()
        self.chat_session.send_message("detect currency and amount of money in the image and read only that. But if there is now money in the image say 'No money detected'.")
        response = self.chat_session.send_message(image)
        read_text(response.text.replace("*", ""))
        led.off()

    def translate_language(self):
        led.on()
        status = self.captureImg()
        if status == 1:
            read_text("exiting...")
            led.off()
            return 
        image = self.load_image()
        self.chat_session.send_message("translate the text in the image to english . but if there is no text in the image,simply say 'No visibe text detected'")
        response = self.chat_session.send_message(image)
        read_text(response.text.replace("*", ""))
        led.off()

    def chat(self):
        led.on()
        self.chat_session.send_message("hello")
        read_text("... AI mode activated")
        while True:
            text = speech_to_text()
            if any(k in text.lower() for k in ["exit", "back", "return", "quit"]):
                break
            if exit_button.is_pressed:
                break
            elif any(k in text.lower() for k in ["describe", "detect", "read", "image"]):
                self.start_chat()
            else:
                self.chat_session.send_message("generate a short response less than 100 words")
                response = self.chat_session.send_message(text)
                read_text(response.text.replace("*", ""))
        led.off()

    def text_extraction(self):
        led.on()
        status = self.captureImg()
        if status == 1:
            read_text("exiting...")
            led.off()
            return 
        image = self.load_image()
        self.chat_session.send_message("Assume you are an AI designed for an assistive reading device for the visually impaired. Extract the exact text in this image. Do NOT add any additional words.")
        response = self.chat_session.send_message(image)
        read_text(response.text.replace("*", ""))
        led.off()

    def ai_extract_text(self):
        led.on()
        status = self.captureImg()
        if status == 1:
            read_text("exiting...")
            led.off()
            return 
        image = self.load_image()
        self.chat_session.send_message("extract all text")
        response = self.chat_session.send_message(image)
        read_text(response.text.replace("*", ""))
        read_text("You can ask for more details or say return to exit")
        while True:
            text = speech_to_text()
            if any(k in text.lower() for k in ["exit", "back", "return"]):
                break
            response = self.chat_session.send_message(text)
            read_text(response.text.replace("*", ""))
        led.off()

# Entry points
def start_chat():
    chatbot = STEWARD()
    chatbot.start_chat()

def start_plus_chat():
    chatbot = STEWARD()
    chatbot.describe_image()

def chatmain():
    chatbot = STEWARD()
    chatbot.chat()

def translate_language():
    chatbot = STEWARD()
    chatbot.translate_language()

def detect_currency():
    chatbot = STEWARD()
    chatbot.detect_currency()

def ai_extract_text():
    chatbot = STEWARD()
    chatbot.ai_extract_text()

def text_extraction():
    chatbot = STEWARD()
    chatbot.text_extraction()

# Uncomment to run directly:
#start_chat()
