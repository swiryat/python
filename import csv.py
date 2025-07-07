import csv

# Объявление переменных для подсчета значений
Pregnancies, Glucose, BloodPressure = 0, 0, 0

# Открываем CSV файл для чтения
with open("dat.csv", "r") as file:
    reader = csv.DictReader(file)
    
    # Итерация по строкам CSV файла
    for row in reader:
        dat = row["Glucose"] 
        if dat == "Pregnancies":
            Pregnancies += 1
        elif dat == "Glucose":
            Glucose += 1
        elif dat == "BloodPressure":
            BloodPressure += 1

# Вывод результатов
print(f"Pregnancies: {Pregnancies}")
print(f"Glucose: {Glucose}")
print(f"BloodPressure: {BloodPressure}")


