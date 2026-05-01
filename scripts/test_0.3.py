from tensorflow import keras
from tensorflow.keras import layers

# Шаг 1: явный вход
inputs = keras.Input(shape=(5,))

# Шаг 2: скрытый слой
x = layers.Dense(10, activation="relu")(inputs)

# Шаг 3: выход
outputs = layers.Dense(1)(x)

# Шаг 4: модель
model = keras.Model(inputs=inputs, outputs=outputs)

# Шаг 5: компиляция
model.compile(optimizer="adam", loss="mse")

print("Модель собрана и скомпилирована!")
