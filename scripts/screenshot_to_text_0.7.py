import os
import win32gui, win32con, win32ui
from ctypes import windll
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import pyperclip

# 0. Указываем путь к tessdata
tessdata_dir = r"C:\Program Files\Tesseract-OCR\tessdata"
os.environ["TESSDATA_PREFIX"] = tessdata_dir

# 1. Выбираем окно AnyDesk (или активное)
hwnd = win32gui.GetForegroundWindow()
title = win32gui.GetWindowText(hwnd)
print("Снимаем активное окно:", title)

# 2. Размеры окна
left, top, right, bottom = win32gui.GetWindowRect(hwnd)
w, h = right - left, bottom - top

# 3. Создаём DC и Bitmap
hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()
bmp    = win32ui.CreateBitmap()
bmp.CreateCompatibleBitmap(mfcDC, w, h)
saveDC.SelectObject(bmp)

# 4. Печатаем окно в Memory DC
res = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
if res != 1:
    print("⚠️ PrintWindow вернул", res, "- возможно, не получилось захватить содержимое.")

# 5. Конвертируем в PIL Image
bmp_info = bmp.GetInfo()
bmp_str  = bmp.GetBitmapBits(True)
img = Image.frombuffer(
    'RGB',
    (bmp_info['bmWidth'], bmp_info['bmHeight']),
    bmp_str, 'raw', 'BGRX', 0, 1
)

# 6. Очистка ресурсов
win32gui.DeleteObject(bmp.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)

# 7. Улучшаем изображение
scale = 2
img = img.resize((w*scale, h*scale), Image.LANCZOS)
img = img.convert("L")
img = img.filter(ImageFilter.SHARPEN)
img = ImageEnhance.Contrast(img).enhance(2.5)

# 8. Проверяем языки
available = [lang for lang in ("rus","eng")
             if os.path.isfile(os.path.join(tessdata_dir, f"{lang}.traineddata"))]
if not available:
    raise RuntimeError("Нет traineddata!")
lang_opt = "+".join(available)
print("Языки:", lang_opt)

# 9. OCR
config = "--psm 3"
text = pytesseract.image_to_string(img, lang=lang_opt, config=config)

# 10. Копируем и выводим
pyperclip.copy(text)
print("\n=== OCR РЕЗУЛЬТАТ ===\n")
print(text)

# 11. Сохраняем для отладки
img.save("debug_printwindow.png")
print("\n[debug_printwindow.png сохранён]")
