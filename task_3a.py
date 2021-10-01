import configparser
import requests
import json
import datetime
import time

def get_token():
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг
    return config["Weather"]["token"]

def input_city():
    city=input("Enter your own city \n>")
    print("Your own city is "+city)
    return(city)

def delta_temp_day(description):
    deltak=[5]
    omega=[5]
    lenght=len(description["list"])
    for i in range(lenght):
        data=description["list"][i]["dt_txt"]
        if data.endswith("00:00:00",11):
            omega.append(i)
            temp_min=float(description["list"][i]["main"]["temp"])
            feels_like=float(description["list"][i]["main"]["feels_like"])
            deltak.append(abs(temp_min-feels_like))
    id_omega=deltak.index(min(deltak))
    id_list=omega[id_omega]
    print(min(deltak)," °C - минимальная разница температур ночью ")
    print("Дата дня с минимальной разницей",description["list"][id_list]["dt_txt"][:10])

def request_to_api(token,city):
    endpoint = "http://api.openweathermap.org/data/2.5/forecast"          #forecast
    query_params = {"appid":token, "q":city, "units":"metric", "lang":"ru", "mode":"json"}
    response = requests.get(endpoint, params=query_params)
    description=json.loads(response.text)
   
    return(description)

def max_sun(description):
    deltak=[5]
    omega=[5]
    lat=float(description["city"]["coord"]["lat"])
    lon=float(description["city"]["coord"]["lon"])
    endpoint = "http://api.openweathermap.org/data/2.5/onecall"         
    query_params = {"appid":token,"lat":lat, "lon":lon,"exclude":"hourly,current","units":"metric", "lang":"ru", "mode":"json"}
    response=requests.get(endpoint,params=query_params)
    answer=json.loads(response.text)

    for i in range (5):
        sunrise= datetime.datetime.fromtimestamp(answer["daily"][i]["sunrise"])
        sunset= datetime.datetime.fromtimestamp(answer["daily"][i]["sunset"])
        delta=(sunset-sunrise)
        deltak.append(delta.seconds)

    max_index=deltak.index(max(deltak))
    ty_res = time.gmtime(deltak[max_index])
    res = time.strftime("%H:%M:%S",ty_res)

    voshod= datetime.datetime.fromtimestamp(answer["daily"][max_index]["sunrise"])
    print("Восход")
    print(voshod.strftime('%H:%M:%S'))

    zakat= datetime.datetime.fromtimestamp(answer["daily"][max_index]["sunset"])
    print("Закат")
    print(zakat.strftime('%H:%M:%S'))

    print("Максимальная продолжительность дня соcтавила")
    print(res)
    print("По состоянию на ")
    print(zakat.strftime('%Y-%m-%d'))

token=get_token()
city=input_city()
description=request_to_api(token,city)
delta_temp_day(description)
max_sun(description)
