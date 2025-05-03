from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import base64
import cv2
import numpy as np
import module_hand_track as htm
import math
import time

import module as pm

import PullUps.dead_hang as DH

import PullUps.negative_pullups as NP
import PullUps.pull_up as PLU
import PullUps.scapular_contraction as SC

import PushUps.form as PF
import PushUps.go_down as GD
import PushUps.plank as PUP
import PushUps.count as PUPC

import Squats.squats as SSQ





# import push_up3 as pp



app = Flask(__name__)
socketio = SocketIO(app)


detector = htm.handDetector(detectionCon=0.75)
pTime = 0
# Serve the HTML page for the video feed

totalCount = 0  # Renamed to avoid confusion
dir = 0

# Define landmark indices (MediaPipe pose landmarks)
LEFT_SHOULDER = 11
LEFT_ELBOW = 13
LEFT_WRIST = 15
RIGHT_SHOULDER = 12
RIGHT_ELBOW = 14
RIGHT_WRIST = 16
NOSE = 0  # Used to approximate chin position



@app.route('/')
def index():
    return render_template('index.html')  # Serve an HTML page with video element

# Endpoint to receive the camera frames from Flutter
@app.route('/send_video', methods=['POST'])
def receive_video():
    data = request.json
    base64_video_data = data.get('videoData')
    process = data.get('process')

    # print(exercise)

    if base64_video_data:
        
        base64_video_data = processVideo(base64_video_data=base64_video_data , process=process)
        socketio.emit('new_video_frame', {'videoData': base64_video_data} )
        # render_template('index.html')
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "No video data provided"}), 400


def getHands(img):
    pTime = 0

    img =  detector.findHands(img)


    lmList = detector.findPosition(img , draw=False) # landmarks list
    

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    volPer = 0

    if len(lmList) != 0:
        #print(lmList[4] , lmList[8])

        x1 , y1 = lmList[4][1] , lmList[4][2]
        x2 , y2 = lmList[8][1] , lmList[8][2]
        # find center between 2 points
        
        cx , cy = ( x1 + x2)//2 , ( y1 + y2)//2
        
        
        cv2.circle(img , ( x1 , y1 ) , 15 , ( 255 , 0 , 255 ) , cv2.FILLED)
        cv2.circle(img , ( x2 , y2 ) , 15 , ( 255 , 0 , 255 ) , cv2.FILLED)
        cv2.line(img , ( x1, y1 ) , (x2 , y2) , ( 255,0,255 ) , 3 )
        cv2.circle(img , ( cx , cy ) , 15 , ( 255 , 0 , 255 ) , cv2.FILLED)
        # now we will find the length of the line between two points
        # using hypotenuse function
        length = math.hypot( x2 - x1 , y2 - y1 ) # giving the co ordinates 
        print(length)
        # hand limits from 220 - 50
        # volume limits from -65.5 - 0

        vol = np.interp(length , [ 50 , 220 ] , [ 0 , 100 ])
        volBar = np.interp(length , [ 50 , 220 ] , [ 400 , 150 ])
        volPer = np.interp(length , [ 50 , 220 ] , [ 0 , 100 ])
        
        print( int( length ) , vol )
        # volume.SetMasterVolumeLevel( vol , None)
        
        if length<50: # if legth is decreased quite much
            cv2.circle(img , ( cx , cy ) , 15 , ( 0 , 255 , 0 ) , cv2.FILLED)            
        
        cv2.rectangle( img , ( 50 , 150 ) , ( 80,400 ) , ( 0 , 255 ,0), 3 )
        cv2.rectangle( img , ( 50 , int(volBar) ) , ( 80,400 ) , ( 0 , 255 ,0), cv2.FILLED )


    cv2.putText(img , f'FPS:{int(fps)}',  ( 20 , 70 ) , cv2.FONT_HERSHEY_PLAIN , 3 , ( 0,0,255))
    cv2.putText(img , f'{int(volPer)}%' , ( 50 , 450 ) , cv2.FONT_HERSHEY_PLAIN , 3 , ( 0,250,0) )
    return img


def analyze_pre_pushup(img, angles):
    feedback = []
    for side, angle in [("Left Arm", angles["left_arm"]), ("Right Arm", angles["right_arm"])]:
        if 0 <= angle <= 20:
            feedback.append((f"{side}: Good (straight) {angle}", (0, 255, 0)))
        else:
            feedback.append((f"{side}: Bend your arms less, keep them straight {angle}", (0, 0, 255)))

    for side, angle in [("Left Shoulder-Hip", angles["left_shoulder_hip"]), ("Right Shoulder-Hip", angles["right_shoulder_hip"])]:
        if 160 <= angle <= 180:
            feedback.append((f"{side}: Good {angle}", (0, 255, 0)))
        elif angle < 160:
            feedback.append((f"{side}: {angle}", (0, 0, 255)))
            # feedback.append((f"{side}: Sagging, lift hips {angle}", (0, 0, 255)))
        else:
            feedback.append((f"{side}: {angle}", (0, 0, 255)))
            # feedback.append((f"{side}: Piking, lower hips {angle}", (0, 0, 255)))

    for side, angle in [("Left Hip-Knee", angles["left_hip_knee"]), ("Right Hip-Knee", angles["right_hip_knee"])]:
        if 160 <= angle <= 180:
            feedback.append((f"{side}: Good", (0, 255, 0)))
        else:
            feedback.append((f"{side}: Straighten legs", (0, 0, 255)))

    for side, angle in [("Left Knee-Foot", angles["left_knee_foot"]), ("Right Knee-Foot", angles["right_knee_foot"])]:
        if 160 <= angle <= 180:
            feedback.append((f"{side}: Good", (0, 255, 0)))
        else:
            feedback.append((f"{side}: Straighten legs", (0, 0, 255)))

    # if 0 <= angles["hips"] <= 20:
    #     feedback.append(("Hips: Good", (0, 255, 0)))
    # else:
    #     feedback.append(("Hips: Twisted, keep level", (0, 0, 255)))
    
    angles_handToHip = angles["hip_shoulder_hand"]


    # if 77 <= angles["hip_shoulder_hand"] <= 90:
    #     feedback.append((f"Hand to Hip: {angles_handToHip}", (0, 255, 0)))
    
    # if 33 <= angles['shouler_other_elbow'] <= 47:
    #     feedback.append((f"Angles Shoulder Elbow: { angles['shouler_other_elbow'] }", (0, 255, 0)))
    # angles_shoulder_Elbow = angles['shouler_other_elbow']
    


    # Display feedback with a background rectangle
    h, w, _ = img.shape
    for i, (text, color) in enumerate(feedback):
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 2, 3)
        x, y = 10, 50 + i * 40
        cv2.rectangle(img, (x, y - 30), (x + text_size[0] + 10, y + 10), (0, 0, 0), -1)  # Black background
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
        print(f"Rendering: {text} at ({x}, {y})")
    
    return img


def check_pre_pushup(img):
    
    detector = pm.posedetector()

    lmList = detector.getposition(img, True)

    if len(lmList) != 0:
            # Calculate all angles
            angles = {
                "left_hip_knee": detector.find_angle(img, 23, 25, 26, draw=True),
                "right_hip_knee": detector.find_angle(img, 24, 26, 25, draw=True),
                "left_knee_foot": detector.find_angle(img, 25, 27, 28, draw=True),
                "right_knee_foot": detector.find_angle(img, 26, 28, 27, draw=True),
                "hips": detector.find_angle(img, 23, [0, (lmList[25][1] + lmList[26][1]) // 2, (lmList[25][2] + lmList[26][2]) // 2], 24, draw=True),
                "left_shoulder_hip": detector.find_angle(img, 11, 23, 25, draw=True),
                "right_shoulder_hip": detector.find_angle(img, 12, 24, 26, draw=True),
                "left_arm": detector.find_angle(img, 13, 11, 15, draw=True),
                "right_arm": detector.find_angle(img, 14, 12, 16, draw=True),
                "hip_shoulder_hand": detector.find_angle(img , 16,12,24),
                "shouler_other_elbow" : detector.find_angle(img , 11 , 12 ,14)
            }

            # Analyze push-up form
            # analyze_pushup(img, angles)
            
            img = analyze_pre_pushup(img,angles)
    
    return img

# def getData(img, count, dir, pTime):
#     detector = pm.posedetector()
#     img = detector.findpose(img, False)
#     lmList = detector.getposition(img, False)
    
#     if len(lmList) != 0:
#         # Left Arm
#         angle = detector.find_angle(img, 11, 13, 15)
#         percentage = np.interp(angle, (50, 160), (0, 100))
#         bar = np.interp(angle, (50, 160), (210, 110))
        
#         # Check for the dumbbell curl
#         color = (255, 0, 255)
#         if percentage == 100:
#             if dir == 0:
#                 color = (0, 255, 0)
#                 print("adding for 100")
#                 count += 0.5
#                 dir = 1
#         if percentage == 0:
#             color = (0, 255, 0)
#             print("adding for 0 .....")
#             if dir == 1:
#                 count += 0.5
#                 dir = 0
#         print("count = ", count)

#         # Draw bar
#         cv2.rectangle(img, (20, 110), (50, 210), color)
#         cv2.rectangle(img, (20, int(bar)), (50, 210), color, cv2.FILLED)
#         cv2.putText(img, f'{int(percentage)}', (20, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)

#         # Draw curl count
#         cv2.rectangle(img, (0, 300), (100, 400), (0, 255, 0), cv2.FILLED)
#         cv2.putText(img, str(int(count)), (25, 375), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime

#     return img, count, dir, pTime


# def processVideo(base64_video_data):
#     img_data = base64.b64decode(base64_video_data)
#     np_arr = np.frombuffer(img_data, np.uint8)
#     img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    


#     count = totalCount

#     # Apply image processing (grayscale conversion)
#     # processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # processed_img = convertToGrayScale(img=img)
    
#     pTime = 0
#     dir = 0
#     # img =  detector.findHands(img)


#     # lmList = detector.findPosition(img , draw=False) # landmarks list
    

#     # cTime = time.time()
#     # fps = 1 / (cTime - pTime)
#     # pTime = cTime

#     # volPer = 0

#     # if len(lmList) != 0:
#     #     #print(lmList[4] , lmList[8])

#     #     x1 , y1 = lmList[4][1] , lmList[4][2]
#     #     x2 , y2 = lmList[8][1] , lmList[8][2]
#     #     # find center between 2 points
        
#     #     cx , cy = ( x1 + x2)//2 , ( y1 + y2)//2
        
        
#     #     cv2.circle(img , ( x1 , y1 ) , 15 , ( 255 , 0 , 255 ) , cv2.FILLED)
#     #     cv2.circle(img , ( x2 , y2 ) , 15 , ( 255 , 0 , 255 ) , cv2.FILLED)
#     #     cv2.line(img , ( x1, y1 ) , (x2 , y2) , ( 255,0,255 ) , 3 )
#     #     cv2.circle(img , ( cx , cy ) , 15 , ( 255 , 0 , 255 ) , cv2.FILLED)
#     #     # now we will find the length of the line between two points
#     #     # using hypotenuse function
#     #     length = math.hypot( x2 - x1 , y2 - y1 ) # giving the co ordinates 
#     #     print(length)
#     #     # hand limits from 220 - 50
#     #     # volume limits from -65.5 - 0

#     #     vol = np.interp(length , [ 50 , 220 ] , [ 0 , 100 ])
#     #     volBar = np.interp(length , [ 50 , 220 ] , [ 400 , 150 ])
#     #     volPer = np.interp(length , [ 50 , 220 ] , [ 0 , 100 ])
        
#     #     print( int( length ) , vol )
#     #     # volume.SetMasterVolumeLevel( vol , None)
        
#     #     if length<50: # if legth is decreased quite much
#     #         cv2.circle(img , ( cx , cy ) , 15 , ( 0 , 255 , 0 ) , cv2.FILLED)            
        
#     #     cv2.rectangle( img , ( 50 , 150 ) , ( 80,400 ) , ( 0 , 255 ,0), 3 )
#     #     cv2.rectangle( img , ( 50 , int(volBar) ) , ( 80,400 ) , ( 0 , 255 ,0), cv2.FILLED )


#     # cv2.putText(img , f'FPS:{int(fps)}',  ( 20 , 70 ) , cv2.FONT_HERSHEY_PLAIN , 3 , ( 0,0,255))
#     # cv2.putText(img , f'{int(volPer)}%' , ( 50 , 450 ) , cv2.FONT_HERSHEY_PLAIN , 3 , ( 0,250,0) )
#     # cv2.imshow('record',img)
    

#     # img = getHands(img=img)

#     img, count, dir, pTime = getData(img, count, dir, pTime )
#     totalCount = count

#     # Convert back to base64
#     _, buffer = cv2.imencode('.jpg', img)
#     processed_base64 = base64.b64encode(buffer).decode('utf-8')
#     return processed_base64



# Global variable to track total curls across frames
totalCount = 0

def getCurls(img, count, dir, pTime):
    detector = pm.posedetector()
    img = detector.findpose(img, False)
    lmList = detector.getposition(img, False)
    
    if len(lmList) != 0:
        # Left Arm
        angle = detector.find_angle(img, 11, 13, 15)
        percentage = np.interp(angle, (50, 160), (0, 100))
        bar = np.interp(angle, (50, 160), (210, 110))
        
        # Check for the dumbbell curl
        color = (255, 0, 255)  # Default color (purple)
        # Add some tolerance to catch near-100% or near-0%
        if percentage >= 95:  # Close to 100%
            if dir == 0:
                color = (0, 255, 0)  # Green
                print("Peak reached, adding 0.5")
                count += 0.5
                dir = 1
        elif percentage <= 5:  # Close to 0%
            if dir == 1:
                color = (0, 255, 0)  # Green
                print("Bottom reached, adding 0.5")
                count += 0.5
                dir = 0
        print(f"Angle: {angle}, Percentage: {percentage}, Count: {count}, Dir: {dir}")

        # Draw bar
        cv2.rectangle(img, (20, 110), (50, 210), color)
        cv2.rectangle(img, (20, int(bar)), (50, 210), color, cv2.FILLED)
        cv2.putText(img, f'{int(percentage)}', (20, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)

        # Draw curl count
        cv2.rectangle(img, (0, 300), (100, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 375), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

    return img, count, dir, pTime

def getPullUps(img):
    # Detect pose and get landmarks
        detector = pm.posedetector()
        frame = detector.findpose(img)
        lmList = detector.getposition(frame)

        feedback = ""

        if len(lmList) > 0:
            # Calculate elbow angles (for form check)
            left_elbow_angle = detector.find_angle(frame, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
            right_elbow_angle = detector.find_angle(frame, RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)

            # Approximate chin position (using NOSE) relative to shoulders
            chin_y = lmList[NOSE][2]
            shoulder_y = (lmList[LEFT_SHOULDER][2] + lmList[RIGHT_SHOULDER][2]) / 2

            # Define pull-up logic
            # Top of pull-up: chin above shoulders
            # Bottom of pull-up: elbows nearly straight (angle > 150 degrees)
            if chin_y < shoulder_y - 20:  # Chin above shoulders (adjust threshold as needed)
                if stage != "up":
                    stage = "up"
            elif left_elbow_angle > 150 and right_elbow_angle > 150:  # Elbows extended
                if stage == "up":
                    stage = "down"
                    # pullup_count += 1  # Count a pull-up when transitioning from up to down
                    totalCount +=1 

            # Form feedback
            feedback = ""
            if stage == "down" and (left_elbow_angle < 140 or right_elbow_angle < 140):
                feedback = "Fully extend elbows at bottom!"
            elif stage == "up" and chin_y > shoulder_y:
                feedback = "Chin above bar!"

        # Display pull-up count and feedback
        # cv2.putText(frame, f"Pull-ups: {pullup_count}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.putText(frame, feedback, (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return frame

def processVideo(base64_video_data , process ):
    global totalCount  # Use the global totalCount

    img_data = base64.b64decode(base64_video_data)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Start with the current totalCount
    count = totalCount
    pTime = 0  # Initialize pTime (could persist this too if needed)
    dir = 0    # Initialize direction (could persist this too)

    # detector = pm.posedetector()

    # img = detector.findpose(img)
    # lmList = detector.getposition(img, True)

    # if len(lmList) != 0:
    #         # Calculate all angles
    #         angles = {
    #             "left_hip_knee": detector.find_angle(img, 23, 25, 26, draw=True),
    #             "right_hip_knee": detector.find_angle(img, 24, 26, 25, draw=True),
    #             "left_knee_foot": detector.find_angle(img, 25, 27, 28, draw=True),
    #             "right_knee_foot": detector.find_angle(img, 26, 28, 27, draw=True),
    #             # "hips": detector.find_angle(img, 23, [0, (lmList[25][1] + lmList[26][1]) // 2, (lmList[25][2] + lmList[26][2]) // 2], 24, draw=True),
    #             "left_shoulder_hip": detector.find_angle(img, 11, 23, 25, draw=True),
    #             "right_shoulder_hip": detector.find_angle(img, 12, 24, 26, draw=True),
    #             "left_arm": detector.find_angle(img, 13, 11, 15, draw=True),
    #             "right_arm": detector.find_angle(img, 14, 12, 16, draw=True),
    #             "hip_shoulder_hand": detector.find_angle(img , 16,12,24),
    #             "shouler_other_elbow" : detector.find_angle(img , 11 , 12 ,14)
    #         }

    #         # Analyze push-up form
    #         # analyze_pushup(img, angles)
    #         print(angles)
    #         # img = analyze_pre_pushup(img,angles)
    #         # img = getPullUps(img)

    # Process the frame
    # img  = check_pre_pushup(img)

    # img = getPullUps(img)

    if process == 'DH':
        img = DH.getDeadHang(img,detector=pm.posedetector())
    elif process == 'NP':
        img = NP.negativePullUps(detector=pm.posedetector() , frame=img)
    elif process == 'PF':
        img = PF.form(detector=pm.posedetector() , img=img)
    elif process == 'GD':
        img = GD.GoDown(detector=pm.posedetector() , frame=img)
    elif process == 'SQ':
        img = SSQ.squats(detector=pm.posedetector() , frame=img)
    

    

    # else:
        # img = check_pre_pushup(img)

    
    # img , count , dir , pTime = getCurls(img,count,dir,pTime)


    # Update the global count
    totalCount = count

    

    # Convert back to base64
    _, buffer = cv2.imencode('.jpg', img)
    processed_base64 = base64.b64encode(buffer).decode('utf-8')
    return processed_base64

def convertToGrayScale(img):
    return cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

def convertToCanny(img):
    edges = cv2.Canny(img, 100, 200)
    return edges

# def doThresholding(img):
#     return cv2.threshold(img, thresh=127, maxval=255, type=cv2.THRESH_BINARY)


def doThresholding(img):
    # Convert to grayscale if image is not already
    if len(img.shape) == 3:  # Check if the image has 3 channels (color image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresholded_img = cv2.threshold(img, thresh=127, maxval=255, type=cv2.THRESH_BINARY)
    
    return thresholded_img



def send_video():
    # Handle the video data sent here
    video_data = request.data
    print("Received video data of length:", len(video_data))
    return "Video received", 200

# Run the app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0', port=5000)
