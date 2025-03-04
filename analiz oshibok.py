import re
import pymorphy3  # Изменено на pymorphy3

# Инициализация морфологического анализатора
morph = pymorphy3.MorphAnalyzer()

# Словарь для хранения известных слов
known_words = set()

# Функция для загрузки слов из файла
def load_known_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            known_words.add(line.strip())

# Функция для проверки текста на ошибки
def check_text(text):
    # Разбиваем текст на слова
    words = re.findall(r'\w+', text)
    errors = []

    for word in words:
        # Нормализуем слово
        normal_word = morph.parse(word)[0].normal_form

        # Проверка на наличие слова в известном словаре
        if normal_word not in known_words:
            errors.append(f"Ошибка: '{word}' не найдено в словаре.")

    return errors

# Пример использования
if __name__ == "__main__":
    # Загрузка известных слов из файла
    load_known_words('known_words.txt')

    # Текст для проверки
    input_text = "Это пример текста с ошибками. В нём есть неправильно написанные слова."
    
    # Проверка текста на ошибки
    errors = check_text(input_text)
    
    # Вывод ошибок
    if errors:
        for error in errors:
            print(error)
    else:
        print("Ошибок не найдено.")
