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




    # Список радиостанций (оставлен без изменений)
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

    # Выбор радиостанции (оставлен без изменений)
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

    # Проигрывание радиостанции (оставлен без изменений)
    play_radio(radio_station)

    # Отображение часов (оставлен без изменений)
    pygame.init()
    screen = pygame.display.set_mode((400, 100))
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        current_time = time.strftime("%H:%M:%S", time.localtime())
        text = font.render(current_time, True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(text, (150, 30))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Запуск программы
if __name__ == "__main__":
    main()
