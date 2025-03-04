from bs4 import BeautifulSoup
from datetime import datetime

# Задайте путь к вашему файлу MHTML
file_path = r"C:\Users\swer\1.mhtml"

# Задайте целевую дату
target_date = datetime(2023, 11, 27)

# Чтение содержимого файла MHTML
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Используем BeautifulSoup для разбора HTML-кода
soup = BeautifulSoup(content, 'html.parser')

# Найдем все таблицы на странице
tables = soup.find_all('table')

# Проходимся по строкам таблиц и выводим те, которые соответствуют условиям
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        # Предположим, что дата окончания находится в последней ячейке каждой строки
        cells = row.find_all(['td', 'th'])
        if len(cells) >= 7:  # Проверяем, что у нас есть достаточное количество ячеек для даты окончания
            end_date_cell = cells[6].text.strip()
            try:
                end_date_value = datetime.strptime(end_date_cell, '%d.%m.%Y')
                if end_date_value < target_date:
                    print(f"Найдена строка с датой окончания ранее чем 27.11.2023: {row}")
                else:
                    print(f"Строка не соответствует условиям: {row}")
                    print(f"Дата окончания: {end_date_value}")
            except ValueError as e:
                # Пропускаем строки, в которых дата не может быть преобразована
                print(f"Ошибка преобразования даты: {end_date_cell}")
                print(f"Ошибка: {e}")
                continue

# Добавляем команду input(), чтобы удержать окно открытым
input("Нажмите Enter для завершения программы")





