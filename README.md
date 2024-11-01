# Humanoid Robot Object Recognition and Response
This system is designed to detect objects in real time using a webcam, allowing the robot to act according to the detected objects. The object detection model used is YOLOv5s, which enables fast and accurate detection, while a Logitech webcam captures the live video feed.
The GUI is implemented using PyQt, which allows users to visually observe the results of the object detection. Through the GUI, users can see the location and type of detected objects in real time and simulate how the robot’s behavior changes based on each object.
To control the robot's movements, code was first written for the Arduino board, allowing the robot to perform specific actions (e.g., moving, turning, grabbing, etc.) when an object is recognized. This system integrates object detection and robot control, enabling the robot to automatically respond to recognized objects.
With this setup, users can intuitively experience how the robot behaves based on real-time object detection and explore various applications through the convergence of object recognition technology and robotic control.

## Writing for webcam.py continued in the Webcam_NativeApp repository..
    Use PySide6 instead of PyQt5.
    Added serial port communication function.
    Using gTTS and pygame for voice output.
    Added the ability to perform robot movements when recognizing a specific object.

## Key feature additions and improvement points are as follows
    1. To create a port that does not exist on the PC, a USB to UART converter called cp2104 was used and a driver is required. 
    http://www.iamamaker.kr/ko/tutorials/cp210x-usb-to-uart-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0/
    2. The code that moves the robot was used by converting Arduino code to Python.
    3. To move the robot, you must first obtain a SerialPort object.
    
![image](https://github.com/BinnieJoe/NativeApp_Humanoid/assets/167211454/143f13b5-5fc8-425a-ab88-c2cea280b4be)
![image](https://github.com/BinnieJoe/NativeApp_Humanoid/assets/167211454/e19880fa-7bc6-44c7-a8ac-f33e65ed06bc)
![image](https://github.com/BinnieJoe/NativeApp_Humanoid/assets/167211454/1c852012-548c-4da7-a363-47caac10918e)
