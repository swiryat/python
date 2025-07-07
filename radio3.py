import requests
import vlc
import pygame
from pygame.locals import *
import time

# import required modules
import requests, json
 
# Enter your API key here
api_key = "360a18422b3aa6cb9e369d69794ef107"
 
# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
# Give city name
city_name = input("Enter city name : ")
 
# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
 
# get method of requests module
# return response object
response = requests.get(complete_url)
 
# json method of response object
# convert json format data into
# python format data
x = response.json()
 
# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if x["cod"] != "404":
 
    # store the value of "main"
    # key in variable y
    y = x["main"]
 
    # store the value corresponding
    # to the "temp" key of y
    current_temperature = y["temp"]
 
    # store the value corresponding
    # to the "pressure" key of y
    current_pressure = y["pressure"]
 
    # store the value corresponding
    # to the "humidity" key of y
    current_humidity = y["humidity"]
 
    # store the value of "weather"
    # key in variable z
    z = x["weather"]
 
    # store the value corresponding
    # to the "description" key at
    # the 0th index of z
    weather_description = z[0]["description"]
 
    # print following values
    print(" Temperature (in kelvin unit) = " +
                    str(current_temperature) +
          "\n atmospheric pressure (in hPa unit) = " +
                    str(current_pressure) +
          "\n humidity (in percentage) = " +
                    str(current_humidity) +
          "\n description = " +
                    str(weather_description))
 
else:
    print(" City Not Found ")

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

    # Список радиостанций
    radio_stations = {
        "Like FM": "https://pub0301.101.ru:8443/stream/air/mp3/256/219",
        "Маятник Фуко": "https://air.radiorecord.ru:805/mf_320",
        "Relax FM": "https://pub0301.101.ru:8443/stream/air/mp3/256/200",
        "Love Radio": "http://stream.loveradio.ru/12_love_28?type=.aac&U..",
        "DFM Rap": "https://dfm-nrp.hostingradio.ru/nrp96.aacp",
        "PHONK FM": "http://radio.real-drift.ru:8000/phonk.ogg",
        "Радио Цой": "https://pub0302.101.ru:8443/stream/pro/aac/64/103",
        "Новая Волна": "https://s01.radio-tochka.com:4840/radio",
        "Европа Плюс": "https://europaplus.hostingradio.ru:8014/europaplus320..",
        "Радио Energy": "https://pub0301.101.ru:8443/stream/air/mp3/256/99",
        "Ретро ФМ": "https://retro.hostingradio.ru:8014/retro320.mp3",
        "Радио Ваня": "https://radiokrug.ru/radio/vanya/icecast.audio",
        "Радио Шансон": "https://chanson.hostingradio.ru:8041/chanson256.mp3",
        "Наше Радио": "https://nashe1.hostingradio.ru/nashe-256",
        "Дорожное Радио": "https://dorognoe.hostingradio.ru/radio",
        "Новое Радио": "https://icecast-newradio.cdnvideo.ru/newradio3",
        "Милицейская Волна": "https://radiomv.hostingradio.ru:80/radiomv256.mp3",
        "Авторадио": "https://pub0301.101.ru:8443/stream/air/mp3/256/100",
        "Рекорд (Основа)": "https://air.radiorecord.ru:805/rr_320",
        "Русское Радио": "https://rusradio.hostingradio.ru/rusradio96.aacp",
        "Rock Radio": "https://air.radiorecord.ru:805/rock_320",
        "DFM": "https://dfm.hostingradio.ru/dfm96.aacp",
        "Mаруся FM": "https://radio-holding.ru:9433/marusya_default",
        "Comedy Radio": "https://ic7.101.ru:8000/s60",
        "Юмор ФМ": "https://pub0301.101.ru:8443/stream/air/mp3/256/102",
        "Inter FM Pop": "https://inter-fm.com/stream",
        "Дальнобой FM": "https://radiokrug.ru/radio/dalnoboifm/icecast.audio"
    }

    # Вывод списка радиостанций
    print("Список радиостанций:")
    for index, station in enumerate(radio_stations, start=1):
        print(f"{index}. {station}")

    # Выбор радиостанции
    while True:
        selection = input("Введите номер радиостанции (или 'q' для выхода): ")
        if selection == "q":
            pygame.quit()
            return
        elif selection.isdigit():
            index = int(selection)
            if 1 <= index <= len(radio_stations):
                radio_station = list(radio_stations.values())[index - 1]
                break
            else:
                print("Неверный номер. Попробуйте еще раз.")
        else:
            print("Неверный ввод. Попробуйте еще раз.")

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

    # Добавить задержку до нажатия клавиши
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN:
                pygame.quit()
                return

        pygame.time.wait(100)  # Пауза в 100 миллисекунд


if __name__ == "__main__":
    main()
