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
#     cap = cv.VideoCapture('FIRST_PULLUP.mp4')
#     detector = PoseDetector()

#     # Define landmark indices (MediaPipe pose landmarks)
#     LEFT_SHOULDER = 11
#     RIGHT_SHOULDER = 12
#     LEFT_ELBOW = 13
#     RIGHT_ELBOW = 14
#     LEFT_WRIST = 15
#     RIGHT_WRIST = 16
#     LEFT_EAR = 7
#     RIGHT_EAR = 8

#     # Variables for tracking scapular movement and reps
#     shoulder_ear_distances = []
#     max_frames = 10  # Store last 10 frames to smooth detection
#     stage = None  # 'up' (elevated) or 'down' (depressed)
#     rep_count = 0  # Count completed scapular contractions

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Detect pose and get landmarks
#         frame = detector.findpose(frame)
#         lmList = detector.getposition(frame)

#         feedback = []
#         if len(lmList) > 0:
#             # 1. Check elbow straightness (angle > 160 degrees)
#             left_elbow_angle = detector.find_angle(frame, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
#             right_elbow_angle = detector.find_angle(frame, RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)
#             if left_elbow_angle < 160 or right_elbow_angle < 160:
#                 feedback.append("Keep elbows straight!")

#             # 2. Check scapular movement (shoulder-to-ear distance)
#             left_shoulder_y = lmList[LEFT_SHOULDER][2]
#             right_shoulder_y = lmList[RIGHT_SHOULDER][2]
#             left_ear_y = lmList[LEFT_EAR][2]
#             right_ear_y = lmList[RIGHT_EAR][2]
#             avg_shoulder_ear_dist = ((left_ear_y - left_shoulder_y) + (right_ear_y - right_shoulder_y)) / 2

#             # Store distance
#             shoulder_ear_distances.append(avg_shoulder_ear_dist)
#             if len(shoulder_ear_distances) > max_frames:
#                 shoulder_ear_distances.pop(0)

#             # Detect movement (up/down)
#             if len(shoulder_ear_distances) == max_frames:
#                 movement_range = max(shoulder_ear_distances) - min(shoulder_ear_distances)
#                 if movement_range > 20:  # Lowered threshold for sensitivity
#                     current_dist = shoulder_ear_distances[-1]
#                     if current_dist <= min(shoulder_ear_distances) + 5 and stage != "down":
#                         stage = "down"  # Shoulders depressed
#                         if stage == "down" and prev_stage == "up":
#                             rep_count += 1  # Count a rep on down phase
#                     elif current_dist >= max(shoulder_ear_distances) - 5 and stage != "up":
#                         stage = "up"  # Shoulders elevated
#                 else:
#                     feedback.append("Move shoulders up and down!")
#             prev_stage = stage

#         # Display feedback and rep count
#         for i, msg in enumerate(feedback):
#             cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
#         if not feedback and stage:
#             cv.putText(frame, f"Good Form! Stage: {stage}", 
#                       (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
#         cv.putText(frame, f"Reps: {rep_count}", (20, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

#         # Show frame
#         cv.imshow("Scapular Contractions Corrector", frame)

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
    cap = cv.VideoCapture('FIRST_PULLUP.mp4')
    detector = PoseDetector()

    # Define landmark indices (MediaPipe pose landmarks)
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16

    # Variables for tracking scapular movement and reps
    shoulder_widths = []
    max_frames = 10  # Store last 10 frames to smooth detection
    stage = None  # 'neutral' (elevated/relaxed) or 'contracted' (depressed/retracted)
    rep_count = 0  # Count completed scapular contractions
    baseline_width = None  # To store initial shoulder width

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect pose and get landmarks
        frame = detector.findpose(frame)
        lmList = detector.getposition(frame)

        feedback = []
        if len(lmList) > 0:
            # 1. Check elbow straightness (angle > 160 degrees)
            left_elbow_angle = detector.find_angle(frame, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
            right_elbow_angle = detector.find_angle(frame, RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)
            if left_elbow_angle < 160 or right_elbow_angle < 160:
                feedback.append("Keep elbows straight!")

            # 2. Check scapular movement (shoulder width reduction)
            shoulder_width = abs(lmList[LEFT_SHOULDER][1] - lmList[RIGHT_SHOULDER][1])
            
            # Set baseline width in first 10 frames
            if baseline_width is None and len(shoulder_widths) < max_frames:
                shoulder_widths.append(shoulder_width)
                if len(shoulder_widths) == max_frames:
                    baseline_width = sum(shoulder_widths) / max_frames
            else:
                shoulder_widths.append(shoulder_width)
                if len(shoulder_widths) > max_frames:
                    shoulder_widths.pop(0)

                # Detect movement (4-5% width reduction)
                if baseline_width:
                    current_width = shoulder_widths[-1]
                    width_reduction = (baseline_width - current_width) / baseline_width * 100
                    if width_reduction >= 4:
                    # and stage != "contracted":
                        stage = "contracted"  # Scapulae depressed/retracted
                    elif width_reduction <= 2: 
                    # and stage == "contracted":
                        stage = "neutral"  # Scapulae relaxed
                        rep_count += 1  # Count a rep on return to neutral
                    if width_reduction < 4 and stage != "contracted" and stage != "neutral":
                        feedback.append("Pull shoulder blades together and down!")

        # Display feedback and rep count
        for i, msg in enumerate(feedback):
            cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        if not feedback and stage:
            cv.putText(frame, f"Good Form! Stage: {stage}", 
                      (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv.putText(frame, f"Reps: {rep_count}", (20, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # Show frame
        cv.imshow("Scapular Contractions Corrector", frame)

        # Exit on 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()