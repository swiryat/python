from bs4 import BeautifulSoup
import os
from urllib.request import Request, urlopen

def download_links(url, output_folder):
    # Создаем папку для сохранения ссылок, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Заголовки User-Agent
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Формируем запрос с заголовками User-Agent
    req = Request(url=url, headers=headers)

    try:
        # Отправляем запрос и получаем ответ
        response = urlopen(req)
    except Exception as e:
        print('Не удалось получить доступ к веб-странице:', e)
        return

    # Проверяем успешность запроса
    if response.getcode() == 200:
        # Используем BeautifulSoup для парсинга HTML-кода страницы
        soup = BeautifulSoup(response.read(), 'html.parser')

        # Находим все теги <a> (ссылки) на странице
        links = soup.find_all('a')

        # Создаем текстовый файл для сохранения ссылок
        output_file = os.path.join(output_folder, 'links.txt')

        # Открываем файл для записи
        with open(output_file, 'w', encoding='utf-8') as f:
            # Записываем каждую ссылку на новой строке
            for link in links:
                href = link.get('href')
                if href:
                    f.write(href + '\n')

        print(f'Ссылки были успешно сохранены в файл {output_file}')
    else:
        print('Не удалось получить доступ к веб-странице')

# Пример использования
url = 'https://studref.com/426930/bzhd/toksikologiya_i_meditsinskaya_zaschita'
output_folder = 'downloaded_links'  # Укажите папку для сохранения ссылок
download_links(url, output_folder)