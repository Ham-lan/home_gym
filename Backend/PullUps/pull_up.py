
import cv2 as cv 
import numpy as np
import time
import module as pm

cap = cv.VideoCapture('PULLUPS.mp4')
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
        print(angle)
        percentage = np.interp(angle, (200, 300), (0, 100))
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