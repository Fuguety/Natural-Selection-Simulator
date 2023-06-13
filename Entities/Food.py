import numpy as np
import pygame
import Entities.Entity as entity
import Configuration as configuration
from math import cos, sin, sqrt

class Food:
    
    def __init__(self, initial_position, color):
        self.position_x = initial_position[0]
        self.position_y = initial_position[1]
        self.screen = configuration.screen
        self.radius = configuration.food_radius
        self.devoured = False
        self.color = color

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [self.position_x, self.position_y], self.radius)
        
    def getPosition(self):
        return [self.position_x, self.position_y, self.radius]