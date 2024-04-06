import pygame
import os
from buttons import *

pygame.init()

# Initialize Screen
WIDTH, HEIGHT = 400, 450
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("To-Do App.")

# Colors
BABY_BLUE = (184, 215, 233)
LIST_BLUE = (135, 206, 250)
SLIGHTLY_DARKER_BLUE = (91, 120, 201)
WHITE = (255, 255, 255)

# Initialize To-Do 
dialog_box = pygame.Surface((250, 230))
dialog_box.fill(LIST_BLUE)

# Check Mark Image
check_mark = pygame.image.load('checkmark.png')
check_mark = pygame.transform.scale(check_mark, (20, 20))
checkmark = pygame.image.load(os.path.join('checkmark.png'))

# Running the Clock
FPS = 60

# Make Check Boxes
y_coord_box = 30

# Make Rectangles for Text
box1 = box2 = box3 = box4 = box5 = pygame.image.load('text_box.png')
box1 = box2 = box3 = box4 = box5 = pygame.transform.scale(check_mark, (100, 20))
box1 = box2 = box3 = box4 = box5 = pygame.image.load(os.path.join('text_box.png'))

# Generate Check Boxes
def check_box(platform):
    y_coord = 28
    for i in range(5):
        pygame.draw.rect(platform, WHITE, pygame.Rect(20, y_coord, 20, 20), 3)
        y_coord += 40

# Generate Box for Title
def title_page():
    title = pygame.Surface((250, 30))
    title.fill(SLIGHTLY_DARKER_BLUE)
    return title

# Combine Everything onto the Screen
def draw_window():

    SCREEN.fill(BABY_BLUE)

    # Blit the various screens
    check_box(dialog_box)
    todo_title = title_page()
    SCREEN.blit(dialog_box, (25, 120))
    SCREEN.blit(todo_title, (25, 100))
    AddText(SCREEN, 26, "To-Do List", WHITE, 100, 105)

    # Text Boxes
    SCREEN.blit(box1, (75, 143))
    SCREEN.blit(box2, (75, 183))
    SCREEN.blit(box3, (75, 223))
    SCREEN.blit(box4, (75, 263))
    SCREEN.blit(box5, (75, 303))

# Defining the buttons
button1 = pygame.Rect(45, 148, 20, 20)
button2 = pygame.Rect(45, 185, 20, 20)
button3 = pygame.Rect(45, 222, 20, 20)
button4 = pygame.Rect(45, 259, 20, 20)
button5 = pygame.Rect(45, 296, 20, 20)

# Main Loop
def main():
    image_click = False
    user_input1, user_input2, user_input3, user_input4, user_input5 = "", "", "", "", ""
    button1_state, button2_state, button3_state, button4_state, button5_state, = False, False, False, False, False
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        # Start the windows
        draw_window()
        pygame.draw.rect(SCREEN, (255, 255, 255), button1, 3)
       
        # Typing Functionality for the Tasks
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    if(box1.get_rect(center=(125, 153)).collidepoint(pygame.mouse.get_pos())): user_input1 = user_input1[:-1]
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(box1.get_rect(center=(125, 153)).collidepoint(pygame.mouse.get_pos())):
                        user_input1 += event.unicode

            AddText(SCREEN, 20, user_input1, (0,0,0), 82, 150)

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    if(box2.get_rect(center=(125, 193)).collidepoint(pygame.mouse.get_pos())): user_input2 = user_input2[:-1]
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(box2.get_rect(center=(125, 193)).collidepoint(pygame.mouse.get_pos())):
                        user_input2 += event.unicode

            AddText(SCREEN, 20, user_input2, (0,0,0), 82, 190)

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    if(box3.get_rect(center=(125, 233)).collidepoint(pygame.mouse.get_pos())): user_input3 = user_input3[:-1]
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(box3.get_rect(center=(125, 233)).collidepoint(pygame.mouse.get_pos())):
                        user_input3 += event.unicode

            AddText(SCREEN, 20, user_input3, (0,0,0), 82, 230)

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    if(box4.get_rect(center=(125, 273)).collidepoint(pygame.mouse.get_pos())): user_input4 = user_input4[:-1]
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(box4.get_rect(center=(125, 273)).collidepoint(pygame.mouse.get_pos())):
                        user_input4 += event.unicode

            AddText(SCREEN, 20, user_input4, (0,0,0), 82, 270)

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    if(box5.get_rect(center=(125, 313)).collidepoint(pygame.mouse.get_pos())): user_input5 = user_input5[:-1]
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(box5.get_rect(center=(125, 313)).collidepoint(pygame.mouse.get_pos())):
                        user_input5 += event.unicode

            AddText(SCREEN, 20, user_input5, (0,0,0), 82, 310)
            
            # Houses the Checkmark Functionality
            pos = pygame.mouse.get_pos()
            if button1.collidepoint(pos) or button2.collidepoint(pos) or button3.collidepoint(pos) or button4.collidepoint(pos) or button5.collidepoint(pos):
                if button1.collidepoint(pos):
                    SCREEN.blit(check_mark, (45, 145))
                if button2.collidepoint(pos):
                    SCREEN.blit(check_mark, (45, 185))
                if button3.collidepoint(pos):
                    SCREEN.blit(check_mark, (45, 225))
                if button4.collidepoint(pos):
                    SCREEN.blit(check_mark, (45, 265))
                if button5.collidepoint(pos):
                    SCREEN.blit(check_mark, (45, 305))

            # Disappearing and Reappearing for Checkmarks.
            # As well as selecting and deselecting.
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                print(click)
                if button1.collidepoint(click) or button2.collidepoint(click) or button3.collidepoint(click) or button4.collidepoint(click) or button5.collidepoint(pos):
                    image_click = True

            if image_click:
                image_click = False
                if button1.collidepoint(click):
                    SCREEN.blit(check_mark, (45, 145))
                    print (button1_state)
                    button1_state = not button1_state
                if button2.collidepoint(click):
                    SCREEN.blit(check_mark, (45, 185))
                    button2_state = not button2_state
                if button3.collidepoint(click):
                    SCREEN.blit(check_mark, (45, 225))
                    button3_state = not button3_state
                if button4.collidepoint(click):
                    SCREEN.blit(check_mark, (45, 265))
                    button4_state = not button4_state
                if button5.collidepoint(click):
                    SCREEN.blit(check_mark, (45, 305))
                    button5_state = not button5_state

            if button1_state:
                SCREEN.blit(check_mark, (45, 145))
            if button2_state:
                SCREEN.blit(check_mark, (45, 185))
            if button3_state:
                SCREEN.blit(check_mark, (45, 225))
            if button4_state:
                SCREEN.blit(check_mark, (45, 265))
            if button5_state:
                SCREEN.blit(check_mark, (45, 305))

            # Update everything.
            pygame.display.flip()

            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()