from HandActuator import thumbAngle, normalise
import cv2 as cv
import HandTrackingModule as htm
import time
import serial

#ArduinoSerial=serial.Serial('com7',9600,timeout=0.1)

###############################
wCam, hCam = 640, 480
###############################

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

        tDist = [0,0,0,0,0]

        if len(lmList): # if hand found

            lmList = normalise(lmList)

            fingers = []
            print(indexFinger)

            tDist[0] = str(thumbAngle(lmList)) # thumb

            # Other four fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    tDist[id] += str(lmList[tipIds[id]-2][2]-lmList[tipIds[id]][2])
                else:
                    fingers.append(0)


        currTime = time.time()
        fps = 1/(currTime-prevTime)
        prevTime = currTime

        string = tDist
        #ArduinoSerial.write(string.encode('utf-8'))
        print(string)

        cv.putText(img, f'FPS {int(fps)}', (420, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv.imshow('Image', img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()
