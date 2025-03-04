import fitz
from PIL import Image
import pytesseract
import io
from googletrans import Translator

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def translate_black_text(pdf_path, target_language):
    try:
        pdf_document = fitz.open(pdf_path)

        if not pdf_document:
            raise Exception("Failed to open PDF document")

        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Получаем изображение из страницы
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                try:
                    # Добавим проверку типа, чтобы обработать только изображения
                    if not isinstance(img, fitz.Image):
                        continue

                    base_image = pdf_document.extract_image(img_index)
                    image_bytes = base_image["image"]

                    image = Image.open(io.BytesIO(image_bytes))
                    x, y, width, height = img["rect"]
                    text = pytesseract.image_to_string(image.crop((x, y, x + width, y + height)))

                    if text:
                        translated_text = translate_text(text, target_language)

                        if translated_text:
                            print(f"Original text: {text}")
                            print(f"Translated text: {translated_text}")
                        else:
                            print("Translation error: Translated text is None")
                    else:
                        print("OCR error: Unable to extract text from the image")
                except Exception as e:
                    print(f"Image processing error: {e}")

    except Exception as e:
        print(f"PDF processing error: {e}")

if __name__ == "__main__":
    pdf_path = 'C:/Users/swer/AlgorithmsNotesForProfessionals.pdf'
    target_language = 'ru'
    translate_black_text(pdf_path, target_language)
