import requests
from bs4 import BeautifulSoup

# URL веб-страницы
url = 'https://www.ozon.ru/category/chemodany-1657'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'

# Отправьте GET-запрос с пользовательским агентом
response = requests.get(url, headers={'User-Agent': user_agent})

# Проверьте успешность запроса
if response.status_code == 200:
    # Убедитесь, что кодировка правильно установлена
    response.encoding = 'utf-8'
    
 # Получаем куки из ответа
    cookies = response.cookies

    # Выводим куки
    for cookie in cookies:
        print(f'Имя куки: {cookie.name}')
        print(f'Значение куки: {cookie.value}')    

    # Сохраните содержимое страницы в переменной
    page_content = response.text

    # Создайте объект BeautifulSoup для парсинга
    soup = BeautifulSoup(page_content, 'html.parser')

    # Извлекайте данные, как вам нужно
    # Например, извлеките заголовок страницы:
    page_title = soup.title.string
    print("Заголовок страницы:", page_title)

    # Другие действия с данными...

    # Если хотите сохранить HTML-код страницы в файл
    with open('web_page.html', 'w', encoding='utf-8') as file:
        file.write(page_content)

    print("Веб-страница сохранена в файл 'web_page.html'")

else:
    print(f"Ошибка при загрузке страницы. Код статуса: {response.status_code}")


