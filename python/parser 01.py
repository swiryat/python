import os
import requests
import logging
import time
from bs4 import BeautifulSoup
import re
import csv
import sqlite3

# Настройка логгера
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Заголовки для предотвращения блокировки
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Функция для отправки запроса с обработкой ошибок
def fetch_page(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на статус код 200
        logging.info(f"Запрос успешен для страницы {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе страницы {url}: {e}")
        return None

# Функция для извлечения данных из таблицы
def extract_case_data(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    case_rows = soup.find_all('tr', {'valign': 'top'})
    
    case_data = []
    for row in case_rows:
        case_number = row.find('a').text.strip() if row.find('a') else 'Не найдено'
        case_date = row.find_all('td')[1].text.strip() if len(row.find_all('td')) > 1 else 'Не найдено'
        case_info = row.find_all('td')[2].text.strip() if len(row.find_all('td')) > 2 else 'Не найдено'
        judge_name = row.find_all('td')[3].text.strip() if len(row.find_all('td')) > 3 else 'Не найдено'
        decision_date = row.find_all('td')[4].text.strip() if len(row.find_all('td')) > 4 else 'Не найдено'
        decision = row.find_all('td')[5].text.strip() if len(row.find_all('td')) > 5 else 'Не найдено'

        case_info = re.sub(r'\s+', ' ', case_info)  # Убираем лишние пробелы

        case_data.append({
            'Номер дела': case_number,
            'Дата подачи': case_date,
            'Информация по делу': case_info,
            'Судья': judge_name,
            'Дата решения': decision_date,
            'Решение': decision
        })
    
    if not case_data:
        logging.warning("Данные с этой страницы не были извлечены.")
    
    return case_data

# Функция для обработки нескольких страниц
def process_pages(base_url, start_page=1, end_page=5):
    all_cases = []
    
    for page_num in range(start_page, end_page + 1):
        logging.info(f"Обрабатываем страницу {page_num}...")
        url = f"{base_url}?page={page_num}"  # Формируем URL для каждой страницы
        page_content = fetch_page(url)
        
        if page_content:
            case_data = extract_case_data(page_content)
            all_cases.extend(case_data)
        
        # Пауза между запросами, чтобы не перегрузить сервер
        time.sleep(1)
    
    return all_cases

# Функция для сохранения данных в CSV файл
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    logging.info(f"Данные успешно сохранены в {filename}.")

# Функция для сохранения данных в SQLite базу
def save_to_db(data, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создание таблицы, если она еще не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS cases (
                        case_number TEXT,
                        case_date TEXT,
                        case_info TEXT,
                        judge_name TEXT,
                        decision_date TEXT,
                        decision TEXT)''')

    # Вставка данных
    for case in data:
        cursor.execute('''INSERT INTO cases (case_number, case_date, case_info, judge_name, decision_date, decision) 
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (case['Номер дела'], case['Дата подачи'], case['Информация по делу'], case['Судья'],
                        case['Дата решения'], case['Решение']))

    conn.commit()
    conn.close()
    logging.info(f"Данные успешно сохранены в базу данных {db_name}.")

# Основная функция
def main():
    base_url = "http://example.com/cases"  # Укажите URL для сайта с делами
    all_cases = process_pages(base_url, start_page=1, end_page=5)
    
    if all_cases:
        # Сохраняем данные в CSV
        save_to_csv(all_cases, 'cases.csv')
        
        # Сохраняем данные в SQLite базу данных
        save_to_db(all_cases, 'cases.db')
    else:
        logging.warning("Не удалось получить данные с указанных страниц.")

if __name__ == "__main__":
    main()
