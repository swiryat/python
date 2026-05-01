import time                            # Шаг 1: для тайминга
import win32gui, win32con              # Шаг 2: работа с окнами Windows
from PIL import ImageGrab              # Шаг 3: захват экрана
import pytesseract                     # Шаг 4: OCR
import pyperclip                       # Шаг 5: буфер обмена

# Шаг 1: найти окно AnyDesk по заголовку
hwnd = win32gui.FindWindow(None, "AnyDesk")  
if not hwnd:
    raise RuntimeError("Окно AnyDesk не найдено")

# Шаг 2: получить координаты окна (л, в, п, н)
left, top, right, bottom = win32gui.GetWindowRect(hwnd)

# Шаг 3: делать скриншот только этой области
screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

# Шаг 4: распознать текст (рус./англ.)
recognized = pytesseract.image_to_string(
    screenshot, lang="rus+eng", 
    config="--psm 6"
)

# Шаг 5: (Опционально) распознать формулы через модель
def parse_formula(img) -> str:
    # здесь вы можете вызвать вашу im2latex-модель
    return "<формула в LaTeX>"

formula = parse_formula(screenshot)

# Шаг 6: собрать итоговую строку
output_text = f"{recognized}\n\n{formula}"

# Шаг 7: скопировать в буфер обмена
pyperclip.copy(output_text)

print("Результат скопирован в буфер обмена.")
time.sleep(0.5)  # можно убрать или увеличить при необходимости
