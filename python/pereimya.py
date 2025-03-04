import tkinter as tk
from tkinter import filedialog
import os
import PyPDF2

def extract_text_from_pdf(file_path):
    """Извлекает текст из PDF файла."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def rename_file(file_path):
    """Переименовывает файл на основе извлеченного текста."""
    text = extract_text_from_pdf(file_path)
    
    # Простейшая обработка текста: берем первое слово
    keywords = text.split()[0] if text else "NoText"
    
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
