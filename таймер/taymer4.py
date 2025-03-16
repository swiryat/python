import tkinter as tk
from tkinter import messagebox, filedialog
import time
import threading
import pygame  # Импорт библиотеки pygame

# Инициализация модуля микшера в pygame
pygame.mixer.init()

# Глобальная переменная для хранения пути к выбранному музыкальному файлу
selected_music = None

# Функция для выбора музыкального файла
def choose_music():
    global selected_music
    selected_music = filedialog.askopenfilename(
        title="Выберите музыкальный файл",
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
    )
    if selected_music:
        messagebox.showinfo("Музыка выбрана", f"Выбранный файл: {selected_music}")

# Функция для воспроизведения музыки
def play_music():
    if selected_music:
        pygame.mixer.music.load(selected_music)
        pygame.mixer.music.play()
    else:
        messagebox.showinfo("Ошибка", "Музыкальный файл не выбран!")

# Функция для остановки музыки
def stop_music():
    if pygame.mixer.music.get_busy():  # Проверка, играет ли музыка
        pygame.mixer.music.stop()

# Функция для запуска отсчета и выдачи сигнала
def start_timer(interval, button):
    def run_timer():
        # Изменить цвет кнопки на зелёный при старте таймера
        button.config(bg="green")
        time.sleep(interval * 60)  # Перевод минут в секунды
        play_music()
        # Вернуть цвет кнопки на красный по окончании таймера
        button.config(bg="red")

    # Остановить текущее воспроизведение перед запуском нового таймера
    stop_music()

    # Запуск таймера в отдельном потоке, чтобы интерфейс оставался отзывчивым
    timer_thread = threading.Thread(target=run_timer, daemon=True)
    timer_thread.start()

# Создание интерфейса
root = tk.Tk()
root.title("Таймер сигналов")

# Кнопка для выбора музыкального файла
choose_music_button = tk.Button(root, text="Выбрать музыку", command=choose_music)
choose_music_button.pack(pady=5)

# Кнопка для остановки музыки
stop_music_button = tk.Button(root, text="Остановить музыку", command=stop_music)
stop_music_button.pack(pady=5)

# Создание кнопок для выбора интервала
intervals = [5, 10, 15, 30, 45, 60]  # Интервалы в минутах

for interval in intervals:
    button = tk.Button(root, text=f"{interval} минут", bg="red")
    button.config(command=lambda i=interval, b=button: start_timer(i, b))
    button.pack(pady=5)

# Добавление кнопки с отсчетом в 1 минуту
one_minute_button = tk.Button(root, text="1 минута", bg="red")
one_minute_button.config(command=lambda: start_timer(1, one_minute_button))
one_minute_button.pack(pady=5)

# Запуск приложения
root.mainloop()
