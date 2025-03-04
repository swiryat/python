import tkinter as tk
from tkinter import filedialog, ttk
import random
import pyttsx3
from docx import Document
from googletrans import Translator

engine = pyttsx3.init()



# Загрузка словаря из .docx файла
def load_dictionary(file_path):
    doc = Document(file_path)
    dictionary = []
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            dictionary.append(text)
    return dictionary

# Инициализация окна приложения
root = tk.Tk()
root.title("Учим английский")

# Инициализация текстового двигателя для английских фраз
english_engine = pyttsx3.init()
english_voices = english_engine.getProperty('voices')

# Инициализация текстового двигателя для русских фраз
russian_engine = pyttsx3.init()
russian_voices = russian_engine.getProperty('voices')

# Функция для выбора голосового движка и скорости для английской фразы
def select_english_voice():
    selected_voice_name = english_voice_combo.get()
    selected_voice_rate = english_rate_combo.get()
    for voice in english_voices:
        if voice.name == selected_voice_name:
            english_engine.setProperty('voice', voice.id)
            english_engine.setProperty('rate', selected_voice_rate)  # Установка скорости
            break

# Функция для выбора голосового движка и скорости для русской фразы
def select_russian_voice():
    selected_voice_name = russian_voice_combo.get()
    selected_voice_rate = russian_rate_combo.get()
    for voice in russian_voices:
        if voice.name == selected_voice_name:
            russian_engine.setProperty('voice', voice.id)
            russian_engine.setProperty('rate', selected_voice_rate)  # Установка скорости
            break

def update_english_rate(event):
    selected_voice_rate = english_rate_combo.get()
    select_english_voice()
    english_rate_combo.set(selected_voice_rate)  # Установите значение в Combobox

def update_russian_rate(event):
    selected_voice_rate = russian_rate_combo.get()
    select_russian_voice()
    russian_rate_combo.set(selected_voice_rate)  # Установите значение в Combobox


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
            speak_english_button.config(state="normal")
            speak_russian_button.config(state="normal")
        else:
            load_next_phrase()
    else:
        question_label.config(text="Поздравляем, словарь закончился!", font=("Helvetica", 18))
        next_button.config(state="disabled")
        wrong_button.config(state="disabled")
        speak_english_button.config(state="disabled")
        speak_russian_button.config(state="disabled")

# Функция для проверки ответа и продолжения
def next_phrase():
    load_next_phrase()
    feedback_label.config(text="", font=("Helvetica", 14))

# Функция для неправильного ответа
def wrong_answer():
    feedback_label.config(text="Неправильно. Правильный перевод: " + current_translation, font=("Helvetica", 14), fg="red")

# Функция произношения текущей фразы на английском
def speak_english_phrase():
    select_english_voice()  # Выбор голосового движка
    engine.setProperty('rate', int(english_rate_combo.get()))  # Установка скорости как целого числа
    engine.say(current_phrase)
    engine.runAndWait()

# Функция произношения текущей фразы на русском
def speak_russian_translation():
    select_russian_voice()  # Выбор голосового движка
    engine.setProperty('rate', int(russian_rate_combo.get()))  # Установка скорости как целого числа
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

# Создание выпадающих списков для выбора голосовых движков
english_voice_label = tk.Label(root, text="Выберите голосовой движок для английского:", font=("Helvetica", 14))
english_voice_label.pack(pady=5)

english_voice_combo = ttk.Combobox(root, values=[voice.name for voice in english_voices], font=("Helvetica", 14))
english_voice_combo.pack(pady=5)
english_voice_combo.set(english_voices[0].name)  # Установите первый голос по умолчанию

russian_voice_label = tk.Label(root, text="Выберите голосовой движок для русского:", font=("Helvetica", 14))
russian_voice_label.pack(pady=5)

russian_voice_combo = ttk.Combobox(root, values=[voice.name for voice in russian_voices], font=("Helvetica", 14))
russian_voice_combo.pack(pady=5)
russian_voice_combo.set(russian_voices[0].name)  # Установите первый голос по умолчанию

# Создание выпадающих списков для выбора скорости
english_rate_label = tk.Label(root, text="Выберите скорость для английского:", font=("Helvetica", 14))
english_rate_label.pack(pady=5)

# Измените список значений для английской скорости
english_rate_combo = ttk.Combobox(root, values=["50", "70", "90", "110", "130", "150", "170", "190"], font=("Helvetica", 14))
english_rate_combo.pack(pady=5)
english_rate_combo.set("150")  # Установите скорость по умолчанию

russian_rate_label = tk.Label(root, text="Выберите скорость для русского:", font=("Helvetica", 14))
russian_rate_label.pack(pady=5)

# Измените список значений для русской скорости
russian_rate_combo = ttk.Combobox(root, values=["50", "70", "90", "110", "130", "150", "170", "190"], font=("Helvetica", 14))
russian_rate_combo.pack(pady=5)
russian_rate_combo.set("150")  # Установите скорость по умолчанию


# Привязка обновления скорости к событию изменения значения выпадающего списка
english_rate_combo.bind("<<ComboboxSelected>>", update_english_rate)
russian_rate_combo.bind("<<ComboboxSelected>>", update_russian_rate)

# Создание кнопок
next_button = tk.Button(root, text="Следующее слово", command=next_phrase, font=("Helvetica", 14))
next_button.pack(pady=10)

wrong_button = tk.Button(root, text="Неправильно", command=wrong_answer, font=("Helvetica", 14))
wrong_button.pack(pady=10)

speak_russian_button = tk.Button(root, text="Произнести перевод", command=speak_russian_translation, font=("Helvetica", 14))
speak_russian_button.pack(pady=10)
speak_russian_button.config(state="disabled")

speak_english_button = tk.Button(root, text="Произнести фразу на английском", command=speak_english_phrase, font=("Helvetica", 14))
speak_english_button.pack(pady=10)
speak_english_button.config(state="disabled")

feedback_label = tk.Label(root, text="", font=("Helvetica", 14))
feedback_label.pack(pady=10)

# Запуск приложения
root.mainloop()
