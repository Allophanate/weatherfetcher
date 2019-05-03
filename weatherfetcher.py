""" this module downloads the current weather for a given location from 
from openweatherbase.org and saves it as a json file. It makes use of 
the requests module for easy API interaction. """

#The requests module allows for easy connection to a web adress, without worrying about connection timeout etc.
import requests
#allows the encoding, decoding, writing and reading of json-files
import json

import os

from datetime import datetime as dt

def load_config_file():
    """
    This function reads a config file in json formatting.
    the parameter-value-pairs are returned as dictionary.
    """
    #generates the path the script resides in so no relative paths are needed for config.json
    dir_path = os.path.dirname(__file__)
    with open(dir_path + "/config.json") as config_file:
        config_data = json.load(config_file)
        return config_data

config_data = load_config_file()


# binding of the config parameters to global variables
API_KEY = config_data["api_key"]
FILE_PATH = config_data["file_path"]
CITY_ID = config_data["city_id"]


def get_timestamp():
    """
    This function creates a string of the current time in the format yyyymmddhh.
    It uses inbuilt formatting capabilities of the datetime object.
    """
    current_time = dt.now()
    timestamp = current_time.strftime("%Y%m%d%H")
    return timestamp

def create_filename():
    """
    This function concatenates several strings to create the full filename
    including path for the file to be saved.
    """
    path_to_file = FILE_PATH
    timestamp = get_timestamp()
    filename = path_to_file + timestamp + "raw_data.json"
    return filename
    
def fetch_weather():
    """
    This function makes use of the requests-module to get weather data
    from openweathermap.org
    """
    
    # constructs the correct api adress from the necessary parts
    api_adress = "http://api.openweathermap.org/data/2.5/weather?id=" + CITY_ID + "&APPID=" + API_KEY
    filename = create_filename()
    
    # actual fetchin of the weather data
    data = requests.get(api_adress)
    
    # encode data as json
    # the format is correct, but python needs to recognize it as json
    json_data = data.json()
    
    # write date to file as json
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile)

fetch_weather()
