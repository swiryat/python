import os
import sqlite3
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch

# ------------- Настройки -------------
MODEL_NAME = "gpt2"                      # или ваша локальная модель
SAVED_MODEL_DIR = "./saved_model"
DB_PATH = "./chat_history.db"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ------------- Инициализация БД -------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        role        TEXT,       -- 'user' или 'bot'
        message     TEXT,
        timestamp   TEXT
    )""")
    conn.commit()
    return conn

# ------------- Функции работы с БД -------------
def save_message(conn, role, message):
    ts = datetime.utcnow().isoformat()
    conn.execute("INSERT INTO history (role, message, timestamp) VALUES (?, ?, ?)",
                 (role, message, ts))
    conn.commit()

def load_history(conn, limit=10):
    c = conn.cursor()
    c.execute("SELECT role, message FROM history ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()[::-1]
    # Возвращаем список кортежей [(role, msg), ...]
    return rows

# ------------- Загрузка или создание модели -------------
def load_or_init_model():
    if os.path.isdir(SAVED_MODEL_DIR):
        print("Loading model from", SAVED_MODEL_DIR)
        tokenizer = AutoTokenizer.from_pretrained(SAVED_MODEL_DIR)
        model = AutoModelForCausalLM.from_pretrained(SAVED_MODEL_DIR)
    else:
        print("Downloading model:", MODEL_NAME)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        os.makedirs(SAVED_MODEL_DIR, exist_ok=True)
        tokenizer.save_pretrained(SAVED_MODEL_DIR)
        model.save_pretrained(SAVED_MODEL_DIR)
    model.to(DEVICE)
    return tokenizer, model

# ------------- Генерация ответа -------------
def generate_response(tokenizer, model, prompt, max_length=200):
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    outputs = model.generate(**inputs,
                             max_new_tokens=100,
                             pad_token_id=tokenizer.eos_token_id,
                             do_sample=True,
                             top_p=0.9,
                             temperature=0.8)
    resp = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return resp[len(prompt):].strip()

# ------------- Основной чат-цикл -------------
def chat_loop():
    conn = init_db()
    tokenizer, model = load_or_init_model()
    print("Бот готов! Начните разговор (введите 'exit' для выхода).")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break

        # Сохраняем запрос
        save_message(conn, "user", user_input)

        # Собираем последние n сообщений для контекста
        history = load_history(conn, limit=6)
        prompt = ""
        for role, msg in history:
            prefix = "User: " if role=="user" else "Bot: "
            prompt += prefix + msg + "\n"
        prompt += "Bot: "

        # Генерация
        bot_reply = generate_response(tokenizer, model, prompt)
        print("Bot:", bot_reply)

        # Сохраняем ответ
        save_message(conn, "bot", bot_reply)

    # При выходе — сохраняем финальную модель (без дообучения)
    model.save_pretrained(SAVED_MODEL_DIR)
    tokenizer.save_pretrained(SAVED_MODEL_DIR)
    conn.close()

# ------------- Скрипт для дообучения (fine-tuning) -------------
def fine_tune():
    conn = init_db()
    # Собираем всё из таблицы
    rows = conn.execute("SELECT role, message FROM history ORDER BY id").fetchall()
    # Формируем обучающие примеры: "User: xxx\nBot: yyy\n"
    texts = []
    for i in range(0, len(rows)-1, 2):
        if rows[i][0]=="user" and rows[i+1][0]=="bot":
            texts.append(f"User: {rows[i][1]}\nBot: {rows[i+1][1]}\n")
    # Сохраняем в файл
    with open("train_data.txt", "w", encoding="utf-8") as f:
        for t in texts:
            f.write(t)

    # Создаём датасет
    from datasets import load_dataset
    ds = load_dataset("text", data_files="train_data.txt")["train"]

    # Переинициализируем токенизатор и модель
    tokenizer = AutoTokenizer.from_pretrained(SAVED_MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(SAVED_MODEL_DIR).to(DEVICE)

    # Токенизация
    def tokenize_fn(ex):
        return tokenizer(ex["text"], truncation=True, max_length=512)
    ds = ds.map(tokenize_fn, batched=True, remove_columns=["text"])

    # Запускаем тренировку
    args = TrainingArguments(
        output_dir="./finetuned",
        per_device_train_batch_size=1,
        num_train_epochs=1,
        logging_steps=10,
        save_steps=100,
        push_to_hub=False,
    )
    trainer = Trainer(model=model, args=args, train_dataset=ds)
    trainer.train()

    # Сохраняем дообученную модель поверх старой
    model.save_pretrained(SAVED_MODEL_DIR)
    tokenizer.save_pretrained(SAVED_MODEL_DIR)
    print("Финетюнинг завершён, новая модель сохранена в", SAVED_MODEL_DIR)
    conn.close()

# ------------- Вызов -------------
if __name__ == "__main__":
    print("1) Chat\n2) Fine-tune\nВыберите режим (1/2):", end=" ")
    mode = input().strip()
    if mode == "1":
        chat_loop()
    elif mode == "2":
        fine_tune()
    else:
        print("Неверный режим.")
