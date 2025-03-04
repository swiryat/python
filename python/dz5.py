import pandas as pd
import pandas as pd

# Загрузите свой набор данных
data = pd.read_csv("data.csv")

# Выведите первые несколько строк данных
print(data.head())

# Получите информацию о типах данных и непустых значениях
print(data.info())

# Получите описательную статистику
print(data.describe())

# Проверьте на наличие пропущенных значений
print(data.isnull().sum())

