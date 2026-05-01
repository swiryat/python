import requests

# Шаг 1: Указываем URL и параметры
url = 'https://api.weatherapi.com/v1/current.json'
params = {
    'key': 'ВАШ_API_КЛЮЧ',
    'q': 'Moscow'
}

# Шаг 2: Отправляем GET-запрос
response = requests.get(url, params=params)

# Шаг 3: Обрабатываем результат
if response.status_code == 200:
    data = response.json()
    print(f"Температура: {data['current']['temp_c']}°C")
else:
    print("Ошибка запроса:", response.status_code)
