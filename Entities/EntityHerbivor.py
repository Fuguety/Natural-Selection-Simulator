import pygame
from math import sin, cos, radians, sqrt, atan2, pi, degrees, acos, floor
import Configuration as configuration
import Entities.Entity as Entity
import Entities.Food as Food



class EntityHerbivor(Entity.Entity):
    def __init__(self, position_x, position_y, vision_angle, tier, speed):

        super().__init__(position_x, position_y, vision_angle)

        self.type = "herbivor"
        self.speed = 2
        self.tier = tier
        self.color = "green"
        self.food_type = "plant"

    def drawHerbivor(self):
        pygame.draw.circle(configuration.screen, self.color, self.getPosition(), self.radius)
        pygame.draw.line(configuration.screen, self.color, self.getPosition(), self.frontLine(), 2)

