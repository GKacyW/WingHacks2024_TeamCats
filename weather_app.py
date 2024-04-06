import pygame
from weather import *
from datetime import timedelta, datetime
from buttons import *
pygame.init()
screen = pygame.display.set_mode((400,450))
clock = pygame.time.Clock()
running = True


# weather specific code

weather_icons = {
    "clear sky": {"day": "images/clear.png", "night": "images/clear night.png"},
    "few clouds": {"day": "images/scattered clouds.png", "night": "images/scattered clouds night.png"},
    "scatted clouds": {"day": "images/scattered clouds.png", "night": "images/scattered clouds night.png"},
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
settings_icon = pygame.image.load('images/settings.png')

city = "Gainesville, Florida, USA"
unit = "C"
military_time = False



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #not weather specific
    font_size_25 = pygame.font.Font('VT323-Regular.ttf', 25)
    font_size_15 = pygame.font.Font('VT323-Regular.ttf', 20)
    font_size_30 = pygame.font.Font('VT323-Regular.ttf', 30)
    font_size_50 = pygame.font.Font('VT323-Regular.ttf', 45)
    font_size_7 = pygame.font.Font('VT323-Regular.ttf', 18)
    
    screen.fill((184,215,233))
    #do weather determinations
    weather_data = get_weather(city, unit)
    weather_condition = weather_data[1]
    temp = str(weather_data[0]) + unit

    #time determinations
    time_determinations = get_time(city)
    day_or_night = time_determinations[1]
    
    sunrise_time = time_determinations[0][0]
    sunset_time = time_determinations[0][1]
    local_time = time_determinations[0][2]
    local_time_for_non_military = time_determinations[0][2]

    if not military_time:
        if(local_time.hour > 12):
            subtract_12 = timedelta(hours=-12)
            local_time = local_time + subtract_12
        elif(local_time.hour == 00):
            add_12 = timedelta(hours=12)
            local_time = local_time + add_12
            
            
       


    weather_picture = (weather_icons.get(weather_condition, {}).get(day_or_night))
    weather = pygame.image.load(weather_picture).convert_alpha()
    bar_path = bar.get(day_or_night)
    bar_ = pygame.image.load(bar_path).convert_alpha()
    

    if(day_or_night == "day"):
        weather_color = (0,0,0)
    else:
        weather_color = (255,255,255)

    
    if(not military_time):
        if(00 <= local_time_for_non_military.hour < 12):
            time_thing = "AM"
        else:
            time_thing = "PM"

            

    
    


    weather_description = font_size_15.render(weather_condition, False, weather_color)
    

    if( day_or_night == "day"):
        sun = sunset_time.strftime("%H:%M")
        sun_pic = pygame.image.load('images/sunset.png').convert_alpha()
    else:
        sun = sunrise_time.strftime("%H:%M")
        sun_pic = pygame.image.load('images/sunrise.png').convert_alpha()



    #Images
    screen.blit(bar_,(25,10))
    screen.blit(weather, (30,20))
    screen.blit(sun_pic, (135, 85))
    


    # Text
    AddText(screen, 20, sun, weather_color, 145, 87)
    if(not military_time): AddText(screen, 18, time_thing, weather_color, 360, 50)
    AddText(screen, 25, local_time.strftime("%Y-%m-%d"),weather_color, 260, 78)
    AddText(screen, 30, local_time.strftime("%H:%M"), weather_color, 296, 50)
    AddText(screen, 45, temp, weather_color, 135, 25)
    AddText(screen, 18, weather_condition, weather_color, 135, 60)
    
    setting_button = Button(353, 10, settings_icon)
    setting_button.clicked = False
    

    
    
    pygame.display.flip()
