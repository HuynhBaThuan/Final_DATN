import cv2
import numpy as np
from keras.models import load_model
import os
import time

model=load_model('model/model_file.h5')
directory = os.path.dirname(__file__)
video=cv2.VideoCapture(0)

weights = os.path.join(directory, "model/yunet_n_320_320.onnx")
faceDetect = cv2.FaceDetectorYN_create(weights, "", (0, 0))

labels_dict={0:'Angry',1:'Disgust', 2:'Fear', 3:'Happy',4:'Neutral',5:'Sad',6:'Surprise'}

while True:
    result,image=video.read()
    if not result:
            break

    channels = 1 if len(image.shape) == 2 else image.shape[2]

    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    height, width, _ = image.shape
    faceDetect.setInputSize((width, height))
    _, faces = faceDetect.detect(image)

    faces = faces if faces is not None else []

    for face in faces:
        box = list(map(int, face[:4]))
        print(box)
        color = (0, 0, 255)
        thickness = 2
        cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.5

        x, y, w, h = box
        print(x,y,w,h)
        sub_face_img = image[y:y+h, x:x+w]
        resized = cv2.resize(sub_face_img, (48, 48))
        resized = np.mean(resized, axis=2)
        normalize = resized / 255.0
        reshaped = np.reshape(normalize, (1, 48, 48, 1))
        result = model.predict(reshaped)
        label = np.argmax(result, axis=1)[0]
        emotion_label = labels_dict[label]

        # Draw emotion label on the frame
        text_position = (box[0], box[1] - 10)
        cv2.putText(image, emotion_label, text_position, font, scale, color, thickness, cv2.LINE_AA)
    
    # out.write(image) # Ghi khung hình vào video

    
    cv2.imshow("Camera", image) # Hiển thị khung hình từ camera
    key = cv2.waitKey(1) # Chờ một phím nhấn
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()