import os
import time
from PIL import Image, ImageTk
import tkinter as tk
from pygame import mixer

def change_image():
    global image_index, image_files
    
    # Определяем текущее изображение и переходим к следующему
    image_index = (image_index + 1) % len(image_files)
    image_path = os.path.join(image_folder, image_files[image_index])
    
    # Открываем изображение и обновляем его на холсте
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_item, image=photo)
    canvas.image = photo
    
    # Повторяем через 15 секунд
    root.after(15000, change_image)

# Папка с изображениями
image_folder = r'C:\Users\swer\Downloads\pik'

# Файл аудио
audio_file = r'C:\Users\swer\Downloads\den.mp3'

# Получаем список файлов из папки
image_files = os.listdir(image_folder)
image_files = [f for f in image_files if f.endswith(('.png', '.jpg', '.jpeg'))]

# Инициализируем глобальные переменные
image_index = -1

# Инициализация pygame.mixer
mixer.init()

# Предварительная загрузка аудиофайла
mixer.music.load(audio_file)
# Воспроизведение аудиофайла
mixer.music.play()

# Создаем окно
root = tk.Tk()
root.title("Смена изображений")

# Создаем холст для изображений
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Создаем пустое изображение на холсте
placeholder_image = Image.new('RGB', (800, 600), 'white')
placeholder_photo = ImageTk.PhotoImage(placeholder_image)
image_item = canvas.create_image(0, 0, anchor=tk.NW, image=placeholder_photo)

# Текст для надписи
text = "Ирина, Поздравляю!"

# Задаем начальные координаты
x = 20
y = 20

# Добавляем каждую букву отдельно на холст
for char in text:
    # Создаем надпись для текущей буквы
    text_item = canvas.create_text(x, y, anchor=tk.NW, text=char, font=("Arial", 20), fill="blue")
    # Увеличиваем координаты по вертикали для следующей буквы
    y += 30  # Расстояние между строками (можете изменить по вашему усмотрению)



# Вызываем функцию смены изображений
change_image()

# Запускаем основной цикл программы
root.mainloop()
