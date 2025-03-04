import matplotlib.pyplot as plt

# Типы памяти
memory_types = ['SRAM', 'DRAM', 'HDD', 'SSD']

# Минимальное и максимальное время доступа в миллисекундах для каждого типа памяти
access_times_min_ms = [0.0000005, 0.00006, 2, 0.1]
access_times_max_ms = [0.000002, 0.0001, 20, 0.2]

# Создаем график скорости доступа к разным типам памяти
plt.figure(figsize=(10, 6))
plt.bar(memory_types, access_times_max_ms, color='skyblue', label='Максимальное время доступа')
plt.bar(memory_types, access_times_min_ms, color='lightgreen', label='Минимальное время доступа')

# Добавляем заголовок и метки осей
plt.title('Скорость доступа к разным типам памяти')
plt.xlabel('Тип памяти')
plt.ylabel('Время доступа, миллисекунды')

# Добавляем легенду
plt.legend()

# Отображаем график
plt.show()


