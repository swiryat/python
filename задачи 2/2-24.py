def print_repeating_characters(character, count):
    # Базовый случай: если count становится нулевым, завершаем рекурсию
    if count == 0:
        return
    else:
        # Шаг рекурсии: выводим символ и вызываем функцию с уменьшением count
        print(character)
        print_repeating_characters(character, count - 1)

# Пример использования
char_to_repeat = input("Введите символ: ")
repeat_count = int(input("Введите количество повторений: "))

print_repeating_characters(char_to_repeat, repeat_count)
