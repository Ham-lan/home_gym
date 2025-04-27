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
#                 if draw and id in [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]:
#                     cv.circle(img, (cx, cy), 5, (255, 0, 0), cv.FILLED)
#                     cv.putText(img, str(id), (cx + 10, cy), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
#         return self.lmList

#     def find_angle(self, img, p1, p2, p3, draw=True):
#         if isinstance(p2, list) or isinstance(p2, tuple):
#             x1, y1 = self.lmList[p1][1:]
#             x2, y2 = p2[1], p2[2]
#             x3, y3 = self.lmList[p3][1:]
#         else:
#             x1, y1 = self.lmList[p1][1:]
#             x2, y2 = self.lmList[p2][1:]
#             x3, y3 = self.lmList[p3][1:]
        
#         angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
#         if angle < 0:
#             angle += 360
#         if angle > 180:
#             angle = 360 - angle
        
#         if draw:
#             cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
#             cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), 2)
#             cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
#             cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
#             cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
#             cv.putText(img, f"{int(angle)}°", (x2 - 50, y2 + 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
#         return angle

# def analyze_pre_pushup(img, angles):
#     feedback = []
#     # In starting position, arms should be straight (shoulder-elbow-wrist ~180°)
#     for side, angle in [("Left Arm", angles["left_arm"]), ("Right Arm", angles["right_arm"])]:
#         if 160 <= angle <= 180:

#             feedback.append((f"{side}: Good (straight)", (0, 255, 0)))
#         else:
#             feedback.append((f"{side}: Bend your arms less, keep them straight", (0, 0, 255)))

#     # Shoulder to Hip (torso should be straight, ~180°)
#     for side, angle in [("Left Shoulder-Hip", angles["left_shoulder_hip"]), ("Right Shoulder-Hip", angles["right_shoulder_hip"])]:
#         if 160 <= angle <= 180:
#             feedback.append((f"{side}: Good", (0, 255, 0)))
#         elif angle < 160:
#             feedback.append((f"{side}: Sagging, lift hips", (0, 0, 255)))
#         else:
#             feedback.append((f"{side}: Piking, lower hips", (0, 0, 255)))

#     # Hip to Knee (legs straight, ~180°)
#     for side, angle in [("Left Hip-Knee", angles["left_hip_knee"]), ("Right Hip-Knee", angles["right_hip_knee"])]:
#         if 160 <= angle <= 180:
#             feedback.append((f"{side}: Good", (0, 255, 0)))
#         else:
#             feedback.append((f"{side}: Straighten legs", (0, 0, 255)))

#     # Knee to Foot (legs straight, ~180°)
#     for side, angle in [("Left Knee-Foot", angles["left_knee_foot"]), ("Right Knee-Foot", angles["right_knee_foot"])]:
#         if 160 <= angle <= 180:
#             feedback.append((f"{side}: Good", (0, 255, 0)))
#         else:
#             feedback.append((f"{side}: Straighten legs", (0, 0, 255)))

#     # Between Hips (should be level, ~0-20°)
#     if 0 <= angles["hips"] <= 20:
#         feedback.append(("Hips: Good", (0, 255, 0)))
#     else:
#         feedback.append(("Hips: Twisted, keep level", (0, 0, 255)))

#     # Display feedback
#     for i, (text, color) in enumerate(feedback):
#         cv.putText(img, text, (10, 30 + i * 30), cv.FONT_HERSHEY_PLAIN, 1.5, color, 2)

# def main():
#     cap = cv.VideoCapture("PerfectPushUp.mp4")
#     pTime = 0
#     detector = posedetector()
#     analyzed = False  # Flag to run analysis only once
    
#     while True:
#         success, img = cap.read()
#         if not success:
#             break
        
#         img = detector.findpose(img, draw=True)
#         lmList = detector.getposition(img, draw=True)

#         if len(lmList) != 0 and not analyzed:
#             # Calculate all angles
#             angles = {
#                 "left_hip_knee": detector.find_angle(img, 23, 25, 26, draw=True),
#                 "right_hip_knee": detector.find_angle(img, 24, 26, 25, draw=True),
#                 "left_knee_foot": detector.find_angle(img, 25, 27, 28, draw=True),
#                 "right_knee_foot": detector.find_angle(img, 26, 28, 27, draw=True),
#                 "hips": detector.find_angle(img, 23, [0, (lmList[25][1] + lmList[26][1]) // 2, (lmList[25][2] + lmList[26][2]) // 2], 24, draw=True),
#                 "left_shoulder_hip": detector.find_angle(img, 11, 23, 24, draw=True),
#                 "right_shoulder_hip": detector.find_angle(img, 12, 24, 23, draw=True),
#                 "left_arm": detector.find_angle(img, 13, 11, 15, draw=True),
#                 "right_arm": detector.find_angle(img, 14, 12, 16, draw=True)
#             }

#             # Analyze pre-push-up form
#             analyze_pre_pushup(img, angles)
#             analyzed = True  # Only analyze once

#         # FPS
#         cTime = time.time()
#         fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
#         pTime = cTime
#         cv.putText(img, str(int(fps)), (70, 50), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

#         cv.imshow("Pre-Push-Up Analyzer", img)
#         if cv.waitKey(1) & 0xFF == ord('d'):
#             break

#     cap.release()
#     cv.destroyAllWindows()

# if __name__ == "__main__":
#     main()


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
#                 if draw and id in [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]:
#                     cv.circle(img, (cx, cy), 5, (255, 0, 0), cv.FILLED)
#                     cv.putText(img, str(id), (cx + 10, cy), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
#         return self.lmList

#     def find_angle(self, img, p1, p2, p3, draw=True):
#         if isinstance(p2, list) or isinstance(p2, tuple):
#             x1, y1 = self.lmList[p1][1:]
#             x2, y2 = p2[1], p2[2]
#             x3, y3 = self.lmList[p3][1:]
#         else:
#             x1, y1 = self.lmList[p1][1:]
#             x2, y2 = self.lmList[p2][1:]
#             x3, y3 = self.lmList[p3][1:]
        
#         angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
#         if angle < 0:
#             angle += 360
#         if angle > 180:
#             angle = 360 - angle
        
#         if draw:
#             cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
#             cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), 2)
#             cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
#             # cv.circle(img, (width: 100% ) )
#             cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
#             cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
#             cv.putText(img, f"{int(angle)}°", (x2 - 50, y2 + 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
#         return angle

# def analyze_pre_pushup(img, angles):
#     feedback = []
#     for side, angle in [("Left Arm", angles["left_arm"]), ("Right Arm", angles["right_arm"])]:
#         if 160 <= angle <= 180:
#             feedback.append((f"{side}: Good (straight)", (0, 255, 0)))
#         else:
#             feedback.append((f"{side}: Bend your arms less, keep them straight", (0, 0, 255)))

#     for side, angle in [("Left Shoulder-Hip", angles["left_shoulder_hip"]), ("Right Shoulder-Hip", angles["right_shoulder_hip"])]:
#         if 160 <= angle <= 180:
#             feedback.append((f"{side}: Good", (0, 255, 0)))
#         elif angle < 160:
#             feedback.append((f"{side}: Sagging, lift hips", (0, 0, 255)))
#         else:
#             feedback.append((f"{side}: Piking, lower hips", (0, 0, 255)))

#     for side, angle in [("Left Hip-Knee", angles["left_hip_knee"]), ("Right Hip-Knee", angles["right_hip_knee"])]:
#         if 160 <= angle <= 180:
#             feedback.append((f"{side}: Good", (0, 255, 0)))
#         else:
#             feedback.append((f"{side}: Straighten legs", (0, 0, 255)))

#     for side, angle in [("Left Knee-Foot", angles["left_knee_foot"]), ("Right Knee-Foot", angles["right_knee_foot"])]:
#         if 160 <= angle <= 180:
#             feedback.append((f"{side}: Good", (0, 255, 0)))
#         else:
#             feedback.append((f"{side}: Straighten legs", (0, 0, 255)))

#     if 0 <= angles["hips"] <= 20:
#         feedback.append(("Hips: Good", (0, 255, 0)))
#     else:
#         feedback.append(("Hips: Twisted, keep level", (0, 0, 255)))

#     # Display feedback with a background rectangle for visibility
#     h, w, _ = img.shape
#     for i, (text, color) in enumerate(feedback):
#         text_size, _ = cv.getTextSize(text, cv.FONT_HERSHEY_PLAIN, 2, 3)
#         x, y = 10, 50 + i * 40
#         # Background rectangle
#         cv.rectangle(img, (x, y - 30), (x + text_size[0] + 10, y + 10), (0, 0, 0), -1)  # Black background
#         # Text on top
#         cv.putText(img, text, (x, y), cv.FONT_HERSHEY_PLAIN, 2, color, 3)
#         print(f"Rendering: {text} at ({x}, {y})")  # Debug print

# def main():

#     img = cv.imread("PerfectPushStance.png")

#     detector = posedetector()



#     img = detector.findpose(img, draw=True)
#     lmList = detector.getposition(img, draw=True)

#     analyzed = False

#     if len(lmList) != 0 and not analyzed:
#             angles = {
#                 "left_hip_knee": detector.find_angle(img, 23, 25, 26, draw=True),
#                 "right_hip_knee": detector.find_angle(img, 24, 26, 25, draw=True),
#                 "left_knee_foot": detector.find_angle(img, 25, 27, 28, draw=True),
#                 "right_knee_foot": detector.find_angle(img, 26, 28, 27, draw=True),
#                 "hips": detector.find_angle(img, 23, [0, (lmList[25][1] + lmList[26][1]) // 2, (lmList[25][2] + lmList[26][2]) // 2], 24, draw=True),
#                 "left_shoulder_hip": detector.find_angle(img, 11, 23, 24, draw=True),
#                 "right_shoulder_hip": detector.find_angle(img, 12, 24, 23, draw=True),
#                 "left_arm": detector.find_angle(img, 13, 11, 15, draw=True),
#                 "right_arm": detector.find_angle(img, 14, 12, 16, draw=True)
#             }

#     analyze_pre_pushup(img, angles)


    # cap = cv.VideoCapture("PerfectPushUp.mp4")
    # pTime = 0
    # detector = posedetector()
    # analyzed = False
    
    # while True:
    #     success, img = cap.read()
    #     if not success:
    #         break
        
    #     img = detector.findpose(img, draw=True)
    #     lmList = detector.getposition(img, draw=True)

    #     if len(lmList) != 0 and not analyzed:
    #         angles = {
    #             "left_hip_knee": detector.find_angle(img, 23, 25, 26, draw=True),
    #             "right_hip_knee": detector.find_angle(img, 24, 26, 25, draw=True),
    #             "left_knee_foot": detector.find_angle(img, 25, 27, 28, draw=True),
    #             "right_knee_foot": detector.find_angle(img, 26, 28, 27, draw=True),
    #             "hips": detector.find_angle(img, 23, [0, (lmList[25][1] + lmList[26][1]) // 2, (lmList[25][2] + lmList[26][2]) // 2], 24, draw=True),
    #             "left_shoulder_hip": detector.find_angle(img, 11, 23, 24, draw=True),
    #             "right_shoulder_hip": detector.find_angle(img, 12, 24, 23, draw=True),
    #             "left_arm": detector.find_angle(img, 13, 11, 15, draw=True),
    #             "right_arm": detector.find_angle(img, 14, 12, 16, draw=True)
    #         }

    #         analyze_pre_pushup(img, angles)
    #         analyzed = True

    #     # FPS
    #     cTime = time.time()
    #     fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    #     pTime = cTime
    #     cv.putText(img, str(int(fps)), (70, 50), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    #     cv.imshow("Pre-Push-Up Analyzer", img)
    #     if cv.waitKey(1) & 0xFF == ord('d'):
    #         break

    # cap.release()
    # cv.destroyAllWindows()

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
                if draw and id in [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]:
                    cv.circle(img, (cx, cy), 5, (255, 0, 0), cv.FILLED)  # Red circles for landmarks
                    cv.putText(img, str(id), (cx + 10, cy), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)  # Yellow ID labels
        return self.lmList

    def find_angle(self, img, p1, p2, p3, draw=True):
        if isinstance(p2, list) or isinstance(p2, tuple):
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = p2[1], p2[2]
            x3, y3 = self.lmList[p3][1:]
        else:
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            x3, y3 = self.lmList[p3][1:]
        
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        if angle > 180:
            angle = 360 - angle
        
        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)  # White lines
            cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), 2)
            cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
            cv.putText(img, f"{int(angle)}°", (x2 - 50, y2 + 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        return angle

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
            feedback.append((f"{side}: Sagging, lift hips {angle}", (0, 0, 255)))
        else:
            feedback.append((f"{side}: Piking, lower hips {angle}", (0, 0, 255)))

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

    if 0 <= angles["hips"] <= 20:
        feedback.append(("Hips: Good", (0, 255, 0)))
    else:
        feedback.append(("Hips: Twisted, keep level", (0, 0, 255)))


    angles_handToHip = angles["hip_shoulder_hand"]
    feedback.append((f"Hand to Hip: {angles_handToHip}", (0, 255, 0)))

    angles_shoulder_Elbow = angles['shouler_other_elbow']
    feedback.append((f"Angles Shoulder Elbow: {angles_shoulder_Elbow}", (0, 255, 0)))


    # Display feedback with a background rectangle
    h, w, _ = img.shape
    for i, (text, color) in enumerate(feedback):
        text_size, _ = cv.getTextSize(text, cv.FONT_HERSHEY_PLAIN, 2, 3)
        x, y = 10, 50 + i * 40
        cv.rectangle(img, (x, y - 30), (x + text_size[0] + 10, y + 10), (0, 0, 0), -1)  # Black background
        cv.putText(img, text, (x, y), cv.FONT_HERSHEY_PLAIN, 2, color, 3)
        print(f"Rendering: {text} at ({x}, {y})")

def main():
    # Load the image
    img_path = "Pushups.jpg"  # Ensure this is correct
    img = cv.imread(img_path)

    if img is None:
        print(f"Error: Could not load image at '{img_path}'. Check file path or name.")
        return

    # Resize image if too small (e.g., double the size)
    h, w, _ = img.shape
    print(f"Original image size: {w}x{h}")
    if h < 500 or w < 500:  # If smaller than 500x500, resize
        scale_factor = 2
        img = cv.resize(img, (w * scale_factor, h * scale_factor), interpolation=cv.INTER_LINEAR)
        print(f"Resized image to: {w * scale_factor}x{h * scale_factor}")

    detector = posedetector()

    # Process the image
    img = detector.findpose(img, draw=True)  # Draws pose connections
    lmList = detector.getposition(img, draw=True)  # Draws landmarks and IDs

    if len(lmList) != 0:
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

        analyze_pre_pushup(img, angles)

    # Save the output for inspection (optional)
    cv.imwrite("output_pushup_analysis.png", img)
    print("Output saved as 'output_pushup_analysis.png'")

    # Display the result
    cv.imshow("Pre-Push-Up Analyzer", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()