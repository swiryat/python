import requests

# URL для запроса
url = "https://oblsud--vrn.sudrf.ru/modules.php?name=sud_delo&srv_num=1&name_op=r&page=1&vnkod=36OS0000&srv_num=1&name_op=r&vnkod=36OS0000&delo_id=5&case_type=0&new=5&list=ON&Submit=%CD%E0%E9%F2%E8"

# Заголовки для имитации браузера
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36"
    )
}

# Запрос
response = requests.get(url, headers=HEADERS)

# Проверка статуса
if response.status_code == 200:
    print("Страница доступна!")
else:
    print(f"Ошибка доступа: {response.status_code}")
