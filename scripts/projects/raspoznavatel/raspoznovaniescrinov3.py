import pyautogui
import pytesseract
from PIL import ImageGrab
import time

# Настроить путь к tesseract, если нужно
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Захват экрана
screenshot = ImageGrab.grab(bbox=(0, 0, 800, 600))  # Параметры захвата экрана
screenshot.save('screenshot.png')

# Распознавание текста с помощью Tesseract
text = pytesseract.image_to_string(screenshot)

# Печать распознанного текста
print("Распознанный текст:", text)

# Ожидание, чтобы дать время для активации окна (например, Visual Studio Code)
time.sleep(2)

# Ввод текста в активное окно
pyautogui.typewrite(text)
