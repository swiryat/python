def neural_network(inputs, weight):
    """
    Функция для вычисления предсказания нейронной сети.
    Может работать как с одним входом, так и с массивом входов.

    :param inputs: Один вход (число) или список входов (list)
    :param weight: Вес (коэффициент), используемый для предсказания
    :return: Предсказание или список предсказаний
    """
    if isinstance(inputs, list):  # Проверяем, является ли inputs списком
        # Если inputs — список, возвращаем список предсказаний
        predictions = [inp * weight for inp in inputs]
        return predictions
    else:
        # Если inputs — одно число, возвращаем одиночное предсказание
        return inputs * weight

# Использование функции
inputs = [100, 50, 150]  # Несколько входных данных
weight = 0.2  # Вес для расчёта предсказаний

# Вычисление предсказаний для списка входов
predictions = neural_network(inputs, weight)

# Вычисление предсказания для одиночного входа
single_prediction = neural_network(80, weight)

# Вывод результатов
print(f"Предсказания для списка входов {inputs}: {predictions}")  # [20.0, 10.0, 30.0]
print(f"Предсказание для одиночного входа 80: {single_prediction}")  # 16.0
