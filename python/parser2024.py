import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

# Базовый URL сайта
base_url = "https://oblsud--vrn.sudrf.ru/modules.php"

# Заголовки для имитации браузера
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36"
    )
}

# Функция для парсинга одной страницы
def parse_page(url, session):
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлечение данных (пример: таблица с делами)
        data = []
        table = soup.find("table", class_="data")  # Укажите точный класс таблицы
        if table:
            rows = table.find_all("tr")
            for row in rows[1:]:  # Пропускаем заголовок таблицы
                cols = [col.get_text(strip=True) for col in row.find_all("td")]
                data.append(cols)

        # Поиск ссылки на следующую страницу
        next_page_tag = soup.find("a", title="Следующая страница")
        next_page_url = urljoin(base_url, next_page_tag['href']) if next_page_tag else None

        return data, next_page_url
    except Exception as e:
        print(f"Ошибка при парсинге страницы: {e}")
        return [], None

# Функция для парсинга всех страниц
def parse_all_pages(start_url, max_pages=100, delay=2):
    all_data = []
    session = requests.Session()
    current_url = start_url
    page = 1

    while current_url and page <= max_pages:
        print(f"Парсинг страницы {page}: {current_url}")
        page_data, next_url = parse_page(current_url, session)
        if not page_data:  # Если данных нет, прекращаем
            print("Нет данных на странице или произошла ошибка!")
            break
        all_data.extend(page_data)
        current_url = next_url  # Переход на следующую страницу
        page += 1
        time.sleep(delay)  # Задержка для избежания блокировки

    return all_data

# URL начальной страницы
start_url = (
    "https://oblsud--vrn.sudrf.ru/modules.php?name=sud_delo&srv_num"
)