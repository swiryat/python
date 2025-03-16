import requests

# Инициализация сессии
session = requests.Session()

# Добавьте ваши cookies, которые вы получили из браузера
session.cookies.set("jr-sidebar-mode", "FULL")
session.cookies.set("javarush.user.id", "3425706")
session.cookies.set("JSESSIONID", "48a37049-9d45-46f4-b708-1cac06bd96e8")
session.cookies.set("intercom-session-mqlef7yz", "")
session.cookies.set("intercom-device-id-mqlef7yz", "e30412d1-7c2f-4c73-86be-930bfa384cb5")
session.cookies.set("__stripe_mid", "d92df48d-b7c8-45f7-a6a6-e7da35f218ce1dfa20")
session.cookies.set("CookieConsent", "{stamp:'-1',necessary:true,preferences:true,statistics:true,marketing:true,method:'implied',ver:1,utc:1741007185215,region:'GB'}")
session.cookies.set("jr-featured-content-14", "closed")
session.cookies.set("javarush.daynight", "light")
session.cookies.set("_gcl_au", "1.1.84417750.1741713789")
session.cookies.set("_ga", "GA1.1.346389540.1741713790")
session.cookies.set("_ga_G0F5YPM3KY", "deleted")
session.cookies.set("jr-sidebar-group-university-collapsed", "0")
session.cookies.set("jr-install-mark", "NOT_NOW")
session.cookies.set("jr-last-route", "%2Fall-articles")
session.cookies.set("_ga_G0F5YPM3KY", "GS1.1.1741823636.7.1.1741823935.60.1.1267399023")

# Отправляем GET запрос
response = session.get("https://javarush.com/all-articles")

# Проверка полученных данных
if response.status_code == 200:
    print("Запрос успешен!")
    print(response.text[:500])  # Выводим первые 500 символов ответа
else:
    print(f"Ошибка: {response.status_code}")
