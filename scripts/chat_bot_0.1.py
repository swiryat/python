# Шаг 1: Импорт и загрузка модели
# Вход: названия тем и шаблоны ответов
# Цель: подготовить эмбеддинги шаблонов
# Выход: модель и эмбеддинги шаблонов
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')  # Step 1: загрузка эмбеддингов

templates = {
    'общие': ["Привет! Как у тебя дела?", "Рад тебя видеть! О чём хочешь поговорить?"],
    'отношения': ["Отношения — это искусство компромиссов…", "Что тебя беспокоит в общении с партнёром?"],
    # ... остальные темы ...
}

# Step 2: Эмбеддинг шаблонов
topic_embeddings = {
    topic: model.encode(texts, convert_to_tensor=True)
    for topic, texts in templates.items()
}

# Шаг 3: Функция подбора ответа
# Вход: пользовательское сообщение
# Цель: найти тему + ближайший шаблон
# Выход: текст ответа
def get_response(user_msg: str) -> str:
    msg_emb = model.encode(user_msg, convert_to_tensor=True)
    # выбор темы по максимальной близости к среднему эмбеддингу шаблонов
    scores = {t: util.cos_sim(msg_emb, emb).max().item() for t, emb in topic_embeddings.items()}
    best_topic = max(scores, key=scores.get)
    # выбор конкретного шаблона
    sims = util.cos_sim(msg_emb, topic_embeddings[best_topic])
    idx = sims.argmax().item()
    return templates[best_topic][idx]

# Пример использования
if __name__ == '__main__':
    print(get_response("Мне трудно общаться с коллегами на работе"))
