import pygame
from weather import *
import datetime

pygame.init()
screen = pygame.display.set_mode((400,450))
clock = pygame.time.Clock()
running = True


# weather specific code

weather_icons = {
    "clear sky": {"day": "images/clear.png", "night": "images/clear night.png"},
    "few clouds": {"day": "images/scatted clouds.png", "night": "images/scatted clouds night.png"},
    "scatted clouds": {"day": "images/scatted clouds.png", "night": "images/scatted clouds night.png"},
    "broken clouds":{"day": "images/cloudy.png", "night": "images/cloudy night.png"},
    "shower rain": {"day": "images/rain shower.png", "night": "images/rain shower night.png"},
    "rain": {"day": "images/rain.png", "night": "images/rain night.png"},
    "thunderstorm": {"day": "images/thunderstorm.png", "night": "images/thunderstorm night.png"},
    "snow": {"day": "images/snow.png", "night": "images/snow night.png"},
    "mist": {"day": "images/mist.png", "night": "images/mist night.png"}
}
bar = {
    "day": "images/day_bar.png",
    "night": "images/night_bar.png"
}

city = "Gainesville, Florida, USA"
unit = "F"



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((184,215,233))
    #do weather determinations
    weather_data = get_weather(city, unit)
    weather_condition = weather_data[1]

    #time determinations
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    time = "day"

    image_path = (weather_icons.get(weather_condition, {}).get(time))
    image = pygame.image.load(image_path).convert_alpha()
    bar_path = bar.get(time)
    bar_ = pygame.image.load(bar_path).convert_alpha()
    settings_icon = pygame.image.load('images/settings.png')

    screen.blit(bar_,(25,10))
    screen.blit(image, (30,20))
    screen.blit(settings_icon, (353,10))
    
    
    pygame.display.flip()
    