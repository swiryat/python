import librosa
import numpy as np

def preprocess_audio(audio_file):
    try:
        # Load audio file
        y, sr = librosa.load(audio_file, sr=None)  # Load with original sampling rate

        # Normalize audio data
        y_normalized = librosa.util.normalize(y)

        return y_normalized, sr

    except Exception as e:
        print(f"Error preprocessing audio: {e}")
        return None, None

# Usage example
audio_file = r'C:\Users\swer\GitHub\python\Wallem.mp3'
y, sr = preprocess_audio(audio_file)

if y is not None and sr is not None:
    # Process audio data (detect notes, etc.)
    detected_notes = detect_notes(y, sr)
    print(detected_notes)

