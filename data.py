import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Создайте случайный набор данных (замените его на свой набор данных)
data = np.random.normal(0, 1, 1000)  # Пример нормально распределенных данных

# Рассчитайте дисперсию и стандартное отклонение
variance = np.var(data)
std_deviation = np.std(data)

# Определите выбросы с использованием метода межквартильного размаха (IQR)
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = [x for x in data if x < lower_bound or x > upper_bound]

# Аппроксимируйте значения после удаления выбросов
data_cleaned = [x for x in data if x >= lower_bound and x <= upper_bound]

# Визуализируйте результат
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.title("Исходные данные")
plt.hist(data, bins=30, color='blue', alpha=0.7)
plt.subplot(2, 1, 2)
plt.title("Данные после удаления выбросов")
plt.hist(data_cleaned, bins=30, color='green', alpha=0.7)
plt.show()

print(f"Дисперсия: {variance}")
print(f"Стандартное отклонение: {std_deviation}")
print(f"Количество выбросов: {len(outliers)}")
