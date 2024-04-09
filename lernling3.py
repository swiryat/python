import tkinter as tk
from tkinter import filedialog
import random
import pyttsx3
from docx import Document
from googletrans import Translator
from tkinter import ttk  # Импорт ttk для создания выпадающего списка

# Загрузка словаря из .docx файла
def load_dictionary(file_path):
    doc = Document(file_path)
    dictionary = []
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            dictionary.append(text)
    return dictionary

# Инициализация текстового двигателя для произношения фраз
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Настройка скорости произношения (значение по умолчанию - 200)
engine.setProperty('rate', 120)  # Установите скорость на ваш вкус, например, 150

# Настройка уровня громкости (значение по умолчанию - 1.0)
engine.setProperty('volume', 1.0)  # Установите уровень громкости, например, 0.9

# Инициализация окна приложения
root = tk.Tk()
root.title("Учим английский")

# Создание выпадающего списка для выбора голосового движка
voice_label = tk.Label(root, text="Выберите голосовой движок:", font=("Helvetica", 14))
voice_label.pack(pady=10)

voice_combo = ttk.Combobox(root, values=[voice.name for voice in voices], font=("Helvetica", 14))
voice_combo.pack(pady=10)

# Создание элемента интерфейса question_label
question_label = tk.Label(root, text="", font=("Arial", 18))
question_label.pack(pady=20)

# Загрузка словаря
dictionary = []

# Текущая фраза и её перевод
current_phrase = ""
current_translation = ""

# Функция загрузки следующей фразы
def load_next_phrase():
    global current_phrase, current_translation
    if dictionary:
        random_index = random.randint(0, len(dictionary) - 1)
        phrase_pair = dictionary.pop(random_index)
        # Разделение на фразу на английском и перевод
        phrase_parts = phrase_pair.split(' - ')
        if len(phrase_parts) == 2:
            current_phrase, current_translation = phrase_parts
            question_label.config(text=current_phrase, font=("Arial", 18))
        else:
            load_next_phrase()
    else:
        question_label.config(text="Поздравляем, словарь закончился!", font=("Helvetica", 18))
        next_button.config(state="disabled")
        wrong_button.config(state="disabled")

# Функция для проверки ответа и продолжения
def next_phrase():
    load_next_phrase()
    feedback_label.config(text="", font=("Helvetica", 14))

# Функция для неправильного ответа
def wrong_answer():
    feedback_label.config(text="Неправильно. Правильный перевод: " + current_translation, font=("Helvetica", 14), fg="red")

# Функция произношения текущей фразы на английском
def speak_english_phrase():
    engine.say(current_phrase)
    engine.runAndWait()

# Функция произношения текущей фразы на русском
def speak_russian_translation():
    translator = Translator()
    translation = translator.translate(current_translation, src='en', dest='ru')
    engine.say(translation.text)
    engine.runAndWait()

# Функция для выбора файла .docx и загрузки словаря
def load_dictionary_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
    if file_path:
        global dictionary
        dictionary = load_dictionary(file_path)
        load_next_phrase()

# Создание кнопки для загрузки словаря из файла
load_button = tk.Button(root, text="Загрузить словарь", command=load_dictionary_from_file, font=("Helvetica", 14))
load_button.pack(pady=10)

# Создание кнопок
next_button = tk.Button(root, text="Следующее слово", command=next_phrase, font=("Helvetica", 14))
next_button.pack(pady=10)

wrong_button = tk.Button(root, text="Неправильно", command=wrong_answer, font=("Helvetica", 14))
wrong_button.pack(pady=10)

speak_russian_button = tk.Button(root, text="Произнести перевод", command=speak_russian_translation, font=("Helvetica", 14))
speak_russian_button.pack(pady=10)

speak_english_button = tk.Button(root, text="Произнести фразу на английском", command=speak_english_phrase, font=("Helvetica", 14))
speak_english_button.pack(pady=10)

feedback_label = tk.Label(root, text="", font=("Helvetica", 14))
feedback_label.pack(pady=10)

# Функция для выбора голосового движка из выпадающего списка
def select_voice():
    selected_voice_name = voice_combo.get()
    for voice in voices:
        if voice.name == selected_voice_name:
            engine.setProperty('voice', voice.id)
            break

# Кнопка для выбора голосового движка
select_voice_button = tk.Button(root, text="Выбрать голосовой движок", command=select_voice, font=("Helvetica", 14))
select_voice_button.pack(pady=10)

# Запуск приложения
root.mainloop()
