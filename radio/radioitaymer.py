import time
import vlc  # Для радио
import os   # Для работы с системными вызовами

# Таймер в секундах
def countdown_timer(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')  # вывод в одну строку
        time.sleep(1)
        seconds -= 1
    print("Время вышло!")

# Воспроизведение локального файла музыки
def play_music(file_path):
    os.system(f"start {file_path}")  # для Windows, использовать os.system("open") для MacOS

# Проигрывание радио через VLC
def play_radio(stream_url):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(stream_url)
    player.set_media(media)
    player.play()

# Пример использования
if __name__ == "__main__":
    # Таймер на 10 секунд
    countdown_timer(10)

    # Воспроизведение музыки из локального файла (укажите правильный путь к файлу)
    music_file = "path_to_your_music_file.mp3"
    play_music(music_file)

    # Или проигрывание радио
    radio_url = "http://stream-url.com/example"
    play_radio(radio_url)
