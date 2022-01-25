import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math

###############################
wCam, hCam = 640, 480
###############################

def thumbAngle(lmList):
    """
    :param lmList:
    :return: Approximate distance
    """

    thumb = lmList[3]
    check = lmList[5]

    distance = check[1] - thumb[1]

    return distance

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

prevTime = 0

detector = htm.handDetector(detectConf=0.8)

tipIds = [4, 8, 12, 16, 20]
indexFinger, otherFingers = 100, 100

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList):
        fingers = []

        
        print(indexFinger)

        thumbAngle(lmList)
        
        # Other four fingers
        # for id in range(1, 5):
        #     if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                
        #     else: 
        #         fingers.append(0)

    
    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime = currTime

    cv.putText(img, f'FPS {int(fps)}', (420, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv.imshow('Image', img)
    cv.waitKey(1)