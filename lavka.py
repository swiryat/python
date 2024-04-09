def is_valid_lavki_barcode(barcode):
    # Функция для проверки, соответствует ли штрихкод формату Лавки

    # Разбиваем штрихкод на части, разделенные дефисами
    parts = barcode.split(" - ")

    # Проверяем количество частей
    if len(parts) != 4:
        return False

    # Проверяем номер партии (первая часть)
    if not parts[0].isdigit() or not (1 <= int(parts[0]) <= 9999):
        return False

    # Проверяем логистическую важность (вторая часть)
    if not (len(parts[1]) == 1 and parts[1] in "abc"):
        return False

    # Проверяем сочетание из трех строчных латинских букв (третья часть)
    if not (len(parts[2]) == 3 and parts[2].islower()):
        return False

    # Проверяем количество товаров (четвертая часть)
    if not parts[3].isdigit() or not (1 <= int(parts[3]) <= 999999):
        return False

    return True


def calculate_precision_recall(n, k, results):
    true_positives = 0  # Количество правильно распознанных штрихкодов Лавки
    false_positives = 0  # Количество неправильно распознанных штрихкодов Лавки
    total_actual_lavki = 0  # Общее количество штрихкодов Лавки

    for i in range(n):
        if is_valid_lavki_barcode(results[i]):
            total_actual_lavki += 1
            if " - " in results[i]:
                true_positives += 1
            else:
                false_positives += 1

    if true_positives + false_positives == 0:
        precision = 0  # Если нет правильно распознанных штрихкодов Лавки, устанавливаем точность в 0
    else:
        precision = true_positives / (true_positives + false_positives)
    
    if total_actual_lavki == 0:
        recall = 0  # Если нет штрихкодов Лавки в тестовой выборке, устанавливаем полноту в 0
    else:
        recall = true_positives / total_actual_lavki

    return precision, recall


n, k = map(int, input().split())
results = [input().strip() for _ in range(n + k)]

precision, recall = calculate_precision_recall(n, k, results)
print(f"{recall:.4f} {precision:.4f}")
