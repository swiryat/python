import string
from collections import Counter

def clean_word(word):
    # Убираем знаки пунктуации из слова
    return word.translate(str.maketrans("", "", string.punctuation))

def generate_alphabetical_frequency_dictionary(file_path):
    # Считываем содержимое файла
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Разделяем текст на слова и приводим к нижнему регистру
    words = content.lower().split()

    # Очищаем слова от знаков пунктуации
    words = [clean_word(word) for word in words]

    # Подсчитываем частоту каждого слова
    word_frequency = Counter(words)

    # Сортируем слова в алфавитном порядке
    sorted_words = sorted(word_frequency.items(), key=lambda x: x[0])

    # Выводим алфавитно-частотный словарь
    for word, frequency in sorted_words:
        print(f'{word}: {frequency}')

# Пример использования
file_path = 'C:\\Users\\ra\\Documents\\txt.txt'
generate_alphabetical_frequency_dictionary(file_path)
