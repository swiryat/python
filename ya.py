import pandas as pd

# Загрузка данных из CSV-файла в DataFrame
df = pd.read_csv("C:\\Python\soc.csv")


# Посчитаем количество пользователей, которые не публикуют посты
users_without_publications = df[df['publications'] == 0]

# Найдем долю таких пользователей от всех пользователей
fraction_users_without_publications = len(users_without_publications) / len(df)

# Ответ на вопрос
print(fraction_users_without_publications)

# Отфильтруем пользователей без публикаций
users_without_publications = df[df['publications'] == 0]

# Затем отфильтруем эту выборку по платформе iOS
users_without_publications_ios = users_without_publications[users_without_publications['platform'] == 'iOS']

# Найдем долю таких пользователей от всех пользователей
fraction_users_without_publications_ios = len(users_without_publications_ios) / len(df)

# Ответ на вопрос
print(fraction_users_without_publications_ios)

# Отфильтруем пользователей, которые просмотрели хотя бы 100 постов и не совершили подписок
users_with_views_at_least_100_no_subscriptions = df[(df['views'] >= 100) & (df['subscriptions'] == 0)]

# Посчитаем сумму лайков этих пользователей
total_likes_by_users = users_with_views_at_least_100_no_subscriptions['likes'].sum()

# Ответ на вопрос
print(total_likes_by_users)

