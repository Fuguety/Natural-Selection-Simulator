import pygame
from math import sin, cos, radians, sqrt, atan2, pi
import numpy as np
import Configuration as configuration

class Entity:
    
    def __init__(self, screen, position_x, position_y, vision_angle):
        self.alive = True
        self.radius = 10
        self.position_x = position_x
        self.position_y = position_y
        self.screen = screen
        self.vision_angle = vision_angle
        self.target_vision_angle = self.vision_angle
        self.food_eaten = 0

    def getPosition(self):
        return [self.position_x, self.position_y]
    
    def move(self, possible_foods):
        
        if len(possible_foods) != 0:
            closer_food = [possible_foods[0].getPosition()[0], possible_foods[0].getPosition()[1]]
            closer_distance = self.distanceBetween(possible_foods[0].getPosition()[0], possible_foods[0].getPosition()[1])
            
            for food in possible_foods:
                x = food.getPosition()[0]
                y = food.getPosition()[1]

                actual_distance = self.distanceBetween(x, y)
                if actual_distance < closer_distance:
                    closer_distance = actual_distance
                    closer_food = [x, y]
            
            distance_x = closer_food[0] - self.position_x
            distance_y = closer_food[1] - self.position_y
            
            delta_x = distance_x / closer_distance
            delta_y = distance_y / closer_distance

            #angle = atan2(distance_y, distance_x)
            #angle = angle * 180 / pi

            #self.target_vision_angle = angle
            self.position_x += delta_x
            self.position_y += delta_y
        else:
            if self.vision_angle == self.target_vision_angle:
                if np.random.randint(0, 2):
                    self.target_vision_angle += np.random.randint(10, 21)
                else:
                    self.target_vision_angle -= np.random.randint(10, 21)

            if self.vision_angle > self.target_vision_angle:
                self.vision_angle -= 1        
            elif self.vision_angle < self.target_vision_angle:
                self.vision_angle += 1

            self.position_x += cos(radians(self.vision_angle))
            self.position_y -= sin(radians(self.vision_angle))

    def draw(self):
        pygame.draw.circle(self.screen, "green", self.getPosition(), self.radius)
        pygame.draw.line(self.screen, "green", self.getPosition(), self.frontLine(), 2)
    
    def frontLine(self):
        x = self.position_x + cos(radians(self.vision_angle)) * 20
        y = self.position_y - sin(radians(self.vision_angle)) * 20
        return [x, y]

    def distanceBetween(self, position_x, position_y):
        x_difference = self.position_x - position_x
        y_difference = self.position_y - position_y
        return sqrt(x_difference ** 2 + y_difference ** 2)