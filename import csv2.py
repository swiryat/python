import csv

# Открываем CSV файл для чтения
with open("dat.csv", "r") as file:
    reader = csv.DictReader(file)
    counts = {}
    
    # Итерация по строкам CSV файла
    for row in reader:
        dat = row["Glucose"]
        if dat in counts:
            counts[dat] += 1
        else:
            counts[dat] = 1
#def get_value(Age):
#    return counts[Age]            
#for dat in sorted(counts, key=get_value, reverse=True):
for dat in sorted(counts, key=lambda Glucose: counts[Glucose], reverse=True):
    print(f"{dat}: {counts[dat]}")           
#        Вывод всех столбцов текущей строки
#        for key, value in row.items():
#            print(f"{key}: {value}")
#        print()  # Добавляем пустую строку для разделения между записями
dat = input("Dat: ")
if dat in counts:
    print(f"{dat}: {counts[dat]}")
