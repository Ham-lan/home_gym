import cv2 as cv
import mediapipe as mp
import time
import math

class PoseDetector:
    def __init__(self, mode=False, model_complexity=1, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None
        self.lmList = []

    def findPose(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def getPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw and id in [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]:
                    cv.circle(img, (cx, cy), 5, (255, 0, 0), cv.FILLED)
                    cv.putText(img, str(id), (cx + 10, cy), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
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
            cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), 2)
            cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
            cv.putText(img, f"{int(angle)}°", (x2 - 50, y2 + 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        return angle

def analyzePushUp(img, angles, state, count):
    feedback = []
    was_down = state["was_down"]

    # Arm angles for push-up detection
    left_arm = angles["left_arm"]
    right_arm = angles["right_arm"]
    
    # Detect push-up position
    if left_arm < 100 and right_arm < 100:
        state["was_down"] = True
        feedback.append(("Position: Down", (0, 255, 0)))
    elif left_arm > 160 and right_arm > 160 and was_down:
        state["was_down"] = False
        count[0] += 1
        feedback.append(("Position: Up - Push-up counted!", (0, 255, 0)))
    else:
        feedback.append(("Position: Keep going", (255, 255, 0)))

    # Form feedback
    for side, angle in [("Left Arm", left_arm), ("Right Arm", right_arm)]:
        if 0 <= angle <= 20 or 160 <= angle <= 180:
            feedback.append((f"{side}: Good ({angle}°)", (0, 255, 0)))
        elif angle < 100:
            feedback.append((f"{side}: Lower down more ({angle}°)", (0, 0, 255)))
        else:
            feedback.append((f"{side}: Adjust arm position ({angle}°)", (0, 0, 255)))

    for side, angle in [("Left Shoulder-Hip", angles["left_shoulder_hip"]), ("Right Shoulder-Hip", angles["right_shoulder_hip"])]:
        if 160 <= angle <= 180:
            feedback.append((f"{side}: Good ({angle}°)", (0, 255, 0)))
        elif angle < 160:
            feedback.append((f"{side}: Sagging, lift hips ({angle}°)", (0, 0, 255)))
        else:
            feedback.append((f"{side}: Piking, lower hips ({angle}°)", (0, 0, 255)))

    # Display feedback and count
    h, w, _ = img.shape
    cv.putText(img, f"Push-ups: {count[0]}", (10, 30), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    for i, (text, color) in enumerate(feedback):
        text_size, _ = cv.getTextSize(text, cv.FONT_HERSHEY_PLAIN, 2, 3)
        x, y = 10, 70 + i * 40
        cv.rectangle(img, (x, y - 30), (x + text_size[0] + 10, y + 10), (0, 0, 0), -1)
        cv.putText(img, text, (x, y), cv.FONT_HERSHEY_PLAIN, 2, color, 3)

    return state, count

def main():
    # Initialize video capture (0 for webcam, or provide a video file path)
    cap = cv.VideoCapture(0)  # Change to "path/to/video.mp4" for a video file
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    detector = PoseDetector()
    count = [0]  # Use list to allow modification in function
    state = {"was_down": False}
    pTime = 0

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to read frame.")
            break

        # Resize frame for faster processing (optional)
        img = cv.resize(img, (1280, 720), interpolation=cv.INTER_AREA)

        # Process pose
        img = detector.findPose(img, draw=True)
        lmList = detector.getPosition(img, draw=True)

        if len(lmList) != 0:
            # Calculate relevant angles
            angles = {
                "left_arm": detector.findAngle(img, 13, 11, 15, draw=True),  # Left elbow-shoulder-wrist
                "right_arm": detector.findAngle(img, 14, 12, 16, draw=True),  # Right elbow-shoulder-wrist
                "left_shoulder_hip": detector.findAngle(img, 11, 23, 25, draw=True),  # Left shoulder-hip-knee
                "right_shoulder_hip": detector.findAngle(img, 12, 24, 26, draw=True),  # Right shoulder-hip-knee
            }

            # Analyze push-up and update count
            state, count = analyzePushUp(img, angles, state, count)

        # Display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime) if cTime != pTime else 0
        pTime = cTime
        cv.putText(img, f"FPS: {int(fps)}", (10, 100), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Show frame
        cv.imshow("Push-Up Counter", img)

        # Break on 'q' key
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
    print(f"Total Push-ups: {count[0]}")

if __name__ == "__main__":
    main()