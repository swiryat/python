import transformers
import torch
import os

# Проверка версий библиотек
print(f"Transformers version: {transformers.__version__}")
print(f"Torch version: {torch.__version__}")

# Путь для сохранения модели
model_save_path = "./saved_model"

# Функция для сохранения модели и токенизатора
def save_model(model, tokenizer, save_path):
    # Создаем директорию, если её нет
    os.makedirs(save_path, exist_ok=True)

    # Сохраняем модель и токенизатор
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)
    print(f"Модель и токенизатор сохранены в {save_path}")

# Функция для загрузки модели и токенизатора
def load_model(save_path):
    model = transformers.AutoModel.from_pretrained(save_path)
    tokenizer = transformers.AutoTokenizer.from_pretrained(save_path)
    print(f"Модель и токенизатор загружены из {save_path}")
    return model, tokenizer

# Проверка наличия сохраненной модели
if os.path.exists(model_save_path):
    print("Загружаем модель из сохраненной версии...")
    model, tokenizer = load_model(model_save_path)
else:
    print("Сохраняем новую модель...")
    # Пример загрузки новой модели BERT
    model = transformers.AutoModel.from_pretrained("bert-base-uncased")
    tokenizer = transformers.AutoTokenizer.from_pretrained("bert-base-uncased")

    # Сохраняем модель и токенизатор
    save_model(model, tokenizer, model_save_path)

# Пример использования модели для обработки текста
inputs = tokenizer("Hello, world!", return_tensors="pt")
outputs = model(**inputs)
print("Тензор выходных данных: ", outputs)
