from pydub import AudioSegment
import subprocess

def convert_amr_to_wav(input_file_path, output_file_path, ffmpeg_path):
    # Проверяем наличие ffmpeg
    if not subprocess.run([ffmpeg_path, "-version"]).returncode == 0:
        raise FileNotFoundError("FFmpeg not found. Please make sure it is installed and the path is correctly specified.")

    # Конвертируем .amr в .wav
    subprocess.run([ffmpeg_path, "-i", input_file_path, "-ar", "16000", output_file_path])

def main():
    amr_file_path = r"C:\Users\swer\out.amr"
    output_file_path = "temp.wav"
    ffmpeg_path = r"C:\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"

    # Конвертируем .amr в .wav
    convert_amr_to_wav(amr_file_path, output_file_path, ffmpeg_path)

    # Извлекаем текст из аудиофайла (ваша функция convert_audio_to_text)
    text = convert_audio_to_text(output_file_path)

    # Записываем распознанный текст в файл
    with open("распознанный_текст.txt", "w", encoding="utf-8") as file:
        file.write(text)

if __name__ == "__main__":
    main()

