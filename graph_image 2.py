import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# Функция для построения графика
def plot_graph():
    # Получить текст из поля ввода
    function_text = function_entry.get()
    
    try:
        # Вычислить y на основе введенной функции
        x = np.linspace(-10, 10, 400)
        y = eval(function_text)
        
        # Очистить предыдущий график
        ax.clear()
        ax.plot(x, y, label=function_text)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"График функции {function_text}")
        ax.grid(True)
        ax.legend()
        
        # Обновить холст
        canvas.draw()
    except Exception as e:
        error_label.config(text=f"Ошибка: {e}")

# Функция для выбора изображения
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        # Открыть выбранное изображение и преобразовать его для Tkinter
        image = Image.open(file_path)
        image = ImageTk.PhotoImage(image)
        # Отобразить изображение на холсте
        img_label = tk.Label(root, image=image)
        img_label.image = image  # Сохранить ссылку на изображение, чтобы избежать сбора мусора
        img_label.pack()

# Создание окна
root = tk.Tk()
root.title("Совмещение графика и изображения")

# Создание холста для графика
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Окошко для ввода функции
function_label = tk.Label(root, text="Введите функцию (например, 9*x - 8):")
function_label.pack()
function_entry = tk.Entry(root, width=30)
function_entry.pack()

# Кнопка для построения графика
plot_button = tk.Button(root, text="Построить график", command=plot_graph)
plot_button.pack()

# Метка для отображения ошибок
error_label = tk.Label(root, text="", fg="red")
error_label.pack()

# Кнопка для выбора изображения
image_button = tk.Button(root, text="Выбрать изображение", command=open_image)
image_button.pack()

# Запуск главного цикла обработки событий
root.mainloop()
