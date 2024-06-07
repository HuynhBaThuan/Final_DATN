import os
import numpy as np
from keras.models import load_model
import cv2

def main():
    model=load_model('model/model_file.h5')
    # model=load_model('model/model_file_30epochs.h5')
    directory = os.path.dirname(__file__)
    images_folder = os.path.join(directory, 'images')
    if not os.path.exists(images_folder):
        print("Thư mục 'images' không tồn tại.")
    else:
        # Lấy danh sách các tệp trong thư mục 'images'
        image_files = [os.path.join(images_folder, file) for file in os.listdir(images_folder) if file.endswith('.jpg')]

        # Kiểm tra xem có tệp nào trong thư mục không
        if len(image_files) == 0:
            print("Không có tệp hình ảnh trong thư mục 'images'.")
        else:

            weights = os.path.join(directory, "model/yunet_n_320_320.onnx")
            face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))

            labels_dict={0:'Angry',1:'Disgust', 2:'Fear', 3:'Happy',4:'Neutral',5:'Sad',6:'Surprise'}

            for image_file in image_files:
                image = cv2.imread(image_file)  # Đọc hình ảnh từ tệp
                if image is None:
                    print(f"Cannot read image file: {image_file}")
                    continue
                
                channels = 1 if len(image.shape) == 2 else image.shape[2]

                if channels == 1:
                    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

                if channels == 4:
                    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

                print(image.shape)
                height, width, _ = image.shape
                face_detector.setInputSize((width, height))

                _, faces = face_detector.detect(image)
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
                    # print(x,y,w,h)

                    # image_file1 = os.path.join(directory, 'PrivateTest_518212.jpg')
                    # image1 = cv2.imread(image_file1)

                    sub_face_img = image[y:y+h, x:x+w]
                    resized = cv2.resize(sub_face_img, (48, 48))
                    resized = np.mean(resized, axis=2)
                    # print(resized.dtype, resized.shape)
                    normalize = resized / 255.0
                    # print(normalize.dtype, normalize.shape)
                    reshaped = np.reshape(normalize, (1, 48, 48, 1))
                    result = model.predict(reshaped)
                    label = np.argmax(result, axis=1)[0]
                    emotion_label = labels_dict[label]
                    print(emotion_label)

                # Draw emotion label on the frame
                    text_position = (box[0], box[1] - 10)
                    cv2.putText(image, emotion_label, text_position, font, scale, color, thickness, cv2.LINE_AA)
                
                cv2.imshow("Image", image)  # Hiển thị hình ảnh
                cv2.waitKey(0)  # Chờ một phím nhấn để chuyển sang hình ảnh tiếp theo hoặc thoát

            cv2.destroyAllWindows()  # Đóng tất cả các cửa sổ hiển thị

if __name__ == '__main__':
    main()
