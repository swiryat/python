import speech_recognition as sr
from pydub import AudioSegment

# Указываем путь к аудиофайлу MP3
mp3_audio_file_path = r'C:\Users\swer\Downloads\Каримов.mp3'
# Указываем путь для временного WAV файла
wav_audio_file_path = r'C:\Users\swer\Downloads\Каримов.wav'

# Конвертируем MP3 в WAV
audio = AudioSegment.from_mp3(mp3_audio_file_path)
audio.export(wav_audio_file_path, format="wav")

# Создаем объект recognizer
recognizer = sr.Recognizer()

# Открываем аудиофайл WAV
with sr.AudioFile(wav_audio_file_path) as source:
    # Слушаем аудиофайл и записываем данные в переменную audio_data
    audio_data = recognizer.record(source)
    
    # Пытаемся распознать текст из аудиофайла
    try:
        text = recognizer.recognize_google(audio_data, language='ru-RU') # Для русского языка
        print("Извлеченный текст:")
        print(text)
    except sr.UnknownValueError:
        print("Не удалось распознать речь")
    except sr.RequestError as e:
        print("Ошибка сервиса распознавания: {0}".format(e))
