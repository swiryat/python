import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tkinter as tk
from tkinter import filedialog

def ocr_from_pdf(file_path):
    """Извлекает текст с изображений в PDF с использованием Tesseract OCR."""
    # Конвертируем страницы PDF в изображения
    images = convert_from_path(file_path)
    
    # Для каждой страницы выполняем OCR
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    
    return text

def rename_file(file_path):
    """Переименовывает файл на основе извлеченного текста из сканированного PDF."""
    # Извлекаем текст с помощью OCR
    text = ocr_from_pdf(file_path)
    
    # Если текст пустой, используем fallback имя
    if not text:
        text = "NoText"
    
    # Простейшая обработка текста: берем первое слово
    keywords = text.split()[0]
    
    # Формируем новое имя файла
    new_name = keywords[:10] + '.pdf'
    
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
