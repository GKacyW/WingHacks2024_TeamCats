import pygame
class Button():

    
    def __init__(self, x, y, image):
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

def AddText(screen, font_size, words, color, x, y):
    Font = pygame.font.Font('VT323-Regular.ttf', font_size)
    text = Font.render(words, False, color)
    screen.blit(text, (x, y))