import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# Создание окна
root = tk.Tk()
root.title("Совмещение графика и изображения")

# Создание данных для графика
x = np.linspace(-10, 10, 400)
y = 9 * x - 8

# Создание графика
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, label="y = 9x - 8")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("График функции y = 9x - 8")
ax.grid(True)
ax.legend()

# Создание холста для графика и размещение его в окне
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

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

# Кнопка для выбора изображения
image_button = tk.Button(root, text="Выбрать изображение", command=open_image)
image_button.pack()

# Запуск главного цикла обработки событий
root.mainloop()
