import requests

# Функция для получения данных о погоде
def get_weather_data(url):
    response = requests.get(url)
    data = response.json()
    return data

# Функция для получения погоды по API ссылке для каждого города
def get_weather(api_url, city):
    # Получение данных о погоде
    weather_data = get_weather_data(api_url.format(city))

    if weather_data["cod"] != "404":
        # Извлечение нужных данных о погоде
        main_data = weather_data["main"]
        current_temperature = main_data["temp"]
        current_pressure = main_data["pressure"]
        current_humidity = main_data["humidity"]
        weather_description = weather_data["weather"][0]["description"]

        # Возвращение данных о погоде
        return {
            "City": city,
            "Temperature (in Kelvin)": current_temperature,
            "Atmospheric Pressure (in hPa)": current_pressure,
            "Humidity (in percentage)": current_humidity,
            "Description": weather_description
        }
    else:
        return {"City": city, "Error": "City Not Found"}

# Основная функция программы
def main():
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=360a18422b3aa6cb9e369d69794ef107"

    cities = ["Moscow", "Voronezh", "Perm", "Saint Petersburg"]

    # Получение погоды для каждого города
    for city in cities:
        # Получение данных о погоде
        weather_data = get_weather(api_url, city)

        # Вывод данных о погоде
        print("Weather for", city)
        if "Error" in weather_data:
            print(weather_data["Error"])
        else:
            for key, value in weather_data.items():
                print(key + ":", value)
        print()

# Запуск программы
if __name__ == "__main__":
    main()
