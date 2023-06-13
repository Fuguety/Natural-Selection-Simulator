import pygame

def pause(window):
    pause = True

    first_rectangle = pygame.Rect(1100,50,40,150)
    second_rectangle = pygame.Rect(1180,50,40,150)

    pygame.draw.rect(window, "white", first_rectangle)
    pygame.draw.rect(window, "white", second_rectangle)

    pygame.display.flip()

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:
                    return