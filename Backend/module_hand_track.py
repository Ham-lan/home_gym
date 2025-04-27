
import cv2 as cv
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False ,maxHands=2 ,modelComplex=1 ,detectionCon=0.5 ,trackCon= 0.5 ):
        
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex =modelComplex
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        #self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        
        # self.mode =  mode # initially set mode to the value given by user
        # self.maxHands = maxHands
        # self.detectionCon = detectionCon
        # self.trackCon = trackCon

        # #cap = cv.VideoCapture(0) # using webcam
        # # initialize these values too
        # self.mpHands = mp.solutions.hands
        # # detect the hands in picture
        # self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.detectionCon, self.trackCon)
        
        # #self.hands = self.mpHands.Hands( self.mode , self.maxHands , self.detectionCon , self.trackCon) 
        # self.mpDraw = mp.solutions.drawing_utils

 

    # because of not giving a tab before this function name i was stuck for hour
    def findHands(self , img , draw=True):
    # convert image to RGB
        imgRGB = cv.cvtColor( img , cv.COLOR_BGR2RGB )
        self.results = self.hands.process(imgRGB) # process will return the hands
#    print(results.multi_hand_landmarks)
# if there are multiple hands in the image draw on every hand
        if self.results.multi_hand_landmarks: # If hand detected
            print("hand detected")
            for handLms in self.results.multi_hand_landmarks: # iterate overall landmarks of hand
                if draw:
                    # use mpHands.HAND_CONNECTIONS to create connections between points
                    self.mpDraw.draw_landmarks( img , handLms , self.mpHands.HAND_CONNECTIONS )
        return img
    
    def findPosition( self , img , handNo=0 , draw=True ):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo] # getting 1 hand out of multiple hands
            # now we can find the landmarks for the specific hand
            for id , lm in enumerate(myHand.landmark):
                h , w ,c = img.shape
                cx , cy = int(lm.x*w) , int(lm.y*h)
                #print(cx,cy)
                lmList.append( [id , cx ,cy] )
                if draw:
                    cv.circle(img , (cx , cy) , 25 , (255,0,255) , -1)
        return lmList
def main():
    pTime = 0
    cTime = 0
    detector = handDetector()
    
    cap = cv.VideoCapture(0)
    while True:
        success , img = cap.read() # return an array fro image and a bool variable
        img1 = detector.findHands(img)
        lmList = detector.findPosition(img)
        print(len(lmList)) # when no hand detected len(lmList) = 0       
        if len(lmList) != 0:
            print( lmList[4] )
        
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv.putText( img , str( int(fps) ) , ( 10 , 70 ) , cv.FONT_HERSHEY_PLAIN , 3 , ( 255, 0 , 255 ) ,
    thickness=2 )
    
        cv.imshow("webcam",img1)
        if cv.waitKey(25) & 0xFF == ord('d'): # to end infinite loop
            break
    cap.release()
    cv.destroyAllWindows()


if __name__=="__main__":
    main()