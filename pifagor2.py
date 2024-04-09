import matplotlib.pyplot as plt
import numpy as np

def pythagorean_theorem_proof(a, b, c):
    # Создаем прямоугольный треугольник
    triangle = np.array([[0, 0], [a, 0], [0, b]])

    # Визуализируем треугольник
    plt.figure()
    plt.plot(triangle[:, 0], triangle[:, 1], 'bo-')
    plt.text(-1, -1, 'A (0,0)')
    plt.text(a+1, -1, f'B ({a},0)')
    plt.text(-1, b+1, f'C (0,{b})')

    # Проверяем теорему Пифагора
    if a**2 + b**2 == c**2:
        plt.title('Теорема Пифагора верна')
    else:
        plt.title('Теорема Пифагора неверна')

    plt.show()

# Вводим данные с клавиатуры
a = float(input('Введите длину катета a: '))
b = float(input('Введите длину катета b: '))
c = float(input('Введите длину гипотенузы c: '))

# Вызываем функцию для визуализации и проверки теоремы Пифагора
pythagorean_theorem_proof(a, b, c)
