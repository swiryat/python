def extract_directory_without_os(path):
    # Разделяем путь на компоненты
    components = path.split('/')
    
    # Собираем компоненты обратно, кроме последнего элемента (имени файла)
    directory = '/'.join(components[:-1])

    return directory

# Пример использования
file_path = "/home/vasya/miner.exe"
directory_name = extract_directory_without_os(file_path)
print("Название каталога:", directory_name)
