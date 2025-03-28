import pandas as pd
import glob

# Получите список файлов CSV в текущей директории
csv_files = glob.glob("6.csv")

# Инициализируйте пустой DataFrame для объединения
combined_data = pd.DataFrame()

# Цикл для чтения и объединения таблиц
for csv_file in csv_files:
    table_data = pd.read_csv(csv_file)
    combined_data = pd.concat([combined_data, table_data], join='outer', ignore_index=True)

# Выведите объединенную таблицу
print("Объединенная таблица:")
print(combined_data)
