import pandas as pd
import requests
from io import StringIO
import datetime

# Задайте заголовок User-Agent, чтобы веб-сайт знал, что это запрос от браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

try:
    # Отправить GET-запрос с заголовком User-Agent
    response = requests.get("http://mail.ru/", headers=headers)

    # Проверить статус ответа, чтобы убедиться, что запрос выполнен успешно (код 200 означает успех)
    if response.status_code == 200:
        # Считать таблицы из HTML-контента ответа
        html_content = response.text
        tables = pd.read_html(StringIO(html_content))

        # Вывести и сохранить все найденные таблицы
        for idx, table in enumerate(tables):
            print(f"Таблица {idx + 1}:")
            print(table)
            print()

            # Оптимизация обработки данных - например, фильтрация и агрегация
            # Здесь можно добавить дополнительные операции по обработке данных

            # Генерация имени файла с использованием текущей даты и времени
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"table_{idx + 1}_{current_datetime}.csv"

            # Сохранить таблицу в формате CSV
            table.to_csv(filename, index=False)
            print(f"Таблица {idx + 1} сохранена в файл {filename}")

    else:
        print(f"Ошибка при запросе данных. Код состояния: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")
