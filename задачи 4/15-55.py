import tkinter as tk
from tkinter import messagebox

class ExitConfirmationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exit Confirmation")

        self.create_widgets()

    def create_widgets(self):
        # Создаем метку с приветствием
        label = tk.Label(self.root, text="Добро пожаловать! Хотите выйти?")
        label.pack(pady=10)

        # Создаем кнопку для подтверждения выхода
        exit_button = tk.Button(self.root, text="Выйти", command=self.confirm_exit)
        exit_button.pack(side="left", padx=10)

        # Создаем кнопку для отмены выхода
        cancel_button = tk.Button(self.root, text="Отмена", command=self.cancel_exit)
        cancel_button.pack(side="right", padx=10)

    def confirm_exit(self):
        # Показываем диалоговое окно для подтверждения выхода
        result = messagebox.askokcancel("Подтверждение выхода", "Вы уверены, что хотите выйти?")
        if result:
            self.root.destroy()  # Закрываем приложение, если пользователь подтвердил выход

    def cancel_exit(self):
        # Отменяем выход
        messagebox.showinfo("Отмена", "Выход отменен")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExitConfirmationApp(root)
    root.protocol("WM_DELETE_WINDOW", app.confirm_exit)  # Добавляем обработчик закрытия окна
    root.mainloop()
