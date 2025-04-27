import cv2 as cv
import mediapipe as mp
import time
import math
# import pafy

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
        self.results = None  # Initialize results here

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
                if draw:
                    cv.circle(img, (cx, cy), 5, (255, 0, 0), cv.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        if not self.lmList or len(self.lmList) < max(p1, p2, p3) + 1:
            return 0  # Return 0 if landmarks aren’t detected yet
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        
        # Calculate angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        
        # Draw
        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), 2)
            cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
            cv.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        return angle

def main():
    cap = cv.VideoCapture("videoplayback.mp4")  # Webcam
    # cap = cv.VideoCapture(0)

    # # YouTube URL
    # url = "https://www.youtube.com/watch?v=IODxDxX7oi4"

    # # Get the stream URL using pafy
    # video = pafy.new(url)
    # best = video.getbest(preftype="mp4")  # Get the best mp4 stream
    # stream_url = best.url

    # # Pass the stream URL to VideoCapture
    # cap = cv.VideoCapture(stream_url)

    detector = PoseDetector()
    pTime = 0
    pushup_count = 0
    stage = 'down'

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findPose(img)
        lmList = detector.getPosition(img)

        if len(lmList) != 0:
            # Calculate elbow angles (left arm: 11-13-15, right arm: 12-14-16)
            left_elbow_angle = detector.findAngle(img, 11, 13, 15)
            right_elbow_angle = detector.findAngle(img, 12, 14, 16)
            
            # Check body straightness (shoulder to hip: 11-23)
            body_angle = detector.findAngle(img, 11, 23, 24, draw=True)

            # Push-up logic
            if left_elbow_angle > 160 and right_elbow_angle > 160 and stage != "up":
                stage = "up"
            if left_elbow_angle < 90 and right_elbow_angle < 90 and stage == "up":
                stage = "down"
                pushup_count += 1
                print(f"Push-ups: {pushup_count}")

            # Check form (body should be straight, angle ~170-180°)
            if body_angle < 160 or body_angle > 200:
                cv.putText(img, "Keep body straight!", (10, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            # Display push-up count
            cv.putText(img, f"Push-ups: {pushup_count}", (10, 70), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        # FPS calculation
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv.imshow("Push-Up Detector", img)
        if cv.waitKey(1) & 0xFF == ord('q'):  # Exit with 'q'
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()