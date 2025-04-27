# import cv2 as cv
# import mediapipe as mp
# import math
# import numpy as np

# # Your PoseDetector class
# class PoseDetector:
#     def __init__(self, mode=True, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.model_complexity = model_complexity
#         self.upBody = upBody
#         self.smooth = smooth
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon
#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, 
#                                      self.smooth, self.detectionCon, self.trackCon)
#         self.mpdraw = mp.solutions.drawing_utils

#     def findpose(self, img, draw=True):
#         imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#         self.results = self.pose.process(imgRGB)
#         if self.results.pose_landmarks:
#             if draw:
#                 self.mpdraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
#         return img

#     def getposition(self, img, draw=True):
#         self.lmList = []
#         if self.results.pose_landmarks:
#             for id, lm in enumerate(self.results.pose_landmarks.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 self.lmList.append([id, cx, cy])
#                 if draw:
#                     cv.circle(img, (cx, cy), 1, (255, 0, 0), cv.FILLED)
#         return self.lmList

#     def find_angle(self, img, p1, p2, p3, draw=True):
#         x1, y1 = self.lmList[p1][1:]
#         x2, y2 = self.lmList[p2][1:]
#         x3, y3 = self.lmList[p3][1:]
        
#         angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
#         if angle < 0:
#             angle += 360
        
#         if draw:
#             cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=2)
#             cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), thickness=2)
#             cv.circle(img, (x1, y1), 15, (255, 0, 0))
#             cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
#             cv.circle(img, (x2, y2), 15, (255, 0, 0))
#             cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
#             cv.circle(img, (x3, y3), 15, (255, 0, 0))
#             cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
#             cv.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
#         return angle

# def main():
#     # Initialize video capture (use 0 for webcam or provide a video file path)
#     cap = cv.VideoCapture('PerfectPushUp.mp4')
#     detector = PoseDetector()

#     # Define landmark indices (MediaPipe pose landmarks)
#     LEFT_SHOULDER = 11
#     RIGHT_SHOULDER = 12
#     LEFT_ELBOW = 13
#     RIGHT_ELBOW = 14
#     LEFT_HIP = 23
#     RIGHT_HIP = 24
#     LEFT_ANKLE = 27
#     RIGHT_ANKLE = 28
#     NOSE = 0  # Proxy for head

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Detect pose and get landmarks
#         frame = detector.findpose(frame)
#         lmList = detector.getposition(frame)

#         feedback = []
#         if len(lmList) > 0:
#             # Draw line from toes to head (average ankle to nose)
#             ankle_x = (lmList[LEFT_ANKLE][1] + lmList[RIGHT_ANKLE][1]) // 2
#             ankle_y = (lmList[LEFT_ANKLE][2] + lmList[RIGHT_ANKLE][2]) // 2
#             nose_x, nose_y = lmList[NOSE][1], lmList[NOSE][2]
#             cv.line(frame, (ankle_x, ankle_y), (nose_x, nose_y), (0, 255, 0), thickness=3)

#             # 1. Check body alignment (ankle-hip-shoulder angle ~180°)
#             hip_x = (lmList[LEFT_HIP][1] + lmList[RIGHT_HIP][1]) // 2
#             hip_y = (lmList[LEFT_HIP][2] + lmList[RIGHT_HIP][2]) // 2
#             shoulder_x = (lmList[LEFT_SHOULDER][1] + lmList[RIGHT_SHOULDER][1]) // 2
#             shoulder_y = (lmList[LEFT_SHOULDER][2] + lmList[RIGHT_SHOULDER][2]) // 2
#             alignment_angle = math.degrees(
#                 math.atan2(shoulder_y - hip_y, shoulder_x - hip_x) -
#                 math.atan2(hip_y - ankle_y, hip_x - ankle_x)
#             )
#             if alignment_angle < 0:
#                 alignment_angle += 360
#             if abs(alignment_angle - 180) > 20:
#                 feedback.append("Keep body straight from head to toes!")

#             # 2. Check elbow position (under shoulders)
#             elbow_x = (lmList[LEFT_ELBOW][1] + lmList[RIGHT_ELBOW][1]) / 2
#             if abs(elbow_x - shoulder_x) > 50:  # Threshold in pixels
#                 feedback.append("Place elbows directly under shoulders!")

#             # 3. Check shoulder height (avoid sagging or piking)
#             ankle_y_avg = (lmList[LEFT_ANKLE][2] + lmList[RIGHT_ANKLE][2]) / 2
#             hip_y_avg = (lmList[LEFT_HIP][2] + lmList[RIGHT_HIP][2]) / 2
#             if shoulder_y > hip_y_avg + 50:  # Shoulders too low
#                 feedback.append("Raise shoulders, tighten core!")
#             elif shoulder_y < hip_y_avg - 50:  # Shoulders too high
#                 feedback.append("Lower hips, keep body flat!")

#         # Display feedback
#         for i, msg in enumerate(feedback):
#             cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
#         if not feedback:
#             cv.putText(frame, "Good Plank Form!", 
#                       (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

#         # Show frame
#         cv.imshow("Plank Form Analyzer", frame)

#         # Exit on 'q'
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv.destroyAllWindows()

# if __name__ == "__main__":
#     main()




# import cv2 as cv
# import mediapipe as mp
# import math
# import numpy as np

# # Your PoseDetector class
# class PoseDetector:
#     def __init__(self, mode=True, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.model_complexity = model_complexity
#         self.upBody = upBody
#         self.smooth = smooth
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon
#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, 
#                                      self.smooth, self.detectionCon, self.trackCon)
#         self.mpdraw = mp.solutions.drawing_utils

#     def findpose(self, img, draw=True):
#         imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#         self.results = self.pose.process(imgRGB)
#         if self.results.pose_landmarks:
#             if draw:
#                 self.mpdraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
#         return img

#     def getposition(self, img, draw=True):
#         self.lmList = []
#         if self.results.pose_landmarks:
#             for id, lm in enumerate(self.results.pose_landmarks.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 self.lmList.append([id, cx, cy])
#                 if draw:
#                     cv.circle(img, (cx, cy), 1, (255, 0, 0), cv.FILLED)
#         return self.lmList

#     def find_angle(self, img, p1, p2, p3, draw=True):
#         x1, y1 = self.lmList[p1][1:]
#         x2, y2 = self.lmList[p2][1:]
#         x3, y3 = self.lmList[p3][1:]
        
#         angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
#         if angle < 0:
#             angle += 360
        
#         if draw:
#             cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=2)
#             cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), thickness=2)
#             cv.circle(img, (x1, y1), 15, (255, 0, 0))
#             cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
#             cv.circle(img, (x2, y2), 15, (255, 0, 0))
#             cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
#             cv.circle(img, (x3, y3), 15, (255, 0, 0))
#             cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
#             cv.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
#         return angle

# def main():
#     # Initialize video capture (use 0 for webcam or provide a video file path)
#     cap = cv.VideoCapture('PerfectPushUp.mp4')
#     detector = PoseDetector()

#     # Define landmark indices (MediaPipe pose landmarks)
#     LEFT_SHOULDER = 11
#     RIGHT_SHOULDER = 12
#     LEFT_ELBOW = 13
#     RIGHT_ELBOW = 14
#     LEFT_WRIST = 15
#     RIGHT_WRIST = 16
#     LEFT_HIP = 23
#     RIGHT_HIP = 24
#     LEFT_ANKLE = 27
#     RIGHT_ANKLE = 28
#     NOSE = 0  # Proxy for head

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Detect pose and get landmarks
#         frame = detector.findpose(frame)
#         lmList = detector.getposition(frame)

#         feedback = []
#         if len(lmList) > 0:
#             # Draw line from toes to head (average ankle to nose)
#             ankle_x = (lmList[LEFT_ANKLE][1] + lmList[RIGHT_ANKLE][1]) // 2
#             ankle_y = (lmList[LEFT_ANKLE][2] + lmList[RIGHT_ANKLE][2]) // 2
#             nose_x, nose_y = lmList[NOSE][1], lmList[NOSE][2]
#             cv.line(frame, (ankle_x, ankle_y), (nose_x, nose_y), (0, 255, 0), thickness=3)

#             # 1. Check body alignment (ankle-hip-shoulder angle ~180°)
#             hip_x = (lmList[LEFT_HIP][1] + lmList[RIGHT_HIP][1]) // 2
#             hip_y = (lmList[LEFT_HIP][2] + lmList[RIGHT_HIP][2]) // 2
#             shoulder_x = (lmList[LEFT_SHOULDER][1] + lmList[RIGHT_SHOULDER][1]) // 2
#             shoulder_y = (lmList[LEFT_SHOULDER][2] + lmList[RIGHT_SHOULDER][2]) // 2
#             alignment_angle = math.degrees(
#                 math.atan2(shoulder_y - hip_y, shoulder_x - hip_x) -
#                 math.atan2(hip_y - ankle_y, hip_x - ankle_x)
#             )
#             if alignment_angle < 0:
#                 alignment_angle += 360
#             if abs(alignment_angle - 180) > 20:
#                 feedback.append("Keep body straight from head to toes!")

#             # 2. Check elbow position (under shoulders)
#             elbow_x = (lmList[LEFT_ELBOW][1] + lmList[RIGHT_ELBOW][1]) / 2
#             if abs(elbow_x - shoulder_x) > 50:
#                 feedback.append("Place elbows directly under shoulders!")

#             # 3. Check shoulder height (avoid sagging or piking)
#             ankle_y_avg = (lmList[LEFT_ANKLE][2] + lmList[RIGHT_ANKLE][2]) / 2
#             hip_y_avg = (lmList[LEFT_HIP][2] + lmList[RIGHT_HIP][2]) / 2
#             if shoulder_y > hip_y_avg + 50:
#                 feedback.append("Raise shoulders, tighten core!")
#             elif shoulder_y < hip_y_avg - 50:
#                 feedback.append("Lower hips, keep body flat!")

#             # 4. Check shoulder angle (elbow-shoulder-wrist ~45°)
#             left_shoulder_angle = detector.find_angle(frame, LEFT_ELBOW, LEFT_SHOULDER, LEFT_WRIST)
#             right_shoulder_angle = detector.find_angle(frame, RIGHT_ELBOW, RIGHT_SHOULDER, RIGHT_WRIST)
#             avg_shoulder_angle = (left_shoulder_angle + right_shoulder_angle) / 2
#             if abs(avg_shoulder_angle - 45) > 10:
#                 feedback.append("Adjust arms to ~45° at shoulders!")

#         # Display feedback
#         for i, msg in enumerate(feedback):
#             cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
#         if not feedback:
#             cv.putText(frame, "Good Plank Form!", 
#                       (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

#         # Show frame
#         cv.imshow("Plank Form Analyzer", frame)

#         # Exit on 'q'
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv.destroyAllWindows()

# if __name__ == "__main__":
#     main()

import cv2 as cv
import mediapipe as mp
import math
import numpy as np

# Your PoseDetector class
class PoseDetector:
    def __init__(self, mode=True, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, 
                                     self.smooth, self.detectionCon, self.trackCon)
        self.mpdraw = mp.solutions.drawing_utils

    def findpose(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpdraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def getposition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 1, (255, 0, 0), cv.FILLED)
        return self.lmList

    def find_angle(self, img, p1, p2, p3, draw=True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        
        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=2)
            cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), thickness=2)
            cv.circle(img, (x1, y1), 15, (255, 0, 0))
            cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x2, y2), 15, (255, 0, 0))
            cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x3, y3), 15, (255, 0, 0))
            cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
            cv.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        return angle

def main():
    # Initialize video capture (use 0 for webcam or provide a video file path)
    cap = cv.VideoCapture('PerfectPushUp.mp4')
    detector = PoseDetector()

    # Define landmark indices (MediaPipe pose landmarks)
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    NOSE = 0  # Proxy for head

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect pose and get landmarks
        frame = detector.findpose(frame)
        lmList = detector.getposition(frame)

        feedback = []
        if len(lmList) > 0:
            # Draw line from toes to head (average ankle to nose)
            ankle_x = (lmList[LEFT_ANKLE][1] + lmList[RIGHT_ANKLE][1]) // 2
            ankle_y = (lmList[LEFT_ANKLE][2] + lmList[RIGHT_ANKLE][2]) // 2
            nose_x, nose_y = lmList[NOSE][1], lmList[NOSE][2]
            cv.line(frame, (ankle_x, ankle_y), (nose_x, nose_y), (0, 255, 0), thickness=3)

            # 1. Check body alignment (ankle-hip-shoulder angle ~180°)
            hip_x = (lmList[LEFT_HIP][1] + lmList[RIGHT_HIP][1]) // 2
            hip_y = (lmList[LEFT_HIP][2] + lmList[RIGHT_HIP][2]) // 2
            shoulder_x = (lmList[LEFT_SHOULDER][1] + lmList[RIGHT_SHOULDER][1]) // 2
            shoulder_y = (lmList[LEFT_SHOULDER][2] + lmList[RIGHT_SHOULDER][2]) // 2
            alignment_angle = math.degrees(
                math.atan2(shoulder_y - hip_y, shoulder_x - hip_x) -
                math.atan2(hip_y - ankle_y, hip_x - ankle_x)
            )
            if alignment_angle < 0:
                alignment_angle += 360
            if abs(alignment_angle - 180) > 20:
                feedback.append("Keep body straight from head to toes!")

            # 2. Check elbow position (under shoulders)
            elbow_x = (lmList[LEFT_ELBOW][1] + lmList[RIGHT_ELBOW][1]) / 2
            if abs(elbow_x - shoulder_x) > 50:
                feedback.append("Place elbows directly under shoulders!")

            # 3. Check shoulder height (avoid sagging or piking)
            ankle_y_avg = (lmList[LEFT_ANKLE][2] + lmList[RIGHT_ANKLE][2]) / 2
            hip_y_avg = (lmList[LEFT_HIP][2] + lmList[RIGHT_HIP][2]) / 2
            if shoulder_y > hip_y_avg + 50:
                feedback.append("Raise shoulders, tighten core!")
            elif shoulder_y < hip_y_avg - 50:
                feedback.append("Lower hips, keep body flat!")

            # 4. Check shoulder angle (elbow-shoulder-hip ~45°)
            left_shoulder_angle = detector.find_angle(frame, 13, 11, 23)
            right_shoulder_angle = detector.find_angle(frame, 14, 12, 24)
            avg_shoulder_angle = ( right_shoulder_angle + ( 360 - left_shoulder_angle )) / 2
            print(  left_shoulder_angle )
            print( right_shoulder_angle )
            
            if abs(avg_shoulder_angle - 45) > 10:
                feedback.append("Adjust arms to ~45° at shoulders!")

        # Display feedback
        for i, msg in enumerate(feedback):
            cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        if not feedback:
            cv.putText(frame, "Good Plank Form!", 
                      (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # Show frame
        cv.imshow("Plank Form Analyzer", frame)

        # Exit on 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()