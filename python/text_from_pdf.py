import os
import fitz  # PyMuPDF для извлечения текста из PDF
import re  # Для очистки текста
import numpy as np
import pickle  # Для сохранения токенизатора
from tensorflow.keras.preprocessing.text import Tokenizer
from joblib import Parallel, delayed
from tensorflow.keras.preprocessing.sequence import pad_sequences
from langdetect import detect  # Для определения языка текста

# Шаг 1: Функция для извлечения текста из PDF
def extract_text_from_pdf(pdf_file):
    """Извлекает текст из PDF."""
    doc = fitz.open(pdf_file)  # Открываем PDF-файл
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")  # Извлекаем текст с каждой страницы
    return text

# Шаг 2: Функция для очистки текста в зависимости от языка
def clean_text(text, language="en"):
    """Очищаем текст от лишних символов в зависимости от языка."""
    # Убираем лишние переводы строк и пробелы
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Для английского языка удаляем все символы, которые не ASCII
    if language == "en":
        text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Для русского языка удаляем все символы, кроме русских букв, пробела и знаков препинания
    elif language == "ru":
        text = re.sub(r'[^А-Яа-яЁё\s.,!?]+', '', text)
    
    return text.strip()

# Шаг 3: Функция для токенизации текста
def tokenize_texts(dataset):
    """Токенизация текста."""
    tokenizer = Tokenizer(num_words=5000)  # Ограничиваем словарь 5000 наиболее частыми словами
    tokenizer.fit_on_texts(dataset)
    
    # Преобразуем тексты в последовательности токенов
    sequences = tokenizer.texts_to_sequences(dataset)
    
    # Приводим все последовательности к одной длине (например, 1000 токенов) с использованием pad_sequences
    data = pad_sequences(sequences, maxlen=1000)  # Вы можете изменить maxlen на нужную длину
    
    return data, tokenizer

# Шаг 4: Функции для сохранения данных и токенизатора
def save_tokenizer(tokenizer, filename="tokenizer.pkl"):
    """Сохраняем токенизатор в файл."""
    with open(filename, 'wb') as f:
        pickle.dump(tokenizer, f)

def save_tokenized_data(data, filename="tokenized_data.npy"):
    """Сохраняем токенизированные данные в файл .npy."""
    np.save(filename, data)

def save_text_files(dataset, output_folder):
    """Сохраняем текстовые данные в папке."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for idx, text in enumerate(dataset):
        with open(os.path.join(output_folder, f"book_{idx+1}.txt"), 'w', encoding='utf-8') as file:
            file.write(text)

# Шаг 5: Параллельная обработка извлечения текста
def process_pdfs(pdf_folder, num_jobs=4):
    """Параллельно обрабатывает несколько PDF файлов в папке."""
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    # Создаем список путей к файлам
    pdf_paths = [os.path.join(pdf_folder, pdf_file) for pdf_file in pdf_files]
    
    # Параллельное извлечение текста из всех файлов
    texts = Parallel(n_jobs=num_jobs)(delayed(extract_text_from_pdf)(pdf_path) for pdf_path in pdf_paths)
    
    return texts

# Шаг 6: Функция для определения языка текста
def detect_language(text):
    """Определяет язык текста."""
    try:
        lang = detect(text)
        return lang
    except:
        return "en"  # По умолчанию считаем английским

# Шаг 7: Интегрированное решение для обработки и сохранения данных
def process_and_save_pdfs(pdf_folder, output_folder, num_jobs=4):
    """Обрабатываем и сохраняем данные из всех PDF-файлов."""
    # Извлекаем текст из PDF
    print("Извлекаем текст...")
    texts = process_pdfs(pdf_folder, num_jobs)
    
    # Очищаем текст в зависимости от языка
    print("Очищаем текст...")
    cleaned_texts = []
    for text in texts:
        language = detect_language(text)  # Определяем язык
        cleaned_texts.append(clean_text(text, language))  # Очищаем текст в зависимости от языка
    
    # Токенизируем текст
    print("Токенизируем текст...")
    tokenized_data, tokenizer = tokenize_texts(cleaned_texts)
    
    # Сохраняем токенизированные данные
    print("Сохраняем токенизированные данные...")
    save_tokenized_data(tokenized_data, os.path.join(output_folder, "tokenized_data.npy"))
    
    # Сохраняем токенизатор
    print("Сохраняем токенизатор...")
    save_tokenizer(tokenizer, os.path.join(output_folder, "tokenizer.pkl"))
    
    # Сохраняем текстовые данные
    print("Сохраняем текстовые данные...")
    save_text_files(cleaned_texts, output_folder)

    print("Обработка завершена.")

# Пример вызова
pdf_folder = 'G:/swer/my_pdfs'
output_folder = 'G:/swer/output'

# Проверим, существует ли папка для сохранения данных, если нет — создадим её
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

process_and_save_pdfs(pdf_folder, output_folder)
