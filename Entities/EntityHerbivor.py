import pygame
from math import sin, cos, radians, sqrt, atan2, pi, degrees, acos, floor
import Configuration as configuration
import Entities.Entity as Entity
import Entities.Food as Food
import numpy as np



class EntityHerbivor(Entity.Entity):
    def __init__(self, position_x, position_y, vision_angle, tier, speed):

        super().__init__(position_x, position_y, vision_angle)

        self.type = "herbivor"
        self.speed = 2
        self.tier = tier
        self.color = "green"
        self.food_type = "plant"

    def drawHerbivor(self):
        pygame.draw.circle(self.screen, self.color, self.getPosition(), self.radius)
        pygame.draw.line(self.screen, self.color, self.getPosition(), self.frontLine(), 2)

    def move(self, possible_foods):
        
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
            
            vec1 = [ closer_food_cord[0] - self.position_x, self.position_y - closer_food_cord[1] ]
            vec2 = [1,0]

            produto_escalar = vec1[0] * vec2[0] + vec1[1] * vec2[1]
            modulo_vec1 = sqrt(vec1[0] * vec1[0] + vec1[1] * vec1[1])
            modulo_vec2 = sqrt(vec2[0] * vec2[0] + vec2[1] * vec2[1])

            angulo =  degrees (acos(produto_escalar / (modulo_vec1 * modulo_vec2)))

            if self.position_y < closer_food_cord[1]:
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


            #print(closer_food_cord)
            if self.distanceBetween(closer_food_cord[0],closer_food_cord[1]) <= configuration.food_radius + configuration.entity_radius:
                self.food_eaten += 1
                '''print("******************")
                print("******************")
                print("******************")'''
                return [floor(closer_food_cord[1] / (configuration.x / 20)), floor(closer_food_cord[0] / (configuration.x / 20)), closer_index]
        
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

        return False