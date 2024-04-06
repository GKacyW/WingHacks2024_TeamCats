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
    "Clear": {"day": "images/clear.png", "night": "images/clear night.png"},
    "Clouds": {"day": "images/scattered clouds.png", "night": "images/scattered clouds night.png"},
    "Drizzle": {"day": "images/rain shower.png", "night": "images/rain shower night.png"},
    "Rain": {"day": "images/rain.png", "night": "images/rain night.png"},
    "Thunderstorm": {"day": "images/thunderstorm.png", "night": "images/thunderstorm night.png"},
    "Snow": {"day": "images/snow.png", "night": "images/snow night.png"},
    "Atmosphere": {"day": "images/mist.png", "night": "images/mist night.png"}
}
bar = {
    "day": "images/day_bar.png",
    "night": "images/night_bar.png"
}
settings_icon = pygame.image.load('images/settings.png')
exit_icon = pygame.image.load('images/exit.png')
selected = pygame.image.load('images/selected button.png')
selected_icon = pygame.transform.scale(selected, (15,15))
empty = pygame.image.load('images/empty button.png')
insert_city_bar = pygame.image.load('images/input city.png')
empty_icon = pygame.transform.scale(empty, (15,15))
city = "Gainesville, Florida, USA"
unit = "C"
military_time = False
military_time_toggle = Button(30, 21, empty_icon)

settings = False
clock = pygame.time.Clock()
FPS = 60
user_input = ""
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_BACKSPACE):
                if(settings): user_input = user_input[:-1]
            elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                if(settings):
                    user_input += event.unicode
            


    
    
    screen.fill((184,215,233))

    if(not settings):
    #do weather determinations
        weather_data = get_weather(city, unit)
        weather_condition = weather_data[1]
        weather_description = weather_data[2]
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
                sunset_time = sunset_time + subtract_12
            elif(local_time.hour == 00):
                add_12 = timedelta(hours=12)
                local_time = local_time + add_12
                
                
        


        weather_picture = (weather_icons.get(weather_condition, {}).get(day_or_night))
        weather = pygame.image.load(weather_picture).convert_alpha()
        bar_path = bar.get(day_or_night)
        bar_ = pygame.image.load(bar_path).convert_alpha()
        settings_bar = pygame.image.load(bar_path).convert_alpha()
        

        if(day_or_night == "day"):
            weather_color = (0,0,0)
        else:
            weather_color = (255,255,255)

        
        if(not military_time):
            if(00 <= local_time_for_non_military.hour < 12):
                time_thing = "AM"
            else:
                time_thing = "PM"
        

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
        AddText(screen, 18, weather_description, weather_color, 135, 60)
    
        setting_button = Button(353, 10, settings_icon)
        

        if setting_button.draw(screen):
            settings = True
        
    if settings:
        screen.blit(settings_bar, (25,10))
        exit_button = Button(353, 85, exit_icon)
        if exit_button.draw(screen):
            settings = False
            city = user_input
    
        
        if(unit == "F"): coordinates_for_paw = (30, 42)
        elif(unit == "C"): coordinates_for_paw = (30, 60)
        elif(unit == "K"): coordinates_for_paw = (30, 78)

        far_button = Button(30, 42, empty_icon)
        celcius_button = Button(30, 60, empty_icon)
        kelvin_button = Button(30, 78, empty_icon)

        screen.blit(empty_icon, (30, 21))
        
        


        if far_button.draw(screen) and settings:
            unit = "F"
        elif celcius_button.draw(screen) and settings:
            unit = "C"
        elif kelvin_button.draw(screen) and settings:
            unit = "K"

        if military_time_toggle.draw(screen) and settings:
            if(military_time):
                military_time = False
            else:
                military_time = True

        
        
        
        screen.blit(empty_icon, (30, 42))
        AddText(screen, 18, "Fahrenheit", weather_color, 50, 42)
        screen.blit(empty_icon, (30, 60))
        AddText(screen, 18, "Celcius", weather_color, 50, 60)
        screen.blit(empty_icon, (30, 78))
        AddText(screen, 18, "Kelvin", weather_color, 50, 78)
        screen.blit(selected_icon, coordinates_for_paw)
        if(military_time): screen.blit(selected_icon, (30,21))
        AddText(screen, 18, "Military Time", weather_color, 50, 21)

        screen.blit(insert_city_bar, (140, 78))
        AddText(screen, 20, user_input,(0,0,0), 140, 78)
        AddText(screen, 20, "Change City :P", (0,0,0), 140, 55)
        


        
        
            
        
        

        

        
    

    
    
    pygame.display.flip()
