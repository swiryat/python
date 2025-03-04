def generate_words(alphabet, k):
    if k == 0:
        return ['']
    
    words = []
    for letter in alphabet:
        shorter_words = generate_words(alphabet, k - 1)
        words.extend([letter + word for word in shorter_words])

    return words

# Ввод алфавита
alphabet = input("Введите алфавит (без пробелов): ")

# Ввод длины слова
k = int(input("Введите длину слова (целое число): "))

# Генерация и вывод слов
result = generate_words(alphabet, k)
print("Сгенерированные слова:")
print(result)
