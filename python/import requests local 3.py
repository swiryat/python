from bs4 import BeautifulSoup
from datetime import datetime

# Функция для обработки HTML-контента и подсчета специальностей
def process_html(html_content):
    # Инициализируем объект BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Находим все таблицы в документе
    tables = soup.find_all("table")

    # Итерируемся по всем таблицам
    for table in tables:
        # Получаем строки текущей таблицы
        rows = table.find_all("tr")

        # Пропускаем таблицы без строк
        if not rows:
            continue

        # Проверяем, что в первой строке есть хотя бы одна ячейка
        if rows[0].find_all("td") or rows[0].find_all("th"):
            # Обрабатываем таблицу
            print("Таблица найдена!")

            # Получаем текущую дату
            current_date = datetime.now()

            # Открываем файл для записи результатов
            with open("output.txt", "w", encoding="utf-8") as output_file:
                # Инициализируем счетчики специальностей и должностей
                specialty_counts = {"Врач": 0, "Фельдшер": 0, "Фельдшер скорой медицинской помощи": 0, "Медицинская сестра": 0}
                position_counts = {"медицинская сестра": 0, "врач-психиатр": 0, "акушерка": 0}

                # Итерируемся по строкам таблицы
                for row in rows[1:]:  # Пропускаем заголовок
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

                        # Обновляем счетчик специальности
                        key_specialty = specialty.strip()  # Убираем лишние пробелы
                        if key_specialty in specialty_counts:
                            specialty_counts[key_specialty] += 1
                        else:
                            print(f"Ошибка: Не удалось обработать специальность '{key_specialty}'")

                        # Обновляем счетчик должности
                        key_position = position.lower().strip()  # Приводим к нижнему регистру и убираем пробелы
                        if key_position in position_counts:
                            position_counts[key_position] += 1
                        else:
                            print(f"Ошибка: Не удалось обработать должность '{key_position}'")

            # Выводим количество по каждой специальности
            for specialty, count in specialty_counts.items():
                print(f"Специальность: {specialty} - Количество: {count}")

            # Выводим количество по каждой должности
            for position, count in position_counts.items():
                print(f"Должность: {position} - Количество: {count}")

            break  # Прерываем цикл после обработки первой найденной таблицы
    else:
        print("Таблица не найдена в файле.")

# Читаем содержимое файла
with open("DRF.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Вызываем функцию для обработки HTML-контента и подсчета специальностей
process_html(html_content)
