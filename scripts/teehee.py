import tkinter as tk
import tkinter.colorchooser

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("my silly little drawing app :3")

        self.undo_button = tk.Button(self.root, text="cancel!", command=self.undo)
        self.undo_button.pack()

        self.color_button = tk.Button(self.root, text="change the color!", command=self.choose_color)
        self.color_button.pack()

        self.eraser_button = tk.Button(self.root, text="eraser!", command=self.toggle_eraser)
        self.eraser_button.pack()

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.drawing_list = []  # Список для хранения нарисованных линий

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.drawing = False
        self.current_line = []  # Список для хранения сегментов текущей линии
        self.last_x = 0
        self.last_y = 0
        self.current_color = "black"  # Инициализация цвета
        self.eraser_mode = False  # Инициализация режима ластика

    def choose_color(self):
        color = tkinter.colorchooser.askcolor()[1]
        if color:
            self.current_color = color

    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode
        if self.eraser_mode:
            self.eraser_button.config(relief=tk.SUNKEN)
        else:
            self.eraser_button.config(relief=tk.RAISED)

    def undo(self):
        if self.drawing_list:
            line_segments = self.drawing_list.pop()
            for segment in line_segments:
                self.canvas.delete(segment)

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        self.current_line = []  # Начинаем новую линию

    def draw(self, event):
        if self.drawing:
            x = event.x
            y = event.y
            color = "white" if self.eraser_mode else self.current_color
            line_segment = self.canvas.create_line(self.last_x, self.last_y, x, y, width=2, fill=color)
            self.current_line.append(line_segment)
            self.last_x = x
            self.last_y = y

    def stop_drawing(self, event):
        if self.drawing:
            self.drawing_list.append(self.current_line)
            self.drawing = False

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
