import csv

# Открываем CSV файл для чтения
with open("dat.csv", "r") as file:
    reader = csv.DictReader(file)

    # Переменные для подсчета значений
    pregnancies_count = 0
    glucose_count = 0
    blood_pressure_count = 0

    # Итерация по строкам CSV файла
    for row in reader:
        pregnancies = row["Pregnancies"]
        glucose = row["Glucose"]
        blood_pressure = row["BloodPressure"]

        # Увеличиваем счетчики, если значения не пустые
        if pregnancies:
            pregnancies_count += 1
        if glucose:
            glucose_count += 1
        if blood_pressure:
            blood_pressure_count += 1

# Вывод результатов
print(f"Pregnancies: {pregnancies_count}")
print(f"Glucose: {glucose_count}")
print(f"BloodPressure: {blood_pressure_count}")
