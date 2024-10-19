import cv2
from ultralytics import YOLO
import torch
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage  # This should be imported from QtGui, not QtCore


class DetectionThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)  # Update GUI with new image frame
    update_count_signal = pyqtSignal(str)      # Update GUI with object count text
    detection_ended_signal = pyqtSignal()      # Signal for video end or error

    def __init__(self, model_path, classes_to_consider):
        super().__init__()
        self.model_path = model_path
        self.classes_to_consider = classes_to_consider
        self.running = False
        self.cap = None
        self.model = None
        self.use_webcam = True
        self.video_path = None

    def load_model(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Model loaded on {device}")  # Log which device is being used
        return YOLO(self.model_path).to(device)

    @pyqtSlot(bool)
    def update_source(self, use_webcam):
        self.use_webcam = use_webcam
        if self.cap:
            self.cap.release()
            self.cap = None

        if self.use_webcam:
            self.cap = cv2.VideoCapture(0)
        else:
            if self.video_path:
                self.cap = cv2.VideoCapture(self.video_path)
            else:
                print("Video path is not set.")
                return

        if not self.cap.isOpened():
            raise RuntimeError("Could not open video source.")

    def draw_detections(self, frame, results, class_names, confidence_threshold=0.75):
        object_count = {}
        for box in results[0].boxes:
            confidence = box.conf[0].item()
            if confidence >= confidence_threshold:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0].item())
                class_name = class_names[class_id]
                if class_name not in self.classes_to_consider:
                    continue

                object_count[class_name] = object_count.get(class_name, 0) + 1
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        total_count = sum(object_count.values())
        count_text = f"Total Objects: {total_count}"
        self.update_count_signal.emit(count_text)
        return frame

    def run(self):
        try:
            self.model = self.load_model()
            self.update_source(self.use_webcam)

            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("No frame received from the video source.")
                    self.detection_ended_signal.emit()
                    break

                results = self.model.track(source=frame, show=False)
                frame = self.draw_detections(frame, results, self.model.names)

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.change_pixmap_signal.emit(qt_image)
        except Exception as e:
            print(f"An error occurred in the detection thread: {e}")
        finally:
            if self.cap:
                self.cap.release()
            self.stop_detection()

    def stop_detection(self):
        self.running = False
        self.change_pixmap_signal.emit(QImage())
        self.update_count_signal.emit("Detection stopped.")
        if self.cap:
            self.cap.release()
