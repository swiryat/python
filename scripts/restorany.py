import pandas as pd

# Загрузка данных из файла CSV и создание DataFrame
df = pd.read_csv("C:\\Users\\swer\\orders.csv", encoding='utf-8')

# Вывод первых 5 строк DataFrame
df.head(5)


