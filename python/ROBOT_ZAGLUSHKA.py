import numpy as np
import tensorflow as tf
import random
from collections import deque
import mock_gpio as GPIO  # Импортируйте вашу заглушку
import time

# Константы и параметры
EPISODES = 1000
ACTION_SIZE = 2
STATE_SIZE = 1  # Состояние включает расстояние
epsilon = 1.0  # Начальное значение ε для ε-жадной стратегии
epsilon_decay = 0.995
min_epsilon = 0.01
replay_memory = deque(maxlen=2000)
BATCH_SIZE = 32

# Настройка ультразвукового датчика (заменяем на заглушку)
TRIG = 23
ECHO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    """Функция для получения расстояния от ультразвукового датчика."""
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance

def create_optimized_model():
    """Создание оптимизированной модели нейросети."""
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(24, input_dim=STATE_SIZE, activation='relu'))
    model.add(tf.keras.layers.Dense(24, activation='relu'))
    model.add(tf.keras.layers.Dense(ACTION_SIZE, activation='linear'))
    model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
    return model

# Инициализация модели
model = create_optimized_model()

def update_model(batch):
    """Обновление модели на основе опыта."""
    for state, action, reward, next_state, done in batch:
        target = reward
        if not done:
            target = reward + 0.95 * np.amax(model.predict(next_state)[0])
        target_f = model.predict(state)
        target_f[0][action] = target
        model.fit(state, target_f, epochs=1, verbose=0)

def select_action(state, epsilon):
    """Выбор действия с использованием ε-жадной стратегии."""
    if np.random.rand() <= epsilon:
        return random.randrange(ACTION_SIZE)
    q_values = model.predict(state)
    return np.argmax(q_values[0])

def move_forward():
    """Движение вперед."""
    print("Движение вперед")

def move_backward():
    """Движение назад."""
    print("Движение назад")

# Основной цикл работы терминатора
def robot_control_loop():
    """Основной цикл управления роботом."""
    global epsilon
    for episode in range(EPISODES):
        state = np.reshape(get_distance(), [1, STATE_SIZE])
        done = False
        total_reward = 0

        while not done:
            action = select_action(state, epsilon)
            if action == 0:
                move_forward()
            else:
                move_backward()

            next_state = np.reshape(get_distance(), [1, STATE_SIZE])
            reward = 1 if next_state[0][0] > 30 else -1  # Пример простой системы наград
            done = next_state[0][0] < 10  # Завершение эпизода при близости к препятствию
            replay_memory.append((state, action, reward, next_state, done))
            state = next_state
            total_reward += reward

            if len(replay_memory) > BATCH_SIZE:
                batch = random.sample(replay_memory, BATCH_SIZE)
                update_model(batch)

        if epsilon > min_epsilon:
            epsilon *= epsilon_decay

        print(f"Эпизод: {episode + 1}/{EPISODES}, Общая награда: {total_reward}, Epsilon: {epsilon:.2f}")

try:
    robot_control_loop()
finally:
    GPIO.cleanup()
