""" this module downloads the current weather for a given location from
from openweatherbase.org and saves it in a sqlite database. It makes use of
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
    """
    Holds the relevant data about the local weather.
    """
    def __init__(self, weather, conditions, wind, clouds, name, time):
        self.weather = weather
        self.conditions = conditions
        self.wind = wind
        self.clouds = clouds
        self.name = name
        self.time = time


def get_weather():
    """
    Gathers the current weather data via an api request, saves the relevant
    Data in a weather opbject and returns the object.
    First the api adress ist constructed from hardcoded parts and config
    parameters.
    Then, using the requests module, data is gathered in a response.
    The text is decoded as json and the relevant data used as paramters for
    the weather object constructor.
    """
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
    """
    Creates an squlite database if necessary and saves a weather data into it.
    The fuction takes as parameters an cursor to a squlite database 
    and a weather object.
    If the table weather does not exist, it is created. The weather objects
    attributes are then saved in temporarz variables using typecasting
    to ensure the correct types before storing them as a new entry into the 
    database.
    """
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


if __name__ == "__main__":
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        weather = get_weather()
        write_data_to_db(cursor, weather)
        connection.commit()

    except sqlite3.IntegrityError:
        print("The call happened to soon after the last!\n" +
              "If calls happen less than 1 hour appart,\n" +
              "the key is identical!\n")
