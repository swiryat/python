import tkinter as tk
import imageio
import numpy as np
import cv2
from threading import Thread
from PIL import Image, ImageTk  # Добавьте этот импорт

class VideoRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Видеозапись с камеры")

        # Создаем элементы интерфейса
        self.video_label = tk.Label(root, text="Видео с камеры", width=50, height=2)
        self.video_label.pack()

        self.video_panel = tk.Label(root)  # Метка для отображения видео
        self.video_panel.pack()

        self.record_button = tk.Button(root, text="Начать запись", width=20, height=2, command=self.toggle_recording)
        self.record_button.pack()

        self.cap = cv2.VideoCapture(0)  # Подключаемся к первой доступной камере
        if not self.cap.isOpened():
            print("Не удалось открыть камеру.")
            return

        self.is_recording = False  # Статус записи
        self.out = None  # Объект для записи видео
        self.fps = 20.0  # Частота кадров
        self.frame_size = (640, 480)  # Размер кадра для записи

    def toggle_recording(self):
        """Переключение записи видео"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        """Запуск записи"""
        self.is_recording = True
        self.record_button.config(text="Остановить запись")
        
        # Создаем объект для записи видео с использованием imageio
        self.writer = imageio.get_writer('output.mp4', fps=self.fps)

        # Запускаем отдельный поток для записи видео
        self.record_thread = Thread(target=self.record_video)
        self.record_thread.daemon = True  # Это позволит завершить поток при закрытии окна
        self.record_thread.start()

    def stop_recording(self):
        """Остановка записи"""
        self.is_recording = False
        self.record_button.config(text="Начать запись")
        if self.writer:
            self.writer.close()
            self.writer = None

    def record_video(self):
        """Запись видео с камеры"""
        while self.is_recording:
            ret, frame = self.cap.read()
            if not ret:
                print("Не удалось захватить кадр.")
                break

            # Переводим кадр в формат RGB (imageio ожидает RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Записываем кадр в файл
            if self.writer:
                self.writer.append_data(frame_rgb)

            # Показываем кадр в Tkinter (обновление только один раз за цикл)
            frame_resized = cv2.resize(frame, self.frame_size)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))  # Создаем изображение для Tkinter

            # Обновляем изображение в Tkinter
            self.video_panel.img = img
            self.video_panel.config(image=img)

            # Задержка для плавности отображения
            self.root.after(10, self.update_image)

    def update_image(self):
        """Обновление изображения в Tkinter"""
        self.video_panel.update()

    def run(self):
        """Главный цикл приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoRecorderApp(root)
    app.run()
