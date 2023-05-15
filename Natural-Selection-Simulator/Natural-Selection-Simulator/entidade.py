import pygame
from math import sin,cos,tan,radians, pi, sqrt
import numpy as np


class entidade:
    
    # Builder
    def __init__(self, screen, positionX, positionY, anguloVisao):
        self.radius = 10
        self.positionX = positionX
        self.positionY = positionY
        self.screen = screen
        self.anguloVisao = anguloVisao
        self.anguloVisaoAlvo = self.anguloVisao
        self.currentPosition = [positionX, positionY, self.radius]

    def getPosition(self):
        return [self.positionX, self.positionY]

    def randomMove(self):
        if self.anguloVisao == self.anguloVisaoAlvo:
            if np.random.randint(0,2):
                self.anguloVisaoAlvo += np.random.randint(10,21)
            else:
                self.anguloVisaoAlvo -= np.random.randint(10,21)

        if self.anguloVisao > self.anguloVisaoAlvo:
            self.anguloVisao -= 1
        
        elif self.anguloVisao < self.anguloVisaoAlvo:
            self.anguloVisao += 1

        self.positionX += cos(radians(self.anguloVisao))
        self.positionY -= sin(radians(self.anguloVisao))

    def draw(self):
        pygame.draw.circle(self.screen, "green", self.getPosition(), self.radius)

        pygame.draw.line(self.screen, "green", self.getPosition(), self.varFrente(), 2)
    
    def varFrente(self):
        x = self.positionX + cos(radians(self.anguloVisao)) * 20
        y = self.positionY - sin(radians(self.anguloVisao)) * 20
        return [x,y]

    def calculaDistancia(self,posX, posY):
        a = self.positionX - posX
        b = self.positionY - posY
        return sqrt(a ** 2 + b ** 2)
    
    # Gets current coordinates and size
    def getCurrentPosition(self):
        return self.currentPosition