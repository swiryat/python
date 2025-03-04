def parse_all_pages(start_url, max_pages=100, delay=2):
    all_data = []
    session = requests.Session()
    current_url = start_url
    page = 1

    while current_url and page <= max_pages:
        print(f"Парсинг страницы {page}: {current_url}")
        page_data, next_url = parse_page(current_url, session)
        if not page_data:  # Если данных нет, прекращаем
            print("Нет данных на странице или произошла ошибка!")
            break
        all_data.extend(page_data)
        current_url = next_url  # Переход на следующую страницу
        page += 1
        time.sleep(delay)  # Задержка для избежания блокировки

    return all_data
