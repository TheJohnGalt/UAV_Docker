import urllib.request
import numpy as np
import cv2
from solution import *

def fetch_image():
    url = "http://host.docker.internal:9000/image"
    try:
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img
    except Exception as e:
        print(f"Возникла ошибка: {e}")
        return None

if __name__ == "__main__":

    while True:
        image = fetch_image()
        if image is not None:
            results = predict(image)
            print(results)
        else:
            print("Камера не отвечает, обработка тестового набора изображений")
            run_test_solution()