import tkinter as tk
import random
import pyttsx3
from docx import Document
from googletrans import Translator

# Загрузка словаря из .docx файла
def load_dictionary(file_path):
    doc = Document(file_path)
    dictionary = []
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            dictionary.append(text)
    return dictionary

# Инициализация текстового движка для произношения фраз
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Выбор голоса по вашему выбору, например, первый голос в списке
engine.setProperty('voice', voices[0].id)

# Инициализация окна приложения
root = tk.Tk()
root.title("Учим английский")

# Создание элемента интерфейса question_label
question_label = tk.Label(root, text="", font=("Arial", 18))
question_label.pack(pady=20)

# Загрузка словаря
dictionary = load_dictionary("eng.docx")

# Фразы, которые уже были отмечены как правильные
correct_phrases = []

# Текущая фраза и её перевод
current_phrase = ""
current_translation = ""

# Функция загрузки следующей фразы
def load_next_phrase():
    global current_phrase, current_translation
    if dictionary:
        random_index = random.randint(0, len(dictionary) - 1)
        phrase_pair = dictionary.pop(random_index)
        phrase_parts = phrase_pair.split('-')
        if len(phrase_parts) == 2:
            current_phrase, current_translation = phrase_parts
            question_label.config(text=current_phrase, font=("Arial", 18))

            # После отображения фразы, вызываем функцию произношения перевода
            root.after(2000, speak_russian_translation)
        else:
            # Если запись в словаре некорректная, просто загружаем следующую фразу
            load_next_phrase()
    else:
        question_label.config(text="Поздравляем, словарь закончился!", font=("Helvetica", 18))
        button_correct.config(state="disabled")
        button_wrong.config(state="disabled")

# Функция проверки ответа
def check_answer(answer):
    if answer == current_translation:
        feedback_label.config(text="Правильно!", font=("Helvetica", 14), fg="green")
        correct_phrases.append(current_phrase)
    else:
        feedback_label.config(text="Неправильно. Попробуйте ещё раз.", font=("Helvetica", 14), fg="red")
    
    # После задержки в 2 секунды загружаем следующую фразу
    root.after(2000, load_next_phrase)

# Функция произношения перевода на русском
def speak_russian_translation():
    translator = Translator()
    translation = translator.translate(current_translation, src='en', dest='ru')
    engine.say(translation.text)
    engine.runAndWait()

# Создание кнопок
button_correct = tk.Button(root, text="Правильно", command=lambda: check_answer(current_translation), font=("Helvetica", 14))
button_correct.pack(pady=10)

button_wrong = tk.Button(root, text="Неправильно", command=lambda: check_answer(""), font=("Helvetica", 14))
button_wrong.pack(pady=10)

speak_button = tk.Button(root, text="Произнести фразу", command=speak_russian_translation, font=("Helvetica", 14))
speak_button.pack(pady=10)

feedback_label = tk.Label(root, text="", font=("Helvetica", 14))
feedback_label.pack(pady=10)

# Загрузка первой фразы
load_next_phrase()

# Запуск приложения
root.mainloop()
