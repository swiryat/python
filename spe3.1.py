import speech_recognition as sr
import subprocess

def convert_audio_to_text(audio_data):
    recognizer = sr.Recognizer()

    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        return text
    except sr.UnknownValueError:
        print("Речь не распознана")
        return None
    except sr.RequestError as e:
        print(f"Ошибка запроса к сервису распознавания речи; {e}")
        return None

def convert_amr_to_wav(input_file_path, output_file_path, ffmpeg_path):
    command = [
        ffmpeg_path,
        '-i', input_file_path,
        '-ar', '16000',  # Устанавливаем частоту дискретизации в 16000 Гц
        '-ac', '1',      # Устанавливаем один канал (моно)
        output_file_path
    ]
    
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    amr_file_path = "C:/Users/swer/out.amr"
    output_file_path = "temp.wav"
    ffmpeg_path = r"C:\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"

    convert_amr_to_wav(amr_file_path, output_file_path, ffmpeg_path)

    recognizer = sr.Recognizer()

    with sr.AudioFile(output_file_path) as source:
        for i in range(5):
            audio_data = recognizer.record(source, duration=60)
            text = convert_audio_to_text(audio_data)

            if text:
                print(f"Распознанный текст (минута {i + 1}):")
                print(text)
            else:
                print(f"Распознанный текст (минута {i + 1}) отсутствует.")

if __name__ == "__main__":
    main()
