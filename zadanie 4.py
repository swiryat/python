disc = ['Алгебра', 'Геометрия', 'Топология']
student = ['Сидоров', 'Иванов', 'Петров', 'Иванова']
grades_student = [[2, 4, 4], [3, 4, 4], [3, 3, 3], [5, 5, 5]]

# Создайте словарь с оценками студентов, используя методы dict() и zip()
student_grades_dict = dict(zip(student, grades_student))
print("Словарь с оценками студентов:")
print(student_grades_dict)

# Сформируйте словарь вторым способом с помощью цикла for и метода enumerate()
student_subject_grades_dict = {}
for i, name in enumerate(student):
    student_subject_grades_dict[name] = dict(zip(disc, grades_student[i]))

print("\nСловарь с оценками студентов и предметами:")
print(student_subject_grades_dict)

# Найдите и распечатайте фамилии "круглых отличников" и студентов, несдавших сессию
excellent_students = [name for name, grades in student_grades_dict.items() if all(grade == 5 for grade in grades)]
failed_students = [name for name, grades in student_grades_dict.items() if any(grade < 3 for grade in grades)]

print("\nКруглые отличники:", excellent_students)
print("Несдавшие сессию:", failed_students)
