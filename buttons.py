import pygame
class Button():

    
    def __init__(self, x, y, image):
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self, surface):
            action = False
            #get mouse position
            pos = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

            #draw button on screen
            surface.blit(self.image, (self.rect.x, self.rect.y))

            return action

def AddText(screen, font_size, words, color, x, y):
    Font = pygame.font.Font('VT323-Regular.ttf', font_size)
    text = Font.render(words, True, color)
    screen.blit(text, (x, y))