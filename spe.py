from google.cloud import speech_v1p1beta1 as speech

def recognize_amr(audio_file_path):
    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.AMR,
        sample_rate_hertz=8000,
        language_code="ru-RU",
    )

    response = client.recognize(config=config, audio=audio)

    recognized_text = ""
    for result in response.results:
        recognized_text += result.alternatives[0].transcript + " "

    return recognized_text.strip()

def main():
    amr_file_path = "out.amr"
    text = recognize_amr(amr_file_path)

    if text:
        print(f"Распознанный текст: {text}")
    else:
        print("Речь не распознана")

if __name__ == "__main__":
    main()
