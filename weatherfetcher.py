#The requests module allows for easy connection to a web adress, without worrying about connection timeout etc.
import requests
#allows the encoding, decoding, writing and reading of json-files
import json

from datetime import datetime as dt

def load_config_file():
    with open("config.json") as config_file:
        config_data = json.load(config_file)
        return config_data
        
API_KEY = load_config_file().["api_key"]
FILE_PATH = load_config_file().["file_path"]


def get_api_key():
    api_key = ""
    return api_key

def get_timestamp():
    current_time = dt.now()
    timestamp = current_time.strftime("%Y%m%d%H")
    return timestamp

def create_filename():
    path_to_file = FILE_PATH
    timestamp = get_timestamp()
    filename = path_to_file + timestamp + "raw_data.json"
    return filename
