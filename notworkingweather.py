import pyowm

owm = pyowm.OWM("360a18422b3aa6cb9e369d69794ef107")
place = input("В каком городе/стране?: ")
observation = owm.weather_at_place(place)
w = observation.get_weather()
temp = w.get_temperature("celsius")["temp"]
print("В городе " + place + " сейчас " + w.get_detailed_status())
print("Температура сейчас в районе " + str(temp) + "°C")
if temp < 10:
    print("Холодно")
elif temp < 20:
    print("Очень холодно")
else:
    print("Норм")
