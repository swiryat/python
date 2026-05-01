import os                       # модуль для работы с файловой системой (папки, пути)
import time                     # модуль для управления задержками
import hashlib                  # модуль для вычисления MD5‑хешей строк (для фильтрации повторов)

import cv2                      # OpenCV — для обработки изображений (бинаризация)
import numpy as np             # NumPy — представление изображения в виде массива
import pytesseract             # pytesseract — обёртка для Tesseract OCR
import pyautogui               # pyautogui — захват экрана и получение положения мыши
from PIL import Image          # PIL (Pillow) — для конвертации изображения в оттенки серого
import keyboard                 # keyboard — чтение нажатий клавиш

# === 1) Настройки и подготовка папок для вывода ===

# Указываем путь к исполняемому файлу Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

OUT_DIR    = "output_auto"                         # корневая папка для всех результатов
IMG_DIR    = os.path.join(OUT_DIR, "imgs")         # папка для сохранённых скриншотов
TXT_PATH   = os.path.join(OUT_DIR, "output.txt")   # файл для записи распознанного текста

# создаём папку для картинок (если ещё не существует)
os.makedirs(IMG_DIR, exist_ok=True)

# === 2) Выбор области захвата одним кликом Enter в двух точках ===

print("→ Наведите мышь в ВЕРХНИЙ‑ЛЕВЫЙ угол области и нажмите Enter"); input()
x0, y0 = pyautogui.position()   # фиксируем координаты верхнего‑левого угла
print(f"  Зафиксировали верхний‑левый: ({x0}, {y0})")

print("→ Наведите мышь в НИЖНИЙ‑ПРАВЫЙ угол области и нажмите Enter"); input()
x1, y1 = pyautogui.position()   # фиксируем координаты нижнего‑правого угла
print(f"  Зафиксировали нижний‑правый: ({x1}, {y1})")

# Нормализуем: убедимся, что x0<x1 и y0<y1
x0, x1 = sorted([x0, x1])
y0, y1 = sorted([y0, y1])

# Вычисляем ширину (W) и высоту (H) области
W, H = x1 - x0, y1 - y0
region = (x0, y0, W, H)         # кортеж, описывающий область захвата
print(f"Область захвата экрана: {region}")

# === 3) Параметры автопрокрутки и фильтрации ===

OVERLAP = 100                   # количество пикселей перекрытия между скринами
STEP = H - OVERLAP              # на сколько пикселей скроллим вниз за шаг
PAUSE = 0.5                     # пауза в секундах после каждой прокрутки

seen_texts = set()              # множество для хранения уже записанных строк
img_counter = 0                 # счётчик сохранённых картинок

# Подготавливаем текстовый файл: перезаписываем или создаём новый
with open(TXT_PATH, "w", encoding="utf-8") as f:
    f.write("OCR‑автосбор (без повторов)\r\n\r\n")  # заголовок в файле

# === 4) Функция предварительной обработки изображения ===

def preprocess(img: Image.Image) -> np.ndarray:
    """
    Принимает PIL‑изображение, конвертирует его в чёрно‑белое (градации серого),
    а затем выполняет пороговую бинаризацию OTSU для улучшения контраста перед OCR.
    """
    gray = img.convert("L")             # конвертируем RGB→оттенки серого
    arr  = np.array(gray)               # переводим в NumPy‑массив
    # OTSU‑бинаризация: автоматически подбирается порог, шумы убираются
    _, th = cv2.threshold(arr, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    return th                          # возвращаем бинарное изображение

# === 5) Ожидание команды старта ===

print("\nНажмите 's', чтобы запустить автосбор. Нажмите 'q', чтобы остановить без старта.\n")
# ждём, пока пользователь нажмёт 's'
while True:
    if keyboard.is_pressed('s'):
        print("Старт автосбора...")
        break
    if keyboard.is_pressed('q'):
        print("Прервано пользователем до старта.")
        exit(0)
    time.sleep(0.1)                   # короткая задержка, чтобы снизить нагрузку

# === 6) Основной автоматический цикл ===

print("\nАвтосбор запущен: скриншоты → OCR → запись. Для остановки нажмите 'q'.\n")
while True:
    # 6.1) Захват скриншота выбранной области
    shot = pyautogui.screenshot(region=region)
    img_counter += 1
    img_name = f"step_{img_counter:04d}.png"
    shot_path = os.path.join(IMG_DIR, img_name)
    shot.save(shot_path)             # сохраняем скриншот для наглядности

    # 6.2) OCR‑распознавание с предварительной обработкой
    proc = preprocess(shot)          # бинаризуем скриншот
    text = pytesseract.image_to_string(proc, lang="rus+eng")  # получаем строку
    # разбиваем на отдельные непустые строки и убираем пробелы
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # 6.3) Фильтрация новых строк и запись
    new_lines = []
    for ln in lines:
        if ln not in seen_texts:     # если строка ещё не была записана
            seen_texts.add(ln)       # помечаем её
            new_lines.append(ln)     # добавляем в список новых

    if new_lines:
        # открываем файл и дописываем: сначала ссылка на картинку, потом новые строки
        with open(TXT_PATH, "a", encoding="utf-8") as f:
            f.write(f"[Image: {img_name}]\r\n")
            for ln in new_lines:
                f.write(ln + "\r\n")
            f.write("\r\n")
        print(f"✔ Записано {len(new_lines)} новых строк из {img_name}")
    else:
        print(f"— Новых строк не найдено в {img_name}")

    # 6.4) Прокрутка вниз на STEP пикселей (H - OVERLAP)
    pyautogui.scroll(-STEP)
    time.sleep(PAUSE)                # ждём, чтобы страница успела прокрутиться

    # 6.5) Проверка клавиши 'q' для остановки
    if keyboard.is_pressed('q'):
        print("\nОстановка автосбора по ключу 'q'.")
        break

# === 7) Завершение работы ===
print(f"\nГотово! Текст сохранён в: {TXT_PATH}")
print(f"Картинки сохранены в папке: {IMG_DIR}")