import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,modelComplexity=1,maxHands=2,detectionCon=0.5, trackCon=0.5):
        self.mode=mode
        self.modelComplexity=modelComplexity
        self.maxHands=maxHands
        self.detectionCon=detectionCon  
        self.trackCon=trackCon
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.modelComplexity,
                self.detectionCon,self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for eachHand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,eachHand,self.mpHands.HAND_CONNECTIONS)
        return img


    def findPosition(self,img,handNo=0,draw=True):
        positions=[]
        if self.results.multi_hand_landmarks:
            currHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(currHand.landmark):
                h,w,c=img.shape
                cx=int(lm.x*w)
                cy=int(lm.y*h)
                positions.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),10,(145,210,177),cv2.FILLED)
        return positions

def main():
    cap=cv2.VideoCapture(0)

    current_time=0
    previous_time=0
    detector=handDetector()

    while True:
        ret, frame= cap.read()
        frame=detector.findHands(frame)

        #For calculating Frames per second
        current_time=time.time()
        fps=1/(current_time-previous_time)
        previous_time=current_time
        cv2.putText(frame,str(int(fps)),(20,100),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),5)

        #For displaying the video
        cv2.imshow("cam",frame)

        #To close the window
        k=cv2.waitKey(1)  
        if k==27:
            break

if __name__=="main":
    main()