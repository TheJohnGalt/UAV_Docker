import socket
import cv2
import numpy as np
import pickle

HOST = '192.168.0.24'  # Замените на IP-адрес сервера
PORT = 9000

def process_image(frame):
    """Пример обработки изображения: применение размытия."""
    processed_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    return processed_frame

def start_client():
    """Запускает клиент."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print(f"Подключено к серверу: {HOST}:{PORT}")

        while True:
            # 1. Получение изображения с сервера
            size_data = client_socket.recv(4)
            if not size_data:
                break  # Сервер отключился
            received_size = int.from_bytes(size_data, 'big')
            received_data = b''
            while len(received_data) < received_size:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                received_data += chunk
            if not received_data:
                break
            frame = pickle.loads(received_data)

            # 2. Обработка изображения
            processed_frame = process_image(frame)

            # 3. Отправка обработанного изображения на сервер
            data = pickle.dumps(processed_frame)
            size = len(data)
            client_socket.sendall(size.to_bytes(4, 'big'))  # Отправляем размер данных
            client_socket.sendall(data)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        print("Отключение от сервера.")
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    start_client()
