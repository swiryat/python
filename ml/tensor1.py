import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

# Генерация случайных данных
x_train = np.random.rand(1000, 20)
y_train = np.random.randint(2, size=(1000, 1))

# Создание модели
model = keras.Sequential([
    layers.Input(shape=(20,)),
    layers.Dense(128, activation='relu'),  # Увеличено количество нейронов
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Компиляция модели
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),  # Настройка скорости обучения
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Обучение модели
model.fit(x_train, y_train, epochs=20, batch_size=32)  # Увеличено количество эпох

# Оценка модели
loss, accuracy = model.evaluate(x_train, y_train)
print(f"Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")
