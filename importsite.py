import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL сайта, с которого нужно получить информацию
url = "https://borpnd.zdrav36.ru/medrabotniki"

# Дата, по которой будет выполняться фильтрация (7.1.2023)
target_date = datetime(2023, 1, 7)

# Заголовки User-Agent и Referer
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.mail.ru'
}

# Путь к файлу сертификата браузера (замените на реальный путь)
browser_cert_path = '1.pem'

# Отправляем GET-запрос на сайт с использованием сертификата браузера
response = requests.get(url, headers=headers, verify=browser_cert_path)

# Проверяем, что запрос выполнен успешно
if response.status_code == 200:
    # Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Найдем все строки таблицы
    table_rows = soup.find_all('tr')

    # Пропустим заголовок таблицы (первая строка)
    for row in table_rows[1:]:
        # Разбиваем строку таблицы на столбцы
        columns = row.find_all('td')
        
        # Извлекаем данные
        fio = columns[0].text.strip()
        position = columns[1].text.strip()
        expiration_date_str = columns[6].text.strip()
        
        # Преобразуем дату из строки в объект datetime
        expiration_date = datetime.strptime(expiration_date_str, '%d.%m.%Y')
        
        # Проверяем, соответствует ли дата условию
        if expiration_date < target_date:
            # Выводим информацию, удовлетворяющую условию
            print(f"FIO: {fio}, Position: {position}, Expiration Date: {expiration_date.strftime('%d.%m.%Y')}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
