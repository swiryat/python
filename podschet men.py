import pandas as pd

# Загрузим датасет
df = pd.read_csv('C:/Python/stat.csv')

# Задача 1: Какую долю от всех пользователей составляют мужчины?
male_count = len(df[df['gender'] == 'male'])
total_users = len(df)
male_percentage = (male_count / total_users) * 100
print(f"Доля мужчин среди пользователей: {male_percentage:.3f}%")

# Задача 2: Какая доля мужчин использует Android?
male_android_count = len(df[(df['gender'] == 'male') & (df['platform'] == 'android')])
total_android_users = len(df[df['platform'] == 'android'])
male_android_percentage = (male_android_count / total_android_users) * 100
print(f"Доля мужчин, использующих Android: {male_android_percentage:.3f}%")

# Задача 3: Сколько в среднем секунд в приложении проводят пользователи с 2 подписками и 3 лайками?
average_time_spent = df[(df['subscriptions'] >= 2) & (df['likes'] >= 3)]['timespent'].mean()
print(f"Среднее время в приложении для пользователей с 2 подписками и 3 лайками: {average_time_spent:.3f} секунд")
