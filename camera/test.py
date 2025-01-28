import cv2

width = 1920
height = 1080

vidPath = 'container_output/bench.mp4'
cam = cv2.VideoCapture(vidPath)

ret, frame = cam.read()
if ret:
    print(frame)
else:
    print("Failed to capture frame")
