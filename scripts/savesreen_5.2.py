import os
import time
import hashlib

import cv2
import numpy as np
import pytesseract
import pyautogui
import keyboard
from PIL import Image

# === 1) Настройки ===
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

OUT_DIR    = "output_txt"
TXT_PATH   = os.path.join(OUT_DIR, "output.txt")
IMG_DIR    = os.path.join(OUT_DIR, "imgs")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

PAUSE      = 0.1      # короткая пауза в цикле ожидания
seen_texts = set()    # для фильтрации одинаковых распознанных текстов
seen_shots = set()    # для фильтрации повторных скриншотов
img_counter = 0       # счётчик картинок

# === 2) Вспомогательные функции ===
def preprocess(pil_img: Image.Image) -> np.ndarray:
    gray = pil_img.convert("L")
    arr  = np.array(gray)
    _, th = cv2.threshold(arr, 0, 255,
                          cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    return th

def ocr_text(img_np: np.ndarray) -> str:
    return pytesseract.image_to_string(img_np, lang="rus+eng")

# === 3) Интерактивный выбор области через Enter ===
def select_region():
    print("→ Наведите мышь в ВЕРХНИЙ‑ЛЕВЫЙ угол области и нажмите Enter.")
    input()
    x0, y0 = pyautogui.position()
    print(f"  Зафиксировали: ({x0}, {y0})")

    print("→ Наведите мышь в НИЖНИЙ‑ПРАВЫЙ угол области и нажмите Enter.")
    input()
    x1, y1 = pyautogui.position()
    x0_, x1_ = sorted([x0, x1])
    y0_, y1_ = sorted([y0, y1])
    w, h = x1_ - x0_, y1_ - y0_
    print(f"  Область: x={x0_}, y={y0_}, w={w}, h={h}")
    return (x0_, y0_, w, h)

# === 4) Основной блок ===
def main():
    global img_counter

    region = select_region()

    # инициализируем файл
    with open(TXT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write("OCR‑лог (DOS newlines)\r\n")
        f.write("Скроллите страницу вручную, затем нажмите 'c' для захвата.\r\n\r\n")

    print("\nГотово к захвату. Нажмите 'c' в этом окне, чтобы сделать снимок и распознать текст.")
    print("Повторные скриншоты и одинаковый текст будут пропущены.\n")
    while True:
        if keyboard.is_pressed('c'):
            time.sleep(0.2)  # антидребезг

            # 1) снимок области
            shot = pyautogui.screenshot(region=region)
            # 2) проверяем, не такой ли скрин уже был
            raw = shot.tobytes()
            hshot = hashlib.md5(raw).hexdigest()
            if hshot in seen_shots:
                print("— Этот экран уже захвачен, пропускаем.")
            else:
                seen_shots.add(hshot)

                # 3) сохраняем картинку
                img_counter += 1
                img_name = f"step_{img_counter:04d}.png"
                shot.save(os.path.join(IMG_DIR, img_name))

                # 4) OCR
                proc = preprocess(shot)
                text = ocr_text(proc).strip()
                # 4) OCR
                proc = preprocess(shot)
                text = ocr_text(proc).strip()

                 # ДОБАВЬ ЭТУ СТРОКУ:
                
                print(f"OCR результат: [{text}]")
                if text:
                    # фильтруем повторные тексты
                    htxt = hashlib.md5(text.encode('utf-8')).hexdigest()
                    if htxt not in seen_texts:
                        seen_texts.add(htxt)
                        # записываем картинку + текст
                        with open(TXT_PATH, "a", encoding="utf-8", newline="") as f:
                            f.write(f"[Image: {img_name}]\r\n")
                            for line in text.splitlines():
                                f.write(line + "\r\n")
                            f.write("\r\n")
                        print(f"✔ Захвачено и записано: {img_name}")
                    else:
                        print("— Текст совпадает с уже записанным, пропускаем.")
                else:
                    print("— Текст не распознан, пропускаем.")

            # ждём отпускания 'c'
            while keyboard.is_pressed('c'):
                time.sleep(PAUSE)

        elif keyboard.is_pressed('q'):
            print("\nНажата 'q' — завершаем.")
            break

        time.sleep(PAUSE)

    print(f"\nГотово! Смотрите папку `{OUT_DIR}`.")

if __name__ == "__main__":
    main()
