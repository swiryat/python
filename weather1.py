"""
import pyowm

owm = pyowm.OWM("360a18422b3aa6cb9e369d69794ef107")
place = input("В каком городе/стране?: ")
observation = owm.weather_manager().weather_at_place(place)
w = observation.weather
temp = w.temperature("celsius")["temp"]
print("В городе " + place + " сейчас " + w.detailed_status)
print("Температура сейчас в районе " + str(temp) + "°C")
if temp < 10:
    print("Холодно")
elif temp < 20:
    print("Очень холодно")
else:
    print("Норм")
"""

t = 5
while t == 5:
    import pyowm

    owm = pyowm.OWM("360a18422b3aa6cb9e369d69794ef107")
    place = input("В каком городе/стране?: ")
    observation = owm.weather_manager().weather_at_place(place)
    w = observation.weather
    temp = w.temperature("celsius")["temp"]
    print("В городе " + place + " сейчас " + w.detailed_status)
    print("Температура сейчас в районе " + str(temp) + "°C")
    if temp < 10:
        print("Холодно")
    elif temp < 20:
        print("Очень холодно")
    else:
        print("Норм")
    
