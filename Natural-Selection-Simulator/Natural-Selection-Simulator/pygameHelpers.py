import pygame

def pause(janela):
    pause = True

    rect1 = pygame.Rect(50,50,40,150)
    rect2 = pygame.Rect(130,50,40,150)

    pygame.draw.rect(janela, "white", rect1)
    pygame.draw.rect(janela, "white", rect2)

    pygame.display.flip()

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return