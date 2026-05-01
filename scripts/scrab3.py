import pandas as pd
import requests
from io import StringIO
import datetime
from bs4 import BeautifulSoup
import sqlite3

# Задайте заголовок User-Agent, чтобы веб-сайт знал, что это запрос от браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def read_tables_from_html(html_content):
    # Создайте объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Используйте BeautifulSoup для поиска и извлечения таблиц
    tables = soup.find_all('table')

    if not tables:
        return []

    return tables

def optimize_and_save_table_to_db(table, index, conn):
    # Оптимизация обработки данных - например, фильтрация и агрегация
    # Здесь можно добавить дополнительные операции по обработке данных

    # Генерация имени таблицы в базе данных
    table_name = f"table_{index + 1}"

    # Преобразовать таблицу в DataFrame
    df = pd.read_html(str(table))[0]

    # Сохранить DataFrame в базу данных SQLite
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    print(f"Таблица {index + 1} сохранена в базу данных в таблицу {table_name}")

def main():
    try:
        # Отправить GET-запрос с заголовком User-Agent
        response = requests.get("http://mail.ru/", headers=headers)

        # Проверить статус ответа, чтобы убедиться, что запрос выполнен успешно
        if response.status_code == 200:
            # Считать HTML-контент ответа
            html_content = response.text

            # Извлечь и сохранить все найденные таблицы
            tables = read_tables_from_html(html_content)
            if not tables:
                print("Таблицы не найдены в HTML-контенте.")
            else:
                # Создать подключение к базе данных SQLite
                conn = sqlite3.connect("tables.db")

                for idx, table in enumerate(tables):
                    # Обработать и сохранить таблицу в базе данных
                    optimize_and_save_table_to_db(table, idx, conn)

                # Закрыть подключение к базе данных
                conn.close()

        else:
            print(f"Ошибка при запросе данных. Код состояния: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

if __name__ == "__main__":
    main()
