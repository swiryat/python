import os
import re
import sqlite3
import requests
import random
import pdfkit
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

# Инициализация сессии
session = requests.Session()

# Добавьте ваши cookies, которые вы получили из браузера
session.cookies.set("jr-sidebar-mode", "FULL")
session.cookies.set("javarush.user.id", "3425706")
session.cookies.set("JSESSIONID", "48a37049-9d45-46f4-b708-1cac06bd96e8")
session.cookies.set("intercom-session-mqlef7yz", "")
session.cookies.set("intercom-device-id-mqlef7yz", "e30412d1-7c2f-4c73-86be-930bfa384cb5")
session.cookies.set("__stripe_mid", "d92df48d-b7c8-45f7-a6a6-e7da35f218ce1dfa20")
session.cookies.set("CookieConsent", "{stamp:'-1',necessary:true,preferences:true,statistics:true,marketing:true,method:'implied',ver:1,utc:1741007185215,region:'GB'}")
session.cookies.set("jr-featured-content-14", "closed")
session.cookies.set("javarush.daynight", "light")
session.cookies.set("_gcl_au", "1.1.84417750.1741713789")
session.cookies.set("_ga", "GA1.1.346389540.1741713790")
session.cookies.set("_ga_G0F5YPM3KY", "deleted")
session.cookies.set("jr-sidebar-group-university-collapsed", "0")
session.cookies.set("jr-install-mark", "NOT_NOW")
session.cookies.set("jr-last-route", "%2Fall-articles")
session.cookies.set("_ga_G0F5YPM3KY", "GS1.1.1741823636.7.1.1741823935.60.1.1267399023")

# Список User-Agent для рандомизации
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/537.36"
]

# Функция для получения случайного User-Agent
def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://javarush.com",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }

# Базовый URL
BASE_URL = "https://javarush.com"
ARTICLES_URL = BASE_URL + "/all-articles"

# Директории
SAVE_DIR = "JavaRush_Articles"
IMG_DIR = os.path.join(SAVE_DIR, "images")
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Подключение к базе SQLite
DB_PATH = os.path.join(SAVE_DIR, "articles.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT UNIQUE,
    category TEXT,
    saved_at TEXT
)
""")
conn.commit()

# Функция получения списка ссылок
def get_article_links():
    links = set()
    page = 1
    while True:
        url = f"{ARTICLES_URL}?page={page}"
        print(f"Загружаем страницу {page}...")

        response = session.get(url, headers=get_headers())  # Используем случайный заголовок
        if response.status_code != 200:
            print(f"Ошибка {response.status_code}, завершаем.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        new_links = {
            BASE_URL + a["href"]
            for a in soup.find_all("a", href=True)
            if "/groups/posts/" in a["href"]
        }

        if not new_links:
            break

        links.update(new_links)
        page += 1
        sleep(random.uniform(0.5, 1.5))  # Рандомная задержка

    print(f"🔗 Найдено {len(links)} статей.")
    return links

# Функция загрузки и сохранения статьи (многопоточно)
def save_article(article_url):
    response = session.get(article_url, headers=get_headers())  # Используем случайный заголовок
    if response.status_code != 200:
        print(f"Ошибка {response.status_code}, пропускаем {article_url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Заголовок
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "Без названия"
    filename_base = re.sub(r"[^\w\-_]", "_", title)

    # Категория
    category = "Разное"
    for cat in ["Java", "Python", "Алгоритмы"]:
        if cat.lower() in title.lower():
            category = cat
            break

    # Проверка в БД
    cursor.execute("SELECT id FROM articles WHERE url=?", (article_url,))
    if cursor.fetchone():
        print(f"Статья '{title}' уже есть, пропускаем.")
        return None

    # Сохранение в БД
    cursor.execute("INSERT INTO articles (title, url, category, saved_at) VALUES (?, ?, ?, datetime('now'))",
                   (title, article_url, category))
    conn.commit()

    # Сохраняем HTML
    html_path = os.path.join(SAVE_DIR, f"{filename_base}.html")
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(response.text)

    print(f"✅ Сохранено: {title} (HTML)")

# Основной процесс парсинга (с многопоточностью)
def main():
    print("🔍 Начинаем парсинг статей JavaRush...")

    # Получаем ссылки
    article_links = get_article_links()

    # Количество потоков
    MAX_THREADS = 50

    # Запускаем многопоточный парсинг
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_url = {executor.submit(save_article, url): url for url in article_links}

        for future in as_completed(future_to_url):
            try:
                future.result()  # Ожидание выполнения потока
            except Exception as e:
                print(f"Ошибка при обработке: {e}")

    print("✅ Все статьи сохранены!")

if __name__ == "__main__":
    main()
