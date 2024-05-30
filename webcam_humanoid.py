import sys
import cv2
import torch
import time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer
import serial
from gtts import gTTS
import pygame
import os
from webcam_pyuic import Ui_MainWindow 

# COCO 클래스 이름
class_names = [
    'person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'sofa',
    'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard',
    'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
    'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

class ObjectDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('YOLOv5 Object Detection')
        self.setGeometry(100, 100, 1200, 600) 
        self.initUI()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load('.\yolov5', model='custom', path='.pt\yolov5n.pt', source='local')
        self.model.to(self.device)

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.detect_webcam)

        self.webcam = cv2.VideoCapture(0)  # 웹캠 열기
        self.ui.start_webcam_button.clicked.connect(self.start_webcam)

        self.ser = serial.Serial('COM8', 115200)  # 포트와 속도는 환경에 맞게 설정
        pygame.mixer.init()
        time.sleep(2)
        self.speak("준비완료.")

    def initUI(self):
        self.ui.start_webcam_button.clicked.connect(self.start_webcam)

    def start_webcam(self):
        if not self.timer.isActive():
            self.timer.start()

    def detect_webcam(self):
        ret, frame = self.webcam.read()  # 프레임 캡처
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.display_image(frame_rgb, self.ui.image_label)

            start = time.perf_counter()
            results = self.model(frame_rgb)
            end = time.perf_counter()

            results.render()  # Draw boxes and labels on the image
            rendered_img = results.ims[0]
            rendered_img_rgb = cv2.cvtColor(rendered_img, cv2.COLOR_BGR2RGB)
            self.display_image(rendered_img_rgb, self.ui.result_label)
            self.ui.label_3.setText(f'판독시간: {round((end - start) * 1000, 4)} ms')

            detections = results.xyxy[0].cpu().numpy()
            if len(detections) > 0:
                sorted_detections = sorted(detections, key=lambda x: x[4], reverse=True)[:1]
                for det in sorted_detections:
                    xyxy = det[:4]
                    conf = det[4]
                    cls = int(det[5])
                    class_name = class_names[cls] if cls < len(class_names) else f"클래스 {cls}"
                    self.ui.label.setText(f"클래스: {cls} - {class_name}, confidence: {conf:.2f}")
                    self.ui.label_2.setText("")
                    
                    # 모델인식 결과에 따른 로봇의 행동과 음성을 지정
                    if class_name == 'person':
                        self.robotAction(23) #Motion Table에 정의된 16번동작(Defence)
                        self.speak("사람 인식")
                        time.sleep(1)
                    elif class_name == 'bottle':
                        self.robotAction(25) #Motion Table에 정의된 16번동작(Back)
                        self.speak("병 인식")
                        time.sleep(1)

    def display_image(self, image, label):
        if image is None or image.size == 0:
            return
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.setText("")

    def robotAction(self, no):
        print(f"Robot Action: {no}")
        if self.ser.is_open:
            exeCmd = bytearray([0xff, 0xff, 0x4c, 0x53, 0x00,
                                0x00, 0x00, 0x00, 0x30, 0x0c, 0x03,
                                no, 0x00, 100, 0x00])
            exeCmd[14] = sum(exeCmd[6:14]) & 0xFF
            self.ser.write(exeCmd)
            time.sleep(0.05)

    def closeEvent(self, event):
        if self.ser.is_open:
            self.ser.close()
        event.accept()

    def speak(self, text):
        self.timer.stop()
        tts = gTTS(text=text, lang='ko')
        tts.save("output.mp3")
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        os.remove("output.mp3")
        self.timer.start()

def main():
    app = QApplication(sys.argv)
    window = ObjectDetectionApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
