from PIL import Image, ImageDraw, ImageFont

# Размер изображения
image_width = 400
image_height = 100

# Создаём изображение с оранжевым фоном (RGB: 250, 100, 0)
image = Image.new('RGB', (image_width, image_height), color=(250, 100, 0))
draw = ImageDraw.Draw(image)

# Укажите текст
text = "Погнали кодить!"

# Попробуем использовать более качественный шрифт
try:
    font = ImageFont.truetype("arial.ttf", 40)  # Увеличиваем размер шрифта до 40
except IOError:
    font = ImageFont.load_default()  # Используем стандартный шрифт, если Arial не найден

# Получаем размер текста
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]  # Ширина текста
text_height = bbox[3] - bbox[1]  # Высота текста

# Рассчитываем координаты для центрирования текста
x = (image_width - text_width) / 2
y = (image_height - text_height) / 2

# Добавление тени (для улучшения читаемости)
shadow_offset = 3  # Смещение тени
draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill="black")

# Рисуем белый текст на оранжевом фоне
draw.text((x, y), text, font=font, fill="white")

# Сохраняем изображение
image.save("output_image.png")
image.show()

# Выводим размеры текста
print(f"Ширина текста: {text_width}, Высота текста: {text_height}")
