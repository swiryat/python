import sqlite3

# Укажите путь к файлу базы данных SQLite
db_file = "1.db"

# Создайте соединение с базой данных
conn = sqlite3.connect(db_file)

# Создайте объект-курсор для выполнения SQL-запросов
cursor = conn.cursor()

# Выполните SQL-запрос для получения списка таблиц в базе данных
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Получите результат запроса
tables = cursor.fetchall()

# Выведите список таблиц
for table in tables:
    print(table[0])

# Закройте курсор и соединение
cursor.close()
conn.close()
