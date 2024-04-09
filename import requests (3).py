import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://vssmp.zdrav36.ru/medrabotniki"
response = requests.get(url, verify=False)
html = response.text

# Инициализируем объект BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Ищем заголовок таблицы
header_row = soup.find("thead").find("tr")

# Если заголовок таблицы найден
if header_row:
    # Инициализируем список для хранения имен столбцов
    column_names = [header.text.strip() for header in header_row.find_all(["th", "td"])]

    # Находим таблицу с данными
    table = soup.find("table", {"class": "table"})

    # Проверяем наличие таблицы
    if table:
        print("Таблица найдена!")
        # Получаем текущую дату
        current_date = datetime.now()

        # Итерируемся по строкам таблицы
        for row in table.find_all("tr")[1:]:  # Пропускаем заголовок
            # Получаем ячейки текущей строки
            cells = row.find_all("td")

            # Создаем словарь для хранения данных
            data = {}
            for i in range(len(column_names)):
                data[column_names[i]] = cells[i].text.strip()

            # Извлекаем данные из словаря
            fio = data.get("ФИО")
            position = data.get("Должность")
            education_level = data.get("Уровень образования")
            issuing_organization = data.get("Организация, выдавшая документ об образовании")
            year_of_issue = int(data.get("Год выдачи", 0))
            specialty = data.get("Специальность")
            qualification = data.get("Квалификация")
            expiration_date = datetime.strptime(data.get("Срок действия сертификата", ""), "%d.%m.%Y")

            # Проверяем, истек ли срок действия сертификата
            if expiration_date and expiration_date < current_date:
                # Выводим информацию о человеке
                print(f"FIO: {fio}")
                print(f"Position: {position}")
                print(f"Education Level: {education_level}")
                print(f"Issuing Organization: {issuing_organization}")
                print(f"Year of Issue: {year_of_issue}")
                print(f"Specialty: {specialty}")
                print(f"Qualification: {qualification}")
                print(f"Expiration Date: {expiration_date.strftime('%d.%m.%Y')}")
                print("=" * 50)
    else:
        print("Таблица не найдена на странице.")
else:
    print("Заголовок таблицы не найден на странице.")
