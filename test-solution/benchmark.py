from PIL import Image
import io
import numpy as np
import pandas as pd
import cv2
import torch
import os
import csv
import torch
from ultralytics import YOLO
import time
import csv
import subprocess

vidPath = 'container_output/1.MP4'
    
cam = cv2.VideoCapture(vidPath)

if torch.cuda.is_available():
    print("Загрузка модели на CUDA")
    model = YOLO("best_fire.pt").to('cuda')

start_time = time.time()
frames_counter = 0
seconds = 1

while True:

    status, bgr_image = cam.read()
    
    if status:
        #bgr_image = cv2.resize(bgr_image, (680, 640))
        res = model(source=bgr_image, verbose = False)
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

    	
