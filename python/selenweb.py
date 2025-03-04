from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
from bs4 import BeautifulSoup

# Отключаем JavaScript в Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-javascript")  # Отключаем выполнение JavaScript

# Инициализация драйвера с отключением JavaScript
driver = webdriver.Chrome(options=chrome_options)

# Функция для авторизации на сайте
def login(driver, username, password):
    driver.get("https://sdo.academydpo.org/?nr=1&login=351039716&password=w4rba")
    
    wait = WebDriverWait(driver, 10)
    login_field = wait.until(EC.presence_of_element_located((By.NAME, "user")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    login_field.clear()
    password_field.clear()
    
    login_field.send_keys(username)
    password_field.send_keys(password)

    password_field.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
    print("Успешный вход!")

# Функция для закрытия всплывающего окна (если есть)
def close_popup(driver):
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='close-popup']"))
        )
        close_button.click()
        print("Всплывающее окно закрыто.")
    except Exception as e:
        print("Не удалось закрыть всплывающее окно:", e)

# Функция для пропуска обучающих подсказок (если есть)
def skip_tutorial(driver):
    try:
        skip_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Пропустить')]"))
        )
        skip_button.click()
        print("Обучение пропущено.")
    except Exception as e:
        print("Не удалось пропустить обучение:", e)

# Функция для прокрутки страницы
def scroll_visible_area(driver):
    last_scroll_position = driver.execute_script("return window.pageYOffset;")
    scroll_pause_time = 2
    while True:
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(scroll_pause_time)
        
        new_scroll_position = driver.execute_script("return window.pageYOffset;")
        if new_scroll_position == last_scroll_position:
            break
        last_scroll_position = new_scroll_position

# Функция для скачивания изображений
def download_images(driver, url):
    driver.get(url)
    
    # Закрытие всплывающего окна и пропуск обучения
    close_popup(driver)
    skip_tutorial(driver)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_pause_time = 3
    scroll_attempts = 0
    max_scroll_attempts = 10

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            scroll_attempts += 1
            if scroll_attempts >= max_scroll_attempts:
                print("Не удается прокрутить страницу до конца.")
                break
        else:
            scroll_attempts = 0
        
        last_height = new_height

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    img_tags = soup.find_all("img")

    os.makedirs("downloaded_images", exist_ok=True)

    for img in img_tags:
        img_url = img.get("src")
        if img_url:
            if img_url.startswith("/"):
                img_url = "https://sdo.academydpo.org" + img_url
            try:
                response = requests.get(img_url)
                if response.status_code == 200:
                    img_name = os.path.basename(img_url)
                    img_path = os.path.join("downloaded_images", img_name)
                    with open(img_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Изображение сохранено как {img_name}")
                else:
                    print(f"Не удалось скачать изображение: {img_url}")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка скачивания изображения: {e}")

# Функция для нахождения и открытия окна с файлом
def keep_window_open(driver):
    try:
        file_window = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='file-window']"))
        )
        print("Окно с файлом открыто и активно.")
    except Exception as e:
        print("Не удалось найти окно с файлом:", e)

    # Делаем паузу, чтобы пользователь мог вручную скопировать или взаимодействовать с файлом
    print("Окно с файлом будет оставаться открытым. Для продолжения работы закройте его вручную.")
    time.sleep(600)  # Здесь можно увеличить или уменьшить время ожидания в зависимости от необходимости

# Главная часть кода
if __name__ == "__main__":
    username = "351039716"  # Ваш логин
    password = "w4rba"  # Ваш пароль

    try:
        login(driver, username, password)

        lecture_url = "https://sdo.academydpo.org/file_lecture.php?path=files_lecture/lecture_1734086208_tSip.doc&t=1"
        download_images(driver, lecture_url)

        keep_window_open(driver)  # Оставляем окно с файлом открытым

    finally:
        driver.quit()
