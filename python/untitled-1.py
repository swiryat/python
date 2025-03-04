import librosa

def analyze_audio(audio_file):
    try:
        # Загрузка аудиофайла
        y, sr = librosa.load(audio_file)

        # Определение характеристик звука
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)

        # Вывод результатов
        print(f"Анализ аудиофайла: {audio_file}")
        print(f"Длительность аудиофайла: {librosa.get_duration(y=y, sr=sr):.2f} секунд")
        print(f"Tempo (ритм): {tempo:.2f} BPM")
        print(f"Количество ударов (beats): {len(beats)}")
        print(f"Количество начал звуков (onsets): {len(onset_frames)}")

    except Exception as e:
        print(f"Ошибка при обработке аудиофайла: {e}")

# Путь к вашему аудиофайлу
audio_file_path = r'C:\Users\swer\GitHub\python\Wallem.mp3'

# Вызов функции для анализа аудиофайла
analyze_audio(audio_file_path)



