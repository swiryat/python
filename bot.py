import datetime
import requests

class Friend:
    def __init__(self, name, city):
        self.name = name
        self.city = city

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        params = {"q": city, "appid": self.api_key}
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            weather_data = response.json()
            weather_description = weather_data.get("weather")[0].get("description")
            return weather_description
        else:
            return "Не удалось получить данные о погоде"

class FriendManager:
    def __init__(self):
        self.friends = []

    def add_friend(self, friend):
        self.friends.append(friend)

    def get_time_and_weather(self, friend_name, weather_service):
        friend = next((f for f in self.friends if f.name == friend_name), None)
        if friend:
            current_time = datetime.datetime.now()
            friend_weather = weather_service.get_weather(friend.city)
            return f"Для {friend.name}: время - {current_time}, погода - {friend_weather}"
        else:
            return "Друг не найден"

def main():
    api_key = "YOUR_API_KEY"  # Замените на свой ключ API
    weather_service = WeatherService(api_key)
    friend_manager = FriendManager()

    while True:
        print("1. Добавить друга")
        print("2. Узнать время и погоду для друга")
        print("3. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Введите имя друга: ")
            city = input("Введите город друга: ")
            friend = Friend(name, city)
            friend_manager.add_friend(friend)
            print(f"Друг {name} добавлен.")
        elif choice == "2":
            friend_name = input("Введите имя друга: ")
            result = friend_manager.get_time_and_weather(friend_name, weather_service)
            print(result)
        elif choice == "3":
            break
        else:
            print("Некорректный выбор.")

if __name__ == "__main__":
    main()
