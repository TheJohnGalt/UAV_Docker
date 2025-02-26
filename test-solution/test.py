import numpy as np
import pandas as pd
from typing import List, Union
import cv2
import torch
import os
import csv
from ultralytics import YOLO

print(torch.cuda.is_available())

# import cv2

# width = 3280
# height = 2464

# cam = cv2.VideoCapture("nvarguscamerasrc sensor-id=0 tnr-mode=2 tnr-strength=1 ! video/x-raw(memory:NVMM), width=(int){width}, height=(int){height}, framerate=21/1, format=(string)NV12 ! nvvidconv ! video/x-raw, format=(string)BGRx ! appsink")

# stat, img = cam.read()

# print(stat)