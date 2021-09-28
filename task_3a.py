import configparser
import requests

def get_token():
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг
    return config["Weather"]["token"]

#print(get_token())
token=get_token()
#print(token)
city=input("Enter your own city \n>")
#print("Your own city is "+city)
endpoint = "http://api.openweathermap.org/data/2.5/weather"
query_params = {"appid":token, "q":city, "units":"metric", "lang":"ru"}

response = requests.get(endpoint, params=query_params)

print(response.text)