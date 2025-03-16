import pyautogui
from PIL import Image

# Получаем размер экрана
screen_width, screen_height = pyautogui.size()
print(screen_width, screen_height)

# Определяем границы левой и правой половины экрана
left_half = (0, 0, screen_width // 2, screen_height)  # Левая половина экрана
right_half = (screen_width // 2, 0, screen_width // 2, screen_height)  # Правая половина экрана

# Функция для захвата экрана
def capture_screen(region):
    screenshot = pyautogui.screenshot(region=region)
    return screenshot

# Захватываем левую половину экрана
left_screenshot = capture_screen(left_half)
# Захватываем правую половину экрана
right_screenshot = capture_screen(right_half)

# Сохраняем изображения (если нужно)
left_screenshot.save("left_half.png")
right_screenshot.save("right_half.png")

# Показываем изображения (если нужно)
left_screenshot.show()
right_screenshot.show()

# Пример дальнейшей работы с этими изображениями (например, распознавание текста)
# text_left = recognize_text(left_screenshot)
# text_right = recognize_text(right_screenshot)
