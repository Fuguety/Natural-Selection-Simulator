import Entities.EntityHerbivor as Entity
import Entities.EntityCarnivor as EntityCarnivor 
import Entities.Food as Food
import pygame
import Configuration as configuration
from math import cos,sin,radians,floor,sqrt,ceil
import numpy as np
import time
import threading

class Simulation:
    
    def __init__(self, entity_quantity_herbivor, entity_quantity_carnivor, food_quantity, show_simulation):
        
        self.show_simulation = show_simulation
        self.global_food = [[[] for row in range(20)] for column in range(ceil(configuration.y / (configuration.x / 20)))]
        self.herbivor_id_matrix = [[[] for row in range(20)] for column in range(ceil(configuration.y / (configuration.x / 20)))]
        self.entity_list_herbivor = []  
        self.entity_list_carnivor = [] 
        self.food_quantity = food_quantity
        self.entity_quantity_herbivor = entity_quantity_herbivor
        self.entity_quantity_carnivor = entity_quantity_carnivor
        self.food_quantity_present = food_quantity
        self.entity_quantity_alive = entity_quantity_herbivor + entity_quantity_carnivor
        self.show_render = False

        self.startRound(entity_quantity_herbivor, entity_quantity_carnivor, food_quantity)

    def temp(self):
        for row in self.herbivor_id_matrix:
            print(row)

    def startRound(self, entity_quantity_herbivor, entity_quantity_carnivor,food_quantity, restart = False):
        if restart:
            self.global_food = [[[] for row in range(20)] for column in range(ceil(configuration.y / (configuration.x / 20)))]
            self.herbivor_id_matrix = [[[] for row in range(20)] for column in range(ceil(configuration.y / (configuration.x / 20)))]
            self.entity_list_herbivor = []  
            self.entity_list_carnivor = [] 
            self.food_quantity = food_quantity
            self.entity_quantity_herbivor = entity_quantity_herbivor
            self.entity_quantity_carnivor = entity_quantity_carnivor
            self.food_quantity_present = food_quantity
            self.entity_quantity_alive = entity_quantity_herbivor + entity_quantity_carnivor
            self.show_render = False

        for i in range(1, entity_quantity_herbivor + 1):
            position_x = i * (configuration.x / (entity_quantity_herbivor + 2))
            new_entity = Entity.EntityHerbivor(position_x, configuration.y - 5, 90, 1, 1)
            new_entity.matrixPosition = self.getMatrixPosition(new_entity)
            new_id_position = new_entity.matrixPosition
            self.entity_list_herbivor.append(new_entity)
            self.herbivor_id_matrix[new_id_position[0]][new_id_position[1]].append(i - 1)


        for i in range(1, entity_quantity_carnivor + 1):
            position_x = i * (configuration.x / (entity_quantity_carnivor + 2))
            self.entity_list_carnivor.append(EntityCarnivor.EntityCarnivor(position_x, 10, 270, 1, 1))

        for _ in range(food_quantity):
            food_x = np.random.randint(70,configuration.x - 70)
            food_y = np.random.randint(70, configuration.y - 90)

            food = Food.Food([food_x, food_y], "orange")

            self.global_food[floor(food_y / (configuration.x / 20))][floor(food_x / (configuration.x / 20))].append(food)

        if self.show_simulation:
            self.drawFoods()
            self.drawEntities()

            pygame.display.flip()

    def drawFoods(self):
        for column in self.global_food:
            for row in column:
                for food in row:
                    if not food.devoured:
                        food.draw()
                        
    # re grow the food that were eaten
    def growFood(self):
        while self.food_quantity_present <= self.food_quantity:
            
            self.food_quantity_present += 1

            food_x = np.random.randint(50,configuration.x - 50)
            food_y = np.random.randint(50, configuration.y - 50)

            food = Food.Food([food_x, food_y], "orange")

            self.global_food[floor(food_y / (configuration.x / 20))][floor(food_x / (configuration.x / 20))].append(food)
            
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
            pygame.draw.line(configuration.screen, "white", [0, row * block_size], [configuration.x, row * block_size])
           
           #cima para baixo
            pygame.draw.line(configuration.screen, "white", [row * block_size,0], [row * block_size, configuration.y])
    
    def tick(self):
        if self.show_simulation:
            self.drawFoods()

        for id, entity in enumerate(self.entity_list_herbivor):
            if entity.alive:
                if self.show_simulation:
                    entity.drawHerbivor()
                position = entity.getPosition()
    
                if (3 < position[0] < configuration.x - 3) and (3 < position[1] < configuration.y - 3) :
                    
                    return_type = entity.move(self.global_food[entity.matrixPosition[0]][entity.matrixPosition[1]], self.show_render)
                
                    if return_type != False:
                        self.food_quantity_present -= 1
                        del self.global_food[return_type[0]][return_type[1]][return_type[2]]

                    old_matriz_position = self.herbivor_id_matrix[entity.matrixPosition[0]][entity.matrixPosition[1]]

                    for index_id, old_id in enumerate(old_matriz_position):
                        if old_id == id:
                            del old_matriz_position[index_id]
                            

                    entity.matrixPosition = self.getMatrixPosition(entity)
                    self.herbivor_id_matrix[entity.matrixPosition[0]][entity.matrixPosition[1]].append(id)


                else:
                    entity.alive = False
                    self.entity_quantity_alive -= 1
        
        for entity in self.entity_list_carnivor:

            if entity.alive:
                if self.show_simulation:
                    entity.drawCarnivor()
                
                position = entity.getPosition()
    
                if (2 < position[0] < configuration.x) and (0 < position[1] < configuration.y) :
                    temp = self.getMatrixPosition(entity)
                    possible_ids = []
                    for adjacente_row in range(-1 if (temp[0] > 0) else 0, 2 if (temp[0] < 11) else 1):
                        actual_row = temp[0] + adjacente_row
                        for adjacente_column in range(-1 if (temp[1] > 0) else 0, 2 if (temp[1] < 19) else 1):
                            actual_column = temp[1] + adjacente_column
                            for actual_id in self.herbivor_id_matrix[actual_row][actual_column]:
                                if self.entity_list_herbivor[actual_id].alive == True:
                                    possible_ids.append(actual_id)

                    possible_pray = [self.entity_list_herbivor[i] for i in possible_ids]
                    
                    return_type = entity.move(possible_pray, self.show_render)
    
                    if return_type != False:
                        self.entity_quantity_herbivor -= 1
                        prey_position = possible_ids[return_type[2]]
                        self.entity_list_herbivor[prey_position].alive = False
                        self.entity_quantity_alive -= 1

                    entity.matrixPosition = self.getMatrixPosition(entity)



                else:
                    entity.alive = False
                    self.entity_quantity_alive -= 1
                    self.entity_quantity_carnivor -= 1  

    def drawStatistics(self, position):
        font = pygame.font.SysFont("Verdana", 20)
        text_entities = font.render(f'entidades vivas: {str(self.entity_quantity_alive)}',True, "white")
        text_food = font.render(f'comidas presentes: {str(self.food_quantity_present)}',True, "white")

        configuration.screen.blit(text_entities, position)
        configuration.screen.blit(text_food, [position[0], position[1] + 25])

    def drawRender(self):
        self.show_render = not self.show_render
    
    

    def createHerb(self, cord):    
        self.entity_quantity_alive +=1
        self.entity_quantity_herbivor += 1
        temp = Entity.EntityHerbivor(cord[0], cord[1], np.random.randint(0,360), 2, 2)
        temp.food_eaten = 1
        self.entity_list_herbivor.append(temp)

    def createCar(self,cord):
        self.entity_quantity_alive +=1
        self.entity_quantity_carnivor += 1
        temp = EntityCarnivor.EntityCarnivor(cord[0], cord[1], np.random.randint(0,360), 2, 2)
        temp.food_eaten = 2
        self.entity_list_carnivor.append(temp)
   
   
    def reproduceHerbivorOrDie(self):
        for entityHerbivor in self.entity_list_herbivor:
            if entityHerbivor.alive == True:
                if entityHerbivor.food_eaten >= 2: # reproduce
                    self.createHerb(entityHerbivor.getPosition())

                elif entityHerbivor.food_eaten < 1:
                    entityHerbivor.alive = False
                    self.entity_quantity_alive -= 1
                    self.entity_quantity_herbivor -= 1
        
                entityHerbivor.food_eaten = 0

    def reproduce(self):
        self.reproduceCarnivore()
        self.reproduceHerbivorOrDie()

    def reproduceCarnivore(self):
        for entity in self.entity_list_carnivor:
            if entity.alive == True:
                if entity.food_eaten >= 3: # reproduce
                    self.createCar(entity.getPosition())

                elif entity.food_eaten < 2:
                    entity.alive = False
                    self.entity_quantity_alive -= 1
                    self.entity_quantity_carnivor -= 1

                entity.food_eaten = 0


    def getMatrixPosition(self, entity):
        ent_position = entity.getPosition()
        return [floor(ent_position[1] / (configuration.x / 20)), floor(ent_position[0] / (configuration.x / 20))]

                