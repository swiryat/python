import pyaudio
import numpy as np
import noisereduce as nr

# Настройки аудиопотока
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024  # Количество сэмплов в одном фрейме

# Инициализация PyAudio
audio = pyaudio.PyAudio()

# Функция для записи фона (используется для определения шума)
def record_background_noise(seconds=3):
    print("Запись фонового шума...")
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)
    frames = []

    for _ in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(np.frombuffer(data, dtype=np.int16))

    stream.stop_stream()
    stream.close()
    print("Фоновый шум записан.")
    return np.hstack(frames)

# Функция для запуска аудио с фильтрацией шума
def start_streaming(noise_sample):
    print("Начало трансляции...")
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, output=True, frames_per_buffer=CHUNK)

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Фильтрация шума
            reduced_noise = nr.reduce_noise(
                y=audio_data, 
                sr=RATE, 
                y_noise=noise_sample, 
                prop_decrease=0.9
            )

            # Преобразование и воспроизведение
            output_data = reduced_noise.astype(np.int16).tobytes()
            stream.write(output_data)
    except KeyboardInterrupt:
        print("\nОстановка трансляции...")
    finally:
        stream.stop_stream()
        stream.close()

# Основной блок программы
if __name__ == "__main__":
    # Запись фонового шума
    noise_sample = record_background_noise()
    
    # Запуск аудиопотока с фильтрацией
    start_streaming(noise_sample)

    # Завершение PyAudio
    audio.terminate()
