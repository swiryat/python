def is_anagram(a, b):
    # Проверяем, имеют ли строки одинаковую длину
    if len(a) != len(b):
        return "False"
    
    # Создаем словарь для подсчета частот символов в строке a
    freq = {}
    for char in a:
        freq[char] = freq.get(char, 0) + 1
    
    # Итерируемся по строке b и уменьшаем частоту встречаемости символов
    for char in b:
        if char not in freq:
            return "False"  # Символ встречается в b, но отсутствует в a
        freq[char] -= 1
    
    # Проверяем, все ли символы встречаются одинаковое количество раз
    return "True" if all(count == 0 for count in freq.values()) else "False"

# Пример использования:
a = "anagram"
b = "nagaram"
print(is_anagram(a, b))  # Выведет: "True"
