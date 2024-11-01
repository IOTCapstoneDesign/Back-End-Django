import torch
import cv2
import time
import threading
from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cap = cv2.VideoCapture(0)

# 운동별 카운트 및 설정 초기화
exercise_counts = {
    "squat": 0,
    "armcurl": 0,
    "standAndReturn": 0,
    "walk2Minutes": 0,
    "walk6Minutes": 0,
    "shape8Walk": 0
}

# 각 운동의 최소 카운트 및 차단 시간 설정
exercise_settings = {
    "squat": {"min_count": 1, "block_time": 1},
    "armcurl": {"min_count": 1, "block_time": 1},
    "standAndReturn": {"min_count": 2, "block_time": 1},
    "walk2Minutes": {"min_count": 1, "block_time": 2},
    "walk6Minutes": {"min_count": 1, "block_time": 2},
    "shape8Walk": {"min_count": 1, "block_time": 2}
}

detection_active = False
current_exercise = "squat"  # 기본 운동 설정
lock = threading.Lock()  # 스레드 안전성을 위한 Lock

# 운동별 모델 경로 설정
model_paths = {
    "squat": "/Users/giwonjun/Desktop/capstone/ML/squat.pt",
    "armcurl": "/Users/giwonjun/Desktop/capstone/ML/biceps.pt",
    "standAndReturn": "/Users/giwonjun/Desktop/capstone/ML/knee.pt",
    "walk2Minutes": "/Users/giwonjun/Desktop/capstone/ML/squat.pt",
    "walk6Minutes": "/Users/giwonjun/Desktop/capstone/ML/squat.pt",
    "shape8Walk": "/Users/giwonjun/Desktop/capstone/ML/squat.pt"
}

def load_model(exercise_name):
    """운동 이름에 맞는 YOLO 모델 로드."""
    model_path = model_paths.get(exercise_name)
    if not model_path:
        raise ValueError(f"{exercise_name}에 해당하는 모델이 없습니다.")
    return torch.hub.load('/Users/giwonjun/Desktop/capstone/ML/yolov5', 'custom',
                          path=model_path, source='local')

@app.route('/detect', methods=['GET'])
def detect():
    global detection_active, current_exercise

    if detection_active:
        return jsonify({'error': '이미 감지 중입니다.'}), 500

    exercise_name = request.args.get('exercise', 'squat')

    if exercise_name not in model_paths:
        return jsonify({'error': f'{exercise_name}은(는) 지원되지 않는 운동입니다.'}), 400

    current_exercise = exercise_name  # 선택된 운동 설정
    detection_active = True

    # 운동 탐지 스레드 시작
    threading.Thread(target=detect_exercise, args=(exercise_name,)).start()

    return jsonify({'message': f'{exercise_name} 탐지를 시작합니다.'})

def detect_exercise(exercise_name):
    """선택된 운동 탐지 수행."""
    global detection_active, exercise_counts

    model = load_model(exercise_name)
    start_time = time.time()
    count_detected = 0  # 탐지된 개수 초기화

    while time.time() - start_time < 30:  # 30초 동안 감지
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(frame_rgb)
        results_df = results.pandas().xyxy[0]

        # min_count 개수만큼 탐지했을 경우 카운트
        if (results_df['name'] == exercise_name).any():
            count_detected += 1  # 탐지된 개수 증가
            if count_detected >= exercise_settings[exercise_name]['min_count']:
                with lock:  # 스레드 안전하게 카운트 업데이트
                    exercise_counts[exercise_name] += 1
                count_detected = 0  # 카운트 초기화
                time.sleep(exercise_settings[exercise_name]['block_time'])  # 카운트 차단 시간

    detection_active = False

@app.route('/video_feed')
def video_feed():
    """현재 선택된 운동의 비디오 피드 제공."""
    model = load_model(current_exercise)  # 선택된 운동의 모델 로드

    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(frame_rgb).render()[0]
            annotated_frame_bgr = cv2.cvtColor(results, cv2.COLOR_RGB2BGR)

            # 운동 카운트 텍스트 오버레이
            text = f"{current_exercise.capitalize()} Count: {exercise_counts[current_exercise]}"
            cv2.putText(annotated_frame_bgr, text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', annotated_frame_bgr)
            frame_encoded = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
