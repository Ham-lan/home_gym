import math
import time
import cv2 as cv
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#import sys
# sys.path is a list of absolute path strings

#sys.path('D:\Programming\Python\Projects\OpenCv\Adavnce_Topics_Opencv\module_hand_track.py')

import module_hand_track as htm

wCam , hCam = 640 , 480

cap = cv.VideoCapture(0)
cap.set(3 , wCam)
cap.set(4, hCam)
pTime = 0
# detectionConfidence = 0.7 we want this value because we want it ttodetect hand with more confimirmation
detector = htm.handDetector()


# https://github.com/AndreMiras/pycaw.git Volume library

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
minVol = volrange[0]
maxVol = volrange[1]


vol = 0
volBar = 400
volPer = 0
while True:
    success , img = cap.read()
    img = detector.findHands(img)
    
    lmList = detector.findPosition(img , draw=False) # landmarks list
    

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    if len(lmList) != 0:
        #print(lmList[4] , lmList[8])

        x1 , y1 = lmList[4][1] , lmList[4][2]
        x2 , y2 = lmList[8][1] , lmList[8][2]
        # find center between 2 points
        
        cx , cy = ( x1 + x2)//2 , ( y1 + y2)//2
        
        
        cv.circle(img , ( x1 , y1 ) , 15 , ( 255 , 0 , 255 ) , cv.FILLED)
        cv.circle(img , ( x2 , y2 ) , 15 , ( 255 , 0 , 255 ) , cv.FILLED)
        cv.line(img , ( x1, y1 ) , (x2 , y2) , ( 255,0,255 ) , 3 )
        cv.circle(img , ( cx , cy ) , 15 , ( 255 , 0 , 255 ) , cv.FILLED)
        # now we will find the length of the line between two points
        # using hypotenuse function
        length = math.hypot( x2 - x1 , y2 - y1 ) # giving the co ordinates 
        print(length)
        # hand limits from 220 - 50
        # volume limits from -65.5 - 0

        vol = np.interp(length , [ 50 , 220 ] , [ minVol , maxVol ])
        volBar = np.interp(length , [ 50 , 220 ] , [ 400 , 150 ])
        volPer = np.interp(length , [ 50 , 220 ] , [ 0 , 100 ])
        
        print( int( length ) , vol )
        volume.SetMasterVolumeLevel( vol , None)
        
        if length<50: # if legth is decreased quite much
            cv.circle(img , ( cx , cy ) , 15 , ( 0 , 255 , 0 ) , cv.FILLED)            
        
        cv.rectangle( img , ( 50 , 150 ) , ( 80,400 ) , ( 0 , 255 ,0), 3 )
        cv.rectangle( img , ( 50 , int(volBar) ) , ( 80,400 ) , ( 0 , 255 ,0), cv.FILLED )


    cv.putText(img , f'FPS:{int(fps)}',  ( 20 , 70 ) , cv.FONT_HERSHEY_PLAIN , 3 , ( 0,0,255))
    cv.putText(img , f'{int(volPer)}%' , ( 50 , 450 ) , cv.FONT_HERSHEY_PLAIN , 3 , ( 0,250,0) )
    cv.imshow('record',img)
    if cv.waitKey(1) & 0xFF == ord('d'):
        break
cap.release()
cv.destroyAllWindows()
