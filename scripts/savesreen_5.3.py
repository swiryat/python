import os, time, hashlib
import cv2, numpy as np, pytesseract, pyautogui
from PIL import Image
import keyboard

# === 1) Настройки ===
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

OUT_DIR    = "output_auto"
IMG_DIR    = os.path.join(OUT_DIR, "imgs")
TXT_PATH   = os.path.join(OUT_DIR, "output.txt")
os.makedirs(IMG_DIR, exist_ok=True)

# Размер области (скриншота)  
# — выбираем один раз через Enter (как раньше)  
print("→ Наведите мышь в ВЕРХНИЙ‑ЛЕВЫЙ угол области и нажмите Enter"); input()
x0, y0 = pyautogui.position()
print("→ Наведите мышь в НИЖНИЙ‑ПРАВЫЙ угол области и нажмите Enter"); input()
x1, y1 = pyautogui.position()
x0, x1 = sorted([x0, x1]);  y0, y1 = sorted([y0, y1])
W, H = x1 - x0, y1 - y0
region = (x0, y0, W, H)
print(f"Область: {region}")

# Параметры прокрутки
OVERLAP = 100     # перекрытие в пикселях
STEP = H - OVERLAP

PAUSE = 0.5       # пауза после прокрутки

# Множество для фильтрации повторов по строкам
seen_texts = set()
img_counter = 0

# Подготовка файла
with open(TXT_PATH, "w", encoding="utf-8") as f:
    f.write("OCR‑автосбор (без повторов)\r\n\r\n")

def preprocess(img: Image.Image):
    gray = img.convert("L")
    arr = np.array(gray)
    _, th = cv2.threshold(arr, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    return th

print("\nНажмите 's' чтобы стартануть автосбор. 'q' — остановить.\n")

# === 2) Автоматический цикл ===
while True:
    if keyboard.is_pressed('s'):
        print("Старт автосбора...")
        break
    time.sleep(0.1)

while True:
    # 1) Скрин, сохраняем для отладки
    shot = pyautogui.screenshot(region=region)
    img_counter += 1
    img_name = f"step_{img_counter:04d}.png"
    shot.save(os.path.join(IMG_DIR, img_name))

    # 2) OCR
    proc = preprocess(shot)
    text = pytesseract.image_to_string(proc, lang="rus+eng")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # 3) Фильтрация и запись
    new = []
    for ln in lines:
        if ln not in seen_texts:
            seen_texts.add(ln)
            new.append(ln)

    if new:
        with open(TXT_PATH, "a", encoding="utf-8") as f:
            f.write(f"[Image: {img_name}]\r\n")
            for ln in new:
                f.write(ln + "\r\n")
            f.write("\r\n")
        print(f"Записано {len(new)} новых строк из {img_name}")
    else:
        print(f"Нет новых строк в {img_name}")

    # 4) Прокрутка
    pyautogui.scroll(-STEP)       # скроллим вниз на STEP пикселей
    time.sleep(PAUSE)

    # 5) Стоп
    if keyboard.is_pressed('q'):
        print("Остановка по 'q'")
        break

print(f"\nГотово! Текст в {TXT_PATH}, картинки в {IMG_DIR}")
