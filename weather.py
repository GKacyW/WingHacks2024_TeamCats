import requests
from suntime import Sun
import datetime
import pytz 
from tzlocal import get_localzone
import time

api_key = 'a04ce32f6a47777c9dd312e6da67966b'
#default settings

def get_weather(city, unit):

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        celc = int(temp) - 273.15
        far = round(celc * (9/5) + 32,2)
        if unit == "C":
            tempre = round(celc,2)
        elif unit == "F":
            tempre = far
        elif unit == "K":
            tempre = round(temp, 2)
        else:
            tempre = "uh oh" 
    else:
        print("uh oh")
    
    return_list = [tempre, desc]
    return return_list

def get_time(city):

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        lon = data['coord']['lon']
        lat = data['coord']['lat']
        
        sun = Sun(lat, lon)
        date = datetime.datetime.now()


        local_tz = get_localzone()
        #local_tz = pytz.timezone('Asia/Seoul')
        local_time = datetime.datetime.now(local_tz)

        sun_rise = sun.get_local_sunrise_time(date, local_tz)
        sun_set = sun.get_local_sunset_time(date, local_tz)
 
        

        

        if(sun_set.hour > local_time.hour > sun_rise.hour):
            day_or_night = "day"
            print(sun_rise, sun_set)
        else:
            day_or_night = "night"

        return_list = [sun_rise, sun_set, local_time]
        return (return_list, day_or_night)
        
    else:
        print("uh oh")



if __name__ == "__main__":
    print(get_time("Clearwater"))
