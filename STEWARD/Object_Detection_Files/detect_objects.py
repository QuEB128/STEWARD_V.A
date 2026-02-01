import cv2
import pyttsx3
import os
import time
import subprocess

# ================== TTS ==================
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("SPEAK:", text)
    engine.say(text)
    engine.runAndWait()

# ================== DIRECTORY ==================
directory = 'ImgExtractObj'
os.makedirs(directory, exist_ok=True)
IMAGE_PATH = os.path.join(directory, "image.jpg")

def delete_existing_files():
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        os.remove(file_path)

# ================== RPICAM CAPTURE ==================

def captureImg():
    speak("Camera ready")
    time.sleep(1)  # allow sensor + ISP to stabilise

    delete_existing_files()

    cmd = [
        "rpicam-still",
        "-o", IMAGE_PATH,
        "--timeout", "1",
        "--nopreview",
        "--immediate"
    ]

    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        speak("Camera error")
        print(e)
        return None

    print(f"Image saved as: {IMAGE_PATH}")
    return IMAGE_PATH

# ================== OBJECT DETECTION ==================

classNames = []
classFile = "/home/pi/STEWARD_V.A/STEWARD/Object_Detection_Files/coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/pi/STEWARD_V.A/STEWARD/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/STEWARD_V.A/STEWARD/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img, thres=0.45, nms=0.2, draw=True):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    objectInfo = {}

    if len(classIds) != 0:
        for classId, confidence, box in zip(
            classIds.flatten(), confs.flatten(), bbox
        ):
            className = classNames[classId - 1]

            if className in objectInfo:
                objectInfo[className] += 1
            else:
                objectInfo[className] = 1

            if draw:
                cv2.rectangle(img, box, (0, 255, 0), 2)
                cv2.putText(
                    img,
                    className.upper(),
                    (box[0] + 10, box[1] + 30),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1, (0, 255, 0), 2
                )

    return img, objectInfo

# ================== MAIN PIPELINE ==================

def main(image_path):
    img = cv2.imread(image_path)
    if img is None:
        speak("Failed to read image")
        return

    result, objectInfo = getObjects(img)

    if objectInfo:
        speak("Objects detected")
        for obj, count in objectInfo.items():
            print(obj, count)
            speak(obj)
            speak(str(count))
    else:
        speak("No objects detected")

    #cv2.imshow("STEWARD Vision", result)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

def detectImg():
    speak("Keep the camera steady")
    image_path = captureImg()
    if image_path:
        speak("Analyzing image")
        main(image_path)

# ================== ENTRY ==================
'''
if __name__ == "__main__":
    while True:
        detectImg()
        speak("Scan complete. Waiting.")
        time.sleep(2)'''
