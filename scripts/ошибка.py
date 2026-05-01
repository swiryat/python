# ... (предыдущий код)

def set_alarm():
    try:
        # Код установки будильника без изменений
        pass
    except ValueError as e:
        print(e)  # Выводим ошибку в консоль для более детального просмотра
        messagebox.showerror("Ошибка", str(e))

# ... (продолжение кода)
