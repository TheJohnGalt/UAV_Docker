import cv2
import torch
from ultralytics import YOLO
import time
import csv
import subprocess

vidPath = 'container_input/1.MP4'

cam = cv2.VideoCapture(vidPath)

if torch.cuda.is_available():
    print("Загрузка модели на CUDA")
    model = YOLO("best.pt").to('cuda')
else:
    print("Загрузка модели на NPU")
    model = YOLO("yolo11n_rknn_model")

start_time = time.time()
frames_counter = 0
seconds = 1

while True:

    status, bgr_image = cam.read()

    if status:
        res = model(source=bgr_image, verbose = False, task="obb")
    else: print('cant read file')
        
    frames_counter += 1
    
    if time.time() - start_time >= seconds:

        temp = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)
        temp = temp.decode("utf-8")
        temp = int(temp) / 1000
    
        data = [{'sec': seconds, 'FPS': frames_counter, 'temp': temp}]
        
        print(data)

        #with open('container_output/data.csv', 'a', newline='') as csvfile:
            #fieldnames = ['sec', 'FPS', 'temp']
            #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writerows(data)
            
        frames_counter = 0
        seconds += 1