import tkinter as tk  # Импортирование библиотеки tkinter и задание псевдонима "tk"

class DrawingApp:
    def __init__(self, root):
        # Инициализация класса DrawingApp, который будет управлять приложением
        self.root = root  # Сохранение ссылки на главное окно приложения
        self.root.title("Альбом для рисования")  # Задание заголовка окна

        self.canvas = tk.Canvas(self.root, bg="white")  # Создание холста для рисования на главном окне
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Размещение холста на главном окне, заполняя его полностью

        # Привязка событий мыши к методам класса DrawingApp
        self.canvas.bind("<Button-1>", self.start_drawing)       # Обработка нажатия левой кнопки мыши
        self.canvas.bind("<B1-Motion>", self.draw)               # Обработка движения мыши с зажатой левой кнопкой
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing) # Обработка отпускания левой кнопки мыши

        self.drawing = True  # Флаг, указывающий на состояние рисования (True - рисование, False - нет рисования)
        self.last_x = 0  # Последняя известная позиция курсора по X
        self.last_y = 0  # Последняя известная позиция курсора по Y

    def start_drawing(self, event):
        # Метод вызывается при нажатии левой кнопки мыши
        self.drawing = True  # Установка флага рисования в True
        self.last_x = event.x  # Запоминание текущей позиции курсора по X
        self.last_y = event.y  # Запоминание текущей позиции курсора по Y

    def draw(self, event):
        # Метод вызывается при движении мыши с зажатой левой кнопкой
        if self.drawing:  # Если флаг рисования установлен в True
            x = event.x  # Текущая позиция курсора по X
            y = event.y  # Текущая позиция курсора по Y
            # Создание линии на холсте от последней позиции курсора до текущей позиции
            self.canvas.create_line(self.last_x, self.last_y, x, y, width=2, fill="black")
            self.last_x = x  # Обновление последней позиции курсора по X
            self.last_y = y  # Обновление последней позиции курсора по Y

    def stop_drawing(self, event):
        # Метод вызывается при отпускании левой кнопки мыши
        self.drawing = False  # Установка флага рисования в False

def main():
    root = tk.Tk()  # Создание главного окна tkinter
    app = DrawingApp(root)  # Создание экземпляра класса DrawingApp, передача главного окна
    root.mainloop()  # Запуск главного цикла событий tkinter

if __name__ == "__main__":
    main()  # Вызов функции main(), запускающей приложение
