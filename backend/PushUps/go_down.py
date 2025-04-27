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

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect pose and get landmarks
        frame = detector.findpose(frame)
        lmList = detector.getposition(frame)

        feedback = []
        if len(lmList) > 0:
            # Check shoulder angle (elbow-shoulder-hip ~45°)
            left_shoulder_angle = detector.find_angle(frame, LEFT_ELBOW, LEFT_SHOULDER, LEFT_HIP)
            right_shoulder_angle = detector.find_angle(frame, RIGHT_ELBOW, RIGHT_SHOULDER, RIGHT_HIP)
            avg_shoulder_angle = ( ( 360 -left_shoulder_angle ) + right_shoulder_angle) / 2
            if abs(avg_shoulder_angle - 45) > 10:
                feedback.append("Adjust arms to ~45° at shoulders!")
            else:
                feedback.append(f"Shoulder Angle: {int(avg_shoulder_angle)}° (Good)")

        # Display feedback
        for i, msg in enumerate(feedback):
            cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, 
                       (0, 0, 255) if "Adjust" in msg else (0, 255, 0), 2)

        # Show frame
        cv.imshow("Plank Shoulder Angle Calculator", frame)

        # Exit on 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()