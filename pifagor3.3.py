import matplotlib.pyplot as plt
import numpy as np

def pythagorean_trousers_proof(a, b, c):
    # Создаем прямоугольный треугольник
    triangle = np.array([[0, 0], [a, 0], [0, b], [0, 0]])

    # Создаем квадраты на катетах и гипотенузе
    square_a = np.array([[a, 0], [a, a], [0, a], [0, 0]])
    square_b = np.array([[0, b], [b, b], [b, 0], [0, 0]])
    square_c = np.array([[a, b], [a, a+b], [a+b, a+b], [b, a]])

    # Визуализируем треугольник и квадраты
    plt.plot(triangle[:, 0], triangle[:, 1], 'bo-')
    plt.plot(square_a[:, 0], square_a[:, 1], 'g--', label='Квадрат на a')
    plt.plot(square_b[:, 0], square_b[:, 1], 'g--', label='Квадрат на b')
    plt.plot(square_c[:, 0], square_c[:, 1], 'g--', label='Квадрат на c')

    # Подписываем оси
    plt.xlabel('Длина оси X')
    plt.ylabel('Длина оси Y')

    plt.title('Метод Пифагоровых штанов для теоремы Пифагора')
    plt.legend()
    plt.grid(True)
    plt.show()

# Задаем значения катетов и гипотенузы
a = 3
b = 4
c = 5

# Вызываем функцию для визуализации метода Пифагоровых штанов
pythagorean_trousers_proof(a, b, c)
