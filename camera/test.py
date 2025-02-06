import socket

def request_image():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.0.24', 65432))

    client_socket.sendall(b'GET_IMAGE')
    
    with open('received_image.jpg', 'wb') as image_file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            image_file.write(data)

    print("Изображение получено и сохранено как 'received_image.jpg'.")
    client_socket.close()

if __name__ == "__main__":
    request_image()
