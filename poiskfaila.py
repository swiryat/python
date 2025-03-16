import os

def list_files_in_directory(path):
    # Проверяем, существует ли путь и является ли он директорией
    if os.path.exists(path) and os.path.isdir(path):
        # Перебираем все элементы в директории
        for root, dirs, files in os.walk(path):
            print(f"Текущая директория: {root}")
            if files:
                print("Найденные файлы:")
                for file in files:
                    print(f"  - {file}")
            else:
                print("Нет файлов в этой директории.")
            print("-" * 40)
    else:
        print("Указанный путь не существует или это не директория.")

# Пример использования
directory_path = input("Введите путь к папке: ")
list_files_in_directory(directory_path)
