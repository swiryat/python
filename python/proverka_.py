import tensorflow as tf

# Проверка версии TensorFlow
print("TensorFlow version:", tf.__version__)

# Пример создания и запуска простого графа
a = tf.constant(5)
b = tf.constant(3)
c = tf.add(a, b)
print("Результат сложения a + b:", c.numpy())
