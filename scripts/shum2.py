import pyaudio
import numpy as np
import noisereduce as nr
import time

# Параметры аудио
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
SAMPLE_SIZE = 2  # Размер сэмпла (16 бит = 2 байта)
FILENAME = 'filtered_output.wav'

# Проверка доступности микрофона и аудиовыхода
def check_audio_devices():
    pyaudio_instance = pyaudio.PyAudio()
    num_devices = pyaudio_instance.get_device_count()
    
    input_device_found = False
    output_device_found = False
    
    for i in range(num_devices):
        device_info = pyaudio_instance.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            input_device_found = True
        if device_info['maxOutputChannels'] > 0:
            output_device_found = True
    
    pyaudio_instance.terminate()
    
    if not input_device_found:
        print("Ошибка: Не найдено входное аудиоустройство.")
    if not output_device_found:
        print("Ошибка: Не найдено выходное аудиоустройство.")
    
    return input_device_found, output_device_found

# Запись фонового шума
def record_background_noise(seconds=3):
    print(f"Запись фонового шума в течение {seconds} секунд...")
    pyaudio_instance = pyaudio.PyAudio()
    stream = pyaudio_instance.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    noise_frames = []

    for _ in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        noise_frames.append(data)
    
    stream.stop_stream()
    stream.close()
    pyaudio_instance.terminate()

    noise_audio = b''.join(noise_frames)
    noise_data = np.frombuffer(noise_audio, dtype=np.int16)

    print("Фоновый шум записан.")
    return noise_data

# Сохранение обработанного звука
def save_audio(filename, data, rate):
    import wave
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_SIZE)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(f"Файл сохранён как {filename}")

# Основная функция обработки звука с динамической адаптацией и задержкой
def start_streaming_dynamic_noise(noise_sample):
    print("Начало трансляции с динамическим обновлением шума...")
    
    # Проверяем доступность устройств
    input_device, output_device = check_audio_devices()
    if not input_device or not output_device:
        print("Необходимо подключить устройства.")
        return

    # Открытие потока для записи и воспроизведения
    stream = pyaudio.PyAudio().open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                      input=True, output=True, frames_per_buffer=CHUNK)
    
    processed_frames = []
    
    # Период обновления образца шума (например, каждые 10 секунд)
    noise_update_interval = 10
    last_noise_update_time = time.time()

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Если прошло достаточно времени, обновляем образец шума
            if time.time() - last_noise_update_time > noise_update_interval:
                print("Обновление образца шума...")
                noise_sample = record_background_noise(seconds=3)  # Записать новый образец шума
                last_noise_update_time = time.time()

            # Фильтрация шума
            reduced_noise = nr.reduce_noise(
                y=audio_data,
                sr=RATE,
                y_noise=noise_sample,
                prop_decrease=0.95  # Увеличиваем пропорцию уменьшения шума
            )

            # Преобразование в байты для воспроизведения
            output_data = reduced_noise.astype(np.int16).tobytes()
            stream.write(output_data)
            processed_frames.append(output_data)

            # Добавление задержки для улучшения качества фильтрации
            time.sleep(0.05)  # Пауза 50 миллисекунд
    except KeyboardInterrupt:
        print("\nОстановка трансляции...")
    finally:
        stream.stop_stream()
        stream.close()

        # Сохранение обработанного звука
        save_audio(FILENAME, b''.join(processed_frames), RATE)

# Запуск программы
if __name__ == "__main__":
    # Записываем первый образец шума
    initial_noise_sample = record_background_noise(seconds=3)

    # Запускаем потоковую обработку с динамическим обновлением шума
    start_streaming_dynamic_noise(initial_noise_sample)
