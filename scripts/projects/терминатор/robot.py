import numpy as np
import tensorflow as tf
import cv2
import RPi.GPIO as GPIO
import time
import random
from collections import deque

# Константы и параметры
EPISODES = 1000
ACTION_SIZE = 2
STATE_SIZE = 1  # Состояние включает расстояние
epsilon = 1.0  # Начальное значение ε для ε-жадной стратегии
epsilon_decay = 0.995
min_epsilon = 0.01
replay_memory = deque(maxlen=2000)
BATCH_SIZE = 32

# Настройка GPIO для ультразвукового датчика
TRIG = 23
ECHO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Настройка GPIO для управления моторами
MOTOR_LEFT_FORWARD = 17
MOTOR_LEFT_BACKWARD = 27
MOTOR_RIGHT_FORWARD = 22
MOTOR_RIGHT_BACKWARD = 5
ENABLE_LEFT = 18  # ШИМ для управления скоростью левого мотора
ENABLE_RIGHT = 13  # ШИМ для управления скоростью правого мотора

GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
GPIO.setup(ENABLE_LEFT, GPIO.OUT)
GPIO.setup(ENABLE_RIGHT, GPIO.OUT)

# Создание PWM для управления скоростью
pwm_left = GPIO.PWM(ENABLE_LEFT, 100)  # Частота 100 Гц
pwm_right = GPIO.PWM(ENABLE_RIGHT, 100)

pwm_left.start(0)  # Начальная скорость 0%
pwm_right.start(0)

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
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
    pwm_left.ChangeDutyCycle(70)  # Установим скорость на 70%
    pwm_right.ChangeDutyCycle(70)
    print("Движение вперед")

def move_backward():
    """Движение назад."""
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(70)  # Установим скорость на 70%
    pwm_right.ChangeDutyCycle(70)
    print("Движение назад")

def stop():
    """Остановка движения."""
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
    pwm_left.ChangeDutyCycle(0)  # Остановить моторы
    pwm_right.ChangeDutyCycle(0)
    print("Остановка")

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

            time.sleep(1)  # Время для выполнения действия

            next_state = np.reshape(get_distance(), [1, STATE_SIZE])
            reward = 1 if next_state[0][0] > 30 else -1  # Пример простой системы наград
            done = next_state[0][0] < 10  # Завершение эпизода при близости к препятствию
            replay_memory.append((state, action, reward, next_state, done))
            state = next_state
            total_reward += reward

            if len(replay_memory) > BATCH_SIZE:
                batch = random.sample(replay_memory, BATCH_SIZE)
                update_model(batch)

            # Остановка после каждого действия для безопасности
            stop()

        if epsilon > min_epsilon:
            epsilon *= epsilon_decay

        print(f"Эпизод: {episode + 1}/{EPISODES}, Общая награда: {total_reward}, Epsilon: {epsilon:.2f}")

try:
    robot_control_loop()
finally:
    pwm_left.stop()
    pwm_right.stop()
    GPIO.cleanup()
