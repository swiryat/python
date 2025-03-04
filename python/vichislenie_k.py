import math
import numpy as np
import matplotlib.pyplot as plt

# Данные
m = 9.11e-31  # масса электрона, кг
h_bar = 1.0545718e-34  # постоянная Планка, Дж*с
E = 3 * 1.60218e-19  # энергия частицы, Дж
U = 5 * 1.60218e-19  # высота барьера, Дж

# Рассчёт ∆U (U - E)
delta_U = U - E

# Массив значений ширины барьера a (от 0.1 нм до 1.0 нм)
a_values = np.linspace(0.1e-9, 1.0e-9, 100)

# Вероятность туннелирования T для разных значений ширины барьера
T_values = [math.exp(-2 * (math.sqrt(2 * m * delta_U) / h_bar) * a) for a in a_values]

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(a_values * 1e9, T_values, label="Вероятность туннелирования T", color="blue")
plt.xlabel("Ширина барьера a (нм)")
plt.ylabel("Вероятность туннелирования T")
plt.title("Зависимость вероятности туннелирования от ширины барьера")
plt.grid()
plt.legend()
plt.show()

# Расчёт вероятности туннелирования для конкретного значения ширины барьера (например, a = 0.5e-9 м)
a_specific = 0.5e-9  # конкретное значение ширины барьера, м
kappa = math.sqrt(2 * m * delta_U) / h_bar
T = math.exp(-2 * kappa * a_specific)

# Вывод вероятности туннелирования для выбранного a
print(f"Вероятность туннелирования при a = {a_specific * 1e9:.1f} нм составляет: {T:.5f}")
