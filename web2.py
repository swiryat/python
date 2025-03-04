from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service as EdgeService
import time
import pickle
import os

# Путь к обновленному веб-драйверу Edge
driver_path = 'C:/Users/swer/Downloads/edgedriver_win64/msedgedriver.exe'

# Путь к файлу для хранения логина и пароля
credentials_file = 'credentials.pkl'

# Функция для загрузки логина и пароля из файла
def load_credentials():
    if os.path.exists(credentials_file):
        with open(credentials_file, 'rb') as file:
            return pickle.load(file)
    return None

# Функция для сохранения логина и пароля в файл
def save_credentials(username, password):
    with open(credentials_file, 'wb') as file:
        pickle.dump({'username': username, 'password': password}, file)

# Функция для входа в учетную запись
def login(username, password):
    try:
        email_input = driver.find_element(By.NAME, 'login')  # Найдите правильный локатор для поля email
        password_input = driver.find_element(By.NAME, 'password')  # Найдите правильный локатор для поля пароля
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Найдите правильный локатор для кнопки входа

        email_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        print("Login successful")
    except Exception as e:
        print(f"Error during login: {e}")

# Создаем экземпляр веб-драйвера для Edge с использованием Service
service = EdgeService(executable_path=driver_path)
driver = webdriver.Edge(service=service)

# URL страницы входа
login_url = 'https://www.b17.ru/login.php?utm=main'

# Открываем страницу входа
driver.get(login_url)

# Загружаем сохраненные учетные данные, если они есть
credentials = load_credentials()

if credentials:
    username = credentials['username']
    password = credentials['password']
    print("Using saved credentials.")
else:
    # Если нет сохраненных учетных данных, вводим новые
    username = 'zatura55@mail.ru'
    password = 'masa34'
    save_credentials(username, password)
    print("Saved new credentials.")

# Вход в учетную запись
login(username, password)

# Пауза для завершения процесса входа
time.sleep(5)  # Увеличьте, если требуется больше времени для входа

# URL страницы, на которую нужно перейти после входа
url = 'https://www.b17.ru/online/?page_plus=145'

# Открываем нужную страницу
driver.get(url)

# Функция для нажатия на кнопку добавления в закладки
def click_bookmark():
    try:
        bookmark_button = driver.find_element(By.XPATH, '//span[@class="b0 bf bkmrk460228 bookmark_on"]')
        ActionChains(driver).move_to_element(bookmark_button).click(bookmark_button).perform()
        print("Bookmark clicked")
    except Exception as e:
        print(f"Error clicking bookmark: {e}")

# Функция для нажатия на кнопку "Показать ещё 10 специалистов"
def show_more_specialists():
    try:
        show_more_button = driver.find_element(By.ID, 'ajax_page_next')
        ActionChains(driver).move_to_element(show_more_button).click(show_more_button).perform()
        print("Show more specialists clicked")
    except Exception as e:
        print(f"Error clicking 'show more specialists': {e}")

# Нажимаем на кнопку добавления в закладки 10 раз
for _ in range(10):
    click_bookmark()
    time.sleep(1)  # Пауза, чтобы избежать слишком быстрого нажатия

# Нажимаем на кнопку "Показать ещё 10 специалистов"
show_more_specialists()

# Закрываем браузер
time.sleep(50)  # Ждем несколько секунд, чтобы увидеть результат
driver.quit()
