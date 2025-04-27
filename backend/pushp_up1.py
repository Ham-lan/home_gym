# import cv2 as cv
# import mediapipe as mp
# import time
# import math

# class posedetector():
#     def __init__(self, mode=False, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.model_complexity = model_complexity
#         self.upBody = upBody
#         self.smooth = smooth
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon
#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)
#         self.mpdraw = mp.solutions.drawing_utils

#     def findpose(self, img, draw=True):
#         imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#         self.results = self.pose.process(imgRGB)
#         if self.results.pose_landmarks and draw:
#             self.mpdraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
#         return img

#     def getposition(self, img, draw=True):
#         self.lmList = []
#         if self.results.pose_landmarks:
#             for id, lm in enumerate(self.results.pose_landmarks.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 self.lmList.append([id, cx, cy])
#                 if draw and id in [23, 24, 25, 26, 27, 28]:  # Only draw hips, knees, feet
#                     cv.circle(img, (cx, cy), 5, (255, 0, 0), cv.FILLED)
#                     cv.putText(img, str(id), (cx + 10, cy), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
#         return self.lmList

#     def find_angle(self, img, p1, p2, p3, draw=True):
#         x1, y1 = self.lmList[p1][1:]
#         x2, y2 = self.lmList[p2][1:]
#         x3, y3 = self.lmList[p3][1:]
        
#         # Calculate angle
#         angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
#         if angle < 0:
#             angle += 360
        
#         # Draw lines and points
#         if draw:
#             cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
#             cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), 2)
#             cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
#             cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
#             cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
#             cv.putText(img, f"{int(angle)}°", (x2 - 50, y2 + 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
#         return angle

# def main():
#     cap = cv.VideoCapture("videoplayback.mp4")
#     pTime = 0
#     detector = posedetector()  # Create detector once, reuse it
    
#     while True:
#         success, img = cap.read()
#         if not success:
#             break
        
#         # Detect pose and get landmarks
#         img = detector.findpose(img, draw=True)
#         lmList = detector.getposition(img, draw=True)

#         if len(lmList) != 0:
#             # Key landmarks: 23 (left hip), 24 (right hip), 25 (left knee), 26 (right knee), 27 (left foot), 28 (right foot)
            
#             # Hip to Knee angles (left: 23-25-26, right: 24-26-25)
#             left_hip_knee = detector.find_angle(img, 23, 25, 26, draw=True)
#             right_hip_knee = detector.find_angle(img, 24,26, 25, draw=True)
            
#             # Knee to Foot angles (left: 25-27-28, right: 26-28-27)
#             left_knee_foot = detector.find_angle(img, 25, 27, 28, draw=True)
#             right_knee_foot = detector.find_angle(img, 26, 28, 27, draw=True)
            
#             # Between Hips (23-ref-24, using midpoint of knees as ref)
#             ref_x = (lmList[25][1] + lmList[26][1]) // 2
#             ref_y = (lmList[25][2] + lmList[26][2]) // 2
#             # hips_angle = detector.find_angle(img, 23, [0, ref_x, ref_y], 24, draw=True)

#             # Display all angles
#             cv.putText(img, f"L Hip-Knee: {int(left_hip_knee)}°", (10, 30), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
#             cv.putText(img, f"R Hip-Knee: {int(right_hip_knee)}°", (10, 60), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
#             cv.putText(img, f"L Knee-Foot: {int(left_knee_foot)}°", (10, 90), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
#             cv.putText(img, f"R Knee-Foot: {int(right_knee_foot)}°", (10, 120), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
#             # cv.putText(img, f"Hips: {int(hips_angle)}°", (10, 150), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

#         # FPS calculation
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#         cv.putText(img, str(int(fps)), (70, 50), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

#         cv.imshow("Img", img)
#         if cv.waitKey(1) & 0xFF == ord('d'):
#             break

#     cap.release()
#     cv.destroyAllWindows()

# if __name__ == "__main__":
#     main()




import cv2 as cv
import mediapipe as mp
import time
import math

class posedetector():
    def __init__(self, mode=False, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        self.mpdraw = mp.solutions.drawing_utils

    def findpose(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpdraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def getposition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                # Draw key landmarks: shoulders (11, 12), elbows (13, 14), wrists (15, 16), hips (23, 24), knees (25, 26), feet (27, 28)
                if draw and id in [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]:
                    cv.circle(img, (cx, cy), 5, (255, 0, 0), cv.FILLED)
                    cv.putText(img, str(id), (cx + 10, cy), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
        return self.lmList

    def find_angle(self, img, p1, p2, p3, draw=True):
        # Handle case where p2 is a manual reference point (list/tuple)
        if isinstance(p2, list) or isinstance(p2, tuple):
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = p2[1], p2[2] if len(p2) > 2 else p2[0], p2[1]
            x3, y3 = self.lmList[p3][1:]
        else:
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            x3, y3 = self.lmList[p3][1:]
        
        # Calculate angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        
        # Draw lines and points
        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), 2)
            cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
            cv.putText(img, f"{int(angle)}°", (x2 - 50, y2 + 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        return angle

def main():
    cap = cv.VideoCapture("videoplayback.mp4")
    pTime = 0
    detector = posedetector()
    
    while True:
        success, img = cap.read()
        if not success:
            break
        
        img = detector.findpose(img, draw=True)
        lmList = detector.getposition(img, draw=True)

        if len(lmList) != 0:
            # Hip to Knee (left: 23-25-26, right: 24-26-25)
            left_hip_knee = detector.find_angle(img, 23, 25, 26, draw=True)
            right_hip_knee = detector.find_angle(img, 24, 26, 25, draw=True)
            
            # Knee to Foot (left: 25-27-28, right: 26-28-27)
            left_knee_foot = detector.find_angle(img, 25, 27, 28, draw=True)
            right_knee_foot = detector.find_angle(img, 26, 28, 27, draw=True)
            
            # Between Hips (23-ref-24, ref = midpoint of knees)
            ref_x = (lmList[25][1] + lmList[26][1]) // 2
            ref_y = (lmList[25][2] + lmList[26][2]) // 2
            # hips_angle = detector.find_angle(img, 23, [0, ref_x, ref_y], 24, draw=True)

            # Shoulder to Hip (left: 11-23-24, right: 12-24-23)
            left_shoulder_hip = detector.find_angle(img, 11, 23, 24, draw=True)
            right_shoulder_hip = detector.find_angle(img, 12, 24, 23, draw=True)

            # Elbow-Shoulder-Wrist (left: 13-11-15, right: 14-12-16)
            left_arm_angle = detector.find_angle(img, 13, 11, 15, draw=True)
            right_arm_angle = detector.find_angle(img, 14, 12, 16, draw=True)

            # Display all angles
            cv.putText(img, f"L Hip-Knee: {int(left_hip_knee)}°", (10, 30), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
            cv.putText(img, f"R Hip-Knee: {int(right_hip_knee)}°", (10, 60), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
            cv.putText(img, f"L Knee-Foot: {int(left_knee_foot)}°", (10, 90), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
            cv.putText(img, f"R Knee-Foot: {int(right_knee_foot)}°", (10, 120), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
            # cv.putText(img, f"Hips: {int(hips_angle)}°", (10, 150), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
            cv.putText(img, f"L Shoulder-Hip: {int(left_shoulder_hip)}°", (10, 180), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
            cv.putText(img, f"R Shoulder-Hip: {int(right_shoulder_hip)}°", (10, 210), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
            cv.putText(img, f"L Arm: {int(left_arm_angle)}°", (10, 240), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
            cv.putText(img, f"R Arm: {int(right_arm_angle)}°", (10, 270), cv.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (70, 50), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        cv.imshow("Img", img)
        if cv.waitKey(1) & 0xFF == ord('d'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()


    