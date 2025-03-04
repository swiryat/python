from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import librosa
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


# Загружаем модель и процессор
model_name = "facebook/wav2vec2-large-960h"
processor = Wav2Vec2Processor.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)

# Загружаем аудиофайл
audio_path = r"G:\swer\Music\звонки\Входящий звонок 11 ноября 2024 в 11-33-56_ EndedByHandler.wav"
audio, rate = librosa.load(audio_path, sr=16000)

# Преобразуем в тензор
input_values = processor(audio, sampling_rate=rate, return_tensors="pt").input_values

# Пропускаем через нейросеть
with torch.no_grad():
    logits = model(input_values).logits

# Декодируем текст
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)[0]

print("Распознанный текст:", transcription)
