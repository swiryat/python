import os
import requests
import pdfkit
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from markdownify import markdownify as md

# Конфигурация pdfkit
pdfkit_config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

# Базовый URL
BASE_URL = "https://javarush.com"
ARTICLES_PAGE = "/all-articles"

# Создаём папки для сохранения
SAVE_DIR = "articles"
IMG_DIR = os.path.join(SAVE_DIR, "images")
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Файл с уже скачанными статьями
CSV_PATH = os.path.join(SAVE_DIR, "articles.csv")

# Загружаем список уже скачанных статей
if os.path.exists(CSV_PATH):
    old_articles = pd.read_csv(CSV_PATH)["Ссылка"].tolist()
else:
    old_articles = []

# Функция для загрузки всех страниц со статьями
def get_all_articles():
    articles = []
    page = 1

    while True:
        url = f"{BASE_URL}{ARTICLES_PAGE}?page={page}"
        print(f"Загружаем страницу {page}: {url}")

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            break  # Если страницы нет — заканчиваем

        soup = BeautifulSoup(response.text, "html.parser")
        article_links = soup.find_all("a", class_="all-articles__list-item-link")

        if not article_links:
            break  # Если нет новых ссылок — заканчиваем

        for a_tag in article_links:
            article_url = urljoin(BASE_URL, a_tag["href"])
            articles.append({"title": a_tag.text.strip(), "url": article_url})

        page += 1  # Переходим на следующую страницу

    return articles

# Получаем статьи
articles = get_all_articles()
new_articles = [a for a in articles if a["url"] not in old_articles]

if not new_articles:
    print("Нет новых статей для скачивания.")
else:
    print(f"Найдено {len(new_articles)} новых статей!")

    article_data = []

    for i, article in enumerate(new_articles):
        try:
            # Загружаем страницу статьи
            response = requests.get(article["url"], headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                print(f"Ошибка загрузки: {article['url']}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # Название статьи
            title_tag = soup.find("h1")
            title = title_tag.text.strip() if title_tag else f"Статья_{i+1}"
            safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)

            # Основное содержимое статьи
            article_body = soup.find("div", class_="article__content")
            article_html = str(article_body) if article_body else "Нет содержимого"
            article_markdown = md(article_html)  # Конвертируем в Markdown

            # Сохраняем HTML
            html_path = os.path.join(SAVE_DIR, f"{safe_title}.html")
            with open(html_path, "w", encoding="utf-8") as file:
                file.write(f"<h1>{title}</h1>\n{article_html}")

            # Конвертируем в PDF
            pdf_path = os.path.join(SAVE_DIR, f"{safe_title}.pdf")
            pdfkit.from_file(html_path, pdf_path, configuration=pdfkit_config)

            # Сохраняем Markdown
            md_path = os.path.join(SAVE_DIR, f"{safe_title}.md")
            with open(md_path, "w", encoding="utf-8") as file:
                file.write(f"# {title}\n\n{article_markdown}")

            # Скачиваем изображения
            img_tags = article_body.find_all("img") if article_body else []
            for img_tag in img_tags:
                img_url = urljoin(BASE_URL, img_tag["src"])
                img_name = os.path.basename(img_url)
                img_path = os.path.join(IMG_DIR, img_name)

                img_response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
                if img_response.status_code == 200:
                    with open(img_path, "wb") as img_file:
                        img_file.write(img_response.content)

            # Добавляем в CSV
            article_data.append({"Название": title, "Ссылка": article["url"], "HTML": html_path, "PDF": pdf_path, "Markdown": md_path})

            print(f"[{i+1}/{len(new_articles)}] Сохранено: {title}")

        except Exception as e:
            print(f"Ошибка при обработке {article['url']}: {e}")

    # Обновляем CSV
    df = pd.DataFrame(articles)  # Все статьи, включая старые
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")

    print(f"\nВсе статьи сохранены! Список в {CSV_PATH}")
