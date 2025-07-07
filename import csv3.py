import csv

# Открываем CSV файл для чтения
with open("dat.csv", "r") as file:
    reader = csv.DictReader(file)
    
    # Получаем заголовки из файла автоматически
    headers = reader.fieldnames
    
    # Создаем словарь для подсчета значений
    counts = {header: {} for header in headers}
    
    # Итерация по строкам CSV файла
    for row in reader:
        for header in headers:
            dat = row[header]
            if dat in counts[header]:
                counts[header][dat] += 1
            else:
                counts[header][dat] = 1

# Вывод результатов
for header, values in counts.items():
    print(f"Заголовок: {header}")
    for dat, count in values.items():
        print(f"{dat}: {count}")
