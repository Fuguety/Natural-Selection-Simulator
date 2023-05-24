import Entities.EntityHerbivor as Entity
import Entities.EntityCarnivor as EntityCarnivor
import Entities.Food as Food
import pygame
import Configuration as configuration
from math import cos,sin,radians,floor,sqrt,ceil
import numpy as np

class Simulation:
    
    def __init__(self, entity_quantity_herbivor, entity_quantity_carnivor, food_quantity, arena_radius):
        
        self.global_food = [[[] for row in range(20)] for column in range(ceil(configuration.y / (configuration.x / 20)))]
        self.arena_radius = arena_radius
        self.entity_list_herbivor = []  
        self.entity_list_carnivor = [] 
        self.food_list = []
        self.food_quantity = food_quantity
        self.entity_quantity_herbivor = entity_quantity_herbivor
        self.entity_quantity_carnivor = entity_quantity_carnivor
        self.food_quantity_present = food_quantity
        self.entity_quantity_alive = entity_quantity_herbivor + entity_quantity_carnivor
        self.show_render = False

        self.startRound(entity_quantity_herbivor, entity_quantity_carnivor, food_quantity)

    def startRound(self, entity_quantity_herbivor, entity_quantity_carnivor,food_quantity, restart = True):
        if restart:
            self.global_food = [[[] for row in range(20)] for column in range(ceil(configuration.y / (configuration.x / 20)))]
            self.entity_list_herbivor = []
            self.entity_list_carnivor = []    
            self.food_list = []
            self.food_quantity = food_quantity
            self.entity_quantity = entity_quantity_herbivor + entity_quantity_carnivor
            self.entity_quantity_herbivor_alive = entity_quantity_herbivor
            self.entity_quantity_carnivor_alive = entity_quantity_carnivor
            self.food_quantity_present = food_quantity
            self.entity_quantity_alive = entity_quantity_herbivor + entity_quantity_carnivor

        for i in range(1, entity_quantity_herbivor + 1):
            position_x = i * (configuration.x / (entity_quantity_herbivor + 2))
            self.entity_list_herbivor.append(Entity.EntityHerbivor(position_x, configuration.y - 5, 90, 1, 1))

        for i in range(1, entity_quantity_carnivor + 1):
            position_x = i * (configuration.x / (entity_quantity_herbivor + 2))
            self.entity_list_carnivor.append(EntityCarnivor.EntityCarnivor(position_x, configuration.y - 10, 90, 1, 1))

        for _ in range(food_quantity):
            food_x = np.random.randint(50,configuration.x - 50)
            food_y = np.random.randint(50, configuration.y - 50)

            food = Food.Food([food_x, food_y], "orange")

            self.global_food[floor(food_y / (configuration.x / 20))][floor(food_x / (configuration.x / 20))].append(food)

        self.drawFoods()
        self.drawEntities()

        pygame.display.flip()

    def drawFoods(self):
        for column in self.global_food:
            for row in column:
                for food in row:
                    if not food.devoured:
                        food.draw()
            
    def drawEntities(self):
        for entity in self.entity_list_herbivor:
            entity.drawHerbivor()        
        for entity in self.entity_list_carnivor:
            entity.drawCarnivor()

    def drawHemispheres(self):
        x = 20
        block_size = configuration.x / x
        for row in range(x):
           #esquerda para direita
            pygame.draw.line(configuration.screen, "black", [0, row * block_size], [configuration.x, row * block_size])
           
           #cima para baixo
            pygame.draw.line(configuration.screen, "black", [row * block_size,0], [row * block_size, configuration.y])
    
    def tick(self, collision = True):
        for entity in self.entity_list_herbivor:
            entity.drawHerbivor()

            if entity.alive:
                
                position = entity.getPosition()
    
                if (2 < position[0] < configuration.x) and (0 < position[1] < configuration.y) :
                    temp = self.getMatrixPosition(entity)
                    entity.move(self.global_food[temp[0]][temp[1]])
                    if collision:
                        self.collision(entity, temp[0], temp[1])                
                else:
                    entity.alive = False
                    self.entity_quantity_alive -= 1        
        
        for entity in self.entity_list_carnivor:
            entity.drawCarnivor()

            if entity.alive:
                
                position = entity.getPosition()
    
                if (2 < position[0] < configuration.x) and (0 < position[1] < configuration.y) :
                    temp = self.getMatrixPosition(entity)
                    entity.move(self.global_food[temp[0]][temp[1]])
                    if collision:
                        self.collision(entity, temp[0], temp[1])                
                else:
                    entity.alive = False
                    self.entity_quantity_alive -= 1



        

    def collision(self, entity, column, row):
        ent_x = entity.getPosition()[0]
        ent_y = entity.getPosition()[1]
        
        for index, food_for in enumerate(self.global_food[column][row]):
            if not food_for.devoured:
                food_x = food_for.position_x
                food_y = food_for.position_y
                radius_sum = configuration.entity_radius + configuration.food_radius

                if entity.distanceBetween(food_x, food_y) <= radius_sum:
                    food_for.devoured = True
                    self.food_quantity_present -= 1
                    entity.food_eaten += 1 # when food is eaten, it adds to invetory
                    del self.global_food[column][row][index]
                
                if self.show_render:
                    pygame.draw.line(configuration.screen, "blue", [ent_x, ent_y], [food_x, food_y])

    def drawStatistics(self, position):        
        font = pygame.font.SysFont("Verdana", 20)
        text_entities = font.render(f'entidades vivas: {str(self.entity_quantity_alive)}',True, "black")
        text_food = font.render(f'comidas presentes: {str(self.food_quantity_present)}',True, "black")

        configuration.screen.blit(text_entities, position)
        configuration.screen.blit(text_food, [position[0], position[1] + 25])

    def drawRender(self):
        self.show_render = not self.show_render
    
    # at end of simluation define who reproduces, survive or die    
    def addEntity(self):
        for entityEat in self.entity_list_herbivor:
            if entityEat.food_eaten >= 2: # reproduce
                entityEat.food_eaten = 0 # resets invetory to 0
                self.entity_quantity_herbivor_alive += 1
            elif entityEat.food_eaten == 1: # survives
                entityEat.food_eaten = 0
            else:                           # dies
                self.entity_quantity_herbivor_alive -= 1
        
        for entityEat in self.entity_list_carnivor:
            if entityEat.food_eaten >= 2: # reproduce
                entityEat.food_eaten = 0 # resets invetory to 0
                self.entity_quantity_carnivor_alive += 1
            elif entityEat.food_eaten == 1: # survives
                entityEat.food_eaten = 0
            else:                           # dies
                self.entity_quantity_carnivor_alive -= 1
    
    def getMatrixPosition(self, entity):
        ent_position = entity.getPosition()
        return [floor(ent_position[1] / (configuration.x / 20)), floor(ent_position[0] / (configuration.x / 20))]

                