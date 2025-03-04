from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import numpy as np

# Инициализация сети в Keras
model = Sequential()

# Первый слой (Dense + ReLU)
model.add(Dense(5, input_dim=4, activation='relu'))

# Дропаут после первого слоя
model.add(Dropout(0.5))

# Второй (выходной) слой
model.add(Dense(3, activation='linear'))

# Компиляция модели с SGD оптимизатором
model.compile(optimizer=SGD(learning_rate=0.01), loss='mean_squared_error')

# Пример данных (та же выборка, что и в ручной реализации)
X = np.random.randn(1, 4)
y = np.array([[0, 1, 0]])  # Пример целевых меток

# Обучение на одном шаге (одна эпоха)
model.fit(X, y, epochs=1, verbose=0)

# Прогнозирование
output_keras = model.predict(X)
print("Keras Output:", output_keras)
