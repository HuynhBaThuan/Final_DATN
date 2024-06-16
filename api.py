import io
from flask import Flask, request, send_file, jsonify, send_from_directory, render_template
from flask_cors import CORS
import cv2
import numpy as np
import os
from keras.models import load_model
import base64
from io import BytesIO

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

directory = os.path.dirname(__file__)
weights = os.path.join(directory, "model/yunet_n_320_320.onnx")
face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))

model=load_model('model/model_17_5_file.h5')

labels_dict={0:'Angry',1:'Disgust', 2:'Fear', 3:'Happy',4:'Neutral',5:'Sad',6:'Surprise'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('./', filename)

@app.route('/detect_faces', methods=['POST'])
def detect_faces():
    image = request.files['image']
    image_np = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
  
    channels = 1 if len(image_np.shape) == 2 else image_np.shape[2]

    if channels == 1:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)

    if channels == 4:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGRA2BGR)

    height, width, _ = image_np.shape
    face_detector.setInputSize((width, height))

    _, faces = face_detector.detect(image_np)
    faces = faces if faces is not None else []

    results = []  # Danh sách để chứa tất cả kết quả dự đoán

    for face in faces:
        box = list(map(int, face[:4]))
        color = (0, 0, 255)
        thickness = 2
        cv2.rectangle(image_np, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), color, thickness, cv2.LINE_AA)

        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.5

        x, y, w, h = box

        sub_face_img = image_np[y:y+h, x:x+w]
        resized = cv2.resize(sub_face_img, (48, 48))
        resized = np.mean(resized, axis=2)
        normalize = resized / 255.0
        reshaped = np.reshape(normalize, (1, 48, 48, 1))
        result = model.predict(reshaped)
        label = np.argmax(result, axis=1)[0]
        emotion_label = labels_dict[label]
        print(emotion_label)

        # Thêm kết quả dự đoán vào danh sách
        results.append({
            'box': box,
            'result': result.tolist(),  # Chuyển kết quả thành danh sách để dễ dàng chuyển đổi thành JSON
            'label': emotion_label
        })

        # Vẽ nhãn cảm xúc lên khung hình
        text_position = (box[0], box[1] - 10)
        cv2.putText(image_np, emotion_label, text_position, font, scale, color, thickness, cv2.LINE_AA)

    # Chuyển đổi hình ảnh đã xử lý sang dạng base64
    _, buffer = cv2.imencode('.jpg', image_np)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Trả về JSON chứa cả hình ảnh đã xử lý và kết quả dự đoán
    return jsonify({
        'image': image_base64,
        'results': results
    })


# Định nghĩa hàm phát hiện khuôn mặt theo thời gian thực
@app.route('/detect_faces_realtime', methods=['POST'])
def detect_faces_realtime():
    data = request.get_json()
    image_data = data['image'].split(',')[1]
    image = BytesIO(base64.b64decode(image_data))
    image_np = np.frombuffer(image.read(), np.uint8)
    image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
  
    channels = 1 if len(image_np.shape) == 2 else image_np.shape[2]

    if channels == 1:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)

    if channels == 4:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGRA2BGR)

    height, width, _ = image_np.shape
    face_detector.setInputSize((width, height))

    _, faces = face_detector.detect(image_np)
    faces = faces if faces is not None else []

    results = []  # Danh sách để chứa tất cả kết quả dự đoán

    for face in faces:
        box = list(map(int, face[:4]))
        color = (0, 0, 255)
        thickness = 2
        cv2.rectangle(image_np, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), color, thickness, cv2.LINE_AA)

        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.5

        x, y, w, h = box

        sub_face_img = image_np[y:y+h, x:x+w]
        resized = cv2.resize(sub_face_img, (48, 48))
        resized = np.mean(resized, axis=2)
        normalize = resized / 255.0
        reshaped = np.reshape(normalize, (1, 48, 48, 1))
        result = model.predict(reshaped)
        label = np.argmax(result, axis=1)[0]
        emotion_label = labels_dict[label]

        # Thêm kết quả dự đoán vào danh sách
        results.append({
            'box': box,
            'result': result.tolist(),  # Chuyển kết quả thành danh sách để dễ dàng chuyển đổi thành JSON
            'label': emotion_label
        })

        # Vẽ nhãn cảm xúc lên khung hình
        text_position = (box[0], box[1] - 10)
        cv2.putText(image_np, emotion_label, text_position, font, scale, color, thickness, cv2.LINE_AA)

    # Chuyển đổi hình ảnh đã xử lý sang dạng base64
    _, buffer = cv2.imencode('.jpg', image_np)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Trả về JSON chứa cả hình ảnh đã xử lý và kết quả dự đoán
    return jsonify({
        'image': image_base64,
        'results': results
    })

    
if __name__ == '__main__':
    app.run(debug=True)
