import speech_recognition as sr

# Указываем путь к аудиофайлу
audio_file_path = r'C:\Users\swer\Downloads\carimow.wav'

# Создаем объект recognizer
recognizer = sr.Recognizer()

# Открываем аудиофайл
with sr.AudioFile(audio_file_path) as source:
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
