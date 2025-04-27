import cv2 as cv
import mediapipe as mp
import math
import numpy as np

# Assuming your PoseDetector class is defined as provided
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
    cap = cv.VideoCapture("PerfectPull-Up.mp4")
    detector = PoseDetector()

    # Pull-up tracking variables
    pullup_count = 0
    stage = None  # 'up' or 'down'
    feedback = ""

    # Define landmark indices (MediaPipe pose landmarks)
    LEFT_SHOULDER = 11
    LEFT_ELBOW = 13
    LEFT_WRIST = 15
    RIGHT_SHOULDER = 12
    RIGHT_ELBOW = 14
    RIGHT_WRIST = 16
    NOSE = 0  # Used to approximate chin position

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect pose and get landmarks
        frame = detector.findpose(frame)
        lmList = detector.getposition(frame)

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
                    pullup_count += 1  # Count a pull-up when transitioning from up to down

            # Form feedback
            feedback = ""
            if stage == "down" and (left_elbow_angle < 140 or right_elbow_angle < 140):
                feedback = "Fully extend elbows at bottom!"
            elif stage == "up" and chin_y > shoulder_y:
                feedback = "Chin above bar!"

        # Display pull-up count and feedback
        cv.putText(frame, f"Pull-ups: {pullup_count}", (20, 50), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv.putText(frame, feedback, (20, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        # Show frame
        cv.imshow("Pull-up Detector", frame)

        # Exit on 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()