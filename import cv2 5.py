import cv2
import numpy as np

# Функция для чтения изображения из файла
def read_image(file_path):
    return cv2.imread(file_path)

# Функция для преобразования изображения в оттенки серого
def convert_to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Функция для применения медианного размытия к изображению
def apply_median_blur(image, kernel_size):
    return cv2.medianBlur(image, kernel_size)

# Функция для изменения размера изображения
def resize_image(image, width, height):
    return cv2.resize(image, (width, height))

# Функция для сохранения изображения в файл
def save_image(file_path, image):
    cv2.imwrite(file_path, image)

# Функция для отображения изображения на экране
def display_image(title, image):
    cv2.imshow(title, image)

# Функция для замены всех цветов в изображении на синий
def replace_with_blue_color(img):
    """
    Заменяет все цвета в изображении на синий

    Args:
        img (numpy.ndarray): Изображение в формате uint8

    Returns:
        numpy.ndarray: Изображение в формате uint8 с синими цветами
    """
    blue_img = np.zeros_like(img)  # Создаем изображение с нулевыми значениями, что представляет собой черное изображение
    blue_img[:, :] = (10, 50, 150)  # Задаем все пиксели в синий цвет (в формате BGR)
    return blue_img

# Основная функция программы
def main():
    file_path = 'image.jpg'  # Путь к файлу с изображением
    img = read_image(file_path)  # Чтение изображения из файла
    if img is not None:  # Проверка успешного чтения изображения
        gray = convert_to_gray(img)  # Преобразование изображения в оттенки серого
        blur = apply_median_blur(gray, 1)  # Применение медианного размытия
        edges = cv2.Canny(blur, 15, 80)  # Обнаружение границ на изображении

        # Отображение оригинального изображения и обработанных версий
        display_image('Оригинал', img)
        display_image('Оттенки серого', gray)
        display_image('Размытое', blur)
        display_image('Границы', edges)

        # Изменение размера изображения и отображение его
        resized_img = resize_image(img, 1000, 1000)
        display_image('Измененное изображение', resized_img)

        # Сохранение обработанных изображений в файлах
        save_image('gray_image.jpg', gray)
        save_image('blurred_image.jpg', blur)
        save_image('edges_image.jpg', edges)
        save_image('resized_image.jpg', resized_img)

        # Изменение размера изображения и замена всех цветов на синий
        resized_img = resize_image(img, 3000, 3000)
        blue_color_img = replace_with_blue_color(resized_img)
        display_image('Синее изображение', blue_color_img)

        # Ожидание нажатия клавиши для завершения программы
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

# Вызов основной функции
main()
