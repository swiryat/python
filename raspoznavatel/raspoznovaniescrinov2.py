import pytesseract
import cv2
import os

# Указываем путь к Tesseract (если нужно, измените путь в зависимости от вашей установки)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Путь к Tesseract

# Функция для регулировки контраста и яркости
def adjust_brightness_contrast(image, alpha=1.2, beta=50):
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image

# Функция для адаптивной бинаризации с использованием Гауссова размытия
def adaptive_thresholding(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Преобразуем в оттенки серого
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Применяем Гауссово размытие для уменьшения шума
    bw_image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)  # Адаптивная бинаризация
    return bw_image

# Функция для извлечения текста из изображения
def extract_text_from_image(image):
    adjusted_image = adjust_brightness_contrast(image)  # Настроить яркость и контраст
    bw_image = adaptive_thresholding(adjusted_image)  # Адаптивная бинаризация
    text = pytesseract.image_to_string(bw_image, lang='eng+rus')  # Извлекаем текст на английском и русском языках
    return text

# Функция для обработки и сохранения текста из изображений в файлы
def process_and_save_images(folder_path, output_folder):
    # Создаем папку для сохранения результатов, если её нет
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получаем список всех файлов в папке
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)  # Загружаем изображение

            # Проверка на успешную загрузку изображения
            if image is None:
                print(f"Ошибка: Не удалось загрузить изображение по пути {image_path}")
                continue

            # Извлечение текста
            text = extract_text_from_image(image)

            # Очистка текста от нежелательных символов, если есть
            text = text.replace('©', '')  # Пример очистки символов, которые могут вызвать проблемы
            text = text.replace('\xa5', 'Y')  # Заменить символ, который вызывает ошибку

            # Сохранение текста в файл с таким же именем, как у изображения
            output_filename = f'{os.path.splitext(filename)[0]}.txt'  # Создаем имя для текстового файла
            output_path = os.path.join(output_folder, output_filename)

            # Запись текста в файл с кодировкой utf-8
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)  # Записываем извлеченный текст в файл
                print(f'Результат для {filename} сохранён в {output_filename}')
            except Exception as e:
                print(f"Ошибка при сохранении текста для {filename}: {e}")

# Папка с изображениями и папка для сохранения результатов
folder_path = r'C:\Users\swer\Pictures\screen'  # Замените на путь к вашей папке с изображениями
output_folder = r'C:\Users\swer\Pictures\screen\results'  # Путь, где будут сохраняться текстовые файлы

# Обработка и сохранение результатов
process_and_save_images(folder_path, output_folder)
