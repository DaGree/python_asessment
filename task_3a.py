import configparser
import requests
import json
import datetime
import time

def get_token():  #функция для получения токена апи скрыто с целью не публикации ключа в системе контроля версий
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг
    return config["Weather"]["token"]

def input_city(): #функция реализует ввод города для получения различных запросов 
    city=input("Enter your own city \n>")
    print("Your own city is "+city)
    return(city)

def delta_temp_day(description): #функция реализует первую часть задачи 
    deltak=[5]    #списки для дальнейшего анализа и подсчета
    omega=[5]
    lenght=len(description["list"])     #получение длины списка в JSON файлк
    for i in range(lenght):       #перебор всех полученных ответов по дням
        data=description["list"][i]["dt_txt"]
        if data.endswith("00:00:00",11):
            omega.append(i)                    #добавление порядкого номера в списке в массив
            temp_min=float(description["list"][i]["main"]["temp"])   #получение нужных данных 
            feels_like=float(description["list"][i]["main"]["feels_like"])
            deltak.append(abs(temp_min-feels_like))    #расчет абсолютного значения - дельты
    id_omega=deltak.index(min(deltak))                 #поиск минимальной дельты и номера списка в JSON
    id_list=omega[id_omega]
    print(round(min(deltak),2)," °C - минимальная разница температур ночью ")
    print("Дата дня с минимальной разницей",description["list"][id_list]["dt_txt"][:10])

def request_to_api(token,city):   #функция релизует необходимый запрос к серверу
    endpoint = "http://api.openweathermap.org/data/2.5/forecast"          #forecast
    query_params = {"appid":token, "q":city, "units":"metric", "lang":"ru", "mode":"json"} #ввод необходимых параметров
    response = requests.get(endpoint, params=query_params)
    description=json.loads(response.text)
   
    return(description)

def max_sun(description): #функция реализует вторую часть задачи
    deltak=[5]
    omega=[5]
    lat=float(description["city"]["coord"]["lat"])         #получение координат для выяснения времени закатов и рассветов
    lon=float(description["city"]["coord"]["lon"])
    endpoint = "http://api.openweathermap.org/data/2.5/onecall"         
    query_params = {"appid":token,"lat":lat, "lon":lon,"exclude":"hourly,current","units":"metric", "lang":"ru", "mode":"json"}
    response=requests.get(endpoint,params=query_params)  #реализация запорса к серверу 
    answer=json.loads(response.text)

    for i in range (5):
        sunrise= datetime.datetime.fromtimestamp(answer["daily"][i]["sunrise"])    #запись и преобразование вемни заката и восхода их unix в необходимый формат
        sunset= datetime.datetime.fromtimestamp(answer["daily"][i]["sunset"])
        delta=(sunset-sunrise)
        deltak.append(delta.seconds)

    max_index=deltak.index(max(deltak))
    ty_res = time.gmtime(deltak[max_index])     #поиск максимального длительности в секундах
    res = time.strftime("%H:%M:%S",ty_res)      #преобразование в читаемый вид

    voshod= datetime.datetime.fromtimestamp(answer["daily"][max_index]["sunrise"])
    print("Восход")
    print(voshod.strftime('%H:%M:%S'))

    zakat= datetime.datetime.fromtimestamp(answer["daily"][max_index]["sunset"])
    print("Закат")
    print(zakat.strftime('%H:%M:%S'))

    print("Максимальная продолжительность дня соcтавила")
    print(res)                                              #вывод на экран
    print("По состоянию на ")
    print(zakat.strftime('%Y-%m-%d'))

token=get_token()    #получение токена

answer=True
while answer:        #цикл необходим для опроса пользвателя с конечным условием
    city=input_city()
    description=request_to_api(token,city)
    delta_temp_day(description)
    max_sun(description)
    #print("Вы хотите продолжить?(y/n)\n>")
    check=input("Вы хотите продолжить?(y/n)\n>")
    if (check=='y'):
        answer=True
    else:
        answer=False
