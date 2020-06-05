import math
import cv2
import numpy as np
import pyautogui
(camx, camy) = (320, 240)
# lower and upper bound values for the color green
# just change hue value if color change reqd
lowerGreen = np.array([33, 80, 40])  # h,s,v
upperGreen = np.array([102, 255, 255])  # h,s,v
center = 0
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((10, 10))
cam = cv2.VideoCapture(0)
cam.set(3, camx)
cam.set(4, camy)
##
pinchFlag = 0
openx, openy, openw, openh = (0, 0, 0, 0)
##
while cam.isOpened():
    ret, img = cam.read()
    # img = cv2.resize(img, (340, 220))

    # converting BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lowerGreen, upperGreen)
   
    # morphology
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
    maskFinal = maskClose

    _, contours, h = cv2.findContours(
        maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if(len(contours) == 2):
        if(pinchFlag == 1):
            pinchFlag = 0
        x1, y1, w1, h1 = cv2.boundingRect(contours[0])
        x2, y2, w2, h2 = cv2.boundingRect(contours[1])
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
        if(angle < 0):
            angle += 180
        if(angle < 100 and angle > 80):
            if(center == 0):
                center = 1
        elif(angle > 115):
            if(center == 1):
                center = 0
                pyautogui.press('left', presses=1)
        elif(angle < 75):
            if(center == 1):
                center = 0
                pyautogui.press('right', presses=1)
        cv2.putText(img, str(angle), (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
        cv2.putText(img, str(center), (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
        openx, openy, openw, openh = cv2.boundingRect(
            np.array([[[x1, y1], [x1+w1, y1+h1], [x2, y2], [x2+w2, y2+h2]]]))
    elif(len(contours) == 1):
        x, y, w, h = cv2.boundingRect(contours[0])
        if(pinchFlag == 0):
            if(abs((w*h-openw*openh)*100/(w*h)) < 20):
                pinchFlag = 1
                openx, openy, openw, openh = (0, 0, 0, 0)
                pyautogui.press('up', presses=1)
        else:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cx = int(x+w/2)
            cy = int(y+h/2)
            cv2.circle(img, (cx, cy), int((w+h)/4), (0, 0, 255), 2)
    #elif(len(contours) == 0):
        #pyautogui.press('down', presses=1)

    cv2.imshow("Cam", img)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
