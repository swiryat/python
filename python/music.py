from music21 import stream, note, chord, meter, tempo, key

# Создаем партитуру
score = stream.Score()

# Устанавливаем ключ C-dur (До мажор)
score.append(key.KeySignature(0))  # Без знаков

# Темп: Andante (медленно, благоговейно)
score.append(tempo.MetronomeMark(number=76)) 

# Размер: 4/4
time_signature = meter.TimeSignature('4/4')
score.append(time_signature)

# Мелодия (вокальная линия) и аккорды
melody = stream.Part()
melody.append(note.Rest(quarterLength=2))  # Вступительная пауза

# Первый фрагмент: "Господи, помилуй, Господи, помилуй"
melody.append([note.Note('C4', quarterLength=1), note.Note('D4', quarterLength=1)])
melody.append([note.Note('E4', quarterLength=2)])
melody.append([note.Note('C4', quarterLength=1), note.Note('G4', quarterLength=1)])
melody.append(note.Note('E4', quarterLength=2))

# Аккорды для сопровождения
chords = stream.Part()
chords.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=4))  # C-dur
chords.append(chord.Chord(['A3', 'C4', 'E4'], quarterLength=4))  # Am

# Вторая фраза: "Господи, прости меня, грешного раба"
melody.append([note.Note('F4', quarterLength=1), note.Note('E4', quarterLength=1)])
melody.append([note.Note('D4', quarterLength=2)])
melody.append([note.Note('C4', quarterLength=1), note.Note('G4', quarterLength=1)])
melody.append(note.Note('E4', quarterLength=2))

# Соответствующие аккорды
chords.append(chord.Chord(['F4', 'A4', 'C5'], quarterLength=4))  # F-dur
chords.append(chord.Chord(['G3', 'B3', 'D4'], quarterLength=4))  # G-dur

# Объединение мелодии и аккордов в партитуру
score.insert(0, melody)
score.insert(0, chords)

# Сохранение партитуры в формате MusicXML и PDF
output_path_xml = "C:/Users/swer/GitHub/python/Gospodi_Pomiluy.xml"
output_path_pdf = "/mnt/data/Gospodi_Pomiluy.pdf"
score.write('musicxml', fp=output_path_xml)
score.write('pdf', fp=output_path_pdf)

(output_path_xml, output_path_pdf)
