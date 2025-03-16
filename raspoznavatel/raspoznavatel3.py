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

def improve_contrast(image):
    """Улучшение контраста и яркости изображения."""
    alpha = 1.5  # Контрастность (чем выше, тем сильнее контраст)
    beta = 50    # Яркость (положительное значение увеличивает яркость)
    improved = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return improved

def extract_text_from_image(image):
    """Распознает текст на изображении."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Переводим в ЧБ

    # Улучшаем контрастность изображения
    improved_image = improve_contrast(gray)
    
    # Применяем различные фильтры для улучшения качества изображения
    blurred = cv2.GaussianBlur(improved_image, (5, 5), 0)  # Применение размытия для устранения шума
    _, thresholded = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)  # Пороговое преобразование
    
    # Распознаем текст с улучшенным изображением
    text = pytesseract.image_to_string(thresholded, lang="eng+rus")
    
    # Логирование результата
    print("Распознанный текст (после обработки):", text)
    
    # Отображение изображения для отладки
    cv2.imshow("Processed Image", thresholded)
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
