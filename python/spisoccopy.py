import os

def list_file_headers(directory):
    headers = []
    
    if not os.path.isdir(directory):
        print(f"Директория '{directory}' не существует.")
        return headers
    
    files = os.listdir(directory)
    
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        
        if os.path.isfile(file_path):
            header = os.path.splitext(file_name)[0]
            headers.append(header)
    
    return headers

def save_headers_to_file(headers, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for header in headers:
            f.write(header + '\n')

if __name__ == "__main__":
    # Указываем путь к целевой директории
    target_directory = r'C:\Users\swer\Desktop\медикпроф'
    
    # Получаем заголовки файлов
    headers = list_file_headers(target_directory)
    
    # Указываем путь для сохранения списка заголовков в файл
    output_file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'headers.txt')
    
    # Сохраняем заголовки в файл
    save_headers_to_file(headers, output_file_path)
    
    print(f"Список заголовков файлов сохранён в '{output_file_path}'.")
