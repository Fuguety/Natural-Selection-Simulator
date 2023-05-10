import numpy as np
import pygame
import Entities.Entity as entity
import Configuration as configuration
from math import cos, sin, sqrt

class Food:
    
    def __init__(self, screen, arena_radius, initial_position, color):
        food_center_distance = np.random.randint(10, arena_radius * (4/5))
        food_angle = np.random.randint(0,361)
        
        self.position_x = cos(food_angle) * food_center_distance + initial_position[0]
        self.position_y = initial_position[1] - sin(food_angle) * food_center_distance
        self.screen = screen
        self.radius = 5
        self.devoured = False
        self.arena_radius = arena_radius
        self.color = color
        self.food_type = "plant"
        self.spawn(initial_position)

    def spawn(self, initial_position, recursive = False):
        sum_radius = configuration.entity_radius + configuration.food_radius
        if recursive:
            food_radius = np.random.randint(60, self.arena_radius * (4/5))
            food_angle = np.random.randint(0,361)
            self.position_x = cos(food_angle) * food_radius + initial_position[0]
            self.position_y = initial_position[1] - sin(food_angle) * food_radius

        if abs(self.position_x - initial_position[0]) <= sum_radius:
            if self.position_x > initial_position[0]:
                self.position_x += np.random.randint(sum_radius, sum_radius + 5)
            else:
                self.position_x -= np.random.randint(sum_radius, sum_radius + 5)

        if abs(self.position_y - initial_position[1]) <= sum_radius:
            if self.position_y > initial_position[1]:
                self.position_y += np.random.randint(sum_radius, sum_radius + 5)
            else:
                self.position_y -= np.random.randint(sum_radius, sum_radius + 5)

        distance = sqrt((initial_position[0] - self.position_x) ** 2 + (initial_position[1] - self.position_y) ** 2)

        for i in range(0, configuration.quantity_circles):
            if abs(distance - (300 - (60 * i))) <= sum_radius:                
                self.spawn(initial_position, recursive=True)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [self.position_x, self.position_y], self.radius)
        
    def getPosition(self):
        return [self.position_x, self.position_y, self.radius]