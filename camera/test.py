import time
from PIL import ImageGrab

def capture_screenshot(filename):
    # Захват экрана
    screenshot = ImageGrab.grab()
    # Сохранение изображения в формате JPG
    screenshot.save(filename, "JPEG")

if __name__ == "__main__":
    # Генерация имени файла с текущей меткой времени
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.jpg"
    
    # Вызов функции для захвата и сохранения скриншота
    capture_screenshot(filename)