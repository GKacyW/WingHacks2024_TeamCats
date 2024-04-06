import pygame
import weather

pygame.init()
screen = pygame.display.set_mode((400,450))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((184,215,233))
    pygame.draw.rect(screen, "Red", [30,20,400-50,90], 4)
    pygame.display.flip()
    