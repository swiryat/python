import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.preprocessing import image
import numpy as np

# Функция для создания и компиляции модели
def create_model():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10))

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    return model

# Загрузка данных CIFAR-10
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# Нормализация значений пикселей к диапазону [0, 1]
train_images, test_images = train_images / 255.0, test_images / 255.0

# Создание и обучение модели
model = create_model()
model.fit(train_images, train_labels, epochs=10, validation_data=(test_images, test_labels))

# Сохранение модели
model.save('initial_model')

# Загрузка модели
loaded_model = tf.keras.models.load_model('initial_model')

# Дополнительное обучение загруженной модели
loaded_model.fit(train_images, train_labels, epochs=5, validation_data=(test_images, test_labels))

# Сохранение обновленной модели
loaded_model.save('updated_model')
