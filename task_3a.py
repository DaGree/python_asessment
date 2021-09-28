import configparser
import requests

def get_token():
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг
    return config["Weather"]["token"]

print(get_token())
city=input("Enter your own city \n>")
print("Your own city is "+city)