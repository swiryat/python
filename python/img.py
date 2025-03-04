# Импортируем необходимые библиотеки
import os  # Для работы с файловой системой (проверка существования директорий, создание директорий)
import torch  # Для работы с PyTorch (модели машинного обучения)
import asyncio  # Для асинхронного программирования
import logging  # Для ведения логов
from diffusers import StableDiffusionPipeline  # Импортируем нужный класс из библиотеки diffusers для работы с моделями стабильной диффузии
from huggingface_hub import hf_hub_download, hf_hub_url  # Для работы с Hugging Face API, скачивания моделей
import aiohttp  # Для асинхронных HTTP-запросов

# Путь для сохранения скачанных или загруженных моделей
local_path = "./stable-diffusion-local"  # Локальная директория для хранения модели
models_cache = {}  # Словарь, который будет хранить уже загруженные модели, чтобы не загружать их повторно

# Настройка логирования: выводим информацию о процессе работы программы
logging.basicConfig(level=logging.INFO)  # Устанавливаем уровень логирования на INFO (информационные сообщения)
logger = logging.getLogger(__name__)  # Получаем логгер для текущего модуля

# Функция для получения информации о версии модели из Hugging Face
def get_model_version(model_name="runwayml/stable-diffusion-v1-5"):
    """
    Получаем информацию о последней версии модели из Hugging Face.
    """
    url = hf_hub_url(model_name, filename="pytorch_model.bin")  # Получаем URL для модели с Hugging Face
    logger.info(f"🔹 Проверка последней версии модели по URL: {url}")  # Логируем URL
    return url  # Возвращаем URL для загрузки модели

# Асинхронная функция для загрузки модели из локального хранилища или скачивания с Hugging Face
async def load_or_download_model(model_name="runwayml/stable-diffusion-v1-5", local_dir=local_path):
    """
    Асинхронно загружает модель из локального хранилища или скачивает с Hugging Face.
    """
    try:
        if model_name in models_cache:  # Проверяем, есть ли модель уже в кэше
            logger.info(f"🔹 Модель {model_name} уже загружена в память.")  # Если модель в кэше, выводим лог
            return models_cache[model_name]  # Возвращаем модель из кэша
        
        if os.path.exists(local_dir):  # Проверяем, существует ли директория с локальной моделью
            logger.info(f"🔹 Загружаем модель из локального хранилища: {local_dir}")  # Если существует, выводим лог
            pipe = StableDiffusionPipeline.from_pretrained(local_dir)  # Загружаем модель из локальной директории
        else:
            logger.info(f"🔹 Локальная модель не найдена. Скачиваем {model_name}...")  # Если директория не найдена, скачиваем модель
            pipe = await download_model_async(model_name)  # Асинхронно скачиваем модель
            save_model(pipe, local_dir)  # Сохраняем модель локально для будущих запусков

        # Определяем, на каком устройстве будет работать модель (GPU или CPU)
        device = "cuda" if torch.cuda.is_available() else "cpu"  # Проверяем, доступен ли GPU
        if device == "cuda" and torch.cuda.device_count() > 1:  # Если есть несколько доступных GPU
            device = torch.device("cuda:0")  # Используем первый доступный GPU
        pipe.to(device)  # Переводим модель на выбранное устройство
        models_cache[model_name] = pipe  # Кэшируем модель, чтобы не загружать её повторно
        logger.info(f"✅ Модель загружена и готова к использованию на {device}.")  # Логируем успешную загрузку модели
        return pipe  # Возвращаем модель

    except Exception as e:
        logger.error(f"Ошибка при загрузке или скачивании модели: {str(e)}")  # Логируем ошибку, если что-то пошло не так
        raise e  # Генерируем исключение для обработки в дальнейшем

# Асинхронная функция для скачивания модели с Hugging Face
async def download_model_async(model_name):
    """
    Асинхронно скачивает модель с Hugging Face.
    """
    url = get_model_version(model_name)  # Получаем URL для скачивания модели
    
    # Асинхронно скачиваем файл
    async with aiohttp.ClientSession() as session:  # Открываем сессию HTTP-запросов
        async with session.get(url) as response:  # Отправляем GET-запрос
            if response.status == 200:  # Если ответ успешный (код 200)
                model_path = os.path.join(local_path, model_name.split('/')[-1])  # Определяем путь для сохранения модели
                os.makedirs(local_path, exist_ok=True)  # Создаём директорию, если её нет
                with open(model_path, 'wb') as f:  # Открываем файл для записи
                    f.write(await response.read())  # Записываем содержимое файла
                logger.info(f"🔹 Модель {model_name} успешно скачана.")  # Логируем успешную загрузку
                return StableDiffusionPipeline.from_pretrained(model_path)  # Загружаем модель из скачанного пути
            else:
                logger.error(f"Не удалось скачать модель {model_name}. Статус ответа: {response.status}")  # Логируем ошибку, если скачивание не удалось
                raise Exception(f"Ошибка скачивания модели {model_name}")  # Генерируем исключение

# Функция для сохранения модели в локальной директории
def save_model(pipe, local_dir=local_path):
    """
    Сохраняет загруженную модель в указанную директорию.
    Если модель уже сохранена, обновляет только изменённые файлы.
    """
    try:
        if os.path.exists(local_dir):  # Проверяем, существует ли директория
            logger.info(f"🔹 Обновляем сохранённую модель в {local_dir}...")  # Если существует, логируем, что обновляем
        else:
            logger.info(f"🔹 Сохраняем модель в {local_dir}...")  # Если не существует, логируем, что создаём
        pipe.save_pretrained(local_dir)  # Сохраняем модель
        logger.info(f"✅ Модель успешно сохранена в {local_dir}")  # Логируем успешное сохранение
    except Exception as e:
        logger.error(f"Ошибка при сохранении модели: {str(e)}")  # Логируем ошибку, если сохранение не удалось
        raise e  # Генерируем исключение

# Асинхронная функция для генерации изображения с помощью модели
async def generate_image(pipe, prompt):
    """
    Генерирует изображение с помощью модели.
    """
    try:
        image = pipe(prompt).images[0]  # Генерируем изображение по запросу
        image.show()  # Показываем изображение
        logger.info(f"✅ Изображение успешно сгенерировано по запросу: {prompt}")  # Логируем успешную генерацию изображения
    except Exception as e:
        logger.error(f"Ошибка при генерации изображения: {str(e)}")  # Логируем ошибку, если генерация не удалась

# Основная асинхронная функция для загрузки и генерации изображений
async def main():
    # Список моделей, которые мы хотим загрузить и использовать
    model_names = ["runwayml/stable-diffusion-v1-5", "CompVis/stable-diffusion-v1-4"]
    tasks = []  # Список задач для загрузки моделей

    # Создаём задачи для каждой модели
    for model_name in model_names:
        task = load_or_download_model(model_name=model_name)  # Задача на загрузку модели
        tasks.append(task)  # Добавляем задачу в список

    # Ожидаем завершения всех задач
    models = await asyncio.gather(*tasks)  # Загружаем все модели

    # Генерация изображений для каждой загруженной модели
    for pipe in models:
        prompt = "A futuristic city with flying cars at sunset"  # Пример запроса для генерации изображения
        await generate_image(pipe, prompt)  # Генерируем изображение по запросу

# Запуск асинхронного процесса
if __name__ == "__main__":  # Если файл запускается напрямую
    asyncio.run(main())  # Запускаем асинхронную функцию main()
