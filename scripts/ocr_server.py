import mss
import cv2
import numpy as np
import pytesseract
from flask import Flask, jsonify
import threading

# Укажи путь к tesseract (если Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Координаты захвата области экрана
screen_region = {
    'top': 200,
    'left': 300,
    'width': 600,
    'height': 300
}

# Снимок экрана + сохранение оригинала
def capture_screen(region):
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        original = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        cv2.imwrite("original.png", original)  # 💾 сохранить оригинал
        return original

# Предобработка изображения
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("preprocessed.png", thresh)  # 💾 сохранить для анализа
    return thresh

# Распознавание текста
def recognize_text(image):
    config = r'--oem 3 --psm 6 -l rus+eng'
    text = pytesseract.image_to_string(image, config=config)
    print("📄 Распознанный текст:\n", text)
    return text

# Классификация текста
def classify_text(text):
    if any(sym in text for sym in "=^√∞∫Σπ⋅×÷∂∇") or '\\frac' in text:
        return "math"
    elif any(kw in text for kw in ["def", "class", "import", "for", "{", "}", ":", "()", "=="]):
        return "code"
    else:
        return "text"

# Главная логика
def process_ocr():
    image = capture_screen(screen_region)
    processed = preprocess_image(image)
    text = recognize_text(processed)
    content_type = classify_text(text)
    return {
        "type": content_type,
        "raw_text": text.strip()
    }

# Flask сервер
app = Flask(__name__)

@app.route("/")
def index():
    return "<h3>OCR-сервер работает. Перейдите на <a href='/get_text'>/get_text</a> для получения распознанного текста.</h3>"

@app.route("/get_text")
def get_text():
    result = process_ocr()
    return jsonify(result)

def run_server():
    app.run(host='0.0.0.0', port=5000, debug=False)

# Запуск
if __name__ == "__main__":
    print("🚀 OCR сервер запущен: http://localhost:5000/get_text")
    print("📂 Снимки сохраняются как original.png и preprocessed.png")
    thread = threading.Thread(target=run_server)
    thread.start()
