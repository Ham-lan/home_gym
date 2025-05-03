import cv2 as cv
import mediapipe as mp
import math
import numpy as np
import base64
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit, join_room
from flask_basicauth import BasicAuth
from io import BytesIO
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key
app.config['BASIC_AUTH_USERNAME'] = 'abc'
app.config['BASIC_AUTH_PASSWORD'] = 'abc12'
app.config['BASIC_AUTH_FORCE'] = True  # Require auth for all routes

basic_auth = BasicAuth(app)
socketio = SocketIO(app)

# Store userId to sid mapping for multi-user isolation
user_to_sid = {}

sid = ''

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

def processVideo(base64_video_data, process, userId):
    # img_data = base64.b64decode(base64_video_data.split(',')[1])
    # img = Image.open(BytesIO(img_data))
    # frame = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    # frame = cv.resize(frame, (640, 480))  # Optimize for performance


    img_data = base64.b64decode(base64_video_data)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv.imdecode(np_arr, cv.IMREAD_COLOR)

    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

    _, buffer = cv.imencode('.jpg', img)
    processed_base64 = base64.b64encode(buffer).decode('utf-8')
    return processed_base64

    # detector = PoseDetector()
    # frame = detector.findpose(frame)
    # lmList = detector.getposition(frame)

    # feedback = [f"User: {userId}"]
    # if len(lmList) > 0:
    #     if process == 'PlU':
    #         left_shoulder_angle = detector.find_angle(frame, 13, 11, 23)
    #         right_shoulder_angle = detector.find_angle(frame, 14, 12, 24)
    #         avg_shoulder_angle = (left_shoulder_angle + right_shoulder_angle) / 2
    #         if abs(avg_shoulder_angle - 45) > 10:
    #             feedback.append(f"Shoulder Angle: {int(avg_shoulder_angle)}° (Adjust to ~45°)")
    #         else:
    #             feedback.append(f"Shoulder Angle: {int(avg_shoulder_angle)}° (Good)")
    #     elif process == 'Sq':
    #         left_khs_angle = detector.find_angle(frame, 25, 23, 11)
    #         right_khs_angle = detector.find_angle(frame, 26, 24, 12)
    #         avg_khs_angle = (left_khs_angle + right_khs_angle) / 2
    #         if abs(avg_khs_angle - 90) > 10:
    #             feedback.append(f"Knee-Hip-Shoulder: {int(avg_khs_angle)}° (Adjust to ~90°)")
    #         else:
    #             feedback.append(f"Knee-Hip-Shoulder: {int(avg_khs_angle)}° (Good)")
    #         left_tkh_angle = detector.find_angle(frame, 27, 25, 23)
    #         right_tkh_angle = detector.find_angle(frame, 28, 26, 24)
    #         avg_tkh_angle = (left_tkh_angle + right_tkh_angle) / 2
    #         if abs(avg_tkh_angle - 90) > 10:
    #             feedback.append(f"Toe-Knee-Hip: {int(avg_tkh_angle)}° (Adjust to ~90°)")
    #         else:
    #             feedback.append(f"Toe-Knee-Hip: {int(avg_tkh_angle)}° (Good)")
    #     else:
    #         feedback.append("Unknown process type!")

    # for i, msg in enumerate(feedback):
    #     cv.putText(frame, msg, (20, 50 + i * 30), cv.FONT_HERSHEY_PLAIN, 2, 
    #                (0, 0, 255) if "Adjust" in msg or "Unknown" in msg else (0, 255, 0), 2)

    # frame = 

    # _, buffer = cv.imencode('.jpg', frame)
    # processed_base64 = 'data:image/jpeg;base64,' + base64.b64encode(buffer).decode('utf-8')
    # return processed_base64

@app.route('/')
# @basic_auth.required
def index():
    return render_template('index.html')

@app.route('/stream')
def stream(base_64_image_data):
    return render_template('stream.html' , base_64_image_data =  base_64_image_data)

@socketio.on('connect')
def handle_connect():
    # auth = request.headers.get('Authorization')

    # print(auth)

    # encoded_credentials = auth.split()[1]
    # decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    # username, password = decoded_credentials.split(':')

    # if not basic_auth.check_credentials(username, password):
    #         print("Invalid credentials")
    #         return False

    # if not auth or not basic_auth.check_credentials(auth.split()[1] if len(auth.split()) > 1 else ''):
    #     return False  # Disconnect if auth fails
    sessionId = request.sid
    room_id = request.args.get('room_id')
    # join_room(room_id)
    print(f"Client connected with sid: {sessionId}")

@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room')
    join_room(room)
    print(f'Client joined room: {room}')

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    # Remove userId associated with this sid
    for userId, user_sid in list(user_to_sid.items()):
        if user_sid == sid:
            del user_to_sid[userId]
    print(f"Client disconnected with sid: {sid}")

@app.route('/send_video', methods=['POST'])
# @basic_auth.required
def receive_video():

    # display_name = request.args.get('display_name')
    # mute_audio = request.args.get('mute_audio')  # 1 or 0
    # mute_video = request.args.get('mute_video')  # 1 or 0
    room_id = request.args.get('room_id')
    
    print(room_id)

    data = request.json
    base64_video_data = data.get('videoData')
    # process = data.get('process')
    # sid = data.get('sid')
    # userId = data.get('userId')

    if base64_video_data:
        try:
            # user_to_sid[userId] = sid  # Map userId to sid
            processed_base64 = processVideo(base64_video_data=base64_video_data, process='', userId='')

            # socketio.emit('new_video_frame', {'videoData': base64_video_data}, room= room_id )

            socketio.emit('new_video_frame', {'videoData': processed_base64 }, room= room_id )

            # stream(base_64_image_data=base64_video_data)
            
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": f"Processing error: {str(e)}"}), 500
    else:
        return jsonify({"status": "error", "message": "Missing videoData, process, sid, or userId"}), 400

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)