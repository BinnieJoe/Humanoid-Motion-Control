# NativeApp_Humanoid
This can detect objects in real time from a webcam, have the robot act according to the detected object, and implement a function to notify by voice.

## I created it by adding functions to the Wecam_NativeApp repository webcam.py.
    Use PySide6 instead of PyQt5.
    Added serial port communication function.
    Using gTTS and pygame for voice output.
    Added the ability to perform robot movements when recognizing a specific object.

## Key feature additions and improvement points are as follows
    1. To create a port that does not exist on the PC, a USB to UART converter called cp2104 was used and a driver is required. 
    2. http://www.iamamaker.kr/ko/tutorials/cp210x-usb-to-uart-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0/
    3. The code that moves the robot was used by converting Arduino code to Python.
    4. To move the robot, you must first obtain a SerialPort object.
    
![image](https://github.com/BinnieJoe/NativeApp_Humanoid/assets/167211454/a4cf6e85-67ff-4a28-a71d-4a6bcda9a399)
![image](https://github.com/BinnieJoe/NativeApp_Humanoid/assets/167211454/46c75db4-b65e-4b07-82ca-ed6544b74640)
![image](https://github.com/BinnieJoe/NativeApp_Humanoid/assets/167211454/1c852012-548c-4da7-a363-47caac10918e)
