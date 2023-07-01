import cv2
import mediapipe as mp
import time

cap=cv2.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
drawShit=mp.solutions.drawing_utils

current_time=0
previous_time=0

while True:
    ret, frame= cap.read()
    framergb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result=hands.process(framergb)

    if result.multi_hand_landmarks:
        for eachHand in result.multi_hand_landmarks:
            drawShit.draw_landmarks(frame,eachHand,mpHands.HAND_CONNECTIONS)
            for id,lm in enumerate(eachHand.landmark):
                h,w,c=frame.shape
                cx=int(lm.x*w)
                cy=int(lm.y*h)
                if id==0:
                    cv2.circle(frame,(cx,cy),10,(145,210,177),cv2.FILLED)

    current_time=time.time()
    fps=1/(current_time-previous_time)
    previous_time=current_time

    cv2.putText(frame,str(int(fps)),(20,100),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),5)

    cv2.imshow("cam",frame)

    #To close the window
    k=cv2.waitKey(1)  
    if k==27:
        break
