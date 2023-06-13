import pygame
import Configuration



class fps:

    def __init__(self, position):
        self.clock = Configuration.clock
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(f'fps: {str(round(self.clock.get_fps()))}',True, "white")
        self.position = position
    def draw(self):
        self.text = self.font.render(f'fps: {str(round(self.clock.get_fps()))}',True, "white")
        Configuration.screen.blit(self.text, self.position)
