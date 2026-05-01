import os
import win32gui
from PIL import ImageGrab
import pytesseract
import pyperclip

# 0. (Опционально) Явно указываем, где лежит tesseract.exe
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 1. Указываем папку с traineddata и фиксируем её в среде процесса
tessdata_dir = r"C:\Program Files\Tesseract-OCR\tessdata"
os.environ["TESSDATA_PREFIX"] = tessdata_dir

# 2. Перебираем все видимые окна и находим AnyDesk по подстроке в заголовке
def enum_windows():
    windows = []
    def _cb(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if title and win32gui.IsWindowVisible(hwnd):
            windows.append((hwnd, title))
    win32gui.EnumWindows(_cb, None)
    return windows

cands = [(h, t) for h, t in enum_windows() if "anydesk" in t.lower()]
if not cands:
    print("Не нашёл окно AnyDesk. Вот все заголовки:")
    for _, t in enum_windows():
        print("   ", t)
    raise SystemExit("Окно AnyDesk не найдено.")

hwnd, title = cands[0]
print(f"Нашёл окно: «{title}» (HWND={hwnd})")

# 3. Делаем скриншот этой области
left, top, right, bottom = win32gui.GetWindowRect(hwnd)
img = ImageGrab.grab(bbox=(left, top, right, bottom))

# 4. Смотрим, какие языки доступны в tessdata_dir
available = []
for lang in ("rus", "eng"):
    path = os.path.join(tessdata_dir, f"{lang}.traineddata")
    if os.path.isfile(path):
        available.append(lang)
    else:
        print(f"Внимание: файл {lang}.traineddata не найден в {tessdata_dir}")

if not available:
    raise RuntimeError("Нет ни rus, ни eng traineddata в указанной папке!")

lang_opt = "+".join(available)
print("Будем распознавать языки:", lang_opt)

# 5. Конфиг для tesseract: только psm (без --tessdata-dir, т.к. TESSDATA_PREFIX уже задан)
config = "--psm 6"

# 6. Запускаем OCR
try:
    text = pytesseract.image_to_string(img, lang=lang_opt, config=config)
except pytesseract.TesseractError as e:
    print("Ошибка Tesseract:", e)
    raise

# 7. Копируем в буфер обмена и выводим на экран
pyperclip.copy(text)
print("=== РЕЗУЛЬТАТ OCR (скопирован в буфер) ===\n")
print(text)
