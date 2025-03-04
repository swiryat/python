import sounddevice as sd
import numpy as np
import time
import noisereduce as nr
import scipy.io.wavfile as wav

# Параметры записи
sampling_rate = 44100  # частота дискретизации
duration = 3  # продолжительность записи фонового шума в секундах
num_update_cycles = 5  # количество циклов обновления фонового шума

# Функция записи шума
def record_noise(duration, sampling_rate):
    print("Запись фонового шума...")
    noise = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=1, dtype='float32')
    sd.wait()
    print("Фоновый шум записан.")
    return noise.flatten()

# Функция для применения фильтрации шума
def reduce_noise(noise, audio, sampling_rate):
    print("Применение шумоподавления...")
    reduced_audio = nr.reduce_noise(y=audio, sr=sampling_rate, stationary=True, time_mask_smooth_ms=200, prop_decrease=1.0)
    print("Шум подавлен.")
    return reduced_audio

# Функция для сохранения файла
def save_filtered_audio(audio, filename):
    wav.write(filename, sampling_rate, audio)
    print(f"Файл сохранён как {filename}")

# Запись фонового шума
background_noise = record_noise(duration, sampling_rate)

# Основной процесс
audio_stream = np.zeros(0)  # инициализация пустого массива для потока аудио
for cycle in range(num_update_cycles):
    print(f"Начало трансляции с динамическим обновлением шума... Цикл {cycle + 1} из {num_update_cycles}")
    
    # Обновление образца шума
    noise_sample = record_noise(duration, sampling_rate)
    audio_stream = np.concatenate((audio_stream, noise_sample))
    
    # Применение фильтрации
    reduced_audio = reduce_noise(background_noise, audio_stream, sampling_rate)
    
    # Пауза перед обновлением
    time.sleep(1)

# Сохранение результата
save_filtered_audio(reduced_audio, "filtered_output.wav")
