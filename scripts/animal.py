# Шаг 1: Определение характеристик животных и политиков
animal_traits = {
    "Лев": {"сила": 9, "лидерство": 10, "хитрость": 5, "агрессия": 7},
    "Ворон": {"сила": 4, "лидерство": 6, "хитрость": 9, "агрессия": 3},
    "Заяц": {"сила": 2, "лидерство": 3, "хитрость": 6, "агрессия": 1},
    "Лиса": {"сила": 5, "лидерство": 6, "хитрость": 10, "агрессия": 4},
    # Добавьте другие животные по аналогии
}

# Шаг 2: Определение характеристик политика (условно)
politician_traits = {
    "сила": 4,
    "лидерство": 4,
    "хитрость": 9,
    "агрессия": 8
}

# Шаг 3: Функция для подсчёта сходства
def similarity_score(p_traits, a_traits):
    return sum(abs(p_traits[key] - a_traits[key]) for key in p_traits)

# Шаг 4: Поиск наиболее подходящего животного
best_match = None
lowest_score = float('inf')
for animal, traits in animal_traits.items():
    score = similarity_score(politician_traits, traits)
    if score < lowest_score:
        lowest_score = score
        best_match = animal

print(f"Политик похож на: {best_match} (оценка сходства: {lowest_score})")
