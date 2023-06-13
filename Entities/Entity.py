import pygame
import Configuration as configuration
from math import sin, cos, radians, sqrt, atan2, pi, acos, degrees, floor
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
        self.matrixPosition = [0,0]

    def getPosition(self):
        return [self.position_x, self.position_y]
    
    def move(self, possible_foods, show_renderer):
        
        if len(possible_foods) != 0:
            closer_food = possible_foods[0]
            closer_food_cord = [possible_foods[0].getPosition()[0], possible_foods[0].getPosition()[1]]
            closer_distance = self.distanceBetween(possible_foods[0].getPosition()[0], possible_foods[0].getPosition()[1])
            closer_index = 0

            for index, food in enumerate(possible_foods):

                x = food.getPosition()[0]
                y = food.getPosition()[1]
                actual_distance = self.distanceBetween(x, y)
                if actual_distance < closer_distance:
                    closer_distance = actual_distance
                    closer_food_cord = [x, y]
                    closer_food = food
                    closer_index = index

                if show_renderer:
                    pygame.draw.line(configuration.screen, "Blue", self.getPosition(), [x,y])

            vec1 = [ closer_food_cord[0] - self.position_x, self.position_y - closer_food_cord[1] ]
            vec2 = [1,0]

            produto_escalar = vec1[0] * vec2[0] + vec1[1] * vec2[1]
            modulo_vec1 = sqrt(vec1[0] * vec1[0] + vec1[1] * vec1[1])
            modulo_vec2 = sqrt(vec2[0] * vec2[0] + vec2[1] * vec2[1])

            angulo =  degrees (acos(produto_escalar / (modulo_vec1 * modulo_vec2)))

            if self.position_y < closer_food_cord[1]:
                angulo = 360 - angulo
            self.target_vision_angle = angulo


            if (self.vision_angle - self.target_vision_angle) * (self.vision_angle - self.target_vision_angle) <= 25:
                self.vision_angle = self.target_vision_angle
            if self.vision_angle > self.target_vision_angle:
                self.vision_angle -= 5       
            elif self.vision_angle < self.target_vision_angle:
                self.vision_angle += 5


            self.position_x += cos(radians(self.vision_angle)) * self.speed
            self.position_y -= sin(radians(self.vision_angle)) * self.speed


            if self.distanceBetween(closer_food_cord[0],closer_food_cord[1]) <= closer_food.radius + configuration.entity_radius:
                self.food_eaten += 1
                return [floor(closer_food_cord[1] / (configuration.x / 20)), floor(closer_food_cord[0] / (configuration.x / 20)), closer_index]
        
        else:
            angular_speed = 1

            matrix_x = self.matrixPosition[0]
            matrix_y = self.matrixPosition[1]

            if matrix_x == 0:
                angular_speed = 5
                if matrix_y == 0:
                    self.target_vision_angle = 315
                elif matrix_y == 19:
                    self.target_vision_angle = 225
                else:
                    self.target_vision_angle = 270

            elif matrix_x == 10:
                angular_speed = 5

                if matrix_y == 0:
                    self.target_vision_angle = 45
                elif matrix_y == 19:
                    self.target_vision_angle = 135
                else:
                    self.target_vision_angle = 90
            
            elif matrix_y == 0:
                angular_speed = 5
                self.target_vision_angle = 0
            
            elif matrix_y == 19:
                angular_speed = 5
                self.target_vision_angle = 180


            elif self.vision_angle == self.target_vision_angle:
                if np.random.randint(0, 2):
                    self.target_vision_angle += np.random.randint(10, 21)
                else:
                    self.target_vision_angle -= np.random.randint(10, 21)

            elif (self.vision_angle - self.target_vision_angle) * (self.vision_angle - self.target_vision_angle) <= 25:
                self.vision_angle = self.target_vision_angle

            if self.vision_angle > self.target_vision_angle:
                self.vision_angle -= angular_speed        
            elif self.vision_angle < self.target_vision_angle:
                self.vision_angle += angular_speed

            self.position_x += cos(radians(self.vision_angle)) * self.speed
            self.position_y -= sin(radians(self.vision_angle)) * self.speed

        return False
    
    def frontLine(self):
        x = self.position_x + cos(radians(self.vision_angle)) * self.radius * 1.5
        y = self.position_y - sin(radians(self.vision_angle)) * self.radius * 1.5
        return [x, y]

    def distanceBetween(self, position_x, position_y):
        x_difference = self.position_x - position_x
        y_difference = self.position_y - position_y
        return sqrt(x_difference ** 2 + y_difference ** 2)
    
