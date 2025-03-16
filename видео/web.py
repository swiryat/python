import cv2
import random
import time

def get_video_devices():
    """Получаем список доступных видеоустройств"""
    devices = []
    for i in range(10):  # Пробуем устройства с 0 по 9
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            devices.append(i)
            cap.release()
    return devices

def connect_random_camera():
    """Подключаемся к случайной камере"""
    devices = get_video_devices()
    
    if not devices:
        print("Нет доступных видеоустройств")
        return
    # Выбираем случайное устройство
    device_id = random.choice(devices)
    print(f"Подключаемся к камере с id: {device_id}")
    
    # Открываем видеопоток с выбранной камеры
    cap = cv2.VideoCapture(device_id)
    
    if not cap.isOpened():
        print("Не удалось подключиться к камере")
        return
    
    # Настройки отображения видео
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось захватить кадр")
            break
        
        # Отображаем видеопоток
        cv2.imshow("Video Stream", frame)

        # Закрываем окно по нажатию клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    connect_random_camera()
