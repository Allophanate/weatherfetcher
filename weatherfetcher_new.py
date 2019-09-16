""" this module downloads the current weather for a given location from
from openweatherbase.org and saves it as a json file. It makes use of
the requests module for easy API interaction."""

# The requests module allows for easy connection to a web adress,
# without worrying about connection timeout etc.
import requests
# allows the encoding, decoding, writing and reading of json-files
import json

import os

from datetime import datetime as dt

import sqlite3


def load_config_file():
    """
    This function reads a config file in json formatting.
    the parameter-value-pairs are returned as dictionary.
    """
    # generates the path the script resides in so no relative
    # paths are needed for config.json
    dir_path = os.path.dirname(__file__)
    print(dir_path)
    with open(dir_path + "config.json") as config_file:
        config_data = json.load(config_file)
        return config_data


config_data = load_config_file()


# binding of the config parameters to global variables
API_KEY = config_data["api_key"]
FILE_PATH = config_data["file_path"]
CITY_ID = config_data["city_id"]
DB_PATH = config_data["db_path"]


class Weather():
    def __init__(self, weather, conditions, wind, clouds, name, time):
        self.weather = weather
        self.conditions = conditions
        self.wind = wind
        self.clouds = clouds
        self.name = name
        self.time = time


def get_weather():
    # constructs the correct api adress from the necessary parts
    api_adress = ("http://api.openweathermap.org/" +
                  "data/2.5/weather?id=" + CITY_ID + "&APPID=" + API_KEY)
    # actual fetchin of the weather data and get the text
    data = requests.get(api_adress).text
    weather_data = json.loads(data)

    weather = Weather(weather_data["weather"][0], weather_data["main"],
                      weather_data["wind"], weather_data["clouds"],
                      weather_data["name"], dt.now())
    return weather


def write_data_to_db(cursor, weather):
    cursor.execute("""CREATE TABLE IF NOT EXISTS weather (timestamp text primary key, year integer, month integer, day integer, hour integer, temperature real, pressure integer, humidity integer, weather text, weather_detail text, wind_speed real, wind_angle integer, clouds integer, name text)""")
    timestamp = weather.time.strftime("%Y%m%d%H")
    year = weather.time.year
    month = weather.time.month
    day = weather.time.day
    hour = weather.time.hour
    temperature = float(weather.conditions["temp"])
    pressure = int(weather.conditions["pressure"])
    humidity = int(weather.conditions["humidity"])
    weather_text = str(weather.weather["main"])
    weather_detail = str(weather.weather["description"])
    wind_speed = float(weather.wind["speed"])
    wind_angle = int(weather.wind["deg"])
    clouds = int(weather.clouds["all"])
    name = str(weather.name)
    
    cursor.execute("INSERT INTO weather " +
                   "(timestamp, year, month, day, hour, temperature, " +
                   "pressure, humidity, weather, weather_detail, " +
                   "wind_speed, wind_angle, clouds, name) " +
                   "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (timestamp, year, month, day, hour, temperature, pressure,
                    humidity, weather_text, weather_detail, wind_speed,
                    wind_angle, clouds, name))


connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
weather = get_weather()
write_data_to_db(cursor, weather)
connection.commit()

for row in cursor.execute("SELECT * FROM weather"):
    print(row)
