import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

# Генерация случайных данных
x_train = np.random.rand(1000, 20)
y_train = np.random.randint(2, size=(1000, 1))

# Создание модели
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(20,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Компиляция модели
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Обучение модели
model.fit(x_train, y_train, epochs=10, batch_size=32)

# Оценка модели
loss, accuracy = model.evaluate(x_train, y_train)
print(f"Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")
