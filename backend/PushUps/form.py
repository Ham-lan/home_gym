# import cv2
# import mediapipe as mp
# import numpy as np
# import math

# class PoseDetector:
#     def __init__(self, mode=True, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.model_complexity = model_complexity
#         self.upBody = upBody
#         self.smooth = smooth
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon
#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)
#         self.mpdraw = mp.solutions.drawing_utils
#         self.results = None

#     def findpose(self, img, draw=True):
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
#                 if draw:
#                     cv2.circle(img, (cx, cy), 1, (255, 0, 0), cv2.FILLED)
#         return self.lmList

#     def find_angle(self, img, p1, p2, p3, draw=True):
#         x1, y1 = self.lmList[p1][1:]
#         x2, y2 = self.lmList[p2][1:]
#         x3, y3 = self.lmList[p3][1:]
#         angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
#         if angle < 0:
#             angle += 360
#         if draw:
#             cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
#             cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 2)
#             cv2.circle(img, (x1, y1), 15, (255, 0, 0))
#             cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
#             cv2.circle(img, (x2, y2), 15, (255, 0, 0))
#             cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
#             cv2.circle(img, (x3, y3), 15, (255, 0, 0))
#             cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)
#             cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
#         return angle

# def is_pushup_form_correct(detector, img):
#     lm_list = detector.getposition(img, draw=False)
#     if not lm_list:
#         return False

#     # Calculate hip angle (shoulder-hip-ankle)
#     hip_angle = detector.find_angle(img, 11, 23, 25, draw=False)  # Left shoulder, left hip, left ankle

#     # Calculate elbow angle (shoulder-elbow-wrist)
#     elbow_angle = detector.find_angle(img, 11, 13, 15, draw=False)  # Left shoulder, left elbow, left wrist

#     # Check if body is straight (hip angle close to 180°) and elbow is bent appropriately
#     return 160 < hip_angle < 200 and elbow_angle < 120

# # Initialize webcam and pose detector
# cap = cv2.VideoCapture(0)
# detector = PoseDetector()

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Detect pose
#     
# img = detector.findpose(frame)

#     # Get landmark positions
#     lm_list = detector.getposition(
# img)

#     if lm_list:
#         # Get coordinates for line (head to toes)
#         head = lm_list[0][1:]  # Nose
#         left_ankle = lm_list[25][1:]  # Left ankle
#         right_ankle = lm_list[26][1:]  # Right ankle

#         # Calculate average ankle position for toes
#         toes_x = (left_ankle[0] + right_ankle[0]) // 2
#         toes_y = (left_ankle[1] + right_ankle[1]) // 2

#         # Draw line from head to toes
#         cv2.line(
# img, (head[0], head[1]), (toes_x, toes_y), (0, 255, 0), 2)

#         # Check push-up form
#         if is_pushup_form_correct(detector, 
# img):
#             cv2.putText(
# img, "Correct Form", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#         else:
#             cv2.putText(
# img, "Incorrect Form", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#     # Display the 
# img
#     cv2.imshow('Push-up Form Correction', 
# img)

#     # Break loop on 'q' press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()
# detector.pose.close()


# import cv2
# import mediapipe as mp
# import numpy as np
# import math

# class PoseDetector:
#     def __init__(self, mode=True, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.model_complexity = model_complexity
#         self.upBody = upBody
#         self.smooth = smooth
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon
#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)
#         self.mpdraw = mp.solutions.drawing_utils
#         self.results = None

#     def findpose(self, img, draw=True):
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
#                 if draw:
#                     cv2.circle(img, (cx, cy), 1, (255, 0, 0), cv2.FILLED)
#         return self.lmList

# # Initialize webcam and pose detector
# cap = cv2.VideoCapture(0)
# detector = PoseDetector()

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Detect pose
#     
# img = detector.findpose(frame, draw=False)

#     # Get landmark positions
#     lm_list = detector.getposition(
# img, draw=False)

#     if lm_list:
#         # Get coordinates for line (head to toes)
#         head = lm_list[0][1:]  # Nose
#         left_ankle = lm_list[25][1:]  # Left ankle
#         right_ankle = lm_list[26][1:]  # Right ankle

#         # Calculate average ankle position for toes
#         toes_x = (left_ankle[0] + right_ankle[0]) // 2
#         toes_y = (left_ankle[1] + right_ankle[1]) // 2

#         # Draw line from head to toes
#         cv2.line(
# img, (head[0], head[1]), (toes_x, toes_y), (0, 255, 0), 2)

#     # Display the 
# img
#     cv2.imshow('Toes to Head Line', 
# img)

#     # Break loop on 'q' press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()
# detector.pose.close()

# import cv2
# import mediapipe as mp
# import numpy as np
# import math

# class PoseDetector:
#     def __init__(self, mode=True, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.model_complexity = model_complexity
#         self.upBody = upBody
#         self.smooth = smooth
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon
#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)
#         self.mpdraw = mp.solutions.drawing_utils
#         self.results = None

#     def findpose(self, img, draw=True):
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
#                 if draw:
#                     cv2.circle(img, (cx, cy), 1, (255, 0, 0), cv2.FILLED)
#         return self.lmList

# # Initialize webcam and pose detector
# cap = cv2.VideoCapture(0)
# detector = PoseDetector()

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Detect pose and draw all landmarks
#     
# img = detector.findpose(frame, draw=True)

#     # Get landmark positions
#     lm_list = detector.getposition(
# img, draw=False)

#     if lm_list:
#         # Get coordinates for line (head to left toe)
#         head = lm_list[0][1:]  # Nose (landmark 0)
#         left_toe = lm_list[25][1:]  # Left ankle (landmark 25)

#         # Draw line from head to left toe
#         cv2.line(
# img, (head[0], head[1]), (left_toe[0], left_toe[1]), (0, 255, 0), 2)

#     # Display the 
# img
#     cv2.imshow('Toe to Head Line with Landmarks', 
# img)

#     # Break loop on 'q' press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()
# detector.pose.close()


# import cv2
# import mediapipe as mp
# import numpy as np
# import math

# class PoseDetector:
#     def __init__(self, mode=True, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.model_complexity = model_complexity
#         self.upBody = upBody
#         self.smooth = smooth
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon
#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)
#         self.mpdraw = mp.solutions.drawing_utils
#         self.results = None

#     def findpose(self, img, draw=True):
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
#                 if draw:
#                     cv2.circle(img, (cx, cy), 1, (255, 0, 0), cv2.FILLED)
#         return self.lmList

# # Initialize webcam and pose detector
# cap = cv2.VideoCapture(0)
# detector = PoseDetector()

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Detect pose and draw all landmarks
#     
# img = detector.findpose(frame, draw=False)

#     # Get landmark positions
#     lm_list = detector.getposition(
# img, draw=False)

#     if lm_list and len(lm_list) > 29:  # Ensure landmark 29 exists
#         # Get coordinates for line (nose to left foot index)
#         nose = lm_list[0][1:]  # Nose (landmark 0)
#         left_toe = lm_list[29][1:]  # Left foot index (landmark 29)

#         # Draw line from nose to left toe
#         cv2.line(
# img, (nose[0], nose[1]), (left_toe[0], left_toe[1]), (0, 255, 0), 2)

#     # Display the 
# img
#     cv2.imshow('Nose to Left Toe Line with Landmarks', 
# img)

#     # Break loop on 'q' press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()
# detector.pose.close()

import cv2
import mediapipe as mp
import numpy as np
import math

class PoseDetector:
    def __init__(self, mode=True, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        self.mpdraw = mp.solutions.drawing_utils
        self.results = None

    def findpose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
                if draw:
                    cv2.circle(img, (cx, cy), 1, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def find_angle(self, img, p1, p2, p3, draw=True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 2)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0))
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0))
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (255, 0, 0))
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        return angle

def check_arm_angle(detector, img):
    lm_list = detector.getposition(img, draw=False)
    if not lm_list or len(lm_list) < 29:
        return False

    # Check left arm angle (shoulder-elbow relative to vertical ground)
    shoulder = lm_list[11][1:]  # Left shoulder (landmark 11)
    elbow = lm_list[13][1:]  # Left elbow (landmark 13)

    # Calculate angle of arm (shoulder-elbow) relative to vertical (y-axis, ground)
    delta_x = elbow[0] - shoulder[0]
    delta_y = elbow[1] - shoulder[1]
    angle = math.degrees(math.atan2(abs(delta_x), abs(delta_y)))  # Angle with vertical

    # Check if arm is approximately 90° to ground (within ±10° tolerance)
    return 80 <= angle <= 100

def form(detector , img):
    # Detect pose and draw all landmarks
    
    img = detector.findpose(img, draw=True)

    # Get landmark positions
    lm_list = detector.getposition(
        img, draw=False)

    if lm_list and len(lm_list) > 29:  # Ensure landmark 29 exists
    # Get coordinates for line (nose to left foot index)
        nose = lm_list[0][1:]  # Nose (landmark 0)
        left_toe = lm_list[29][1:]  # Left foot index (landmark 29)

    # Draw line from nose to left toe
        cv2.line(
            img, (nose[0], nose[1]), (left_toe[0], left_toe[1]), (0, 255, 0), 2)

    # Check arm angle with ground
    if check_arm_angle(detector, 
    img):
        cv2.putText(
            img, "Arms Correct (90°)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(
            img, "Adjust Arms to 90°", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    return img


def main():

    # Initialize webcam and pose detector
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect pose and draw all landmarks
        
        img = detector.findpose(frame, draw=True)

        # Get landmark positions
        lm_list = detector.getposition(
            img, draw=False)

        if lm_list and len(lm_list) > 29:  # Ensure landmark 29 exists
        # Get coordinates for line (nose to left foot index)
            nose = lm_list[0][1:]  # Nose (landmark 0)
            left_toe = lm_list[29][1:]  # Left foot index (landmark 29)

        # Draw line from nose to left toe
            cv2.line(
                img, (nose[0], nose[1]), (left_toe[0], left_toe[1]), (0, 255, 0), 2)

        # Check arm angle with ground
        if check_arm_angle(detector, 
        img):
            cv2.putText(
                img, "Arms Correct (90°)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(
                img, "Adjust Arms to 90°", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the 
        # img
        cv2.imshow('Nose to Left Toe Line with Arm Check', 
        img)

        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    detector.pose.close()

if __name__ == "__main__":
    main()

# import cv2
# import mediapipe as mp
# import numpy as np
# import math

# class PoseDetector:
#     def __init__(self, mode=True, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.model_complexity = model_complexity
#         self.upBody = upBody
#         self.smooth = smooth
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon
#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)
#         self.mpdraw = mp.solutions.drawing_utils
#         self.results = None

#     def findpose(self, img, draw=True):
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
#                 if draw:
#                     cv2.circle(img, (cx, cy), 1, (255, 0, 0), cv2.FILLED)
#         return self.lmList

# # Initialize webcam and pose detector
# cap = cv2.VideoCapture(0)
# detector = PoseDetector()

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Detect pose and draw all landmarks
#     
# img = detector.findpose(frame, draw=True)

#     # Get landmark positions
#     lm_list = detector.getposition(
# img, draw=False)

#     if lm_list and len(lm_list) > 15:  # Ensure landmark 15 exists
#         # Get coordinates for line (left shoulder to left wrist)
#         shoulder = lm_list[11][1:]  # Left shoulder (landmark 11)
#         wrist = lm_list[15][1:]  # Left wrist (landmark 15)

#         # Draw line from shoulder to wrist
#         cv2.line(
# img, (shoulder[0], shoulder[1]), (wrist[0], wrist[1]), (0, 255, 0), 2)

#     # Display the 
# img
#     cv2.imshow('Shoulder to Wrist Line with Landmarks', 
# img)

#     # Break loop on 'q' press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()
# detector.pose.close()