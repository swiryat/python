import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import filedialog
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Функция для выбора изображения
def open_image():
    global img
    file_path = filedialog.askopenfilename()
    img = plt.imread(file_path)
    update_plot()

# Функция для обновления графика
def update_plot():
    # Очищаем текущий график
    ax.cla()

    # Задаем интервал значений x
    x = np.linspace(-10, 10, 400)

    # Вычисляем соответствующие значения y
    y = 9 * x - 8

    # Рисуем изображение
    ax.imshow(img, extent=[-10, 10, -80, 80])  # Выберите подходящие значения для extent

    # Рисуем график
    ax.plot(x, y, label='y = 9x - 8', color='b')

    # Добавляем заголовок и подписи к осям
    ax.set_title('График функции и изображение')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # Добавляем сетку
    ax.grid(True)

    # Отображаем легенду
    ax.legend()

    # Обновляем график
    canvas.draw()

# Создаем графическое окно
root = Tk()
root.title("График и изображение")

# Создаем холст Matplotlib
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Создаем меню выбора изображения
menu = Menu(root)
root.config(menu=menu)
file_menu = Menu(menu)
menu.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Открыть изображение", command=open_image)

# Запускаем интерфейс
root.mainloop()
