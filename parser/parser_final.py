import os
import requests
import sqlite3
import pdfkit
import markdown
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urljoin

# Загрузка логина и пароля из .env
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Настройки путей
BASE_URL = "https://javarush.com"
LOGIN_URL = BASE_URL + "/user/login"
ARTICLES_URL = BASE_URL + "/all-articles"
SAVE_DIR = "JavaRush_Articles"
IMG_DIR = os.path.join(SAVE_DIR, "images")
DB_FILE = "articles.db"

# Создаём папки
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Подключение к БД
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT UNIQUE,
    category TEXT,
    saved_html TEXT,
    saved_markdown TEXT,
    saved_pdf TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Сессия для авторизации
session = requests.Session()

def get_csrf_token():
    """ Получаем CSRF-токен для авторизации (если требуется) """
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    token = soup.find("input", {"name": "_csrf"})
    return token["value"] if token else None

def login():
    """ Авторизация на сайте JavaRush """
    print("🔐 Авторизация на сайте...")

    csrf_token = get_csrf_token()
    login_payload = {
        "username": "zatura55@mail.ru",
        "password": "Masa34!masa35!"
    }
    
    if csrf_token:
        login_payload["_csrf"] = csrf_token

    response = session.post(LOGIN_URL, data=login_payload)

    if response.status_code == 200 and "logout" in response.text:
        print("✅ Успешный вход!")
    else:
        print("❌ Ошибка авторизации! Проверьте логин и пароль.")
        exit()

def get_articles():
    """ Получаем список статей """
    print("🔎 Загружаем список статей...")
    response = session.get(ARTICLES_URL)

    if response.status_code != 200:
        print(f"Ошибка {response.status_code} при загрузке {ARTICLES_URL}")
        exit()

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "/groups/posts/" in href:
            full_url = urljoin(BASE_URL, href)
            articles.append(full_url)

    print(f"📄 Найдено {len(articles)} статей.")
    return articles

def save_article(article_url, index, total):
    """ Парсим и сохраняем статью в HTML, Markdown и PDF """
    print(f"[{index}/{total}] 📥 Загружаем: {article_url}")

    cursor.execute("SELECT saved_html FROM articles WHERE url = ?", (article_url,))
    if cursor.fetchone():
        print("⏭️ Статья уже скачана, пропускаем.")
        return

    response = session.get(article_url)
    if response.status_code != 200:
        print(f"❌ Ошибка {response.status_code}, пропускаем...")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else f"article_{index}"
    
    category_tag = soup.find("span", class_="category")
    category = category_tag.text.strip() if category_tag else "Без категории"

    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)

    # Пути сохранения
    html_path = os.path.join(SAVE_DIR, safe_title + ".html")
    md_path = os.path.join(SAVE_DIR, safe_title + ".md")
    pdf_path = os.path.join(SAVE_DIR, safe_title + ".pdf")

    # Сохраняем HTML
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(response.text)

    # Конвертация в Markdown
    content_div = soup.find("div", class_="content")
    article_text = content_div.get_text("\n") if content_div else ""
    md_content = f"# {title}\n\n{article_text}"

    with open(md_path, "w", encoding="utf-8") as file:
        file.write(md_content)

    # Конвертация в PDF
    pdfkit.from_file(html_path, pdf_path)

    # Сохранение в БД
    cursor.execute("INSERT INTO articles (title, url, category, saved_html, saved_markdown, saved_pdf) VALUES (?, ?, ?, ?, ?, ?)",
                   (title, article_url, category, html_path, md_path, pdf_path))
    conn.commit()

    print(f"✅ Сохранено: {html_path}, {md_path}, {pdf_path}")

    # Скачивание изображений
    for img_tag in soup.find_all("img", src=True):
        img_url = urljoin(BASE_URL, img_tag["src"])
        img_name = os.path.basename(img_url)
        img_path = os.path.join(IMG_DIR, img_name)

        img_response = session.get(img_url, stream=True)
        if img_response.status_code == 200:
            with open(img_path, "wb") as img_file:
                for chunk in img_response.iter_content(1024):
                    img_file.write(chunk)
            print(f"🖼️ Изображение сохранено: {img_path}")

    sleep(1)  # Задержка для обхода блокировок

def main():
    login()
    articles = get_articles()
    for i, article_url in enumerate(articles, 1):
        save_article(article_url, i, len(articles))
    print("🎉 Все статьи загружены!")

    # Закрываем соединение с БД
    conn.close()

if __name__ == "__main__":
    main()
