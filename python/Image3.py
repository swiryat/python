import tkinter as tk
from tkinter import filedialog, colorchooser, font
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Функция для создания изображения
def create_image():
    text = text_entry.get()  # Получаем текст
    font_size = int(font_size_entry.get())  # Получаем размер шрифта
    bg_color = bg_color_var.get()  # Получаем цвет фона
    text_color = text_color_var.get()  # Получаем цвет текста
    font_choice = font_choice_var.get()  # Получаем шрифт

    # Создаём изображение с заданным фоном
    image = Image.new('RGB', (400, 100), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Указываем шрифт
    try:
        font = ImageFont.truetype(font_choice, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Получаем размеры текста
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Рассчитываем координаты для центрирования текста
    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2

    # Добавляем тень для текста
    shadow_offset = 3
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill="black")

    # Рисуем текст на изображении
    draw.text((x, y), text, font=font, fill=text_color)

    # Отображаем изображение в окне
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

    # Сохраняем изображение
    save_button.config(state=tk.NORMAL)
    save_button.image_data = image  # Сохраняем объект изображения для сохранения

# Функция для сохранения изображения
def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        save_button.image_data.save(file_path)

# Функция для выбора цвета фона
def choose_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        bg_color_var.set(color)

# Функция для выбора цвета текста
def choose_text_color():
    color = colorchooser.askcolor()[1]
    if color:
        text_color_var.set(color)

# Функция для выбора шрифта
def choose_font():
    font_choice = filedialog.askopenfilename(filetypes=[("TrueType Fonts", "*.ttf")])
    if font_choice:
        font_choice_var.set(font_choice)

# Создание основного окна
root = tk.Tk()
root.title("Редактор изображений")

# Переменные для настроек
bg_color_var = tk.StringVar(value="#F25064")  # Цвет фона (по умолчанию оранжевый)
text_color_var = tk.StringVar(value="#FFFFFF")  # Цвет текста (по умолчанию белый)
font_choice_var = tk.StringVar(value="arial.ttf")  # Шрифт (по умолчанию Arial)

# Поле ввода текста
text_entry_label = tk.Label(root, text="Текст:")
text_entry_label.pack()
text_entry = tk.Entry(root, width=50)
text_entry.pack()

# Поле ввода размера шрифта
font_size_label = tk.Label(root, text="Размер шрифта:")
font_size_label.pack()
font_size_entry = tk.Entry(root, width=10)
font_size_entry.insert(0, "40")  # Размер по умолчанию
font_size_entry.pack()

# Кнопка для выбора цвета фона
bg_color_button = tk.Button(root, text="Выбрать цвет фона", command=choose_bg_color)
bg_color_button.pack()

# Кнопка для выбора цвета текста
text_color_button = tk.Button(root, text="Выбрать цвет текста", command=choose_text_color)
text_color_button.pack()

# Кнопка для выбора шрифта
font_button = tk.Button(root, text="Выбрать шрифт", command=choose_font)
font_button.pack()

# Кнопка для создания изображения
create_button = tk.Button(root, text="Создать изображение", command=create_image)
create_button.pack()

# Кнопка для сохранения изображения
save_button = tk.Button(root, text="Сохранить изображение", state=tk.DISABLED, command=save_image)
save_button.pack()

# Метка для отображения изображения
image_label = tk.Label(root)
image_label.pack()

# Запуск основного цикла
root.mainloop()
