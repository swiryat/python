from music21 import stream, note, midi

def create_melody(pitches, durations=None):
    """
    Создает музыкальную партию на основе списка нот и их длительностей.
    
    :param pitches: Список строк с нотами (например, ['C4', 'D4', 'E4']).
    :param durations: Список длительностей нот (например, [1, 0.5, 1]). 
                      Если не указано, используется длительность 1 для всех.
    :return: Объект music21.stream.Part с мелодией.
    """
    part = stream.Part()

    # Если длительности не заданы, используем 1 для всех нот
    if durations is None:
        durations = [1] * len(pitches)

    # Проверяем, что длины списков совпадают
    if len(pitches) != len(durations):
        raise ValueError("Длина списка нот и длительностей должна совпадать.")

    # Добавляем ноты в партию
    for pitch, duration in zip(pitches, durations):
        try:
            part.append(note.Note(pitch, quarterLength=duration))
        except Exception as e:
            print(f"Ошибка при добавлении ноты {pitch}: {e}")

    return part

def save_midi(score, filename='melody.mid'):
    """
    Сохраняет партитуру в формате MIDI.
    
    :param score: Объект music21.stream.Score для сохранения.
    :param filename: Имя выходного MIDI-файла.
    """
    score.write('midi', fp=filename)
    print(f"MIDI-файл '{filename}' успешно создан!")

def main():
    # Список нот и их длительностей
    pitches = [
        'C4', 'D4', 'E4', 'C4', 'G3', 'E4', 'F4', 'E4',
        'D4', 'C4', 'G3', 'E4', 'C4', 'D4', 'E4', 'C4',
        'G3', 'E4', 'F4', 'E4', 'D4', 'C4', 'G3', 'E4'
    ]
    durations = [1] * len(pitches)  # Все ноты четвертные

    # Создаем партитуру и добавляем мелодию
    score = stream.Score()
    part = create_melody(pitches, durations)
    score.append(part)

    # Сохраняем партитуру в MIDI
    save_midi(score, 'prayer_melody.mid')

if __name__ == "__main__":
    main()
