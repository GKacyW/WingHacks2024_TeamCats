import pygame 

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 450))
    run_app = True

    while run_app:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_app = False

        screen.fill((184, 215, 233))
        pygame.display.flip()

    pygame.quit()

main()
