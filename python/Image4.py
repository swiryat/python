import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageFont


def choose_font():
    global font_path
    font_path = filedialog.askopenfilename(
        initialdir="C:/MyFonts",  # Папка для выбора шрифтов
        title="Выберите шрифт",
        filetypes=(("Шрифты", "*.ttf *.otf"), ("Все файлы", "*.*")),
    )
    if font_path:
        font_label.config(text=f"Выбран шрифт: {font_path.split('/')[-1]}")
    else:
        font_label.config(text="Шрифт не выбран")


def choose_color():
    global color
    color = colorchooser.askcolor(title="Выберите цвет текста")[0]
    if color:
        color_label.config(text=f"Цвет текста: {color}")


def create_image():
    global font_path, color

    # Текст для изображения
    text = text_entry.get()
    if not text:
        text = "Пример текста"

    # Размер изображения
    width = int(width_entry.get()) if width_entry.get().isdigit() else 400
    height = int(height_entry.get()) if height_entry.get().isdigit() else 100

    # Цвет фона
    bg_color = bg_color_entry.get()
    try:
        bg_color = tuple(map(int, bg_color.split(",")))  # Преобразуем в (R, G, B)
    except:
        bg_color = (250, 100, 0)  # Оранжевый по умолчанию

    # Создаём изображение
    image = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Настраиваем шрифт
    try:
        font = ImageFont.truetype(font_path, 40) if font_path else ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Получаем размер текста
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Центрирование текста
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Рисуем текст
    draw.text((x, y), text, font=font, fill=tuple(map(int, color)) if color else "white")

    # Сохраняем и отображаем изображение
    image.save("custom_image.png")
    image.show()


# Инициализация окна
root = tk.Tk()
root.title("Создание изображения")

# Поля для ввода текста
tk.Label(root, text="Введите текст:").pack()
text_entry = tk.Entry(root, width=50)
text_entry.pack()

# Поля для выбора размера изображения
tk.Label(root, text="Ширина изображения:").pack()
width_entry = tk.Entry(root, width=20)
width_entry.insert(0, "400")
width_entry.pack()

tk.Label(root, text="Высота изображения:").pack()
height_entry = tk.Entry(root, width=20)
height_entry.insert(0, "100")
height_entry.pack()

# Поля для выбора цвета фона
tk.Label(root, text="Цвет фона (R,G,B):").pack()
bg_color_entry = tk.Entry(root, width=20)
bg_color_entry.insert(0, "250,100,0")
bg_color_entry.pack()

# Выбор шрифта
tk.Button(root, text="Выбрать шрифт", command=choose_font).pack()
font_label = tk.Label(root, text="Шрифт не выбран")
font_label.pack()

# Выбор цвета текста
tk.Button(root, text="Выбрать цвет текста", command=choose_color).pack()
color_label = tk.Label(root, text="Цвет текста: white")
color_label.pack()

# Кнопка для создания изображения
tk.Button(root, text="Создать изображение", command=create_image).pack()

root.mainloop()
