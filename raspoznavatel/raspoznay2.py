import pytesseract
from PIL import Image
import pyautogui
import time
import os
import keyboard  # Добавляем библиотеку для работы с клавишами

# Указываем путь к tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Функция для захвата экрана с заданной областью
def capture_screen(region):
    # Захватываем указанный регион экрана
    screenshot = pyautogui.screenshot(region=region)
    return screenshot

# Функция для распознавания текста с изображения
def recognize_text(image):
    # Используем pytesseract для извлечения текста
    text = pytesseract.image_to_string(image, lang='rus+eng')
    return text

# Функция для записи текста в файл (с добавлением, а не перезаписью)
def write_to_notepad(text):
    output_path = "C:\\Users\\swer\\Documents\\output.txt"  # Путь к файлу
    # Открываем файл в режиме добавления
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(text + "\n")  # Добавляем текст и переводим строку

# Функция для проверки нажатия клавиши 'q' для старта/выхода
def check_for_exit():
    return keyboard.is_pressed('q')  # Если нажата клавиша 'q', то программа остановится

# Основной цикл захвата экрана и распознавания текста
running = False  # Начинаем с остановленного состояния

while True:
    if check_for_exit():  # Если нажата клавиша 'q'
        if running:
            print("Программа остановлена.")
            running = False  # Останавливаем программу
        else:
            print("Программа запущена.")
            running = True  # Запускаем программу
        time.sleep(1)  # Задержка, чтобы не загружать процессор

    if running:
        # Устанавливаем область для захвата левой половины экрана
        screen_width, screen_height = pyautogui.size()  # Получаем размер экрана
        left_half_region = (0, 0, screen_width // 2, screen_height)  # Левая половина экрана

        # Захватываем экран
        screenshot = capture_screen(left_half_region)

        # Распознаем текст на изображении
        text = recognize_text(screenshot)

        # Выводим распознанный текст на экран
        print("Распознанный текст:")
        print(text)

        # Записываем распознанный текст в файл (добавление текста)
        write_to_notepad(text)

        # Задержка между захватами (например, каждые 5 секунд)
        time.sleep(5)
