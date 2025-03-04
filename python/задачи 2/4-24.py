def convert_to_base(n, base):
    # Базовый случай: если число меньше основания, вернуть его строковое представление
    if n < base:
        return str(n)
    else:
        # Шаг рекурсии: рекурсивно вызываем функцию с уменьшением числа и основания
        return convert_to_base(n // base, base) + str(n % base)

# Пример использования
number = int(input("Введите число для конвертации: "))
base = int(input("Введите основание системы счисления (от 2 до 9): "))

if 2 <= base <= 9:
    result = convert_to_base(number, base)
    print(f"Результат конвертации: {result}")
else:
    print("Ошибка: Основание должно быть от 2 до 9.")
