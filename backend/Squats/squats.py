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
#     cap = cv.VideoCapture('Squat.mp4')
#     detector = PoseDetector()

#     # Define landmark indices (MediaPipe pose landmarks)
#     LEFT_SHOULDER = 11
#     RIGHT_SHOULDER = 12
#     LEFT_HIP = 23
#     RIGHT_HIP = 24
#     LEFT_KNEE = 25
#     RIGHT_KNEE = 26
#     LEFT_ANKLE = 27
#     RIGHT_ANKLE = 28
#     NOSE = 0  # Proxy for head

#     # Variables for tracking squats
#     stage = None  # 'up' or 'down'
#     rep_count = 0
#     max_frames = 10
#     hip_heights = []

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Detect pose and get landmarks
#         frame = detector.findpose(frame)
#         lmList = detector.getposition(frame)

#         feedback = []
#         if len(lmList) > 0:
#             # Draw line from hips to head (average hip to nose)
#             hip_x = (lmList[LEFT_HIP][1] + lmList[RIGHT_HIP][1]) // 2
#             hip_y = (lmList[LEFT_HIP][2] + lmList[RIGHT_HIP][2]) // 2
#             nose_x, nose_y = lmList[NOSE][1], lmList[NOSE][2]
#             cv.line(frame, (hip_x, hip_y), (nose_x, nose_y), (0, 255, 0), thickness=3)

#             # 1. Check knee angle (~90° at bottom)
#             left_knee_angle = detector.find_angle(frame, LEFT_HIP, LEFT_KNEE, LEFT_ANKLE)
#             right_knee_angle = detector.find_angle(frame, RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE)
#             avg_knee_angle = (left_knee_angle + right_knee_angle) / 2
#             if stage == "down" and abs(avg_knee_angle - 90) > 10:
#                 feedback.append("Bend knees to ~90° at bottom!")

#             # 2. Check back alignment (hip-shoulder-nose ~180°)
#             shoulder_x = (lmList[LEFT_SHOULDER][1] + lmList[RIGHT_SHOULDER][1]) // 2
#             shoulder_y = (lmList[LEFT_SHOULDER][2] + lmList[RIGHT_SHOULDER][2]) // 2
#             alignment_angle = math.degrees(
#                 math.atan2(nose_y - shoulder_y, nose_x - shoulder_x) -
#                 math.atan2(shoulder_y - hip_y, shoulder_x - hip_x)
#             )
#             # if alignment_angle < 0:
#             #     alignment_angle += 360
#             #     print(alignment_angle)
#             print( abs(alignment_angle - 180) )
#             if abs(alignment_angle - 180) > 5:
#                 feedback.append("Keep torso upright, align head to hips!")

#             # 3. Check hip depth (hips near knee level at bottom)
#             knee_y = (lmList[LEFT_KNEE][2] + lmList[RIGHT_KNEE][2]) / 2
#             hip_heights.append(hip_y)
#             if len(hip_heights) > max_frames:
#                 hip_heights.pop(0)
#             if stage == "down" and abs(hip_y - knee_y) > 50:
#                 feedback.append("Lower hips to knee level!")

#             # 4. Check knee position (not too far past toes)
#             left_knee_x = lmList[LEFT_KNEE][1]
#             right_knee_x = lmList[RIGHT_KNEE][1]
#             left_ankle_x = lmList[LEFT_ANKLE][1]
#             right_ankle_x = lmList[RIGHT_ANKLE][1]
#             if left_knee_x > left_ankle_x + 50 or right_knee_x > right_ankle_x + 50:
#                 feedback.append("Keep knees behind toes!")

#             # Detect stage and count reps
#             if avg_knee_angle < 100 and abs(hip_y - knee_y) < 50:  # Bottom position
#                 stage = "down"
#             elif avg_knee_angle > 160:  # Top position
#                 if stage == "down":
#                     stage = "up"
#                     rep_count += 1
#                 if stage == "up" and avg_knee_angle < 160:
#                     feedback.append("Fully extend knees at top!")

#         # Display feedback and rep count
#         for i, msg in enumerate(feedback):
#             cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
#         if not feedback and stage:
#             cv.putText(frame, f"Good Squat Form! Stage: {stage}", 
#                       (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
#         cv.putText(frame, f"Reps: {rep_count}", (20, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

#         # Show frame
#         cv.imshow("Squat Form Analyzer", frame)

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

def squats(detector , frame):
    # Define landmark indices (MediaPipe pose landmarks)
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28

    # Detect pose and get landmarks
    frame = detector.findpose(frame)
    lmList = detector.getposition(frame)

    feedback = []
    if len(lmList) > 0:
        # 1. Check knee-hip-shoulder angle (~90° at bottom)
        left_khs_angle = detector.find_angle(frame, LEFT_KNEE, LEFT_HIP, LEFT_SHOULDER)
        right_khs_angle = detector.find_angle(frame, RIGHT_KNEE, RIGHT_HIP, RIGHT_SHOULDER)
        avg_khs_angle = (left_khs_angle + right_khs_angle) / 2
        if abs(avg_khs_angle - 60) > 10:
            feedback.append(f"Hip-Shoulder: {int(avg_khs_angle)}° (Adjust to ~90°)")
        else:
            feedback.append(f"Hip-Shoulder: {int(avg_khs_angle)}° (Good)")

        # 2. Check toe-knee-hip angle (~90° at bottom)
        left_tkh_angle = detector.find_angle(frame, LEFT_ANKLE, LEFT_KNEE, LEFT_HIP)
        right_tkh_angle = detector.find_angle(frame, RIGHT_ANKLE, RIGHT_KNEE, RIGHT_HIP)
        avg_tkh_angle = (left_tkh_angle + right_tkh_angle) / 2
        if abs(  ( 360 - avg_tkh_angle ) - 90) > 10:
            feedback.append(f"Toe-Knee: {int(avg_tkh_angle)}° (Adjust to ~90°)")
        else:
            feedback.append(f"Toe-Knee: {int(avg_tkh_angle)}° (Good)")

    # Display feedback
    for i, msg in enumerate(feedback):
        cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, 
                    (0, 0, 255) if "Adjust" in msg else (0, 255, 0), 2)

    return frame    



def main():
    # Initialize video capture (use 0 for webcam or provide a video file path)
    cap = cv.VideoCapture('Squat.mp4')
    detector = PoseDetector()

    # Define landmark indices (MediaPipe pose landmarks)
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect pose and get landmarks
        frame = detector.findpose(frame)
        lmList = detector.getposition(frame)

        feedback = []
        if len(lmList) > 0:
            # 1. Check knee-hip-shoulder angle (~90° at bottom)
            left_khs_angle = detector.find_angle(frame, LEFT_KNEE, LEFT_HIP, LEFT_SHOULDER)
            right_khs_angle = detector.find_angle(frame, RIGHT_KNEE, RIGHT_HIP, RIGHT_SHOULDER)
            avg_khs_angle = (left_khs_angle + right_khs_angle) / 2
            if abs(avg_khs_angle - 60) > 10:
                feedback.append(f"Hip-Shoulder: {int(avg_khs_angle)}° (Adjust to ~90°)")
            else:
                feedback.append(f"Hip-Shoulder: {int(avg_khs_angle)}° (Good)")

            # 2. Check toe-knee-hip angle (~90° at bottom)
            left_tkh_angle = detector.find_angle(frame, LEFT_ANKLE, LEFT_KNEE, LEFT_HIP)
            right_tkh_angle = detector.find_angle(frame, RIGHT_ANKLE, RIGHT_KNEE, RIGHT_HIP)
            avg_tkh_angle = (left_tkh_angle + right_tkh_angle) / 2
            if abs(  ( 360 - avg_tkh_angle ) - 90) > 10:
                feedback.append(f"Toe-Knee: {int(avg_tkh_angle)}° (Adjust to ~90°)")
            else:
                feedback.append(f"Toe-Knee: {int(avg_tkh_angle)}° (Good)")

        # Display feedback
        for i, msg in enumerate(feedback):
            cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, 
                       (0, 0, 255) if "Adjust" in msg else (0, 255, 0), 2)

        # Show frame
        cv.imshow("Squat Angle Analyzer", frame)

        # Exit on 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()