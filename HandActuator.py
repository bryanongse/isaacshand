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