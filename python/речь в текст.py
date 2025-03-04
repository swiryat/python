import speech_recognition as sr
import youtube_dl
from pydub import AudioSegment

def download_audio(video_url, output_file):
    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        audio_url = info['formats'][0]['url']
        audio_data = ydl.urlopen(audio_url)
        audio_file = AudioSegment.from_file(audio_data, 'webm')
        audio_file.export(output_file, format="wav")

def recognize_speech(audio_file, language="en-US"):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            return "Речь не распознана"
        except sr.RequestError as e:
            return f"Ошибка при обращении к сервису: {e}"

def main():
    video_url = "https://www.youtube.com/watch?v=GluSLXFGfJ8"
    audio_output_file = "audio.wav"

    try:
        download_audio(video_url, audio_output_file)
        text = recognize_speech(audio_output_file, language="en-US")
        print("Результат распознавания речи:")
        print(text)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
