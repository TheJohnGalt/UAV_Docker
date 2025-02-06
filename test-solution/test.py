import cv2
import numpy as np
import glob

# Параметры видео
frame_size = (640, 640)  # Ширина и высота каждого кадра
fps = 29.97  # Кадры в секунду
output_path = 'container_output/output_video.avi'  # Путь для сохранения видео

# Определение кодека
#fourcc = cv2.VideoWriter_fourcc(*'MP4V')  #  Кодек  для .mp4
fourcc = cv2.VideoWriter_fourcc(*'DIVX') # Альтернативный кодек

# Создание объекта VideoWriter
out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
counter = 100

cap = cv2.VideoCapture('bench.mp4')

# Цикл обработки и записи кадров
while counter > 0:
 # Укажите путь к вашим изображениям
    ret, frame = cap.read()
    img = frame
    # Изменение размера изображения под frame_size
    img = cv2.resize(img, frame_size)

    # Тут можно вставить обработку изображения
    # Пример: преобразование в оттенки серого
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Преобразование обратно в BGR для сохранения в цвете
    color_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)

    out.write(color_img)  # Запись обработанного кадра в видео
    counter += -1

# Завершение записи
out.release()
cv2.destroyAllWindows()