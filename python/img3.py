import os
import torch
import asyncio
import logging
from transformers import BertTokenizer, BertForSequenceClassification  # Для RuBERT
from deep_pavlov import build_model, configs  # Для DeepPavlov
from huggingface_hub import hf_hub_download, hf_hub_url
import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Путь для сохранения моделей
local_path = "./text-models"
models_cache = {}

# Функция для получения информации о версии модели с Hugging Face
def get_model_version(model_name="DeepPavlov/rubert-base-cased"):
    url = hf_hub_url(model_name, filename="pytorch_model.bin")
    logger.info(f"🔹 Проверка последней версии модели по URL: {url}")
    return url

# Асинхронная функция для загрузки модели с проверкой актуальности
async def load_or_download_model(model_name="DeepPavlov/rubert-base-cased", local_dir=local_path, force_download=False):
    """
    Асинхронно загружает модель для обработки текста с возможностью обновления.
    """
    try:
        # Проверка, есть ли модель уже в кэше
        if model_name in models_cache:  
            logger.info(f"🔹 Модель {model_name} уже загружена в память.")
            return models_cache[model_name]
        
        model_path = os.path.join(local_dir, "pytorch_model.bin")
        
        # Проверяем, есть ли модель в локальной директории
        if os.path.exists(model_path) and not force_download:
            logger.info(f"🔹 Модель найдена в локальной директории: {model_path}")
            pipe = build_model(configs.classifiers.rusentiment, download=False)  # Загружаем без скачивания
        else:
            logger.info(f"🔹 Локальная модель не найдена или обновление принудительное. Скачиваем {model_name}...")
            pipe = await download_model_async(model_name)
            save_model(pipe, local_dir)

        # Кэшируем модель для использования в памяти
        models_cache[model_name] = pipe
        logger.info(f"✅ Модель {model_name} загружена и готова к использованию.")
        return pipe
    except Exception as e:
        logger.error(f"Ошибка при загрузке или скачивании модели: {str(e)}")
        raise e

# Асинхронная функция для скачивания модели с Hugging Face
async def download_model_async(model_name):
    """
    Асинхронно скачивает модель с Hugging Face.
    """
    url = get_model_version(model_name)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                model_path = os.path.join(local_path, model_name.split('/')[-1])
                os.makedirs(local_path, exist_ok=True)
                with open(model_path, 'wb') as f:
                    f.write(await response.read())
                logger.info(f"🔹 Модель {model_name} успешно скачана.")
                return build_model(configs.classifiers.rusentiment, download=True)
            else:
                logger.error(f"Не удалось скачать модель {model_name}. Статус ответа: {response.status}")
                raise Exception(f"Ошибка скачивания модели {model_name}")

# Функция для сохранения модели в локальной директории
def save_model(pipe, local_dir=local_path):
    """
    Сохраняет модель в локальной директории.
    """
    try:
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        logger.info(f"🔹 Сохраняем модель в {local_dir}...")
        pipe.save_pretrained(local_dir)
        logger.info(f"✅ Модель успешно сохранена в {local_dir}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении модели: {str(e)}")
        raise e

# Асинхронная функция для использования модели с текстом
async def process_text(pipe, text):
    """
    Обрабатывает текст с помощью модели.
    """
    try:
        # Для модели DeepPavlov
        result = pipe([text])
        logger.info(f"✅ Текст успешно обработан: {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при обработке текста: {str(e)}")

# Основная асинхронная функция
async def main():
    # Список моделей, которые мы хотим загрузить и использовать
    model_names = ["DeepPavlov/rubert-base-cased", "DeepPavlov/rusentiment"]
    tasks = []

    # Создаём задачи для каждой модели
    for model_name in model_names:
        task = load_or_download_model(model_name=model_name)
        tasks.append(task)

    # Загружаем все модели
    models = await asyncio.gather(*tasks)

    # Пример текста для обработки
    text = "Это пример текста для обработки с использованием модели."

    # Обрабатываем текст для каждой модели
    for pipe in models:
        await process_text(pipe, text)

if __name__ == "__main__":
    asyncio.run(main())
