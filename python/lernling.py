import tkinter as tk
from tkinter import messagebox
import random
import docx
from gtts import gTTS
import os
import pygame

# Загрузка словаря из .docx файла
def load_dictionary(file_path):
    doc = docx.Document(file_path)
    dictionary = []
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            dictionary.append(text)
    return dictionary

# Функция для воспроизведения аудио
def play_audio():
    pygame.mixer.init()
    pygame.mixer.music.load("current_phrase.mp3")
    pygame.mixer.music.play()

# Функция для проверки ответа
def check_answer():
    user_answer = var.get()
    if user_answer.lower() == current_translation.lower():
        messagebox.showinfo("Результат", "Правильно!")
        load_next_phrase()
    else:
        messagebox.showerror("Результат", "Неправильно. Попробуйте ещё раз.")

# Загрузка следующей фразы из словаря
def load_next_phrase():
    global current_phrase, current_translation
    if not dictionary:
        messagebox.showinfo("Завершено", "Вы изучили все фразы!")
        return
    index = random.randint(0, len(dictionary) - 1)
    current_phrase, current_translation = dictionary.pop(index).split('-')
    phrase_label.config(text=current_phrase)
    var.set("")
    tts = gTTS(current_phrase, lang='en')
    tts.save("current_phrase.mp3")
    play_audio()  # Воспроизводим аудио

# Создание главного окна
root = tk.Tk()
root.title("Изучение английского")

# Загрузка словаря
dictionary = load_dictionary("eng.docx")

# Инициализация текущей фразы и перевода
current_phrase = ""
current_translation = ""

# Надпись для фразы
phrase_label = tk.Label(root, text=current_phrase, font=("Helvetica", 18))
phrase_label.pack(pady=20)

# Варианты ответов
var = tk.StringVar()
entry = tk.Entry(root, textvariable=var, font=("Helvetica", 16))
entry.pack(pady=10)
entry.bind("<Return>", lambda _: check_answer())

# Кнопка для проверки ответа
check_button = tk.Button(root, text="Проверить", command=check_answer, font=("Helvetica", 14))
check_button.pack()

# Загрузка первой фразы
load_next_phrase()

root.mainloop()
