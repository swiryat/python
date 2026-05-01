import PyPDF2
import re
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    # Открываем PDF-файл в бинарном режиме
    with open(pdf_path, "rb") as file:
        # Создаем объект PdfReader
        pdf_reader = PyPDF2.PdfReader(file)

        # Получаем текущую дату
        current_date = datetime.now()

        # Итерируемся по страницам и извлекаем текст
        for page_num in range(len(pdf_reader.pages)):
            # Получаем объект страницы
            page = pdf_reader.pages[page_num]

            # Извлекаем текст из страницы
            text = page.extract_text()

            # Разделяем текст на строки
            lines = text.split('\n')

            # Итерируемся по строкам и анализируем каждую запись
            for line in lines:
                # Используем регулярные выражения для поиска ФИО и даты в строке
                name_match = re.search(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+', line)
                date_match = re.search(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', line)
                
                # Если найдены и ФИО, и дата, обрабатываем строку
                if name_match and date_match:
                    # Используем попытку-исключение для обработки ошибок формата даты
                    try:
                        # Извлекаем дату из строки
                        expiration_date = datetime.strptime(date_match.group(), "%d.%m.%Y")

                        # Если срок действия сертификата истекает до текущей даты, выводим информацию
                        if expiration_date < current_date:
                            print(line)
                    except ValueError:
                        # Пропускаем строки, которые не соответствуют формату даты
                        pass

# Путь к PDF-файлу
pdf_path = "C:\\Users\\swer\\DRF.pdf"

# Извлекаем и выводим информацию из PDF
extract_text_from_pdf(pdf_path)
