def count_substring_occurrences(main_string, substring):
    # Используем метод count для подсчета вхождений подстроки
    count = main_string.count(substring)
    return count

# Получаем ввод от пользователя
main_string = input("Введите символьную строку: ")
substring = input("Введите подстроку для поиска: ")

# Получаем и выводим результат
occurrences = count_substring_occurrences(main_string, substring)
print(f"Подстрока встречается в строке {occurrences} раз(а).")
