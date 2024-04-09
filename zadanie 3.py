# Создаем словарь с информацией о температуре
temperature_data = {
    "понедельник": 12.0,
    "вторник": 12.0,
    "среда": 17.0,
    "четверг": 17.0,
    "пятница": 14.3,
    "суббота": 11.9,
    "воскресенье": 12.0,
}

# Функция для перевода из градусов Цельсия в градусы Фаренгейта
def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return round(fahrenheit, 2)

# Создаем список кортежей (Celsius, Fahrenheit)
temperature_in_fahrenheit = [(celsius, celsius_to_fahrenheit(celsius)) for celsius in temperature_data.values()]

# Выводим температуры в градусах Цельсия и Фаренгейта для каждого дня
for day, (celsius, fahrenheit) in zip(temperature_data.keys(), temperature_in_fahrenheit):
    print(f"{day}: {celsius}°C, {fahrenheit}°F")

# Находим день с максимальной и минимальной температурой
max_temp_day = max(temperature_data, key=temperature_data.get)
min_temp_day = min(temperature_data, key=temperature_data.get)

print(f"Максимальная температура наблюдалась в {max_temp_day}")
print(f"Минимальная температура наблюдалась в {min_temp_day}")

# Вычисляем среднюю температуру за неделю
average_temperature = sum(temperature_data.values()) / len(temperature_data)
print(f"Средняя температура за неделю: {average_temperature:.2f}°C")

# Находим моду (наиболее часто встречающееся значение)
from collections import Counter
temperature_counts = Counter(temperature_data.values())
mode_temperature = [temp for temp, count in temperature_counts.items() if count == max(temperature_counts.values())]
mode_days = [day for day, temp in temperature_data.items() if temp in mode_temperature]

print(f"Модальное значение температуры за неделю: {', '.join(map(str, mode_temperature))}°C (наблюдалось в {', '.join(mode_days)})")

# Определяем "прохладные" и "теплые" дни
cool_days = [day for day, temp in temperature_data.items() if temp < 14]
warm_days = [day for day, temp in temperature_data.items() if temp >= 14]

print("Прохладные дни:", ', '.join(cool_days))
print("Теплые дни:", ', '.join(warm_days))
