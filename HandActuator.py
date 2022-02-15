import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math

###############################
wCam, hCam = 640, 480
###############################

def normalise(lmlist):
    """
    Normalise entire lm list
    - Wrist == (0,0)
    - Points 0 and 1 so that length is equal to 1

    :param lmlist: list of coordinates [id,x_coord,y_coord]
    :return: lmlist: normalised list
    """

    base_x, base_y = lmlist[0][1], lmlist[0][2]
    thumb_x, thumb_y = lmlist[1][1], lmlist[1][2]
    scale_factor = (((thumb_x - base_x) ** 2) + ((thumb_y - base_y) ** 2)) ** 0.5

    for num in range(len(lmlist)):
        lmlist[num][1] -= base_x
        lmlist[num][1] /= scale_factor

        lmlist[num][2] -= base_y
        lmlist[num][2] /= scale_factor

    return lmlist

def thumbAngle(lmList):
    """
    :param lmList:
    :return: Approximate distance
    """

    thumb = lmList[3]
    check = lmList[5]

    distance = check[1] - thumb[1]

    return distance


def main():
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

        if len(lmList): # if hand found

            lmList = normalise(lmList)

            fingers = []
            print(indexFinger)

            thumbAngle(lmList) # thumb

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

if __name__ == "__main__":
    main()