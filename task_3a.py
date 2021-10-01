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
query_params = {"appid":token, "q":"Moscow", "units":"metric", "lang":"ru", "mode":"json"}

response = requests.get(endpoint, params=query_params)
description=json.loads(response.text)
lenght=len(description["list"])
delta=[5]
omega=[5]
for i in range(lenght):
    data=description["list"][i]["dt_txt"]
    if data.endswith("00:00:00",11):
        omega.append(i)
        temp_min=float(description["list"][i]["main"]["temp"])
        feels_like=float(description["list"][i]["main"]["feels_like"])
        delta.append(abs(temp_min-feels_like))
        print(data)
        print(description["list"][i]["main"]["temp"])
        print(description["list"][i]["main"]["feels_like"])

print(delta)
id_omega=delta.index(min(delta))
id_list=omega[id_omega]
print(omega)
print(min(delta)," °C - минимальная разница температур ночью ")
print("Дата дня с минимальной разницей",description["list"][id_list]["dt_txt"][:10])
