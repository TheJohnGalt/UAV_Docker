import http.server
import socketserver
from PIL import Image
import io
import numpy as np
import cv2
import os
import pickle

class ImageHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        
        status, bgr_image = cam.read()  # Захватываем кадр по запросу

        if status:
            # Сериализация изображения с помощью pickle
            serialized_image = pickle.dumps(bgr_image)
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')  # Указываем тип контента как бинарные данные
            self.send_header('Content-Length', str(len(serialized_image)))  # Указываем длину содержимого
            self.end_headers()
            
            self.wfile.write(serialized_image)
        else:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Error: Unable to capture image.')

if __name__ == '__main__':
    PORT = 9000

    width = 3280
    height = 2464

    cam = cv2.VideoCapture(f'nvarguscamerasrc sensor-id=0 tnr-mode=2 tnr-strength=1 ! video/x-raw(memory:NVMM), width=(int){width}, height=(int){height}, framerate=21/1, format=(string)NV12 ! nvvidconv ! video/x-raw, format=(string)BGRx ! appsink')

    with socketserver.TCPServer(("", PORT), ImageHandler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()
