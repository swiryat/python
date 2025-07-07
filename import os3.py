import os

FILE_NAME = "C:/Users/swer/Documents/hh_vacancies.csv"

# Проверяем, существует ли каталог и создаем его, если он не существует
directory = os.path.dirname(FILE_NAME)
if not os.path.exists(directory):
    os.makedirs(directory)

# Теперь можно использовать переменную FILE_NAME при открытии файла
with open(FILE_NAME, 'w') as f:
    # Здесь можете выполнять операции с файлом
    pass
