import tkinter as tk
from tkinter import scrolledtext

# Функция для обработки введенного текста и цифр
def find_matching_sentences():
    input_text = text.get("1.0", "end-1c")
    input_numbers = numbers_entry.get()
    input_numbers = input_numbers.replace(" ", "")  # Удаляем пробелы между цифрами
    numbers = set(input_numbers.split(','))

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

# Функция для копирования текста
def copy_text():
    result_text.clipboard_clear()
    result_text.clipboard_append(result_text.get("1.0", "end-1c"))

# Создаем главное окно
root = tk.Tk()
root.title("Сортировка предложений")

# Создаем элементы интерфейса
text_label = tk.Label(root, text="Введите текст с предложениями:")
text_label.pack()

text = scrolledtext.ScrolledText(root, height=10, width=40)
text.pack()

numbers_label = tk.Label(root, text="Введите цифры через запятую:")
numbers_label.pack()

numbers_entry = tk.Entry(root)
numbers_entry.pack()

find_button = tk.Button(root, text="Найти совпадения", command=find_matching_sentences)
find_button.pack()

result_text = scrolledtext.ScrolledText(root, height=10, width=40)
result_text.config(state="disabled")
result_text.pack()

copy_button = tk.Button(root, text="Копировать", command=copy_text)
copy_button.pack()

# Запускаем главное окно
root.mainloop()
