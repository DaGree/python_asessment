import configparser
import requests
import json

def get_token():
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг
    return config["Weather"]["token"]

#print(get_token())
token=get_token()
#print(token)
#city=input("Enter your own city \n>")
city="Moscow"
#print("Your own city is "+city)
endpoint = "http://api.openweathermap.org/data/2.5/forecast"
query_params = {"appid":token, "q":"Moscow", "units":"metric", "lang":"ru"}

response = requests.get(endpoint, params=query_params).json()
description=response
print(description)