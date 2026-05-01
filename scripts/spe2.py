import subprocess
from pydub import AudioSegment

def convert_amr_to_wav(input_file_path, output_file_path, ffmpeg_path):
    # Конвертируем .amr в .wav с использованием ffmpeg
    command = [ffmpeg_path, "-i", input_file_path, "-ar", "16000", output_file_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def convert_audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        print("Распознанный текст:", text)
        return text
    except sr.UnknownValueError:
        print("Речь не распознана")
        return ""
    except sr.RequestError as e:
        print(f"Ошибка запроса к сервису распознавания речи; {e}")
        return ""

def main():
    amr_file_path = r"C:\Users\swer\out.amr"
    output_file_path = "temp.wav"
    ffmpeg_path = r"C:\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"

    # Конвертируем .amr в .wav
    convert_amr_to_wav(amr_file_path, output_file_path, ffmpeg_path)

    # Извлекаем текст из аудиофайла
    text = convert_audio_to_text(output_file_path)

    # Записываем распознанный текст в файл
    with open("распознанный_текст.txt", "w", encoding="utf-8") as file:
        file.write(text)

if __name__ == "__main__":
    main()
