import random

# Шаг 1: Простые комплименты
simple_compliments = [
    "У тебя очень приятная улыбка.",
    "Ты выглядишь очень позитивно сегодня.",
    "Отличная энергетика у тебя!",
    "Мне нравится, как ты общаешься с клиентами.",
]

# Шаг 2: Вопросы для поддержания разговора
follow_up_questions = [
    "Как тебе сегодня работа?",
    "Что самое интересное происходит у тебя здесь?",
    "Как ты обычно расслабляешься после смены?",
    "Есть ли у тебя любимое блюдо в этом кафе?",
]

def generate_soft_compliment_and_question():
    compliment = random.choice(simple_compliments)
    question = random.choice(follow_up_questions)
    return f"{compliment} {question}"

# Демонстрация:
if __name__ == "__main__":
    # Шаг 1: Получаем мягкий комплимент + вопрос
    phrase = generate_soft_compliment_and_question()
    print("Пример фразы для первого знакомства:")
    print(phrase)
