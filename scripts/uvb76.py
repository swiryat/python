import numpy as np
import sounddevice as sd

# Параметры записи
sample_rate = 44100  # Частота дискретизации
duration = 10  # Длительность записи в секундах

# Запись сигнала
print("Recording...")
signal = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
sd.wait()
print("Recording completed.")

# Преобразование записи в массив для анализа
signal_data = np.array(signal)

# Пример простого анализа: визуализация сигнала
import matplotlib.pyplot as plt

plt.plot(signal_data[:1000])  # показываем первые 1000 точек для анализа
plt.title("Recorded Signal")
plt.show()
