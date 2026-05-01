from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import csv

# Путь к chromedriver
driver_path = r"C:\Users\swer\selenium\chromedriver-win64\chromedriver.exe"
chrome_path = r"C:\Users\swer\selenium\chrome-win64\chrome-win64\chrome.exe"

# Создание опций для Chrome
chrome_options = Options()
chrome_options.binary_location = chrome_path
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # Безголовый режим
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")

# Инициализация WebDriver
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Открытие страницы
driver.get("https://www.b17.ru")  # Открываем сайт
time.sleep(2)

# Сбор заголовков h1 и h2
headers_h1 = driver.find_elements("tag name", "h1")  # Заголовки h1
headers_h2 = driver.find_elements("tag name", "h2")  # Заголовки h2

# Сбор ссылок на странице
links = driver.find_elements("tag name", "a")  # Все ссылки

# Сбор текстовых блоков (например, параграфы)
paragraphs = driver.find_elements("tag name", "p")  # Параграфы

# Сбор изображений
images = driver.find_elements("tag name", "img")  # Изображения

# Сбор мета-тегов
meta_tags = driver.find_elements("tag name", "meta")  # Мета-теги

# Сбор JavaScript информации
script_tags = driver.find_elements("tag name", "script")  # Сценарии (JavaScript)

# Сбор дополнительных текстовых блоков (например, div, span)
additional_text = driver.find_elements("tag name", "div") + driver.find_elements("tag name", "span")

# Функция для записи данных в CSV файл
def save_to_csv(headers_h1, headers_h2, links, paragraphs, images, meta_tags, script_tags, additional_text, file_path):
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Записываем заголовки
        writer.writerow(["Заголовки H1"])
        for header in headers_h1:
            writer.writerow([header.text])
        
        writer.writerow(["Заголовки H2"])
        for header in headers_h2:
            writer.writerow([header.text])
        
        writer.writerow(["Ссылки"])
        for link in links:
            writer.writerow([link.get_attribute("href")])

        writer.writerow(["Параграфы"])
        for para in paragraphs:
            writer.writerow([para.text])

        writer.writerow(["Изображения"])
        for img in images:
            writer.writerow([img.get_attribute("src")])

        writer.writerow(["Мета-теги"])
        for meta in meta_tags:
            writer.writerow([meta.get_attribute("content")])

        writer.writerow(["JavaScript"])
        for script in script_tags:
            writer.writerow([script.get_attribute("src")])

        writer.writerow(["Дополнительные текстовые блоки"])
        for div in additional_text:
            writer.writerow([div.text])

# Функция для записи данных в JSON файл
def save_to_json(headers_h1, headers_h2, links, paragraphs, images, meta_tags, script_tags, additional_text, file_path):
    data = {
        "headers_h1": [header.text for header in headers_h1],
        "headers_h2": [header.text for header in headers_h2],
        "links": [link.get_attribute("href") for link in links],
        "paragraphs": [para.text for para in paragraphs],
        "images": [img.get_attribute("src") for img in images],
        "meta_tags": [meta.get_attribute("content") for meta in meta_tags],
        "script_tags": [script.get_attribute("src") for script in script_tags],
        "additional_text": [div.text for div in additional_text]
    }

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Путь для сохранения данных
csv_file_path = r"C:/Users/swer/GitHub/python/scraped_data.csv"
json_file_path = r"C:/Users/swer/GitHub/python/scraped_data.json"

# Сохранение данных в файлы с полным путём
save_to_csv(headers_h1, headers_h2, links, paragraphs, images, meta_tags, script_tags, additional_text, csv_file_path)
save_to_json(headers_h1, headers_h2, links, paragraphs, images, meta_tags, script_tags, additional_text, json_file_path)

# Завершаем сессию
driver.quit()

print("Данные успешно собраны и сохранены в файлы.")
