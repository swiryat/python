import requests
import vlc
import pygame
from pygame.locals import *
import time

# Функция для получения погоды по выбранному городу
def get_weather(city):
    api_key = "360a18422b3aa6cb9e369d69794ef107"  # Замените YOUR_API_KEY на ваш собственный ключ API OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == "404":
        return "Город не найден"
    else:
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        return f"Температура: {temperature} K\nПогода: {weather_description}"

# Функция для проигрывания радио
def play_radio(url):
    instance = vlc.Instance("--no-xlib")
    player = instance.media_player_new()
    media = instance.media_new(url)
    player.set_media(media)
    player.play()

# Основная функция программы
def main():
    city = input("Введите город: ")
    print(get_weather(city))

    radio_station = input("Введите URL радио-станции: ")
    play_radio(radio_station)

    # Отображение часов
    pygame.init()
    screen = pygame.display.set_mode((400, 100))
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        current_time = pygame.time.get_ticks() // 1000
        time_text = font.render("Time: " + str(current_time), True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(time_text, (50, 25))
        pygame.display.flip()
        clock.tick(60)

    # Добавить задержку перед закрытием окна
    time.sleep(500)  # Пауза в 500 секунд

    pygame.quit()


if __name__ == "__main__":
    main()
