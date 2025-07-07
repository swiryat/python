import requests
import pygame
from pygame.locals import *
import time
import json
import vlc

def get_weather_data(api_key, location):
    url = f"https://api.tomorrow.io/v4/timelines?location={location}&fields=temperature&timesteps=1h&units=metric&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    temperature = data['data']['timelines'][0]['intervals'][0]['values']['temperature']
    return temperature

def play_radio(radio_station_url):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(radio_station_url)
    player.set_media(media)
    player.play()

def main():
    api_key = "6LVfe8KUGC8koNWMDPY1FD6MkKnPYsZ4"
    location = "40.75872069597532,-73.98529171943665"  # Пример координат для Нью-Йорка

    weather_data = get_weather_data(api_key, location)

    # Вывод данных о погоде
    print(json.dumps(weather_data, indent=4))

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

    pygame.init()
    clock = pygame.time.Clock()

    selected_station = None

    screen = pygame.display.set_mode((400, 100))
    font = pygame.font.SysFont(None, 48)

    # Вывод списка радиостанций
    print("Список радиостанций:")
    for index, station in enumerate(radio_stations, start=1):
        print(f"{index}. {station}")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        if selected_station is None:
            # Выбор радиостанции
            selection = input("Введите номер радиостанции (или 'q' для выхода): ")
            if selection == "q":
                pygame.quit()
                return

            if selection.isdigit():
                index = int(selection)
                if 1 <= index <= len(radio_stations):
                    selected_station = list(radio_stations.values())[index - 1]
                    play_radio(selected_station)
                else:
                    print("Неверный номер. Попробуйте еще раз.")
            else:
                print("Неверный ввод. Попробуйте еще раз.")

        # Обновление экрана
        screen.fill((0, 0, 0))
        current_time = time.strftime("%H:%M:%S", time.localtime())
        text = font.render(current_time, True, (255, 255, 255))
        screen.blit(text, (150, 30))
        pygame.display.flip()
        clock.tick(1)  # Ограничиваем обновление экрана 1 раз в секунду

# Запуск программы
if __name__ == "__main__":
    main()
