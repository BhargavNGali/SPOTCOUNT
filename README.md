**SPOTCOUNT: A Real-Time Object Detection GUI using YOLOv10**
SPOTCOUNT is an object detection and tracking application that uses a graphical user interface (GUI) built with PyQt5. It leverages the power of YOLOv10 for real-time object detection on webcam input or pre-recorded video files. The system is capable of detecting multiple objects, counting them, and displaying real-time results to the user.
__Features:__
Real-Time Object Detection: Detects and tracks multiple objects in real-time using the YOLOv10 model.
Object Counting: Keeps track of the number of detected objects in each frame and displays the total count.
Webcam and Video Input Support: Switch between webcam input or upload video files to analyze.
Customizable Classes: Choose which object classes (like 'person', 'bottle', etc.) to detect, filter results based on object type.
Interactive GUI: Simple, clean, and interactive GUI to control the detection process.

**How It Works:**
SPOTCOUNT uses the YOLOv10 model for object detection and provides a graphical interface for users to easily control the input source, start and stop detection, and view results in real-time.
__Main Components:__
1. detection_thread.py:
This file handles the object detection logic. It utilizes OpenCV to capture frames from either a webcam or a video file. The YOLOv10 model processes these frames to detect objects and output their bounding boxes and confidence scores.
Each detected object is counted, and a real-time count of the objects is displayed on the GUI.
2. gui.py:
The graphical user interface is built using PyQt5. It provides buttons to start and stop detection, select between webcam or video input, and displays both the video feed and the object count in real-time.
Users can switch between webcam detection and video file detection using a simple radio button selection.
3. main.py:
This is the entry point of the application. It initializes the GUI and starts the application.

**Installation:**
__Requirements:__
1. Ensure you have Python 3.8 or higher installed on your machine. The following packages are required to run the project:
2. PyQt5: For building the GUI.
3. OpenCV: For handling video capture and processing.
4. Torch: Required to run the YOLO model.
5. Ultralytics YOLO: The YOLOv10 model for object detection.
__Step-by-Step Installation:__
Clone the repository:
git clone https://github.com/BhargavNGali/SPOTCOUNT.git
cd SPOTCOUNT
__Install the dependencies:__
You can install all the required dependencies via the requirements.txt file using - pip install -r requirements.txt

**Usage:**
__Run the application:__
To start the object detection GUI, run: python src/main.py
__Using the GUI:__
Webcam Input: By default, the application will use your webcam as the video source. Simply click "Start Detection" to begin real-time object detection.
Video File Input: To use a video file, select "Use Input Video," and browse for a video file using the "Browse for Video File" button. Once a file is selected, click "Start Detection."
Stop Detection: You can stop the detection at any time by clicking the "Stop Detection" button, which resets the GUI.
__View Results:__
The detected objects will be highlighted with bounding boxes in the video feed.
The total number of detected objects for each frame will be displayed below the video.

**Configuration:**
You can easily modify the object classes you want to detect by editing the DetectionThread class in detection_thread.py.
For example:
detection_thread = DetectionThread("models/yolov10m.pt", ['person', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'mouse', 'keyboard', 'cell phone'])
You can add or remove object classes based on your needs.
If you have a custom YOLO model, you can replace yolov10m.pt with your custom model weights in the models/ directory and update the path accordingly in detection_thread.py.