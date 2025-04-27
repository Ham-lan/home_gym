import cv2 as cv
import mediapipe as mp
import math
import time
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
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    NOSE = 0  # Proxy for chin position

    # Variables for tracking descent and reps
    shoulder_heights = []
    descent_start_time = None
    stage = None  # 'top', 'descending', 'bottom'
    rep_count = 0
    max_frames = 10  # Smooth detection
    descent_duration = 3  # Target descent time in seconds

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect pose and get landmarks
        frame = detector.findpose(frame)
        lmList = detector.getposition(frame)

        feedback = []
        current_time = time.time()
        if len(lmList) > 0:
            # 1. Check elbow extension at bottom
            left_elbow_angle = detector.find_angle(frame, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
            right_elbow_angle = detector.find_angle(frame, RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)
            if stage == "bottom" and (left_elbow_angle < 160 or right_elbow_angle < 160):
                feedback.append("Fully straighten elbows at bottom!")

            # 2. Check body alignment (shoulders, hips, ankles)
            shoulder_x = (lmList[LEFT_SHOULDER][1] + lmList[RIGHT_SHOULDER][1]) / 2
            hip_x = (lmList[LEFT_HIP][1] + lmList[RIGHT_HIP][1]) / 2
            ankle_x = (lmList[LEFT_ANKLE][1] + lmList[RIGHT_ANKLE][1]) / 2
            if abs(shoulder_x - hip_x) > 30 or abs(hip_x - ankle_x) > 30:
                feedback.append("Keep body straight, align hips and ankles!")

            # 3. Track descent (shoulder height and time)
            avg_shoulder_y = (lmList[LEFT_SHOULDER][2] + lmList[RIGHT_SHOULDER][2]) / 2
            chin_y = lmList[NOSE][2]
            shoulder_heights.append(avg_shoulder_y)
            if len(shoulder_heights) > max_frames:
                shoulder_heights.pop(0)

            # Detect stage
            if chin_y < avg_shoulder_y - 20:  # Chin above shoulders (top position)
                stage = "top"
                descent_start_time = current_time
                shoulder_heights.clear()  # Reset for new descent
            elif len(shoulder_heights) == max_frames:
                height_change = max(shoulder_heights) - min(shoulder_heights)
                if height_change > 50:  # Significant downward movement
                    stage = "descending"
                    if descent_start_time:
                        elapsed_time = current_time - descent_start_time
                        if elapsed_time < descent_duration - 0.5:
                            feedback.append("Lower more slowly!")
                if left_elbow_angle > 160 and right_elbow_angle > 160 and height_change > 50:
                    if stage == "descending":
                        elapsed_time = current_time - descent_start_time
                        if elapsed_time >= descent_duration - 0.5:
                            stage = "bottom"
                            rep_count += 1
                            descent_start_time = None

        # Display feedback and rep count
        for i, msg in enumerate(feedback):
            cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        if not feedback and stage:
            cv.putText(frame, f"Good Form! Stage: {stage}", 
                      (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv.putText(frame, f"Reps: {rep_count}", (20, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # Show frame
        cv.imshow("Negative Pull-ups Corrector", frame)

        # Exit on 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()