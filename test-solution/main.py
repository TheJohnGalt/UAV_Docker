import urllib.request
import numpy as np
import cv2
from solution import *
import pickle

def fetch_image():
    url = "http://server:9000/image"
    try:
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
            # Десериализация изображения с помощью pickle
            img = pickle.loads(image_data)
            return img
    except Exception as e:
        print(f"Возникла ошибка: {e}")
        return None

if __name__ == "__main__":

    image = fetch_image()

    #image = image[:, :, :3] # так как ИИ работает с трёхканальными изображениями, убераем альфа канал

    #cv2.imwrite("container_output/new.jpg", image) # запись изображения для дебага

    while True:
        image = fetch_image()

        image = image[:, :, :3] # так как ИИ работает с трёхканальными изображениями, убераем альфа канал

        if image is not None:
            print("Изображение получено с камеры")
            #cv2.imwrite("container_output/new.jpg", image) # запись изображения для дебага
            results = predict(image)
            print(results)
        else:
            print("Камера не отвечает, обработка тестового набора изображений")
            run_test_solution()