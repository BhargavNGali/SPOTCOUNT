from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from detection_thread import DetectionThread

def create_gui():
    # Setup the main window and layout
    window = QWidget()
    window.setWindowTitle("Object Detection GUI")
    window.setFixedSize(1000, 1000)
    layout = QVBoxLayout()

    # Video display label
    label = QLabel()
    label.setFixedSize(800, 800)
    label.setStyleSheet("border: 5px solid black; background-color: black;")
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label, alignment=Qt.AlignCenter)

    # Label for displaying object counts
    count_display = QLabel()
    count_display.setFixedSize(800, 50)
    count_display.setAlignment(Qt.AlignCenter)
    layout.addWidget(count_display, alignment=Qt.AlignCenter)

    # Start and stop buttons
    start_button = QPushButton("Start Detection")
    start_button.setStyleSheet("background-color: green; color: white;")
    stop_button = QPushButton("Stop Detection")
    stop_button.setStyleSheet("background-color: red; color: white;")
    layout.addWidget(start_button, alignment=Qt.AlignCenter)
    layout.addWidget(stop_button, alignment=Qt.AlignCenter)

    # Input source selection radio buttons
    webcam_button = QRadioButton("Use Webcam")
    video_button = QRadioButton("Use Input Video")
    webcam_button.setChecked(True)
    layout.addWidget(webcam_button, alignment=Qt.AlignCenter)
    layout.addWidget(video_button, alignment=Qt.AlignCenter)

    # File browsing button
    browse_button = QPushButton("Browse for Video File")
    layout.addWidget(browse_button, alignment=Qt.AlignCenter)
    browse_button.hide()

    window.setLayout(layout)
    stop_button.hide()  # Initially hide the stop button

    # Detection thread initialization
    detection_thread = DetectionThread("models/yolov10m.pt", ['person', 'bottle', 'wine glass', 'cup', 'fork', 'knife',
                                                       'spoon', 'bowl', 'mouse', 'keyboard', 'cell phone'])

    # Connect signals to slots for updating GUI based on thread
    detection_thread.change_pixmap_signal.connect(
        lambda qt_image: label.setPixmap(QPixmap.fromImage(qt_image).scaled(800, 800, Qt.KeepAspectRatio)))
    detection_thread.update_count_signal.connect(count_display.setText)
    detection_thread.detection_ended_signal.connect(lambda: reset_gui("No video feed. Please select a source to start detection."))

    # Function to reset GUI on detection end or error
    def reset_gui(message="Detection stopped."):
        label.clear()
        label.setText(message)
        count_display.clear()
        start_button.show()
        stop_button.hide()

    # Start detection
    def start_detection():
        if not detection_thread.isRunning():
            detection_thread.running = True
            detection_thread.start()
            start_button.hide()
            stop_button.show()

    # Stop detection and reset UI components
    def stop_detection():
        detection_thread.stop_detection()  # Command the thread to stop
        reset_gui()  # Reset the GUI after stopping

    # Browse video files and update video path
    def browse_file():
        file_name, _ = QFileDialog.getOpenFileName(window, "Open Video File", "", "Video Files (*.mp4 *.avi)")
        if file_name:
            detection_thread.video_path = file_name
            detection_thread.use_webcam = False
            detection_thread.update_source(False)

    # Handle source toggling and show/hide the browse button
    def toggle_source():
        if video_button.isChecked():
            browse_button.show()
        else:
            browse_button.hide()
            detection_thread.use_webcam = True
            detection_thread.update_source(True)

    # Connect UI elements to their corresponding functions
    start_button.clicked.connect(start_detection)
    stop_button.clicked.connect(stop_detection)
    browse_button.clicked.connect(browse_file)
    webcam_button.toggled.connect(toggle_source)
    video_button.toggled.connect(toggle_source)

    return window
