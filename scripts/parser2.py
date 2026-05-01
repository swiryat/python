import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

url = 'https://scrapingclub.com/exercise/list_basic/'
params = {'page': 1}
pages = 2
n = 1
data = []

while params['page'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', class_='w-full rounded border')

    for item in items:
        product_name = item.find('h4').text.strip()
        product_price = float(item.find('h5').text.strip().replace('$', ''))
        category = item.find('span', class_='title')
        if category:
            category = category.text.strip()
        else:
            category = 'Unknown'
        data.append({'Product': product_name, 'Price': product_price, 'Category': category})

    last_page_element = soup.find_all('a', class_='page-link')
    if last_page_element:
        last_page_num = int(last_page_element[-2].text)
    else:
        last_page_num = params['page']
    pages = last_page_num if pages < last_page_num else pages
    params['page'] += 1

df = pd.DataFrame(data)

# Вычислить среднюю цену
average_price = df['Price'].mean()
print(f"Средняя цена: ${average_price:.2f}")

# Проведем z-оценку для столбца 'Price'
z_scores = stats.zscore(df['Price'])
df['Z-Score'] = z_scores

# Выберем продукты, которые имеют аномальные значения цены (z-оценка больше 3 или меньше -3)
anomalous_products = df[(df['Z-Score'] > 3) | (df['Z-Score'] < -3)]
print("Продукты с аномальными ценами:")
print(anomalous_products[['Product', 'Price', 'Z-Score']])

# Визуализируем данные с использованием box plot
plt.figure(figsize=(8, 6))
plt.boxplot(df['Price'], vert=False)
plt.xlabel('Price')
plt.title('Распределение цен')
plt.show()

# Инициализируем анализатор сентимента
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Добавим столбец Sentiment в датасет
df['Sentiment'] = df['Product'].apply(lambda x: sia.polarity_scores(x)['compound'])

# Оценим сентимент для первых нескольких продуктов
print(df[['Product', 'Sentiment']].head())

# Выявим продукты с положительным сентиментом
positive_sentiment_products = df[df['Sentiment'] > 0]
print("Продукты с положительным сентиментом:")
print(positive_sentiment_products[['Product', 'Sentiment']])

# Выявим продукты с отрицательным сентиментом
negative_sentiment_products = df[df['Sentiment'] < 0]
print("Продукты с отрицательным сентиментом:")
print(negative_sentiment_products[['Product', 'Sentiment']])

# Проведем корреляционный анализ между ценой и категорией
correlation_price_category = stats.pointbiserialr(df['Price'], df['Category'])
print(f"Корреляция между ценой и категорией: {correlation_price_category.correlation:.2f}")

# Проведем регрессионный анализ между ценой и категорией
X = pd.get_dummies(df['Category'], drop_first=True)  # Преобразуем категории в бинарные признаки
X = sm.add_constant(X)  # Добавим константу
model = sm.OLS(df['Price'], X).fit()
print(model.summary())

# Преобразовать столбец 'Price' в числовой формат
df['Price'] = df['Price']

# Первые 5 строк датасета
print(df.head())

# Выбрать только продукты с ценой выше $30:
high_price_products = df[df['Price'] > 30.00]

# Основные статистические данные
print(df.describe())

# Группировка данных
category_group = df.groupby('Category')
avg_prices = category_group['Price'].mean()

# Визуализация данных
plt.hist(df['Price'], bins=10)
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Вычисление z-оценки для цены
z_scores = stats.zscore(df['Price'])
outliers = (z_scores > 3) | (z_scores < -3)
print(f"Индексы выбросов: {df.index[outliers].tolist()}")

# Визуализация box plot
plt.boxplot(df['Price'])
plt.xlabel('Price')
plt.show()


# Сохранение данных
df.to_csv('products_dataset.csv', index=False)
