import time
import keyboard
import pyautogui
import pytesseract
import numpy as np
import cv2
from PIL import Image, ImageGrab, ImageEnhance
import pyperclip
import os


# Укажите путь к Tesseract, если он не в PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Функция предварительной обработки изображения
def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)  # Перевод в серый цвет

    enhancer = ImageEnhance.Contrast(Image.fromarray(gray))  # Увеличение контраста
    enhanced = np.array(enhancer.enhance(2.0))

    _, binary = cv2.threshold(enhanced, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Бинаризация
    return binary


# Функция распознавания текста
def recognize_text(image):
    preprocessed_image = preprocess_image(image)
    text = pytesseract.image_to_string(preprocessed_image, lang='rus+eng')  # Распознавание
    return text.strip()

# Функция копирования текста в буфер обмена
def copy_to_clipboard(text):
    pyperclip.copy(text)  # Используем pyperclip для копирования текста
    print("✅ Текст скопирован в буфер обмена!")
    
# Функция для захвата изображения из буфера обмена
def capture_from_clipboard():
    print("⏳ Ожидание вставки скриншота в буфер обмена...")
    for _ in range(10):  # Ожидание до 5 секунд (10 * 0.5 сек)
        image = ImageGrab.grabclipboard()
        if image:
            return image
        time.sleep(0.5)
    
    print("❌ Ошибка: изображение не найдено в буфере обмена!")
    return None

# Функция сохранения текста в файл
def save_to_file(text, filename="output.txt"):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(text + "\n" + "-" * 50 + "\n")  # Добавляем разделитель между текстами
    print(f"💾 Текст сохранен в '{filename}'\n")


# Основная функция
def main():
    print("📸 Нажмите Win + Shift + S для захвата экрана...")
    
    # Запрос на ввод имени файла для сохранения (по умолчанию 'output.txt')
    custom_filename = input("Введите имя файла для сохранения (Enter для output.txt): ").strip()
    filename = custom_filename if custom_filename else "output.txt"
    
    while True:
        keyboard.wait("win+shift+s")  # Ждем нажатия комбинации
        time.sleep(2)  # Даём время для вставки в буфер обмена
        
        image = capture_from_clipboard()
        if image:
            text = recognize_text(image)
            print("\n📜 Распознанный текст:\n", text)

            # Копируем текст в буфер обмена
            pyperclip.copy(text)
            print("✅ Текст скопирован в буфер обмена!\n")

            # Сохранение в файл
            save_to_file(text, filename)

        print("📸 Ожидаем новый скриншот...")


# Запуск программы
if __name__ == "__main__":
    main()


