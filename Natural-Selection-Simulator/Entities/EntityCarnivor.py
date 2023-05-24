import pygame
from math import sin, cos, radians, sqrt, atan2, pi
import Configuration as configuration
import Entities.Entity as Entity
import Entities.Food as Food



class EntityCarnivor(Entity.Entity):
    def __init__(self, position_x, position_y, vision_angle, tier, speed):

        super().__init__(position_x, position_y, vision_angle)

        self.type = "carnivor"
        self.speed = 2
        self.tier = tier
        self.color = "red"
        self.food_type = "herbivor"


    def drawCarnivor(self):
        pygame.draw.circle(self.screen, self.color, self.getPosition(), self.radius)
        pygame.draw.line(self.screen, self.color, self.getPosition(), self.frontLine(), 2)
