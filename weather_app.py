import pygame
import weather
from astral.sun import sun

pygame.init()
screen = pygame.display.set_mode((400,450))
clock = pygame.time.Clock()
running = True

weather_icons = {
    "clear": {"day": "images/clear.png", "night": "images/clear night.png"},
    "cloudy": {"day": "images/cloudy.png", "night": "images/cloudy night.png"},
    "rain": {"day": "images/rain.png", "night": "images/rain night.png"}
}

bar = {
    "day": "images/day_bar.png",
    "night": "images/night_bar.png"
}
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((184,215,233))
    #do weather determinations
    weather_condition = "rain"
    time = "day"
    image_path = weather_icons.get(weather_condition, {}).get(time)
    image = pygame.image.load(image_path).convert_alpha()
    bar_path = bar.get(time)
    bar_ = pygame.image.load(bar_path).convert_alpha()

    screen.blit(bar_,(25,10))
    screen.blit(image, (30,20))
    
    pygame.display.flip()
    