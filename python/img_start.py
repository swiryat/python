from diffusers import StableDiffusionPipeline
import torch
import os

local_path = "./stable-diffusion-local"

# Проверяем, существует ли локальная модель
if os.path.exists(local_path) and os.path.isdir(local_path):
    # Загружаем модель из локальной папки
    pipe = StableDiffusionPipeline.from_pretrained(local_path)
    print("Модель загружена из локального пути.")
else:
    # Если модели нет, загружаем её с Hugging Face
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipe.to("cuda")  # Используем GPU для ускорения
    pipe.save_pretrained(local_path)  # Сохраняем модель локально
    print("Модель загружена и сохранена локально.")

# Генерируем изображение по текстовому описанию
prompt = "A futuristic city with flying cars at sunset"
image = pipe(prompt).images[0]

# Показываем изображение
image.show()
