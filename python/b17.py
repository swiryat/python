from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeDriverManager  # Для автоматической загрузки драйвера Edge

# Настройка Selenium WebDriver для Edge
options = Options()
options.headless = False  # Если не хотите, чтобы окно браузера было видно, установите True

# Установка WebDriver для Edge
driver = webdriver.Edge(service=Service(EdgeDriverManager().install()), options=options)

try:
    # Открытие страницы
    url = "https://www.b17.ru/online/?page=4286"
    driver.get(url)

    # Явное ожидание загрузки заголовков (h2)
    wait = WebDriverWait(driver, 10)
    headings = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h2')))

    # Выводим заголовки
    if headings:
        for heading in headings:
            print(heading.text)
    else:
        print("Заголовки не найдены на странице.")

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    # Закрытие браузера
    driver.quit()
