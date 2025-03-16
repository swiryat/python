import pyautogui
import pytesseract
import cv2
import numpy as np

# Указываем путь к Tesseract (если нужно, измените путь в зависимости от вашей установки)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Путь к Tesseract

# Функция для захвата экрана
def capture_screenshot():
    screenshot = pyautogui.screenshot()  # Захватываем скриншот
    screenshot = np.array(screenshot)  # Преобразуем в массив numpy
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Преобразуем цветовую модель из RGB в BGR
    return screenshot

# Функция для регулировки контраста и яркости
def adjust_brightness_contrast(image, alpha=1.2, beta=50):
    # alpha - коэффициент контраста, beta - коэффициент яркости
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image

# Функция для преобразования в черно-белое изображение
def convert_to_black_and_white(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Преобразуем в оттенки серого
    _, black_and_white = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # Простой порог
    return black_and_white

# Функция для извлечения текста из изображения
def extract_text_from_image(image):
    adjusted_image = adjust_brightness_contrast(image)  # Настроить яркость и контраст
    bw_image = convert_to_black_and_white(adjusted_image)  # Преобразуем в черно-белое изображение
    text = pytesseract.image_to_string(bw_image)  # Извлекаем текст с помощью Tesseract
    return text

# Захват экрана
screenshot = capture_screenshot()

# Извлечение текста с преобразованием в черно-белое изображение
text = extract_text_from_image(screenshot)

# Выводим результат
print("Распознанный текст:")
print(text)

# Отображение исходного скриншота
cv2.imshow('Original Screenshot', screenshot)

# Отображение изображения с настроенным контрастом и яркостью
adjusted_screenshot = adjust_brightness_contrast(screenshot)
bw_screenshot = convert_to_black_and_white(adjusted_screenshot)
cv2.imshow('Adjusted Screenshot', adjusted_screenshot)
cv2.imshow('Black and White Screenshot', bw_screenshot)

# Ожидание нажатия клавиши для закрытия окон
cv2.waitKey(0)
cv2.destroyAllWindows()
