import time
import win32gui
from PIL import ImageGrab
import pytesseract
import pyperclip

def enum_window_titles():
    """Возвращает список (hwnd, title) всех видимых окон с непустыми заголовками."""
    result = []
    def callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        # Проверяем, что окно видно и заголовок не пуст
        if title and win32gui.IsWindowVisible(hwnd):
            result.append((hwnd, title))
    win32gui.EnumWindows(callback, None)
    return result

# Шаг 1: ищем окно AnyDesk по подстроке
candidates = [(hwnd, title) for hwnd, title in enum_window_titles()
              if "anydesk" in title.lower()]
if not candidates:
    # Для отладки распечатаем все заголовки
    print("Ни одного окна AnyDesk не найдено. Список всех заголовков:")
    for hwnd, title in enum_window_titles():
        print(f"  HWND={hwnd} → «{title}»")
    raise RuntimeError("Окно AnyDesk не найдено. Проверьте заголовок.")

# Берём первое подходящее окно
hwnd, title = candidates[0]
print(f"Найдено окно: HWND={hwnd}, заголовок=«{title}»")

# Шаг 2: получаем координаты и делаем скриншот
left, top, right, bottom = win32gui.GetWindowRect(hwnd)
screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

# Шаг 3: распознаём текст
recognized = pytesseract.image_to_string(
    screenshot, lang="rus+eng", config="--psm 6"
)

# Шаг 4: (опционально) распознаём формулы
def parse_formula(img) -> str:
    # заглушка, подключите свою модель im2latex
    return "<формула в LaTeX>"

formula = parse_formula(screenshot)

# Шаг 5: копируем в буфер обмена
output_text = f"{recognized}\n\n{formula}"
pyperclip.copy(output_text)
print("Результат скопирован в буфер обмена.")
