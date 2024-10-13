import pyautogui as pag
import cv2

cap = cv2.VideoCapture(0)

def capture_image(screen, width, height):
    # from Screen
    if screen: 
        image = pag.screenshot().resize((width,height))
        return image
    
    # from Webcam
    else:
        ret, image = cap.read()
        return image
