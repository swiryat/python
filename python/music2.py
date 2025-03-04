from music21 import stream, note, converter, environment, metadata, exceptions

# Установите путь к LilyPond
us = environment.UserSettings()
us['lilypondPath'] = r'C:\NIPF\lilypond-2.24.4-mingw-x86_64\lilypond-2.24.4\bin\lilypond.exe'

# Создание музыкальной партитуры
score = stream.Score()
score.metadata = metadata.Metadata()
score.metadata.title = 'Господи, помилуй'
score.metadata.composer = 'Автор'
score.metadata.date = '2024'

# Пример добавления мелодии
melody = stream.Part()
melody.append(note.Note("C4", quarterLength=1))
melody.append(note.Note("D4", quarterLength=1))
melody.append(note.Note("E4", quarterLength=1))

# Добавление мелодии в партитуру
score.append(melody)

# Укажите пути к выходным файлам
output_path_xml = "C:/Users/swer/GitHub/python/Gospodi_Pomiluy.xml"
output_path_pdf = "C:/Users/swer/GitHub/python/Gospodi_Pomiluy.pdf"

try:
    # Запись партитуры в XML
    score.write('musicxml', fp=output_path_xml)
    print(f'Партитура успешно записана в {output_path_xml}.')

    # Конвертация в PDF с помощью LilyPond
    converter.parse(output_path_xml).write('lilypond', fp=output_path_pdf)
    print(f'Партитура успешно конвертирована в PDF: {output_path_pdf}.')
    
except exceptions21.Music21Exception as e:
    print(f'Ошибка при работе с music21: {e}')
except Exception as e:
    print(f'Произошла ошибка: {e}')
