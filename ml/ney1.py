from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from PIL import Image
import numpy as np

# Загрузка данных
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Преобразование размерности изображений
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape((X_train.shape[0], num_pixels)).astype('float32')
X_test = X_test.reshape((X_test.shape[0], num_pixels)).astype('float32')

# Нормализация входных значений
X_train = X_train / 255
X_test = X_test / 255

# Преобразование векторных классов в бинарные матрицы
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
num_classes = y_test.shape[1]

# Определение модели с двумя скрытыми слоями
model = Sequential()
model.add(Dense(num_pixels, kernel_initializer='normal', activation='tanh'))  # Дополнительный скрытый слой
model.add(Dense(num_pixels, kernel_initializer='normal', activation='sigmoid'))  # Дополнительный скрытый слой
model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))

# Компиляция модели
from tensorflow.keras.optimizers import SGD
model.compile(loss='categorical_crossentropy', optimizer=SGD(), metrics=['accuracy'])

# Обучение модели
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=300, verbose=2)

# Оценка модели
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

# Сохранение модели
model.save('my_model.h5')

# Загрузка модели
from tensorflow.keras.models import load_model
model = load_model('my_model.h5')

# Загрузка нового изображения
image_path = '3.png'  # Замените на путь к вашему изображению
image = Image.open(image_path)

# Преобразование изображения в градации серого
image = image.convert('L')

# Изменение размера изображения до 28x28 пикселей
image = image.resize((28, 28))

# Преобразование изображения в массив numpy и нормализация значений пикселей
image = np.array(image) / 255.0

# Изменение формы массива, чтобы он соответствовал входу модели
image = image.reshape(1, num_pixels)

# Предсказание класса изображения
prediction = model.predict(image)
predicted_class = np.argmax(prediction)
print('Predicted class:', predicted_class)
