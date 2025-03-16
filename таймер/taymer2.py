import tkinter as tk
from tkinter import messagebox, filedialog
import time
import threading
from playsound import playsound  # Для воспроизведения музыки

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

# Функция для запуска отсчета и вывода сигнала
def start_timer(interval):
    def run_timer():
        while True:
            time.sleep(interval * 60)  # Перевод минут в секунды
            if selected_music:
                playsound(selected_music)
            else:
                messagebox.showinfo("Сигнал", f"Прошло {interval} минут!")

    # Запуск таймера в отдельном потоке, чтобы интерфейс оставался отзывчивым
    timer_thread = threading.Thread(target=run_timer, daemon=True)
    timer_thread.start()

# Создание интерфейса
root = tk.Tk()
root.title("Таймер сигналов")

# Кнопка для выбора музыкального файла
choose_music_button = tk.Button(root, text="Выбрать музыку", command=choose_music)
choose_music_button.pack(pady=5)

# Создание кнопок для выбора интервала
intervals = [5, 10, 15, 30, 45, 60]  # Интервалы в минутах

for interval in intervals:
    button = tk.Button(root, text=f"{interval} минут", command=lambda i=interval: start_timer(i))
    button.pack(pady=5)

# Запуск приложения
root.mainloop()
