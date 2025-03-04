import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import re

# Функция для обработки введенного текста и цифр
def find_matching_sentences():
    input_text = text.get("1.0", "end-1c")
    input_numbers = numbers_entry.get()
    
    # Разделяем введенные цифры по запятым и точкам
    numbers_list = re.split(r'[,.]', input_numbers)
    numbers_list = [num.strip() for num in numbers_list if num.strip()]
    
    numbers = set(numbers_list)

    # Разбиваем текст на строки
    lines = input_text.split('\n')

    # Создаем список для совпавших предложений
    matching_sentences = []

    for line in lines:
        # Проверяем, начинается ли строка с цифры, которая совпадает
        parts = line.split('. ')
        if len(parts) > 1:
            if parts[0] in numbers:
                matching_sentences.append(line)

    # Выводим совпавшие предложения
    result_text.config(state="normal")
    result_text.delete("1.0", "end")
    if matching_sentences:
        for sentence in matching_sentences:
            result_text.insert("end", sentence + "\n")
    else:
        result_text.insert("end", "Нет совпавших предложений.")
    result_text.config(state="disabled")

# Функция для сохранения текста в файл
def save_to_file():
    content = result_text.get("1.0", "end-1c")
    title = title_entry.get()

    if not title:
        title = "output.txt"

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if file_path:
        with open(file_path, "a") as file:  # Открываем файл в режиме добавления
            file.write(f"{title}\n\n")
            file.write(content)

# Создаем главное окно
root = tk.Tk()
root.title("Сортировка предложений")

# Создаем элементы интерфейса
text_label = tk.Label(root, text="Введите текст с предложениями:")
text_label.pack()

text = scrolledtext.ScrolledText(root, height=10, width=40)
text.pack()

numbers_label = tk.Label(root, text="Введите цифры через запятую или точку:")
numbers_label.pack()

numbers_entry = tk.Entry(root)
numbers_entry.pack()

find_button = tk.Button(root, text="Найти совпадения", command=find_matching_sentences)
find_button.pack()

result_text = scrolledtext.ScrolledText(root, height=10, width=40)
result_text.config(state="disabled")
result_text.pack()

title_label = tk.Label(root, text="Заголовок для сохранения:")
title_label.pack()

title_entry = tk.Entry(root)
title_entry.pack()

save_button = tk.Button(root, text="Сохранить", command=save_to_file)
save_button.pack()

# Запускаем главное окно
root.mainloop()
