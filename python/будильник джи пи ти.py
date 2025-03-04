import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import time
import datetime
import pygame

class AlarmClock:

    def __init__(self, root):
        self.root = root
        self.root.title("Будильник")

        # Создаем Canvas на весь экран
        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        self.canvas.pack()

        # Загружаем изображение по умолчанию и растягиваем его на размер Canvas
        default_image = Image.open("background.jpg")
        default_image = default_image.resize((self.canvas.winfo_screenwidth(), self.canvas.winfo_screenheight()), Image.LANCZOS)
        self.default_photo = ImageTk.PhotoImage(default_image)
        
        # Создаем изображение на Canvas, используя create_image
        self.default_background_label = self.canvas.create_image(0, 0, anchor="nw", image=self.default_photo)

        # Поля для ввода времени
        self.hour_var = tk.StringVar(value="00")
        self.minute_var = tk.StringVar(value="00")
    
        self.hour_entry = tk.Entry(self.canvas, textvariable=self.hour_var, width=2)
        self.hour_entry.grid(row=1, column=0)

        self.colon_label = tk.Label(self.canvas, text=":")
        self.colon_label.grid(row=1, column=1)

        self.minute_entry = tk.Entry(self.canvas, textvariable=self.minute_var, width=2)
        self.minute_entry.grid(row=1, column=2)

        # Кнопки
        self.set_button = tk.Button(self.canvas, text="Установить", command=self.set_alarm)
        self.set_button.grid(row=1, column=3)

        self.choose_photo_button = tk.Button(self.canvas, text="Выбрать фото", command=self.choose_photo)
        self.choose_photo_button.grid(row=2, column=0, columnspan=4)

        self.photo = None
        self.background_label = None

        # Добавляем обработчик события изменения размера окна
        self.root.bind("<Configure>", self.resize_background)

    def choose_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")])
        if file_path:
            # Открываем выбранное фото и растягиваем на размер Canvas
            self.photo = Image.open(file_path)
            self.photo = self.photo.resize((self.canvas.winfo_screenwidth(), self.canvas.winfo_screenheight()), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.photo)
        
            # Если уже есть background_label, удаляем его перед созданием нового
            if self.background_label:
                self.canvas.delete(self.background_label)
        
            # Создаем изображение на Canvas, используя create_image
            self.background_label = self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def resize_background(self, event):
        # Проверяем, есть ли фото
        if self.photo:
            new_width = event.width
            new_height = event.height
            self.photo = self.photo.resize((new_width, new_height), Image.LANCZOS)
            self.canvas.itemconfig(self.background_label, image=self.photo)  # Обновляем изображение

    def set_alarm(self):
        try:
            # Получение введенных часов и минут
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
        
            # Проверка корректности введенных значений
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError("Некорректное время. Введите значения в диапазоне 00-23 часов и 00-59 минут.")

            # Получение текущего времени и даты
            current_time = datetime.datetime.now()

            # Создание объекта для будильника с указанными часами и минутами
            alarm_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # Рассчет времени до будильника
            time_to_alarm = (alarm_time - current_time).seconds

            # Ожидание до времени срабатывания будильника
            time.sleep(time_to_alarm)

            # Проигрывание музыки при срабатывании будильника
            self.play_alarm_sound()

            # Показ всплывающего окна с сообщением о будильнике
            self.show_alarm_popup()

        except ValueError as e:
            print(e)
            messagebox.showerror("Ошибка", str(e))

    def play_alarm_sound(self):
        pygame.mixer.init()
        alarm_sound = pygame.mixer.Sound("C:\\1.wav")  # Замените на путь к вашему аудио файлу
        alarm_sound.play()

    def show_alarm_popup(self):
        messagebox.showinfo("Будильник", "GM :3 :3")

if __name__ == "__main__":
    root = tk.Tk()
    alarm_clock = AlarmClock(root)
    root.mainloop()
