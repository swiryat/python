import shutil
import os

# Путь к файлу настроек
settings_path = os.path.expanduser(r'~\AppData\Roaming\Code\User\settings.json')

# Путь к резервной копии настроек
backup_path = r'C:\path\to\your\settings_backup.json'

# Проверка существования резервной копии
if os.path.exists(backup_path):
    try:
        shutil.copy(backup_path, settings_path)  # Копируем резервную копию в место файла настроек
        print("Настройки восстановлены.")
    except Exception as e:
        print(f"Ошибка при восстановлении настроек: {e}")
else:
    print("Резервная копия настроек не найдена.")
