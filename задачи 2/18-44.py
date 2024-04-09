def count_words(input_string):
    # Удаляем пробелы в начале и конце строки
    input_string = input_string.strip()
    
    # Разбиваем строку на слова с использованием метода split(' ')
    words = input_string.split(' ')
    
    # Удаляем пустые слова, которые могли появиться из-за лишних пробелов
    words = [word for word in words if word]
    
    # Возвращаем количество слов
    return len(words)

# Получаем ввод от пользователя
user_input = input("Введите строку: ")

# Выводим результат
print("Количество слов:", count_words(user_input))
