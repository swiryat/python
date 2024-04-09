import re

# Исходный текст
text = """
Взвейтесь кострами, синие ночи!
Мы пионеры - дети рабочих
Близится время светлых годов
Клич пионера: "Всегда будь готов!"
Радостным шагом с песней веселой
Мы выступаем за комсомолом
Близится время светлых годов
Клич пионера: "Всегда будь готов!"
Мы поднимаем красное знамя
Дети рабочих, смело за нами!
Близится время светлых годов
Клич пионера: "Всегда будь готов!"
Взвейтесь кострами, синие ночи!
Мы пионеры - дети рабочих
Близится время светлых годов
Клич пионера: "Всегда будь готов!"
Клич пионера: "Всегда будь готов!"
"""

# Приведем текст к нижнему регистру
text = text.lower()

# Разделим текст на строки и подсчитаем количество строк
lines = text.strip().split('\n')
num_lines = len(lines)

# Разделим текст на предложения и подсчитаем количество предложений
sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
num_sentences = len(sentences)

# Разделим текст на слова и подсчитаем количество уникальных слов
words = re.findall(r'\b\w+\b', text)
unique_words = set(words)
num_unique_words = len(unique_words)

# Построим частотную таблицу для уникальных слов
word_frequency = {}
for word in words:
    word_frequency[word] = word_frequency.get(word, 0) + 1

# Подсчитаем количество уникальных букв
letters = re.findall(r'\b\w\b', text)
unique_letters = set(letters)
num_unique_letters = len(unique_letters)

# Выведем результаты
print("Количество строк в тексте:", num_lines)
print("Количество предложений в тексте:", num_sentences)
print("Количество уникальных слов в тексте:", num_unique_words)
print("Частотная таблица слов:")
for word, frequency in word_frequency.items():
    print(f"{word}: {frequency} раз")
print("Количество уникальных букв в тексте:", num_unique_letters)
