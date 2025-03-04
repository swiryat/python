import os

def shutdown_in(minutes: int):
    """
    Устанавливает таймер для выключения компьютера через заданное количество минут.

    Параметры:
        minutes (int): Количество минут до выключения.
    """
    try:
        # Перевод минут в секунды
        seconds = minutes * 60

        # Вывод сообщения пользователю
        print(f"Выключение компьютера запланировано через {minutes} минут.")

        # Выполняем системную команду
        os.system(f"shutdown /s /t {seconds}")  # Windows
        # os.system(f"shutdown -h +{minutes}")  # Linux/Unix
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    # Устанавливаем таймер на 50 минут
    shutdown_in(50)
