import pygame
from math import sin, cos, radians, sqrt, atan2, pi
import Configuration as configuration
import Entities.Entity as Entity
import Entities.Food as Food



class EntityHerbivor(Entity.Entity):
    def __init__(self, screen, position_x, position_y, vision_angle, tier, speed):

        super().__init__(screen, position_x, position_y, vision_angle)

        self.type = "herbivor"
        self.speed = 2
        self.tier = tier
        self.color = "green"
        self.food_type = "plant"

    