from moviepy.editor import VideoFileClip

# Укажите путь к вашему исходному видеофайлу
input_video_path = "D:\Моё видео\Письмо маме.mp4"

# Укажите имена файлов для сохранения
output_audio_path = "output_audio.mp3"   # Аудиофайл
output_audio_wav_path = "output_audio.wav"  # Аудиофайл в формате WAV
output_video_path = "output_video_without_audio.mp4"  # Видео без аудио

# Загружаем видеофайл
video_clip = VideoFileClip(input_video_path)

# 1. Извлечение аудиотрека
audio_clip = video_clip.audio
audio_clip.write_audiofile(output_audio_path)  # Сохраняем аудио как MP3
audio_clip.write_audiofile(output_audio_wav_path)  # Сохраняем аудио как WAV

# 2. Сохранение видеотрека без звука
video_clip_without_audio = video_clip.without_audio()
video_clip_without_audio.write_videofile(output_video_path, codec="libx264", audio=False)

# Закрываем ресурсы
audio_clip.close()
video_clip.close()

print("Все файлы успешно сохранены:")
print(f"- Аудиофайл MP3: {output_audio_path}")
print(f"- Аудиофайл WAV: {output_audio_wav_path}")
print(f"- Видео без аудио: {output_video_path}")
