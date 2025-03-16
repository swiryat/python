import numpy as np
import matplotlib.pyplot as plt

# Заданные параметры
h1 = 10          # Высота антенны РЛС (м)
k = 4.12         # Коэффициент, учитывающий кривизну Земли и атмосферную рефракцию

# Создаем массив значений высоты цели от 0.25 до 200 м (500 точек для гладкого графика)
h2_values = np.linspace(0.25, 200, 500)

# Вычисляем дальность обнаружения по формуле D = 4.12 * (sqrt(h1) + sqrt(h2))
D_values = k * (np.sqrt(h1) + np.sqrt(h2_values))

# Построение графика
plt.figure(figsize=(8, 6))
plt.plot(h2_values, D_values, label=r'$D=4.12\cdot(\sqrt{10}+\sqrt{h_2})$', color='blue')
plt.xlabel('Высота цели $h_2$ (м)', fontsize=12)
plt.ylabel('Дальность обнаружения $D$ (км)', fontsize=12)
plt.title('Зависимость дальности обнаружения от высоты цели', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
