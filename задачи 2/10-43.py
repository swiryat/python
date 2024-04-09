def add_parity_bit(binary_string):
    # Подсчитываем количество единиц в исходной строке
    count_ones = binary_string.count('1')
    
    # Определяем бит четности
    parity_bit = '0' if count_ones % 2 == 0 else '1'
    
    # Добавляем бит четности к исходной строке
    result_string = binary_string + parity_bit
    
    return result_string

# Получаем ввод от пользователя
input_string = input("Введите битовую строку: ")

# Добавляем бит четности
result = add_parity_bit(input_string)

# Выводим результат
print("Результат:", result)
