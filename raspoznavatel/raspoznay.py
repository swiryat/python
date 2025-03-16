import pytesseract
from PIL import Image, ImageDraw
import pyautogui
import time

# Указываем путь к tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Функция для захвата всего экрана
def capture_screen():
    # Захват всего экрана
    screenshot = pyautogui.screenshot()
    return screenshot

# Функция для добавления рамки на изображение
def add_border_to_image(image):
    # Создаем объект ImageDraw, чтобы рисовать на изображении
    draw = ImageDraw.Draw(image)
    
    # Получаем размер изображения
    width, height = image.size
    
    # Рисуем прямоугольник (рамку) вокруг всего экрана
    draw.rectangle([0, 0, width, height], outline="red", width=5)
    
    return image

# Функция для распознавания текста с изображения
def recognize_text(image):
    text = pytesseract.image_to_string(image, lang='rus+eng')
    return text

# Функция для записи текста в блокнот
def write_to_notepad(text):
    import os
    os.system(f'echo "{text}" > "C:\\Users\\swer\\Documents\\output.txt"')

# Основной цикл
while True:
    # Захватываем весь экран
    screenshot = capture_screen()
    
    # Добавляем рамку на захваченное изображение
    screenshot_with_border = add_border_to_image(screenshot.copy())
    
    # Показываем изображение с рамкой
    screenshot_with_border.show()  # Это откроет окно с изображением
    
    # Преобразуем снимок в текст
    text = recognize_text(screenshot)
    
    # Выводим текст в терминал
    print("Распознанный текст:")
    print(text)
    
    # Записываем текст в файл
    write_to_notepad(text)
    
    # Задержка между захватами
    time.sleep(5)  # Захватываем каждые 5 секунд
