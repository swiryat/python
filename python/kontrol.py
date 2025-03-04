import re

# Список запрещённых слов (может быть расширен)
FORBIDDEN_WORDS = ["взлом", "хак", "обойти защиту", "фишинг", "вирус"]

def filter_request(user_input: str) -> str:
    """
    Функция анализирует текст запроса и заменяет запрещённые слова предупреждением.
    """
    for word in FORBIDDEN_WORDS:
        # Используем регулярные выражения для поиска слов (нечувствительно к регистру)
        pattern = re.compile(rf"\b{word}\b", re.IGNORECASE)
        if pattern.search(user_input):
            return "⚠ Ваш запрос содержит запрещённое слово и не может быть обработан."
    
    return "✅ Ваш запрос безопасен: " + user_input

# Примеры запросов
requests = [
    "Как взломать Wi-Fi?",
    "Как работают обойти защиту шифрования?",
    "Расскажи про хак и способы защиты.",
]

# Проверяем запросы
for req in requests:
    print(filter_request(req))
