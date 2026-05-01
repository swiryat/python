import os
import win32gui
from PIL import Image, ImageFilter, ImageEnhance, Image
import pytesseract
import pyperclip

# Если mss установлен, раскомментируйте:
# from mss import mss

# 0. Путь к моделям Tesseract
tessdata_dir = r"C:\Program Files\Tesseract-OCR\tessdata"
os.environ["TESSDATA_PREFIX"] = tessdata_dir

def enum_windows():
    """Возвращает список (hwnd, title) всех видимых окон с заголовками."""
    result = []
    def _cb(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if title and win32gui.IsWindowVisible(hwnd):
            result.append((hwnd, title))
    win32gui.EnumWindows(_cb, None)
    return result

# 1. Собираем окна и фильтруем по anydesk
all_windows = enum_windows()
cands = [(h, t) for h, t in all_windows if "anydesk" in t.lower()]
if not cands:
    # Если ни одно не содержит "anydesk", позволяем выбрать из всех
    cands = all_windows

# 2. Выводим список и запрашиваем выбор
print("Выберите окно для скриншота:")
for idx, (_, title) in enumerate(cands):
    print(f"  [{idx}] {title}")
sel = input("Номер окна: ").strip()
try:
    sel_idx = int(sel)
    hwnd, title = cands[sel_idx]
except (ValueError, IndexError):
    raise SystemExit("Неверный ввод. Скрипт завершён.")

print(f"Снимем окно: «{title}» (HWND={hwnd})")

# 3. Захват области окна
left, top, right, bottom = win32gui.GetWindowRect(hwnd)

# Вариант А: через mss (раскомментировать, если установлен)
# with mss() as sct:
#     mon = {"left": left, "top": top, "width": right-left, "height": bottom-top}
#     raw = sct.grab(mon)
#     img = Image.frombytes("RGB", raw.size, raw.rgb)

# Вариант B: через pyautogui (если mss не установлен)
import pyautogui
w, h = right - left, bottom - top
img = pyautogui.screenshot(region=(left, top, w, h))
img = Image.frombytes("RGB", img.size, img.tobytes())

# 4. Улучшаем изображение
scale = 2
img = img.resize((img.width*scale, img.height*scale), Image.LANCZOS)
img = img.convert("L")
img = img.filter(ImageFilter.SHARPEN)
img = ImageEnhance.Contrast(img).enhance(2.5)

# 5. Проверяем модели
available = []
for lang in ("rus", "eng"):
    path = os.path.join(tessdata_dir, f"{lang}.traineddata")
    if os.path.isfile(path):
        available.append(lang)
    else:
        print(f"⚠️ {lang}.traineddata не найдено в {tessdata_dir}")
if not available:
    raise RuntimeError("Нет моделей OCR!")

lang_opt = "+".join(available)
print("Языки для OCR:", lang_opt)

# 6. Запускаем OCR
config = "--psm 3"
try:
    text = pytesseract.image_to_string(img, lang=lang_opt, config=config)
except pytesseract.TesseractError as e:
    print("Ошибка Tesseract:", e)
    raise

# 7. Копируем и выводим результат
pyperclip.copy(text)
print("\n=== РЕЗУЛЬТАТ OCR (скопирован в буфер) ===\n")
print(text)

# 8. Сохраняем отладочный скрин
img.save("debug_screenshot_v06.png")
print("\n[Отладочный скрин сохранён как debug_screenshot_v06.png]")
