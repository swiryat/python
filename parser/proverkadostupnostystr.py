import requests
import os

base_url = "https://javarush.ru/articles/page/"
save_path = "downloaded_pages"

# Создаем папку, если ее нет
os.makedirs(save_path, exist_ok=True)

for page in range(341, 472):  # Загружаем страницы с 341 по 471
    url = f"{base_url}{page}"
    response = requests.get(url)
    
    if response.status_code == 200:
        filename = os.path.join(save_path, f"page_{page}.html")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Сохранено: {filename}")
    else:
        print(f"Ошибка {response.status_code}: страница {page} не найдена")
