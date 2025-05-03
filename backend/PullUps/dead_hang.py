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

def getDeadHang(frame,detector):
    # Detect pose and get landmarks
        LEFT_WRIST = 15
        RIGHT_WRIST = 16
        LEFT_SHOULDER = 11
        RIGHT_SHOULDER = 12
        LEFT_ANKLE = 27
        RIGHT_ANKLE = 28
        frame = detector.findpose(frame)
        lmList = detector.getposition(frame)

        feedback = []
        if len(lmList) > 0:
            # 1. Check if legs are close together (ankle distance)
            ankle_distance = abs(lmList[LEFT_ANKLE][1] - lmList[RIGHT_ANKLE][1])
            if ankle_distance > 60:  # Threshold in pixels (adjust based on resolution)
                feedback.append("Keep legs close together!")

            # 2. Check if hand distance is slightly wider than shoulder width
            wrist_distance = abs(lmList[LEFT_WRIST][1] - lmList[RIGHT_WRIST][1])
            shoulder_distance = abs(lmList[LEFT_SHOULDER][1] - lmList[RIGHT_SHOULDER][1])
            if wrist_distance < shoulder_distance * 1.1 or wrist_distance > shoulder_distance * 3:
                feedback.append("Hands should be slightly wider than shoulders!")

        # Display feedback
        for i, msg in enumerate(feedback):
            cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        if not feedback:
            cv.putText(frame, "Good Dead Hang Form!", (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        
        return frame

def main():
    # Initialize video capture (use 0 for webcam or provide a video file path)
    cap = cv.VideoCapture('FIRST_PULLUP.mp4')
    detector = PoseDetector()

    # Define landmark indices (MediaPipe pose landmarks)
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
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
            # 1. Check if legs are close together (ankle distance)
            ankle_distance = abs(lmList[LEFT_ANKLE][1] - lmList[RIGHT_ANKLE][1])
            if ankle_distance > 60:  # Threshold in pixels (adjust based on resolution)
                feedback.append("Keep legs close together!")

            # 2. Check if hand distance is slightly wider than shoulder width
            wrist_distance = abs(lmList[LEFT_WRIST][1] - lmList[RIGHT_WRIST][1])
            shoulder_distance = abs(lmList[LEFT_SHOULDER][1] - lmList[RIGHT_SHOULDER][1])
            if wrist_distance < shoulder_distance * 1.1 or wrist_distance > shoulder_distance * 3:
                feedback.append("Hands should be slightly wider than shoulders!")

        # Display feedback
        for i, msg in enumerate(feedback):
            cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        if not feedback:
            cv.putText(frame, "Good Dead Hang Form!", (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # Show frame
        cv.imshow("Simple Dead Hang Posture Corrector", frame)

        # Exit on 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()