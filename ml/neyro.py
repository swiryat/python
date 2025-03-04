import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.preprocessing import image
import numpy as np
from datetime import datetime

# Загрузка данных CIFAR-10
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# Нормализация значений пикселей к диапазону [0, 1]
train_images, test_images = train_images / 255.0, test_images / 255.0

# Создание модели сверточной нейронной сети
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

# Добавление полносвязных слоев
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))

# Компиляция модели
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Обучение модели
model.fit(train_images, train_labels, epochs=10, validation_data=(test_images, test_labels))

# Сохранение модели с уникальным именем
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
model.save(f'save_model_{timestamp}')

# Загрузка и изменение размера вашей фотографии
img_path = 'image.jpg'
img = image.load_img(img_path, target_size=(32, 32))
img_array = image.img_to_array(img)
img_array = img_array / 255.0  # Нормализация значений пикселей
img_array = np.expand_dims(img_array, axis=0)

# Предсказание с использованием модели
predictions = model.predict(img_array)

# Вывод результатов предсказания
predicted_class = np.argmax(predictions)
print(f'Predicted class: {predicted_class}')

# Загрузка сохраненной модели с уникальным именем
loaded_model = tf.keras.models.load_model(f'save_model_{timestamp}')

# Загрузка и изменение размера вашей фотографии
img_path = 'image.jpg'
img = image.load_img(img_path, target_size=(32, 32))
img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Предсказание с использованием загруженной модели
predictions = loaded_model.predict(img_array)

# Вывод результатов предсказания
predicted_class = np.argmax(predictions)
print(f'Predicted class: {predicted_class}')

