import requests
from bs4 import BeautifulSoup

def extract_metadata(url):
    # Отправляем GET-запрос к веб-странице
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлекаем метаданные
        title = soup.title.text if soup.title else 'No title'
        description = soup.find('meta', attrs={'name': 'description'})
        description = description.get('content') if description else 'No description'

        # Выводим результат
        print(f'Title: {title}')
        print(f'Description: {description}')
    else:
        print(f'Error: Unable to fetch the webpage. Status code: {response.status_code}')

# Замените 'https://example.com' на URL нужной вам веб-страницы
url_to_scrape = 'https://klinpsy.ru'
extract_metadata(url_to_scrape)
