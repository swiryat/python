import pytesseract
import cv2
import numpy as np
import os

# Указываем путь к Tesseract (если нужно, измените путь в зависимости от вашей установки)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Путь к Tesseract

# Функция для регулировки контраста и яркости
def adjust_brightness_contrast(image, alpha=1.2, beta=50):
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image

# Функция для адаптивной бинаризации с использованием Гауссова размытия
def adaptive_thresholding(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Преобразуем в оттенки серого
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Применяем Гауссово размытие для уменьшения шума
    bw_image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)  # Адаптивная бинаризация
    return bw_image

# Функция для извлечения текста из изображения
def extract_text_from_image(image):
    adjusted_image = adjust_brightness_contrast(image)  # Настроить яркость и контраст
    bw_image = adaptive_thresholding(adjusted_image)  # Адаптивная бинаризация
    text = pytesseract.image_to_string(bw_image)  # Извлекаем текст с помощью Tesseract
    return text

# Функция для обработки списка изображений
def process_images_from_folder(folder_path):
    results = {}

    # Получаем список всех файлов в папке
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)  # Загружаем изображение

            # Извлечение текста
            text = extract_text_from_image(image)
            results[filename] = text  # Сохраняем результат с именем файла

    return results

# Папка с изображениями
folder_path = r'C:\Users\swer\Pictures\screen'  # Замените на путь к вашей папке с изображениями

# Обработка всех изображений в папке
results = process_images_from_folder(folder_path)

# Печать результатов
for filename, text in results.items():
    print(f'Результат для {filename}:')
    print(text)
    print('-------------------')
