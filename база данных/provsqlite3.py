import sqlite3

try:
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # Создаём тестовую таблицу (если её нет)
    cursor.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
    
    # Вставляем тестовые данные
    cursor.execute("INSERT INTO test (name) VALUES (?)", ("Hello, SQLite!",))
    conn.commit()  # Сохраняем изменения
    
    # Проверяем, записались ли данные
    cursor.execute("SELECT * FROM test")
    rows = cursor.fetchall()
    
    # Выводим содержимое таблицы
    for row in rows:
        print(row)
    
except sqlite3.Error as e:
    print("Ошибка SQLite:", e)
finally:
    conn.close()  # Закрываем соединение
