
# import cv2 as cv 
# import numpy as np
# import time
# import module as pm
# cap=cv.VideoCapture(0)
# #img = cv.imread("D:\Programming\Python\Projects\OpenCv\Adavnce_Topics_Opencv\Project_3_AI_Personal_Trainer\Train1.png")
# detector = pm.posedetector()

# totalCount = 0
# dir = 0
# pTime = 0

# def getData(img):
    
    
#     # count = 0
#     # dir = 0
#     # pTime = 0
    
#     img = detector.findpose(img , False)
#     lmList = detector.getposition(img , False)
#     #print(lmList)
#     if len(lmList) != 0:
#         # # Right Arm 
#         # detector.find_angle(img , 12, 14 , 16)
#         # # Left Arm
#         angle = detector.find_angle(img , 11 , 13 , 15)
#         percentage = np.interp( angle , ( 50 , 160 ) , ( 0, 100 ) )
#         bar = np.interp( angle , ( 50 , 160 ) , ( 210 , 110 ) )
#         #print( angle , percentage )
#         # Check for the dumbell curve
#         color = ( 255 , 0 , 255)
#         if percentage == 100:
#             # if percentage is 100 we will add 1 to it but if its crosses 100 we will not add 
#             # so we have a condition that after we have added the count we will change the dir value
#             if dir == 0:
#                 color = (0, 255 ,0)
#                 print("adding for 100")
#                 count += 0.5
#                 dir = 1
#         if percentage == 0:
#             color = ( 0 , 255 , 0)
#             print("adding for 0 .....")
#             if dir == 1:
#                 count += 0.5
#                 dir = 0
#         print("count = ",count)
#         # Draw bar
#         cv.rectangle( img , ( 20 , 110 ) , ( 50 , 210 ) , color  )
#         cv.rectangle( img , ( 20 , int(bar)  ) , ( 50 , 210 ) , color , cv.FILLED )
#         cv.putText(img , f'{int(percentage)}' , ( 20 , 250 ) , cv.FONT_HERSHEY_PLAIN , 3 ,(255 , 255 , 255) , 5)

#         # Draw curl bar
#         cv.rectangle( img , ( 0 , 450 ) , ( 150 , 600 ) , (0,255,0) , cv.FILLED )
#         cv.putText(img , str(int( count )) , ( 50 , 550 ) , cv.FONT_HERSHEY_PLAIN , 5 ,(255 , 255 , 255) , 5)

#         cTime = time.time()
#         fps = 1/( cTime - pTime )
#         pTime = cTime

#     return img,count

        

# while True:
#     success , img = cap.read()
#     #img = cv.resize(img , ( 600, 360 ))
#     #img = cv.imread("D:\Programming\Python\Projects\OpenCv\Adavnce_Topics_Opencv\Project_3_AI_Personal_Trainer\Train1.png")
    
#     # img = detector.findpose(img , False)
#     # lmList = detector.getposition(img , False)
#     # #print(lmList)
#     # if len(lmList) != 0:
#     #     # # Right Arm 
#     #     # detector.find_angle(img , 12, 14 , 16)
#     #     # # Left Arm
#     #     angle = detector.find_angle(img , 11 , 13 , 15)
#     #     percentage = np.interp( angle , ( 50 , 160 ) , ( 0, 100 ) )
#     #     bar = np.interp( angle , ( 50 , 160 ) , ( 210 , 110 ) )
#     #     #print( angle , percentage )
#     #     # Check for the dumbell curve
#     #     color = ( 255 , 0 , 255)
#     #     if percentage == 100:
#     #         # if percentage is 100 we will add 1 to it but if its crosses 100 we will not add 
#     #         # so we have a condition that after we have added the count we will change the dir value
#     #         if dir == 0:
#     #             color = (0, 255 ,0)
#     #             print("adding for 100")
#     #             count += 0.5
#     #             dir = 1
#     #     if percentage == 0:
#     #         color = ( 0 , 255 , 0)
#     #         print("adding for 0 .....")
#     #         if dir == 1:
#     #             count += 0.5
#     #             dir = 0
#     #     print("count = ",count)
#     #     # Draw bar
#     #     cv.rectangle( img , ( 20 , 110 ) , ( 50 , 210 ) , color  )
#     #     cv.rectangle( img , ( 20 , int(bar)  ) , ( 50 , 210 ) , color , cv.FILLED )
#     #     cv.putText(img , f'{int(percentage)}' , ( 20 , 250 ) , cv.FONT_HERSHEY_PLAIN , 3 ,(255 , 255 , 255) , 5)

#     #     # Draw curl bar
#     #     cv.rectangle( img , ( 0 , 450 ) , ( 150 , 600 ) , (0,255,0) , cv.FILLED )
#     #     cv.putText(img , str(int( count )) , ( 50 , 550 ) , cv.FONT_HERSHEY_PLAIN , 5 ,(255 , 255 , 255) , 5)

#     #     cTime = time.time()
#     #     fps = 1/( cTime - pTime )
#     #     pTime = cTime

        
#     # cv.putText(img , f'FPS:{int(fps)}' , ( 50 , 100) , cv.FONT_HERSHEY_PLAIN , 5 ,(255 , 255 , 255) , 5)

#     img , count = getData(img=img)

    

#     print(count)


#     cv.imshow('Cap',img)

#     if cv.waitKey(1) & 0xFF == ord('d'):
#         break
# cap.release()
# cv.destroyAllWindows()
 


import cv2 as cv 
import numpy as np
import time
import module as pm

cap = cv.VideoCapture('PerfectPushUp.mp4')
detector = pm.posedetector()

totalCount = 0  # Renamed to avoid confusion
dir = 0
pTime = 0

def getData(img, count, dir, pTime):
    img = detector.findpose(img, False)
    lmList = detector.getposition(img, False)
    
    if len(lmList) != 0:
        # Left Arm
        angle = detector.find_angle(img, 11, 13, 15)
        percentage = np.interp(angle, (50, 160), (0, 100))
        bar = np.interp(angle, (50, 160), (210, 110))
        
        # Check for the dumbbell curl
        color = (255, 0, 255)
        if percentage == 100:
            if dir == 0:
                color = (0, 255, 0)
                print("adding for 100")
                count += 0.5
                dir = 1
        if percentage == 0:
            color = (0, 255, 0)
            print("adding for 0 .....")
            if dir == 1:
                count += 0.5
                dir = 0
        print("count = ", count)

        # Draw bar
        cv.rectangle(img, (20, 110), (50, 210), color)
        cv.rectangle(img, (20, int(bar)), (50, 210), color, cv.FILLED)
        cv.putText(img, f'{int(percentage)}', (20, 250), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)

        # Draw curl count
        cv.rectangle(img, (0, 300), (100, 400), (0, 255, 0), cv.FILLED)
        cv.putText(img, str(int(count)), (25, 375), cv.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

    return img, count, dir, pTime

# Initialize variables for the loop
count = totalCount

def main():
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from camera.")
            break

        # Process the frame
        img, count, dir, pTime = getData(img, count, dir, pTime)
        print("Total count = ", count)

        cv.imshow('Cap', img)

        if cv.waitKey(1) & 0xFF == ord('d'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()