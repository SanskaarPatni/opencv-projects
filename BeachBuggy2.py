import math
import cv2
import numpy as np
import pyautogui
import time
# variables
(camx, camy) = (320, 240)
lowerGreen = np.array([33, 80, 40])  # h,s,v
upperGreen = np.array([102, 255, 255])  # h,s,v
# lowerRed = np.array([0, 120, 70])  # h,s,v
# upperRed = np.array([10, 255, 255])  # h,s,v
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((10, 10))
right=0
breakk=0
# capturing video
cam = cv2.VideoCapture(0)
cam.set(3, camx)
cam.set(4, camy)

while cam.isOpened():
    ret, img = cam.read()
    # converting BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # masking
    maskGreen = cv2.inRange(imgHSV, lowerGreen, upperGreen)
    # morphology
    maskOpenG = cv2.morphologyEx(maskGreen, cv2.MORPH_OPEN, kernelOpen)
    maskCloseG = cv2.morphologyEx(maskOpenG, cv2.MORPH_CLOSE, kernelClose)
    maskFinalG = maskCloseG
    # finding contours
    contoursG, h = cv2.findContours(
        maskFinalG.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # conditions
    if(len(contoursG) == 2):
        if(breakk==1):
            breakk=0
        x1, y1, w1, h1 = cv2.boundingRect(contoursG[0])
        x2, y2, w2, h2 = cv2.boundingRect(contoursG[1])
        cv2.rectangle(img, (x1, y1), (x1+w1, y1+h1), (255, 0, 0), 2)
        cv2.rectangle(img, (x2, y2), (x2+w2, y2+h2), (255, 0, 0), 2)
        cx1 = int(x1+w1/2)
        cx2 = int(x2+w2/2)
        cy1 = int(y1+h1/2)
        cy2 = int(y2+h2/2)
        cx = int((cx1+cx2)/2)
        cy = int((cy1+cy2)/2)
        cv2.circle(img, (cx, cy), 2, (0, 0, 255), 2)
        cv2.line(img, (cx1, cy1), (cx2, cy2), (255, 0, 0), 2)
        try:
            angle = int(math.atan((cy2-cy1)/(cx2-cx1))*180/math.pi)
        except:
            angle = 90
        if(angle > -20 and angle < 20):
            if(right == -1):
                pyautogui.keyUp('left')
                pyautogui.press('right',presses=4)
            if(right == 1):
                pyautogui.keyUp('right')
                pyautogui.press('left',presses=3)
            right = 0
        
        if(angle < -16 and angle > -20):
            if(right==0):
                pyautogui.keyDown('right')
                time.sleep(0.1)
                pyautogui.keyUp('right')
            #pyautogui.press('right',presses=3)
        elif(angle > 13 and angle < 20):
            pyautogui.keyDown('left')
            time.sleep(0.1)
            pyautogui.keyUp('left')
            #pyautogui.press('left',presses=3)
        elif(angle > 20 and angle < 24):
            pyautogui.keyDown('left')
            time.sleep(0.2)
            pyautogui.keyUp('left')
        elif(angle < -20 and angle > -24):
            pyautogui.keyDown('right')
            time.sleep(0.2)
            pyautogui.keyUp('right')
        elif(angle>25):
            pyautogui.keyDown('left')
            right=-1
        elif(angle<-25):
            pyautogui.keyDown('right')
            right=1
        
        cv2.putText(img, str(angle), (80, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
        cv2.putText(img, str(right), (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
    else:
        pyautogui.press('down',4)
        breakk=1


    cv2.imshow("Cam", img)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()