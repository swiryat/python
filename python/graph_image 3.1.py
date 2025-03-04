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
        ax.set_ylim(-10, 10)  # Установить ограничение по оси y от -15 до +15
        ax.legend()
        
        # Отобразить изображение на графике (если выбрано)
        if image_label.image:
            ax.imshow(image_label.image_data, extent=(x.min(), x.max(), -15, 15), aspect='auto', alpha=0.5)
        
        # Обновить холст
        canvas.draw()
    except Exception as e:
        error_label.config(text=f"Ошибка: {e}")

# Функция для выбора изображения
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp")])
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((400, 400))  # Уменьшить изображение до размера 400x400
        image_label.image_data = image
        image_label.image = ImageTk.PhotoImage(image)
        image_label.config(image=image_label.image)

# Создать главное окно приложения
root = tk.Tk()
root.title("График функции с изображением")

# Создать фрейм для графика
graph_frame = tk.Frame(root)
graph_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Создать фрейм для настроек и изображения
settings_frame = tk.Frame(root)
settings_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Создать ввод для функции
function_label = tk.Label(settings_frame, text="Функция:")
function_label.pack()
function_entry = tk.Entry(settings_frame, width=30)
function_entry.pack()

# Создать кнопку для построения графика
plot_button = tk.Button(settings_frame, text="Построить график", command=plot_graph)
plot_button.pack()

# Создать кнопку для выбора изображения
image_button = tk.Button(settings_frame, text="Выбрать изображение", command=open_image)
image_button.pack()

# Фрейм для отображения изображения
image_label = tk.Label(graph_frame)
image_label.pack()

# Создать холст для графика
fig, ax = plt.subplots(figsize=(6, 6))
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack()
canvas.draw()

# Метка для вывода ошибок
error_label = tk.Label(settings_frame, text="", fg="red")
error_label.pack()

# Запустить главный цикл приложения
root.mainloop()
