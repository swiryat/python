import tkinter as tk
from tkinter import messagebox
import time
import threading

# Функция для запуска отсчета и вывода сигнала
def start_timer(interval):
    def run_timer():
        while True:
            time.sleep(interval * 60)  # Перевод минут в секунды
            messagebox.showinfo("Сигнал", f"Прошло {interval} минут!")
    
    # Запуск таймера в отдельном потоке, чтобы интерфейс оставался отзывчивым
    timer_thread = threading.Thread(target=run_timer, daemon=True)
    timer_thread.start()

# Создание интерфейса
root = tk.Tk()
root.title("Таймер сигналов")

# Создание кнопок для выбора интервала
intervals = [5, 10, 15, 30, 45, 60]  # Интервалы в минутах

for interval in intervals:
    button = tk.Button(root, text=f"{interval} минут", command=lambda i=interval: start_timer(i))
    button.pack(pady=5)

# Запуск приложения
root.mainloop()
