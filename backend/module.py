

from re import I
import cv2 as cv
import mediapipe as mp
import time
import math

class posedetector():
    def __init__(self , mode=True ,model_complexity=1, upBody=False , smooth=True , detectionCon = 0.5 , trackCon = 0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        # self.results = []  # Initialize results as None
    # Now mpPose , pose , mpdraw are also part of the object for pose so they will also be initialized
        self.mpPose = mp.solutions.pose
        # Pose() function will return some value 
        self.pose = self.mpPose.Pose(self.mode , self.model_complexity ,self.upBody , 
        self.smooth, self.detectionCon, self.trackCon) 
        self.mpdraw = mp.solutions.drawing_utils #  an object to draw points on the detected pose

    def findpose(self , img , draw=True):
        imgRGB =cv.cvtColor(img , cv.COLOR_BGR2RGB)    
        self.results = self.pose.process(imgRGB) # process the image to find the pose in it
        print(self.results.pose_landmarks) #  print all landmarks
        if self.results.pose_landmarks: # detect a pose ( land marks )
            if draw:
                # results.pose_landmarks will give the landmark points if they exist
                self.mpdraw.draw_landmarks( img , self.results.pose_landmarks , self.mpPose.POSE_CONNECTIONS )
        return img
    def getposition(self , img , draw=True):
        self.lmList = []
        if self.results.pose_landmarks:    
        # this can only be printed in we have detected the pose landmarks
            for id , lm in enumerate( self.results.pose_landmarks.landmark ):
                h , w ,c = img.shape
                cx , cy = int(lm.x * w) , int( lm.y * h )
                self.lmList.append( [ id , cx , cy ] )
                if draw:
                    cv.circle( img , ( cx , cy ) , 1, ( 255 , 0 , 0 ) , cv.FILLED )
                    print( id , lm )
        return self.lmList
    
    def findAngle(self, img, p1, p2, p3, draw=True):

        # # Get the landmarks
        # x1, y1 = self.lmList[p1][1:]
        # x2, y2 = self.lmList[p2][1:]
        # x3, y3 = self.lmList[p3][1:]

        x1 , y1 = self.lmList[p1][1:]
        x2 , y2 = self.lmList[p2][1:]
        x3 , y3 = self.lmList[p3][1:]

       # Draw
        if draw:
            #cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            #cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            '''cv.circle(img, (x1, y1), 10, (0, 0, 255), cv.FILLED)'''
            #cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            '''cv.circle(img, (x2, y2), 10, (0, 0, 255), cv.FILLED)'''
            #cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            '''cv.circle(img, (x3, y3), 10, (0, 0, 255), cv.FILLED)'''
            #cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            #cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
            #            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            cv.circle( img , (x1,y1) , 10 , (255 , 0 , 0) ,cv.FILLED )
            cv.circle( img , (x2,y2) , 10 , (255 , 0 , 0) ,cv.FILLED )
            cv.circle( img , (x3,y3) , 10, (255 , 0 , 0) ,cv.FILLED )
        #return angle

    
    def find_angle(self , img , p1 ,p2 ,p3 , draw=True):
        # points
        x1 , y1 = self.lmList[p1][1:]
        x2 , y2 = self.lmList[p2][1:]
        x3 , y3 = self.lmList[p3][1:]
        
        # Calculate angels
        angle = math.degrees( math.atan2( y3 - y2 , x3 - x2 ) - math.atan2( y1 - y2 , x1 - x2  ) )
        print(angle)
        if angle < 0:
            angle += 360
        
        # draw
        if draw:
            cv.line(img , (x1,y1) , ( x2 , y2 ) , (255 , 255 , 255 ) , thickness= 2  )
            cv.line(img , (x2,y2) , ( x3 , y3 ) , (255 , 255 , 255 ) , thickness= 2  )

            cv.circle( img , (x1,y1) , 15 , (255 , 0 , 0)  )
            cv.circle( img , (x1,y1) , 10 , (255 , 0 , 0) , cv.FILLED  )
            
            
            cv.circle( img , (x2,y2) , 15 , (255 , 0 , 0)  )
            cv.circle( img , (x2,y2) , 10 , (255 , 0 , 0) , cv.FILLED )
            
            
            
            cv.circle( img , (x3,y3) , 15, (255 , 0 , 0)  )
            cv.circle( img , (x3,y3) , 10, (255 , 0 , 0) , cv.FILLED )

            cv.putText( img , str(int(angle)) , (x2 - 50 , y2 + 50) , cv.FONT_HERSHEY_PLAIN , 2 , (255,0,255) , 2 )
        return angle 

def main():
    # cap = cv.VideoCapture("D:\Programming\Python\Projects\OpenCv\Videos\Test4.mp4")
    cap = cv.VideoCapture(0)
    pTime = 0
    while True:
        success , img = cap.read()
        detector = posedetector()
        img = detector.findpose(img)
        lmList = detector.getposition(img)
        #detector.find_angle(img,12,14,16)
        if len(lmList) != 0:
            print( lmList[14] )
            cv.circle(img , ( lmList[14][1] , lmList[14][2] ), 15 , (255 , 0 , 0 ) , cv.FILLED )
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv.putText(img,str( int(fps) ) , ( 70, 50 ) , cv.FONT_HERSHEY_PLAIN , 3 ,  ( 0 , 255 , 0) , 3 )
        cv.imshow("Img",img)
        if cv.waitKey(10) & 0xFF == ord('d'):
            break
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()