import os
import win32gui
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import pyperclip
from mss import mss

# 0. Устанавливаем путь к traineddata (где лежат rus.traineddata и eng.traineddata)
tessdata_dir = r"C:\Program Files\Tesseract-OCR\tessdata"
os.environ["TESSDATA_PREFIX"] = tessdata_dir

# 1. Ищем окно AnyDesk
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
    print("Не найдено окно AnyDesk. Вот список всех окон:")
    for _, t in enum_windows():
        print("  ", t)
    raise SystemExit("Завершено.")

hwnd, title = cands[0]
print(f"Нашёл окно: «{title}» (HWND={hwnd})")

# 2. Получаем координаты окна
left, top, right, bottom = win32gui.GetWindowRect(hwnd)

# 3. Скриншот с помощью mss
with mss() as sct:
    monitor = {"left": left, "top": top, "width": right - left, "height": bottom - top}
    raw_img = sct.grab(monitor)
    img = Image.frombytes("RGB", raw_img.size, raw_img.rgb)

# 4. Преобразуем изображение: ч/б, контраст, резкость
img = img.convert("L")
img = img.filter(ImageFilter.SHARPEN)
img = ImageEnhance.Contrast(img).enhance(2.0)

# 5. Проверка наличия языков
available = []
for lang in ("rus", "eng"):
    path = os.path.join(tessdata_dir, f"{lang}.traineddata")
    if os.path.isfile(path):
        available.append(lang)
    else:
        print(f"Нет файла: {lang}.traineddata")

if not available:
    raise RuntimeError("Ни одного языка не найдено!")

lang_opt = "+".join(available)
print("Будем использовать языки:", lang_opt)

# 6. OCR
config = "--psm 6"
try:
    text = pytesseract.image_to_string(img, lang=lang_opt, config=config)
except pytesseract.TesseractError as e:
    print("Ошибка Tesseract:", e)
    raise

# 7. Копируем результат в буфер и печатаем
pyperclip.copy(text)
print("\n=== РЕЗУЛЬТАТ OCR (скопирован в буфер) ===\n")
print(text)

# 8. (опционально) сохраняем отладочное изображение
img.save("debug_screenshot.png")
