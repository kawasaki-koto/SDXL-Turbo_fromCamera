import pyautogui as pag
import cv2
from PIL import Image

cap = cv2.VideoCapture(1)

def capture_image(screen, width, height):
    # from Screen
    if screen: 
        image = pag.screenshot().resize((width,height))
        return image
    
    # from Webcam
    else:
        ret, image = cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        image = cv2.resize(image, (width, height))
        image = Image.fromarray(image)
        return image
