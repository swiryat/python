from bs4 import BeautifulSoup
from datetime import datetime

# Читаем содержимое файла
with open("C:\\Users\\swer\\smp.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Инициализируем объект BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Находим таблицу с данными
table = soup.find("table", {"class": "table"})

# Если таблица найдена
if table:
    print("Таблица найдена!")

    # Получаем текущую дату
    current_date = datetime.now()

    # Открываем файл для записи результатов
    with open("output.txt", "w", encoding="utf-8") as output_file:
        # Итерируемся по строкам таблицы
        for row in table.find_all("tr")[1:]:  # Пропускаем заголовок
            # Получаем ячейки текущей строки
            cells = row.find_all("td")

            # Извлекаем данные из ячеек
            fio = cells[0].text.strip()
            position = cells[1].text.strip()
            education_level = cells[2].text.strip()
            issuing_organization = cells[3].text.strip()

            # Проверяем, есть ли значение года выдачи и является ли оно числом
            year_of_issue_text = cells[4].text.strip()
            year_of_issue = int(year_of_issue_text) if year_of_issue_text.isdigit() else None

            specialty = cells[5].text.strip()
            qualification = cells[6].text.strip()

            # Проверяем, есть ли значение срока действия сертификата
            expiration_date_text = cells[7].text.strip()
            expiration_date = datetime.strptime(expiration_date_text, "%d.%m.%Y") if expiration_date_text else None

            # Проверяем, истек ли срок действия сертификата
            if expiration_date and expiration_date < current_date:
                # Формируем строку с информацией о человеке
                output_string = (
                    f"ФИО: {fio}\n"
                    f"Должность: {position}\n"
                    f"Уровень образования: {education_level}\n"
                    f"Организация, выдавшая документ об образовании: {issuing_organization}\n"
                    f"Год выдачи: {year_of_issue}\n"
                    f"Специальность: {specialty}\n"
                    f"Квалификация: {qualification}\n"
                    f"Срок действия сертификата: {expiration_date.strftime('%d.%m.%Y')}\n"
                    f"{'=' * 50}\n"
                )

                # Выводим информацию о человеке на экран
                print(output_string)

                # Записываем информацию о человеке в файл
                output_file.write(output_string)
else:
    print("Таблица не найдена в файле.")
