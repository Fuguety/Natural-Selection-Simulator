import pygame
import Configuration as configuration
from math import sin, cos, radians, sqrt, atan2, pi, acos, degrees
import numpy as np

class Entity:
    
    def __init__(self, position_x, position_y, vision_angle):
        self.alive = True
        self.radius = configuration.entity_radius
        self.position_x = position_x
        self.position_y = position_y
        self.screen = configuration.screen
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
            
            vec1 = [ closer_food[0] - self.position_x, self.position_y - closer_food[1] ]
            vec2 = [1,0]

            produto_escalar = vec1[0] * vec2[0] + vec1[1] * vec2[1]
            modulo_vec1 = sqrt(vec1[0] * vec1[0] + vec1[1] * vec1[1])
            modulo_vec2 = sqrt(vec2[0] * vec2[0] + vec2[1] * vec2[1])

            angulo =  degrees (acos(produto_escalar / (modulo_vec1 * modulo_vec2)))

            if self.position_y < closer_food[1]:
                angulo = -angulo

            self.target_vision_angle = angulo


            if (self.vision_angle - self.target_vision_angle) * (self.vision_angle - self.target_vision_angle) <= 25:
                self.vision_angle = self.target_vision_angle
            if self.vision_angle > self.target_vision_angle:
                self.vision_angle -= 5       
            elif self.vision_angle < self.target_vision_angle:
                self.vision_angle += 5


            self.position_x += cos(radians(self.vision_angle))
            self.position_y -= sin(radians(self.vision_angle))
        else:
            if self.vision_angle == self.target_vision_angle:
                if np.random.randint(0, 2):
                    self.target_vision_angle += np.random.randint(10, 21)
                else:
                    self.target_vision_angle -= np.random.randint(10, 21)

            if (self.vision_angle - self.target_vision_angle) * (self.vision_angle - self.target_vision_angle) <= 25:
                self.vision_angle = self.target_vision_angle

            if self.vision_angle > self.target_vision_angle:
                self.vision_angle -= 1        
            elif self.vision_angle < self.target_vision_angle:
                self.vision_angle += 1

            self.position_x += cos(radians(self.vision_angle))
            self.position_y -= sin(radians(self.vision_angle))


    
    def frontLine(self):
        x = self.position_x + cos(radians(self.vision_angle)) * self.radius * 2
        y = self.position_y - sin(radians(self.vision_angle)) * self.radius * 2
        return [x, y]

    def distanceBetween(self, position_x, position_y):
        x_difference = self.position_x - position_x
        y_difference = self.position_y - position_y
        return sqrt(x_difference ** 2 + y_difference ** 2)