import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Функция для обхода сайта
def обход_сайта(url, макс_страниц):
    посещенные = set()  # Множество для хранения посещенных URL-адресов
    посещено_страниц = 0
    начальный_домен = urlparse(url).netloc

    # Проверка и добавление схемы, если ее нет
    if not urlparse(url).scheme:
        url = 'https://' + url

    # Функция для извлечения всех ссылок с страницы
    def получить_ссылки(страница):
        try:
            ответ = requests.get(страница)
            ответ.raise_for_status()  # Проверка на ошибки HTTP
            суп = BeautifulSoup(ответ.content, 'html.parser')
            ссылки = []
            for a in суп.find_all('a', href=True):
                ссылка = urljoin(страница, a.get('href'))
                parsed_url = urlparse(ссылка)
                if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc == начальный_домен:
                    ссылки.append(ссылка)
            print("Найденные ссылки:", ссылки)  # Вывод найденных ссылок
            return ссылки
        except Exception as e:
            print(f"Ошибка при получении ссылок с {страница}: {e}")
            return []

    # Рекурсивная функция обхода
    def рекурсивный_обход(страница):
        nonlocal посещено_страниц
        if посещено_страниц >= макс_страниц:
            return
        if страница in посещенные:
            return
        посещенные.add(страница)
        print("Обход сайта:", страница)
        посещено_страниц += 1
        try:
            ссылки = получить_ссылки(страница)
            for ссылка in ссылки:
                рекурсивный_обход(ссылка)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"Ошибка при обходе {страница}: {e}")

    # Начать обход с указанного URL-адреса
    рекурсивный_обход(url)

# Ввод данных
начальный_url = input("Введите начальный URL: ").strip()
макс_страниц = int(input("Введите максимальное количество страниц для обхода: "))

# Начать обход сайта
обход_сайта(начальный_url, макс_страниц)
