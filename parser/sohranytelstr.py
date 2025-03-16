import os
import re
import sqlite3
import requests
import pdfkit
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from markdown import markdown

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

# Создание таблицы, если её нет
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

# Функция получения списка ссылок на статьи
def get_article_links():
    links = set()
    page = 1
    while True:
        url = f"{ARTICLES_URL}?page={page}"
        print(f"Загружаем страницу {page}...")

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print("Ошибка при загрузке страницы, завершаем парсинг.")
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
        sleep(1)

    print(f"Найдено {len(links)} статей.")
    return links

# Функция загрузки и сохранения статьи
def save_article(article_url):
    response = requests.get(article_url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print(f"Ошибка {response.status_code}, пропускаем...")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Получаем заголовок статьи
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "Без названия"
    filename_base = re.sub(r"[^\w\-_]", "_", title)

    # Определение категории
    category = "Разное"
    for cat in ["Java", "Python", "Алгоритмы"]:
        if cat.lower() in title.lower():
            category = cat
            break

    # Сохранение в БД (проверяем, есть ли уже такая статья)
    cursor.execute("SELECT id FROM articles WHERE url=?", (article_url,))
    if cursor.fetchone():
        print(f"Статья '{title}' уже сохранена, пропускаем.")
        return None

    cursor.execute("INSERT INTO articles (title, url, category, saved_at) VALUES (?, ?, ?, datetime('now'))",
                   (title, article_url, category))
    conn.commit()

    # Сохраняем HTML
    html_path = os.path.join(SAVE_DIR, f"{filename_base}.html")
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(response.text)

    # Преобразуем в Markdown
    md_content = f"# {title}\n\n{article_url}\n\n" + soup.find("article").text
    md_path = os.path.join(SAVE_DIR, f"{filename_base}.md")
    with open(md_path, "w", encoding="utf-8") as file:
        file.write(md_content)

    # Преобразуем в PDF
    pdf_path = os.path.join(SAVE_DIR, f"{filename_base}.pdf")
    pdfkit.from_string(markdown(md_content), pdf_path)

    # Скачиваем изображения
    img_tags = soup.find_all("img")
    for img in img_tags:
        img_url = img.get("src")
        if img_url and img_url.startswith("http"):
            img_name = os.path.basename(img_url).split("?")[0]
            img_path = os.path.join(IMG_DIR, img_name)
            img_data = requests.get(img_url).content
            with open(img_path, "wb") as img_file:
                img_file.write(img_data)

    print(f"Сохранено: {title} (HTML, MD, PDF)")

# Основной процесс парсинга
def main():
    print("🔍 Начинаем парсинг статей JavaRush...")
    
    # Получаем ссылки
    article_links = get_article_links()
    
    # Загружаем статьи
    for i, url in enumerate(article_links, 1):
        print(f"[{i}/{len(article_links)}] Обрабатываем: {url}")
        save_article(url)
        sleep(1)

    # Экспортируем список в CSV
    csv_path = os.path.join(SAVE_DIR, "articles.csv")
    df = pd.read_sql_query("SELECT title, url, category, saved_at FROM articles", conn)
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"📄 CSV-файл создан: {csv_path}")

    print("✅ Все статьи успешно сохранены!")

if __name__ == "__main__":
    main()
