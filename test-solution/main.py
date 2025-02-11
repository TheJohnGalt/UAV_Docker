
import cv2
import torch
from ultralytics import YOLO
import os
import json
import socket
from datetime import datetime
import math

import urllib.request
import numpy as np

import sys

print(sys.argv)

# Загрузка модели YOLO
model = YOLO('best_fire.pt')

# Параметры сети для отправки данных
TCP_IP = '127.0.0.1'
TCP_PORT = 5005

# Создание сокета и подключение к серверу - пока заглушено
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((TCP_IP, TCP_PORT))

# Предварительная обработка
def preprocess_frame(frame):
    frame = cv2.resize(frame, (640, 640))
    return frame

# Вычисление угловых отклонений объекта на изображении - ещё считать и считать, но вроде правильно
def get_object_angles(x_pixel, y_pixel, image_width, image_height, fov_horizontal, fov_vertical):
    # Координаты центра изображения
    center_x = image_width / 2
    center_y = image_height / 2
    delta_x = x_pixel - center_x
    delta_y = center_y - y_pixel
    angle_x = (delta_x / center_x) * (fov_horizontal / 2)
    angle_y = (delta_y / center_y) * (fov_vertical / 2)

    return angle_x, angle_y

# Функция для вычисления координат объекта - вроде правильное
def calculate_object_coordinates(gps_coordinates, azimuth, elevation, distance):

    azimuth_rad = math.radians(azimuth)
    elevation_rad = math.radians(elevation)
    delta_x = distance * math.cos(elevation_rad) * math.sin(azimuth_rad)
    delta_y = distance * math.cos(elevation_rad) * math.cos(azimuth_rad)
    delta_z = distance * math.sin(elevation_rad)
    earth_radius = 6378137.0
    delta_latitude = (delta_z / earth_radius) * (180 / math.pi)
    delta_longitude = (delta_x / (earth_radius * math.cos(math.pi * gps_coordinates['latitude'] / 180))) * (180 / math.pi)
    object_latitude = gps_coordinates['latitude'] + delta_latitude
    object_longitude = gps_coordinates['longitude'] + delta_longitude

    return {
        "latitude": object_latitude,
        "longitude": object_longitude
    }

# Анализ детекций и сбор данных в JSON - основная функция
def analyze_output(results, frame, camera_id, camera_params):
    detections = []
    image_height, image_width = frame.shape[:2]

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            confidence = box.conf.item()
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            object_center_x = (x1 + x2) / 2
            object_center_y = (y1 + y2) / 2

            angle_x, angle_y = get_object_angles(
                x_pixel=object_center_x,
                y_pixel=object_center_y,
                image_width=image_width,
                image_height=image_height,
                fov_horizontal=camera_params['fov_horizontal'],
                fov_vertical=camera_params['fov_vertical']
            )

            absolute_azimuth = (camera_params['azimuth'] + angle_x) % 360
            absolute_elevation = camera_params['elevation'] + angle_y

            # расстояние до объекта - пока 100 метров, дальше будем менять либо фиксированно относительно полёта дрона
            # Либо же динамически менять?
            distance_to_object = 100.0

            object_coordinates = calculate_object_coordinates(
                gps_coordinates=camera_params['gps_coordinates'],
                azimuth=absolute_azimuth,
                elevation=absolute_elevation,
                distance=distance_to_object
            )
            detection = {
                "timestamp": datetime.now().isoformat(),
                "camera_id": camera_id,
                "class_id": class_id,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2],
                "gps_coordinates": camera_params['gps_coordinates'],
                "camera_direction": {
                    "azimuth": camera_params['azimuth'],
                    "elevation": camera_params['elevation']
                },
                "object_direction": {
                    "azimuth": absolute_azimuth,
                    "elevation": absolute_elevation
                },
                "object_coordinates": object_coordinates
            }

            detections.append(detection)

            # Сохранение изображения при достаточной уверенности
            if confidence > 0.6:
                print("save")
                label = "fire" if class_id == 0 else "smoke"
                filename = os.path.join(os.getcwd(), f"container_output/{label}_{camera_id}_{detection['timestamp']}.jpg")
                cv2.imwrite(filename, frame)

        if detections:
            # Отправка данных в формате JSON
            json_data = json.dumps({"detections": detections})
            #sock.sendall(json_data.encode('utf-8'))

        return detections
# Параметры камеры (заменим потом на реальные параметры)
camera_params_operator = {
    "fov_horizontal": 70.0,
    "fov_vertical": 60.0,    # Угол обзора по вертикали и горизонтали
    "gps_coordinates": {
        "latitude": 55.7558,
        "longitude": 37.6173
    },
    "azimuth": 90.0,
    "elevation": 0.0
}

camera_params_uav = {
    "fov_horizontal": 70.0,
    "fov_vertical": 60.0,    # Угол обзора по вертикали и горизонтали
    "gps_coordinates": {
        "latitude": 55.7558,
        "longitude": 37.6173
    },
    "azimuth": 90.0,
    "elevation": -10.0
}

# Инициализация двух видеопотоков - для тестов на ноутбуке второй пока что заглушен, но он ловится
#cap_operator = cv2.VideoCapture(0)  # Камера оператора
#cap_uav = cv2.VideoCapture(1)       # Камера БПЛА

#if not cap_operator.isOpened() or not cap_uav.isOpened():
#    print("Ошибка: Не удалось открыть одну или обе камеры.")
#    exit()

# Функция для получения изображения с другого контейнера
def fetch_image():
    url = "http://host.docker.internal:9000/image"
    try:
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return True, img
    except Exception as e:
        print(f"Возникла ошибка: {e}")
        return False, None

while True:

    ret_op, frame_op = fetch_image() #cap_operator.read()
    if not ret_op:
        break
    input_frame_op = preprocess_frame(frame_op)
    results_op = model(source=input_frame_op, save=False, verbose=False)
    detections_op = analyze_output(results_op, frame_op, camera_id="operator", camera_params=camera_params_operator)

    # Чтение кадра с камеры БПЛА - заглушено п причине выше
    #ret_uav, frame_uav = cap_uav.read()
    #if not ret_uav:
    #    break
    #input_frame_uav = preprocess_frame(frame_uav)
    #results_uav = model(source=input_frame_uav, save=False, verbose=False)
    #detections_uav = analyze_output(results_uav, frame_uav, camera_id="uav", camera_params=camera_params_uav)

    # Отображение кадров
    #cv2.imshow('Operator Camera', frame_op)
    #cv2.imshow('UAV Camera', frame_uav)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
#cap_operator.release()
#cap_uav.release()
cv2.destroyAllWindows()
#sock.close()
