import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import pyautogui
import time
import os
import keyboard  # Добавляем библиотеку для работы с клавишами
import cv2
import numpy as np
from spellchecker import SpellChecker

# Указываем путь к tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Инициализация объектов для проверки орфографии
spell_ru = SpellChecker(language='ru')  # Используем русский язык для проверки орфографии
spell_en = SpellChecker(language='en')  # Используем английский язык для проверки орфографии

# Функция для захвата экрана с заданной областью
def capture_screen(region):
    # Захватываем указанный регион экрана
    screenshot = pyautogui.screenshot(region=region)
    return screenshot

# Функция для преобразования изображения в чёрно-белое (градации серого) с повышением контраста и удалением шума
def preprocess_image(image):
    # Преобразуем изображение из формата PIL в формат OpenCV (numpy array)
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()  # Преобразуем RGB в BGR

    # Преобразование в черно-белое изображение (градации серого)
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # Применяем повышение контраста
    contrast = ImageEnhance.Contrast(Image.fromarray(gray_image))
    gray_image = np.array(contrast.enhance(2.0))  # Увеличиваем контраст

    # Применяем фильтр Шарпа для улучшения четкости
    sharpened_image = cv2.filter2D(gray_image, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))

    # Применяем фильтрацию шума (GaussianBlur) для удаления шумов
    denoised_image = cv2.GaussianBlur(sharpened_image, (5, 5), 0)

    return denoised_image

# Функция для распознавания текста с изображения
def recognize_text(image):
    # Преобразуем изображение с помощью предварительной обработки
    preprocessed_image = preprocess_image(image)

    # Используем pytesseract для извлечения текста
    text = pytesseract.image_to_string(preprocessed_image, lang='rus+eng')
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

# Функция для исправления орфографии
def correct_spelling(text):
    words = text.split()  # Разбиваем текст на слова
    corrected_text = []

    for word in words:
        # Если слово содержит русский символ, используем русский словарь
        if any(char in 'а-яА-ЯёЁ' for char in word):
            corrected_word = spell_ru.correction(word)  # Русский словарь
        else:
            corrected_word = spell_en.correction(word)  # Английский словарь
        
        if corrected_word:  # Проверяем, что исправленное слово не является None
            corrected_text.append(corrected_word)
        else:
            corrected_text.append(word)  # Если исправление не найдено, добавляем оригинальное слово
    
    return " ".join(corrected_text)  # Соединяем слова в одну строку и возвращаем результат

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

        # Исправляем орфографию в распознанном тексте
        corrected_text = correct_spelling(text)

        # Выводим распознанный и исправленный текст на экран
        print("Распознанный и исправленный текст:")
        print(corrected_text)

        # Записываем распознанный и исправленный текст в файл (добавление текста)
        write_to_notepad(corrected_text)

        # Задержка между захватами (например, каждые 5 секунд)
        time.sleep(1)
