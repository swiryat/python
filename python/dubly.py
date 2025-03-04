import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import re
from collections import Counter

# Функция для поиска повторяющихся предложений
def find_duplicate_sentences():
    input_text = text.get("1.0", "end-1c")

    # Разбиваем текст на предложения
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', input_text)

    # Используем Counter для подсчета количества вхождений каждого предложения
    sentence_counts = Counter(sentences)

    # Фильтруем предложения, которые встречаются больше одного раза
    duplicate_sentences = [sentence for sentence, count in sentence_counts.items() if count > 1]

    result_text.config(state="normal")
    result_text.delete("1.0", "end")

    if duplicate_sentences:
        for sentence in duplicate_sentences:
            result_text.insert("end", sentence + "\n")
    else:
        result_text.insert("end", "Нет повторяющихся предложений.")

    result_text.config(state="disabled")

# Функция для сохранения результатов в файл
def save_to_file():
    content = result_text.get("1.0", "end-1c")
    title = title_entry.get()

    if not title:
        title = "duplicates.txt"

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if file_path:
        with open(file_path, "a") as file:
            file.write(f"{title}\n\n")
            file.write(content)

# Создаем главное окно
root = tk.Tk()
root.title("Поиск повторяющихся предложений")

# Создаем элементы интерфейса
text_label = tk.Label(root, text="Введите текст для поиска повторяющихся предложений:")
text_label.pack()

text = scrolledtext.ScrolledText(root, height=10, width=40)
text.pack()

find_button = tk.Button(root, text="Найти повторения", command=find_duplicate_sentences)
find_button.pack()

result_text = scrolledtext.ScrolledText(root, height=10, width=40)
result_text.config(state="disabled")
result_text.pack()

title_label = tk.Label(root, text="Заголовок для сохранения:")
title_label.pack()

title_entry = tk.Entry(root)
title_entry.pack()

save_button = tk.Button(root, text="Сохранить результаты", command=save_to_file)
save_button.pack()

# Запускаем главное окно
root.mainloop()
