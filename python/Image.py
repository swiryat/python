from PIL import Image, ImageDraw, ImageFont

# Создаём изображение с оранжевым фоном (RGB: 255, 165, 0)
image = Image.new('RGB', (700, 100), color=(250, 100, 0))  # Указываем оранжевый цвет
draw = ImageDraw.Draw(image)

# Укажите текст
text = "Погнали, Полина кодить!"

# Попробуем использовать более крупный шрифт
try:
    font = ImageFont.truetype("arial.ttf", 40)  # Увеличиваем размер шрифта до 40
except IOError:
    font = ImageFont.load_default()  # Используем стандартный шрифт, если Arial не найден

# Получаем размер текста
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]  # Ширина текста
text_height = bbox[3] - bbox[1]  # Высота текста

# Рассчитываем координаты для центрирования текста
x = (image.width - text_width) / 2
y = (image.height - text_height) / 2

# Рисуем белый текст на оранжевом фоне
draw.text((x, y), text, font=font, fill="white")

# Сохраняем изображение
image.save("output_image.png")
image.show()

# Выводим размеры текста
print(f"Ширина текста: {text_width}, Высота текста: {text_height}")
