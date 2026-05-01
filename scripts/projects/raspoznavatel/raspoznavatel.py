import cv2
import pytesseract

# Укажите путь к tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Загружаем изображение
image_path = "C:\\Users\\swer\\Pictures\\screen\\2025-03-05 123304.png"
image = cv2.imread(image_path)

# Преобразование изображения в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применяем пороговую обработку (бинаризация)
_, thresholded_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Сохраняем обработанное изображение для проверки
cv2.imwrite("processed_image.png", thresholded_image)

# Теперь используем Tesseract для извлечения текста
text = pytesseract.image_to_string(thresholded_image, lang='rus')

# Печатаем распознанный текст
print(text)
