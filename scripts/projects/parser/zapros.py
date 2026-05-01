import requests
from bs4 import BeautifulSoup

# Инициализация сессии
session = requests.Session()

# Добавьте ваши cookies
session.cookies.set("jr-sidebar-mode", "FULL")
session.cookies.set("javarush.user.id", "3425706")
session.cookies.set("JSESSIONID", "48a37049-9d45-46f4-b708-1cac06bd96e8")
# Добавьте остальные cookies...

# Отправляем GET запрос
response = session.get("https://javarush.com/all-articles")

# Проверка полученных данных
if response.status_code == 200:
    print("Запрос успешен!")
    # Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Пример извлечения заголовков статей (предположим, что заголовки находятся в тегах h2)
    titles = soup.find_all('h2')  # Измените это в зависимости от структуры страницы
    for title in titles:
        print(title.text)
else:
    print(f"Ошибка: {response.status_code}")
