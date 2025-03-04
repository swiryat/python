import os
import re
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tkinter as tk
from tkinter import filedialog

def get_largest_font_text(image):
    """Извлекает текст с изображений и возвращает строку с самым большим шрифтом."""
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang='rus')

    max_font_size = 0
    largest_text_parts = []

    for i in range(len(data['text'])):
        text = data['text'][i]
        font_size = int(data['height'][i])

        if text.strip() != "":
            if font_size > max_font_size:
                max_font_size = font_size
                largest_text_parts = [text]
            elif font_size == max_font_size:
                largest_text_parts.append(text)

    return " ".join(largest_text_parts)

def sanitize_filename(filename):
    """Заменяет некорректные символы в имени файла на допустимые."""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def rename_file(file_path):
    """Переименовывает файл на основе самого крупного шрифта из изображений PDF."""
    try:
        images = convert_from_path(file_path)
        largest_text = ""
        for image in images:
            title = get_largest_font_text(image)
            if len(title) > len(largest_text):
                largest_text = title

        if not largest_text:
            largest_text = "NoText"

        keywords = largest_text.split()[0]
        new_name = sanitize_filename(keywords[:32]) + '.pdf'

        new_path = os.path.join(os.path.dirname(file_path), new_name)
        
        # Попробуем переименовать файл
        os.rename(file_path, new_path)
        print(f"Файл переименован в {new_name}")
        return new_name
    except PermissionError as e:
        print(f"Ошибка доступа: {e}")
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def get_file_path():
    """Открывает диалоговое окно для выбора файла."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path

file_path = get_file_path()
if file_path:
    renamed_file = rename_file(file_path)
    print(f"Файл успешно переименован: {renamed_file}")
else:
    print("Файл не выбран.")
