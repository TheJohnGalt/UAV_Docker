import cv2

width = 1920
height = 1080

cam = cv2.VideoCapture(f'nvarguscamerasrc num-buffers=1 ! video/x-raw(memory:NVMM), width=(int){width}, height=(int){height}, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=I420 ! appsink', cv2.CAP_GSTREAMER)

ret, frame = cam.read()
if ret:
    print(frame)
else:
    print("Failed to capture frame")
