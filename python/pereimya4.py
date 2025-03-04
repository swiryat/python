import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tkinter as tk
from tkinter import filedialog

def ocr_from_pdf(file_path):
    """Извлекает текст с изображений в PDF с использованием Tesseract OCR (с поддержкой русского языка)."""
    # Конвертируем страницы PDF в изображения
    images = convert_from_path(file_path)
    
    # Для каждой страницы выполняем OCR с использованием русского языка
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image, lang='rus')
    
    return text

def get_largest_font_text(image):
    """Извлекает текст с изображений и возвращает строку с самым большим шрифтом."""
    # Получаем данные OCR (с информацией о расположении слов и их размере)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang='rus')

    max_font_size = 0
    largest_text = ""
    
    # Ищем слово с максимальным размером шрифта
    for i in range(len(data['text'])):
        text = data['text'][i]
        font_size = int(data['height'][i])  # Высота строки предполагает размер шрифта
        
        if text.strip() != "" and font_size > max_font_size:
            max_font_size = font_size
            largest_text = text
    
    return largest_text

def get_largest_font_title(image):
    """Извлекает самый крупный шрифт на изображении и делает акцент на заголовке."""
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang='rus')

    max_font_size = 0
    largest_title = ""
    
    # Ищем заголовок с максимальным шрифтом
    for i in range(len(data['text'])):
        text = data['text'][i]
        font_size = int(data['height'][i])
        
        # Пропускаем пустые строки и учитываем только текст
        if text.strip() != "" and font_size > max_font_size:
            max_font_size = font_size
            largest_title = text
    
    return largest_title

def rename_file(file_path):
    """Переименовывает файл на основе самого крупного шрифта из изображений PDF."""
    # Конвертируем страницы PDF в изображения
    images = convert_from_path(file_path)
    
    # Ищем текст с максимальным размером шрифта (заголовок)
    largest_text = ""
    for image in images:
        title = get_largest_font_title(image)
        if len(title) > len(largest_text):  # Выбираем текст с максимальным шрифтом
            largest_text = title
    
    # Если текст пустой, используем fallback имя
    if not largest_text:
        largest_text = "NoText"
    
    # Простейшая обработка текста: берем первое слово
    keywords = largest_text.split()[0]
    
    # Формируем новое имя файла
    new_name = keywords[:32] + '.pdf'
    
    # Переименовываем файл
    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)
    
    print(f"Файл переименован в {new_name}")
    return new_name

def get_file_path():
    """Открывает диалоговое окно для выбора файла."""
    root = tk.Tk()
    root.withdraw()  # Скрыть главное окно Tkinter
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])  # Открытие окна выбора файла
    return file_path

# Получаем путь к выбранному файлу
file_path = get_file_path()

# Если путь указан, переименовываем файл
if file_path:
    renamed_file = rename_file(file_path)
    print(f"Файл успешно переименован: {renamed_file}")
else:
    print("Файл не выбран.")
