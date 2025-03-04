from music21 import stream, note, converter, environment, metadata, exceptions21  # Исправленный импорт

# Установите путь к LilyPond
us = environment.UserSettings()
us['lilypondPath'] = r'C:\NIPF\lilypond-2.24.4-mingw-x86_64\lilypond-2.24.4\bin\lilypond.exe'

# Создание музыкальной партитуры
score = stream.Score()
score.metadata = metadata.Metadata()
score.metadata.title = 'Господи, помилуй'
score.metadata.composer = 'Автор'
score.metadata.date = '2024'

# Определение мелодии
melody = [
    'C4', 'D4', 'E4', 'C4', 'G3', 'E4', 'F4', 'E4', 'D4', 'C4', 'G3', 'E4',
    'C4', 'D4', 'E4', 'C4', 'G3', 'E4', 'F4', 'E4', 'D4', 'C4', 'G3', 'E4',
    'C4', 'D4', 'E4', 'C4', 'G3', 'E4', 'F4', 'E4', 'D4', 'C4', 'G3', 'E4',
    'C4', 'D4', 'E4', 'C4', 'G3', 'E4', 'F4', 'E4', 'D4', 'C4', 'G3', 'E4'
]

# Создание части для мелодии
melody_part = stream.Part()
for pitch in melody:
    melody_part.append(note.Note(pitch, quarterLength=1))  # Добавление нот в партию

# Добавление мелодии в партитуру
score.append(melody_part)

# Укажите пути к выходным файлам
output_path_xml = "C:/Users/swer/GitHub/python/Gospodi_Pomiluy.xml"
output_path_pdf = "C:/Users/swer/GitHub/python/Gospodi_Pomiluy.pdf"
output_path_midi = "C:/Users/swer/GitHub/python/prayer_melody.mid"

try:
    # Запись партитуры в XML
    score.write('musicxml', fp=output_path_xml)
    print(f'Партитура успешно записана в {output_path_xml}.')

    # Конвертация в PDF с помощью LilyPond
    converter.parse(output_path_xml).write('lilypond', fp=output_path_pdf)
    print(f'Партитура успешно конвертирована в PDF: {output_path_pdf}.')
    
    # Сохранение партитуры в MIDI
    score.write('midi', fp=output_path_midi)
    print("MIDI-файл успешно создан!")

except exceptions21.Music21Exception as e:
    print(f'Ошибка при работе с music21: {e}')
except Exception as e:
    print(f'Произошла ошибка: {e}')
