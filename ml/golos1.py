import torch
import numpy as np
from scipy.io.wavfile import write

# Загрузка моделей Tacotron 2 и WaveGlow
tacotron2 = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tacotron2')
waveglow = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_waveglow')

# Перевод текста в формат, подходящий для Tacotron2
text = "Your song lyrics here"

# Функция для подготовки текста
def preprocess_text(text):
    sequence = tacotron2.text_to_sequence(text, ['english_cleaners'])
    return torch.IntTensor(sequence).unsqueeze(0)

# Генерация мел-спектрограммы
with torch.no_grad():
    sequence = preprocess_text(text)
    mel_outputs, mel_outputs_postnet, _, alignments = tacotron2.infer(sequence)

# Генерация аудио с помощью WaveGlow
with torch.no_grad():
    audio = waveglow.infer(mel_outputs_postnet)

# Нормализация и запись в файл
audio_numpy = audio[0].data.cpu().numpy()
audio_normalized = (audio_numpy * 32767 / max(0.01, np.max(np.abs(audio_numpy)))).astype(np.int16)
write("generated_song.wav", 22050, audio_normalized)

print("Файл 'generated_song.wav' успешно создан.")
