import pandas as pd

# Создаем пустой DataFrame, в который будем объединять таблицы
combined_data = pd.DataFrame()

# Список таблиц
table_names = ["table_1", "table_2", "table_3", "table_4", "table_5", "table_6"]

# Объединяем таблицы
for table_name in table_names:
    # Загружаем таблицу из CSV-файла
    table_data = pd.read_csv(f"{table_name}_2023-11-10_04-26-30.csv")
    
    # Объединяем таблицу с общим DataFrame
    combined_data = pd.concat([combined_data, table_data])

# Выводим объединенную таблицу
print(combined_data)

# Сохраняем объединенную таблицу в CSV-файл
combined_data.to_csv("combined_data.csv", index=False)
