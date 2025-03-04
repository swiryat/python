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
from urllib.parse import urlparse, quote_plus  # Для обработки URL
from pathlib import Path  # Для работы с путями

# Список прокси для ротации
proxies = [
    "http://218.61.76.182:9090",  # Пример прокси
    "http://51.79.248.208:46923",  # Пример прокси
    "http://51.75.126.150:13960"   # Пример прокси
]

# Список User-Agent'ов для случайной смены
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko"
]

# Путь к chromedriver
driver_path = r"C:\\Users\\swer\\selenium\\chromedriver-win64\\chromedriver.exe"
# Путь к установленному браузеру Chrome
chrome_path = r"C:\\Users\\swer\\selenium\\chrome-win64\\chrome-win64\\chrome.exe"

# Создание настроек для Chrome
chrome_options = Options()
chrome_options.binary_location = chrome_path
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")

# Ротация прокси и User-Agent'ов
chrome_options.add_argument(f'--proxy-server={random.choice(proxies)}')
chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')

# Инициализация WebDriver
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Создание папки для загрузки файлов
os.makedirs("./downloads", exist_ok=True)

def search_and_download(query):
    """
    Функция для поиска в Google, перехода по ссылкам и скачивания файлов.
    """
    try:
        # Кодирование запроса для URL
        encoded_query = quote_plus(query)
        driver.get(f"https://www.google.com/search?q={encoded_query}")
        time.sleep(random.uniform(2, 5))

        page_counter = 0
        max_pages = 5  # Ограничение на количество страниц

        while page_counter < max_pages:
            # Извлечение всех ссылок с результатов поиска
            links = driver.find_elements(By.CSS_SELECTOR, "a")
            urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]

            for url in urls:
                print(f"Обрабатываем ссылку: {url}")
                try:
                    # Переход по ссылке
                    driver.get(url)
                    time.sleep(random.uniform(2, 5))

                    # Скачивание файлов (например, PDF)
                    if url.endswith(".pdf"):
                        response = requests.get(url)
                        filename = Path(urlparse(url).path).name
                        with open(f"./downloads/{filename}", "wb") as file:
                            file.write(response.content)
                            print(f"Сохранён файл: {filename}")
                except Exception as e:
                    print(f"Ошибка при обработке URL {url}: {e}")

            # Переход на следующую страницу
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "pnnext"))
                )
                next_button.click()
                page_counter += 1
                time.sleep(random.uniform(2, 5))
            except Exception as e:
                print("Ошибка при попытке перейти на следующую страницу:", e)
                break

    except Exception as e:
        print(f"Общая ошибка: {e}")
    finally:
        driver.quit()

# Запуск функции
search_and_download("научная статья по python")
