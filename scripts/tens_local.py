import tensorflow as tf
print("TensorFlow version:", tf.__version__)
print("TensorFlow test op result:", tf.reduce_sum(tf.random.normal([10, 10])))
