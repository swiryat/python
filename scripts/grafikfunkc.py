import matplotlib.pyplot as plt
import numpy as np

# Задаем интервал значений x
x = np.linspace(-10, 10, 400)

# Вычисляем соответствующие значения y
y = 9 * x - 8

# Создаем график
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='y = 9x - 8', color='b')

# Добавляем заголовок и подписи к осям
plt.title('График функции y = 9x - 8')
plt.xlabel('x')
plt.ylabel('y')

# Добавляем сетку
plt.grid(True)

# Отображаем легенду
plt.legend()

# Показываем график
plt.show()
