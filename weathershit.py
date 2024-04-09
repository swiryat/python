import pyowm
from pyowm.weatherapi25.weather import Weather as OWMWeatherAPI

owm = pyowm.OWM('13633e74e192e939b001a5edd18068f3')
place = input("Какой город/страна?: ")
observation = owm.weather_manager().weather_at_place(place)
w = observation.weather
print(w)

