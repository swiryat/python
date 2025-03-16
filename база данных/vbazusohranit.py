import os
import re
import sqlite3
import queue
import threading

# Настройки
SAVE_DIR = r"C:\Users\swer\JavaRush_Articles"  # Папка с исходными файлами
DB_PATH = r"C:\Users\swer\JavaRush_Articles\articles.db"  # Путь к базе данных

# Очередь для работы с базой данных
db_queue = queue.Queue()

# Создание базы данных, если она не существует
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            category TEXT NOT NULL,
            UNIQUE(title, url)
        )
    """)
    conn.commit()
    conn.close()

# Обработка файла и извлечение данных
def process_file(file_path):
    """ Извлекает данные из файла и сохраняет их в базу данных """
    try:
        # Открываем файл
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Извлекаем заголовок из содержимого
        title_tag = re.search(r"<h1>(.*?)</h1>", content)
        title = title_tag.group(1).strip() if title_tag else "Без названия"
        filename_base = re.sub(r"[^\w\-_]", "_", title)

        # Определение категории
        category = "Разное"
        for cat in ["Java", "Python", "Алгоритмы"]:
            if cat.lower() in title.lower():
                category = cat
                break

        # Добавление в очередь на вставку в БД
        db_queue.put(("INSERT OR IGNORE INTO articles (title, url, category) VALUES (?, ?, ?)", 
                      (title, file_path, category)))

        print(f"✅ Обработан файл: {title}")
    except Exception as e:
        print(f"❌ Ошибка при обработке файла {file_path}: {e}")

# Обработчик очереди для записи в базу данных
def db_worker():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    while True:
        try:
            query, params = db_queue.get()
            if query is None:  # Прекращение работы, если в очередь отправлен None
                break
            cursor.execute(query, params)
            conn.commit()
        except Exception as e:
            print(f"❌ Ошибка при вставке в базу данных: {e}")
    
    conn.close()

# Запуск потока для обработки очереди
def start_db_thread():
    db_thread = threading.Thread(target=db_worker)
    db_thread.start()
    return db_thread

# Основная функция
def main():
    # Инициализация базы данных
    init_db()

    # Запуск потока для обработки базы данных
    db_thread = start_db_thread()

    # Обработка всех файлов в директории
    threads = []
    for root, _, files in os.walk(SAVE_DIR):
        for file_name in files:
            if file_name.endswith(".html"):  # Ожидаем файлы с расширением .html
                file_path = os.path.join(root, file_name)
                thread = threading.Thread(target=process_file, args=(file_path,))
                threads.append(thread)
                thread.start()

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    # Завершаем работу потока базы данных
    db_queue.put(None)  # Завершаем работу потока
    db_thread.join()     # Ждём завершения потока

if __name__ == "__main__":
    main()
