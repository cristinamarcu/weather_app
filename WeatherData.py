import requests
import json
import datetime
from typing import NamedTuple, Optional


class DayWeatherForecast(NamedTuple):
    day: str
    time: str
    description: str
    temperature_kelvin: float
    temperature_celsius: float


class WeatherForecast(NamedTuple):
    today: DayWeatherForecast
    tomorrow: DayWeatherForecast


def getdayinfo(weatherdata, day) -> DayWeatherForecast:
    forecastday = DayWeatherForecast(day, str(weatherdata['dt_txt']), str(weatherdata['weather'][0]['description']),
                                     weatherdata['main']['temp'], kelvin_to_celsius(weatherdata['main']['temp']))
    return forecastday


def kelvin_to_celsius(k) -> float:
    result = k - 273.15
    return float("{:.2f}".format(result))


def valid_city(cityName: str) -> bool:
    city_list = open('city.list.json', encoding="utf8")
    content = city_list.read()
    valid_city_list = json.loads(content)
    valid = False

    for validCity in valid_city_list:
        if cityName.casefold() == validCity['name'].casefold():
            valid = True
    return valid


def getweather(cityName: str) -> Optional[WeatherForecast]:
    try:
        res = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?q={cityName}&appid=MYAPPID')
    except:
        print("Could not get weather data")
        return None

    textjson_dict = json.loads(res.text)
    today = datetime.datetime.fromisoformat(textjson_dict['list'][0]['dt_txt'])
    weathertoday = getdayinfo(textjson_dict['list'][0], 'Today')
    tomorrow = today + datetime.timedelta(days=1)
    weathertomorrow = None
    for weatherdata in textjson_dict['list']:
        if datetime.datetime.fromisoformat(weatherdata['dt_txt']) == tomorrow:
            weathertomorrow = getdayinfo(weatherdata, 'Tomorrow')
    weatherforecast = WeatherForecast(weathertoday, weathertomorrow)
    return weatherforecast


forcastdescript = {'light snow': 'snow.jpg',
                   'clear sky': 'sunny.jpg',
                   'clear': 'sunny.jpg',
                   'sunny': 'sunny.jpg',
                   'light rain': 'rain.png',
                   'rain': 'rain.png',
                   'moderate rain': 'rain.png',
                   'thunderstorm': 'rain.png',
                   'overcast clouds': 'cloudy.png',
                   'clouds': 'cloudy.png',
                   'few clouds': 'clouds and sun.png',
                   'broken clouds': 'clouds and sun.png',
                   'scattered clouds': 'clouds and sun.png'}


def getPictureFileFromDescription(weatherdescription):
    return 'images\\' + forcastdescript[weatherdescription]
