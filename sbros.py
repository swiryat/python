import os

# Путь к файлу настроек на Windows
settings_path = os.path.expanduser(r'~\AppData\Roaming\Code\User\settings.json')

# Для Linux/Mac используйте:
# settings_path = os.path.expanduser('~/.config/Code/User/settings.json')

# Проверка существования файла
if os.path.exists(settings_path):
    try:
        # Открываем файл для записи и очищаем его содержимое
        with open(settings_path, 'w') as file:
            file.write('{}')  # Записываем пустой JSON-объект для сброса настроек
        print("Настройки сброшены.")
    except Exception as e:
        print(f"Ошибка при сбросе настроек: {e}")
else:
    print("Файл настроек не найден.")
