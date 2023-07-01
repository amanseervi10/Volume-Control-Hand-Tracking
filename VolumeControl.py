import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam=1280
hcam=640

cap = cv2.VideoCapture(0)
# cap.set(3,wcam)
# cap.set(4,hcam)
curr_time=0
prev_time=0

detector=htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
minVol=volume.GetVolumeRange()[0]
maxVol=volume.GetVolumeRange()[1]
vol=0
volBar=400

while(True):
    
    ret, frame= cap.read()
    frame = detector.findHands(frame,True)

    positions=detector.findPosition(frame,draw=False)
    
    if(len(positions)!=0):

        x1,y1=positions[4][1],positions[4][2]
        x2,y2=positions[8][1],positions[8][2]
        cx,cy= (x1+x2)//2, (y1+y2)//2

        cv2.circle(frame,(x1,y1),7,(0,255,0),-1)
        cv2.circle(frame,(x2,y2),7,(0,255,0),-1)
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,255),5)
        cv2.circle(frame,(cx,cy),7,(0,255,0),-1)

        length=math.hypot(x2-x1,y2-y1)
        # print(length)

        if(length<27):
            cv2.circle(frame,(cx,cy),7,(255,100,0),-1)
            
        vol= np.interp(length,[25,120],[minVol,maxVol])
        volume.SetMasterVolumeLevel(vol, None)

        volBar=np.interp(length,[25,120],[400,150])

    cv2.rectangle(frame,(50,150),(70,400),(130,65,150),5)
    cv2.rectangle(frame,(50,int(volBar)),(70,400),(65,130,190),cv2.FILLED)

    #For showing fps
    curr_time=time.time()
    fps= 1/(curr_time-prev_time)
    prev_time=curr_time
    cv2.putText(frame,str(int(fps)),(20,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0),5)
    cv2.imshow("VolumeControl",frame)

    #To Close the Window
    k=cv2.waitKey(1)  
    if k==27:
        break
    
