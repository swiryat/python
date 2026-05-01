import pygetwindow as gw
import pyautogui
import time
import cv2
import pytesseract
import numpy as np

# Укажите путь к Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def capture_screen():
    """Снимает скриншот экрана и возвращает изображение."""
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Конвертируем в BGR для OpenCV
    return frame

def reduce_brightness(image, factor=0.5):
    """Уменьшает яркость изображения для ослабления светящихся букв."""
    # Если изображение в черно-белом формате (1 канал), преобразуем его в BGR (3 канала)
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Преобразуем в HSV
    hsv[:, :, 2] = hsv[:, :, 2] * factor  # Снижаем яркость
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def blur_image(image, ksize=3):
    """Применяет гауссово размытие для сглаживания контуров текста."""
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

def improve_contrast(image):
    """Улучшение контраста изображения."""
    alpha = 1.5  # Увеличиваем контрастность
    beta = 0     # Яркость
    improved = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return improved
def apply_adaptive_threshold(image):
    """Применяем адаптивную пороговую фильтрацию для улучшения контраста текста."""
    # Преобразуем в черно-белое изображение (если оно цветное)
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY, 11, 2)
    return adaptive_thresh


def extract_text_from_image(image):
    """Распознает текст на изображении."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Переводим в ЧБ

    # Снижаем яркость, чтобы текст не светился слишком сильно
    reduced_brightness_image = reduce_brightness(gray)
    
    # Улучшаем контрастность
    improved_image = improve_contrast(reduced_brightness_image)
    
    # Применяем гауссовое размытие для сглаживания
    blurred_image = blur_image(improved_image)

    # Применяем адаптивное пороговое преобразование
    thresholded_image = apply_adaptive_threshold(blurred_image)
    
    # Распознаем текст с улучшенным изображением
    text = pytesseract.image_to_string(thresholded_image, lang="eng+rus")
    
    # Логирование результата
    print("Распознанный текст (после обработки):", text)
    
    # Отображение изображения для отладки
    cv2.imshow("Processed Image", thresholded_image)
    cv2.waitKey(0)  # Ожидание клавиши для закрытия окна
    cv2.destroyAllWindows()
    
    return text.strip()  # Убираем лишние пробелы

def type_in_vscode(text):
    """Вставляет текст в VS Code."""
    try:
        vscode_window = gw.getWindowsWithTitle("Visual Studio Code")[0]  # Ищем окно по названию
        vscode_window.activate()  # Переводим его в активное состояние
        time.sleep(1)  # Ждём, чтобы окно стало активным
        pyautogui.write(text, interval=0.05)  # Вставляем текст в активное окно
    except IndexError:
        print("Не удалось найти окно Visual Studio Code.")

def get_active_window_title():
    """Возвращает название активного окна."""
    active_window = gw.getActiveWindow()
    return active_window.title if active_window else None

# Основной цикл
while True:
    screen = capture_screen()  # Захват экрана
    text = extract_text_from_image(screen)  # Распознавание текста
    
    if text:
        # Получаем название активного окна
        active_window = get_active_window_title()
        
        # Проверим, что окно действительно VS Code
        if active_window and "Visual Studio Code" in active_window:
            type_in_vscode(text)  # Вставка в редактор
        else:
            print(f"Текст был распознан, но окно не является VS Code. Активное окно: {active_window}")
    else:
        print("Текст не распознан.")
    
    time.sleep(5)  # Ждём 5 секунд перед следующим циклом
