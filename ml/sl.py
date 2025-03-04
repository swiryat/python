# my_sklearn_test.py
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Загружаем данные
iris = load_iris()
X, y = iris.data, iris.target

# Разделяем на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Создаем модель
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Делаем предсказания
predictions = model.predict(X_test)
print(predictions)
