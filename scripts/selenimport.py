# Импорт необходимых библиотек 
import time  # Для добавления случайных задержек
import random  # Для случайных чисел
import requests  # Для отправки HTTP-запросов
import os  # Для работы с файловой системой (создание директорий и сохранение файлов)
from selenium import webdriver  # Для работы с веб-драйвером Selenium
from selenium.webdriver.chrome.service import Service  # Для создания сервиса ChromeDriver
from selenium.webdriver.chrome.options import Options  # Для настроек Chrome
from selenium.webdriver.common.by import By  # Для поиска элементов по разным методам
from selenium.webdriver.support.ui import WebDriverWait  # Для явных ожиданий
from selenium.webdriver.support import expected_conditions as EC  # Для проверки состояний элементов
from random import choice  # Для случайного выбора из списка

# Прокси-серверы для ротации (замените на реальные)
proxies = [
    "http://<proxy_ip>:<proxy_port>",  # Пример прокси
    "http://<proxy_ip>:<proxy_port>",  # Пример прокси
    "http://<proxy_ip>:<proxy_port>"   # Пример прокси
]

# Список User-Agent'ов для случайной смены
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko"
]

# Путь к chromedriver
driver_path = r"C:\Users\swer\selenium\chromedriver-win64\chromedriver.exe"
# Путь к установленному браузеру Chrome
chrome_path = r"C:\Users\swer\selenium\chrome-win64\chrome-win64\chrome.exe"

# Создание настроек для Chrome
chrome_options = Options()  # Создаём объект настроек
chrome_options.binary_location = chrome_path  # Указываем путь к Chrome
chrome_options.add_argument("--no-sandbox")  # Отключаем песочницу для безопасности
chrome_options.add_argument("--disable-dev-shm-usage")  # Отключаем использование общего пространства памяти
chrome_options.add_argument("--headless")  # Запускаем браузер в безголовом режиме (без графического интерфейса)
chrome_options.add_argument("--disable-logging")  # Отключаем логи
chrome_options.add_argument("--log-level=3")  # Устанавливаем уровень логирования (предотвращает вывод ненужных сообщений)

# Ротация прокси: выбираем случайный прокси-сервер для использования
chrome_options.add_argument(f'--proxy-server={choice(proxies)}')
# Ротация User-Agent'ов: выбираем случайный User-Agent
chrome_options.add_argument(f"user-agent={choice(user_agents)}")

# Инициализация WebDriver с заданными параметрами
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def download_file(file_url):
    try:
        # Получение содержимого файла через requests
        response = requests.get(file_url, headers={"User-Agent": choice(user_agents)}, proxies={"http": choice(proxies)})
        if response.status_code == 200:
            # Определение типа файла
            file_name = os.path.basename(file_url)
            # Сохранение файла в текущую директорию
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"Файл {file_name} скачан.")
        else:
            print(f"Не удалось скачать файл с URL: {file_url}")
    except Exception as e:
        print(f"Ошибка при скачивании файла: {e}")

def search_and_download(query):
    try:
        # Открытие Google с поисковым запросом
        driver.get(f"https://www.google.com/search?q={query}")
        time.sleep(random.uniform(2, 5))  # Случайная задержка

        page_counter = 0
        max_pages = 5  # Ограничиваем количество страниц
        while page_counter < max_pages:
            # Извлечение всех ссылок на странице с результатами поиска
            links = driver.find_elements(By.CSS_SELECTOR, "h3 a")
            urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]

            # Фильтрация ссылок, чтобы оставить только те, что начинаются с "http"
            valid_urls = [url for url in urls if url.startswith("http")]

            # Проход по всем найденным ссылкам
            for url in valid_urls:
                print(f"Переход по ссылке: {url}")
                driver.get(url)
                time.sleep(random.uniform(2, 5))  # Случайная задержка

                # Ищем на странице ссылки на файлы, такие как PDF, EPUB, DOCX, TXT
                file_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf') or contains(@href, '.epub') or contains(@href, '.docx') or contains(@href, '.txt')]")
                
                for file_link in file_links:
                    file_url = file_link.get_attribute("href")
                    print(f"Найден файл: {file_url}")

                    # Скачать файл, если он найден
                    download_file(file_url)

            # Пытаемся перейти на следующую страницу
            try:
                next_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next']"))
                )
                next_button.click()
                page_counter += 1
                time.sleep(random.uniform(2, 5))  # Случайная задержка перед загрузкой следующей страницы
            except Exception as e:
                print(f"Не удалось перейти на следующую страницу: {e}")
                break
    except Exception as e:
        print(f"Ошибка при поиске и скачивании: {e}")
    finally:
        driver.quit()  # Закрываем браузер

# Пример использования
search_and_download("психотерапия")
