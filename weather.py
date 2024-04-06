import requests

def weather(city, unit):
    api_key = 'a04ce32f6a47777c9dd312e6da67966b'

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
        print(f'temp: {tempre}')
        
        print(f'description: {desc}')
    else:
        print("uh oh")

    #print(f'temp :{temp3}')

if __name__ == "__main__":
    weather('clearwater', 'K')
    weather('clearwater', 'F')
    weather('clearwater', 'C')
   