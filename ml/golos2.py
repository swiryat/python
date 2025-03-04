import pyttsx3

# Инициализируем pyttsx3
engine = pyttsx3.init()

# Текст для преобразования
text = "Привет, это пример работы с библиотекой pyttsx3."

# Настраиваем параметры (скорость, громкость и голос)
engine.setProperty('rate', 150)    # Скорость
engine.setProperty('volume', 0.9)  # Громкость

# Преобразуем текст в речь
engine.say(text)
engine.runAndWait()
