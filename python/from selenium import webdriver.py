from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Опционально, если нужно запускать в фоновом режиме

# Убедитесь, что драйвер будет соответствовать текущей версии браузера
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.mail.ru")
print(driver.title)

driver.quit()
