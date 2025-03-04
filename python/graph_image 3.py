import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from tkinter import ttk

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

image = None

def evaluate_function(function_text, x_values):
    y_values = []
    for x in x_values:
        try:
            # Заменяем 'ln' на 'np.log', чтобы использовать натуральный логарифм
            function_text = function_text.replace("ln", "np.log")
            y = eval(function_text)
            y_values.append(y)
        except Exception:
            y_values.append(None)
    return y_values

def plot_graph():
    ax.clear()
    function_text = function_entry.get()
    x_min = float(x_min_entry.get())
    x_max = float(x_max_entry.get())
    y_min = float(y_min_entry.get())
    y_max = float(y_max_entry.get())

    # Создайте область для графика
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    x = np.linspace(x_min, x_max, 400)
    y = evaluate_function(function_text, x)
    ax.plot(x, y)

    # Отобразите изображение на области графика
    if image:
        ax.imshow(image, extent=[x_min, x_max, y_min, y_max], aspect='auto')

    canvas.draw()

def open_image():
    global image
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        update_image_scale()

def zoom_in():
    update_image_scale(1.25)
    plot_graph()

def zoom_out():
    update_image_scale(0.8)
    plot_graph()

def update_image_scale(scale_factor=1.0):
    global image
    if image:
        width, height = image.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        image_label.config(image=photo)
        image_label.image = photo

def save_graph():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        fig.savefig(file_path, dpi=100, bbox_inches="tight")

def on_mousewheel(event):
    if event.delta > 0:
        zoom_in()
    else:
        zoom_out()

# Создаем изображение для отображения графика и изображения
def create_combined_image():
    fig, ax = plt.subplots(figsize=(6, 6))
    x = np.linspace(0, 10, 400)
    y = np.sin(x)
    ax.plot(x, y)

    if image:
        ax.imshow(image, extent=[0, 10, 0, 10], aspect='auto')

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()
    return canvas_widget

root = tk.Tk()
root.title("График функции с изображением")

graph_frame = tk.Frame(root)
graph_frame.pack(side=tk.LEFT, padx=10, pady=10)

settings_frame = tk.Frame(root)
settings_frame.pack(side=tk.LEFT, padx=10, pady=10)

function_label = tk.Label(settings_frame, text="Функция:")
function_label.pack()
function_entry = ttk.Entry(settings_frame, width=30)
function_entry.pack()

tooltip_text = (
    "Для ввода спецсимволов, таких как логарифм (например, 'log') и 'x в квадрате' (например, 'x**2'), "
    "используйте соответствующий синтаксис для математических операций и функций."
    "\n\nПримеры:"
    "\n- Для логарифма с основанием 10: log(x)"
    "\n- Для натурального логарифма: log(x, e) или просто ln(x)"
    "\n- Для 'x в квадрате': x**2"
    "\n\nПросто введите соответствующий математический синтаксис в поле ввода функции, "
    "и ваш код будет оценивать эту функцию при построении графика."
)
tooltip = ToolTip(function_entry, tooltip_text)

# Создайте виджеты для ввода значений x_min, x_max, y_min, y_max
x_min_label = tk.Label(settings_frame, text="x мин:")
x_min_label.pack()
x_min_entry = ttk.Entry(settings_frame, width=10)
x_min_entry.pack()

x_max_label = tk.Label(settings_frame, text="x макс:")
x_max_label.pack()
x_max_entry = ttk.Entry(settings_frame, width=10)
x_max_entry.pack()

y_min_label = tk.Label(settings_frame, text="y мин:")
y_min_label.pack()
y_min_entry = ttk.Entry(settings_frame, width=10)
y_min_entry.pack()

y_max_label = tk.Label(settings_frame, text="y макс:")
y_max_label.pack()
y_max_entry = ttk.Entry(settings_frame, width=10)
y_max_entry.pack()

# Установите значения по умолчанию
x_min_entry.insert
