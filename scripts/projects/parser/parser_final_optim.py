import os
import re
import sqlite3
import requests
import random
import time
import pdfkit
import queue
import threading
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Инициализация сессии
session = requests.Session()

# Ваши cookies, которые вы получили из браузера
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

# Базовый URL
BASE_URL = "https://javarush.com"
ARTICLES_URL = BASE_URL + "/all-articles"

# Директория сохранения
SAVE_DIR = "JavaRush_Articles"
os.makedirs(SAVE_DIR, exist_ok=True)

# Очередь SQL-запросов
db_queue = queue.Queue()

def get_headers():
    """ Возвращает случайный User-Agent """
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://javarush.com",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }

def db_worker():
    """ Фоновый поток для работы с SQLite """
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()

    # Создание таблицы, если она не существует
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            category TEXT,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    while True:
        query, params = db_queue.get()
        if query is None:  # Завершение потока
            break
        try:
            cursor.execute(query, params)
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # Игнорируем дубликаты
        except sqlite3.Error as e:
            print(f"❌ Ошибка БД: {e}")
        db_queue.task_done()

    conn.close()

# Запуск фонового потока
worker_thread = threading.Thread(target=db_worker, daemon=True)
worker_thread.start()

def get_article_links():
    """ Парсит ссылки на статьи """
    links = set()
    for page in range(1, 5):  # Ограничим до 5 страниц
        url = f"{ARTICLES_URL}?page={page}"
        print(f"🔍 Загружаем страницу {page}...")

        try:
            response = session.get(url, headers=get_headers(), timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Ошибка загрузки {url}: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        new_links = {BASE_URL + a["href"] for a in soup.find_all("a", href=True) if "/groups/posts/" in a["href"]}
        if not new_links:
            print(f"❌ Нет новых статей, остановка.")
            break

        links.update(new_links)
        time.sleep(random.uniform(1, 2))  # Пауза для избегания блокировки

    print(f"✅ Найдено {len(links)} статей.")
    return links

def save_article(article_url):
    """ Скачивает и сохраняет статью """
    try:
        response = session.get(article_url, headers=get_headers(), timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Ошибка при скачивании {article_url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "Без названия"
    filename_base = re.sub(r"[^\w\-_]", "_", title)

    # Определение категории
    category = "Разное"
    for cat in ["Java", "Python", "Алгоритмы"]:
        if cat.lower() in title.lower():
            category = cat
            break

    # Проверка на существование файла
    html_path = os.path.join(SAVE_DIR, f"{filename_base}.html")
    if os.path.exists(html_path):
        print(f"❌ Файл уже существует: {title}, пропускаем.")
        return  # Пропустить скачивание, если файл уже существует

    # Запрос в БД через очередь
    db_queue.put(("INSERT OR IGNORE INTO articles (title, url, category) VALUES (?, ?, ?)", 
                  (title, article_url, category)))

    # Сохранение в файл
    try:
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"✅ Сохранено: {title}")
    except IOError as e:
        print(f"❌ Ошибка записи файла {html_path}: {e}")

def main():
    print("🔍 Начинаем парсинг...")
    article_links = get_article_links()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(save_article, url) for url in article_links]
        for future in as_completed(futures):
            future.result()

    print("✅ Все статьи сохранены!")

if __name__ == "__main__":
    main()
