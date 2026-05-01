import time
import os
import math

# Шаг 1: Настройка параметров анимации
symbol = "\033[91m♥\033[0m"   # Красный ANSI-цвет
frame_delay = 0.03            # Задержка между кадрами (сек)
frames = 1000                   # Сколько кадров показать

# Шаг 2: Генерация кадров пульсации
for frame in range(frames):
    os.system('cls' if os.name == 'nt' else 'clear')  # Очистка экрана

    scale = 1.2 + 0.3 * math.sin(frame * 0.5)  # Пульсация: масштаб от 0.9 до 1.1

    for y in range(15, -15, -1):
        line = ""
        for x in range(-30, 30):
            x_scaled = x * 0.05 * scale
            y_scaled = y * 0.1 * scale
            eq = (x_scaled**2 + y_scaled**2 - 1)**3 - x_scaled**2 * y_scaled**3
            line += symbol if eq <= 0 else " "
        print(line)

    time.sleep(frame_delay)
