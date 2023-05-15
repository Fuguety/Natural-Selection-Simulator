import Entities.EntityHerbivor as Entity
#import Entities.Entity as Entity
import Entities.Food as Food
import pygame
import Configuration as configuration
from math import cos,sin,radians,floor,sqrt

class Simulation:
    
    def __init__(self, entity_quantity_herbivor, food_quantity, arena_radius):
        
        self.global_food = [ [[], [], [], [], []]  , [[], [], [], [], []],   [[], [], [], [], []] , [[], [], [], [], []] ]
        self.arena_radius = arena_radius
        self.entity_list_herbivor = []
        self.food_list = []
        self.food_quantity = food_quantity
        self.entity_quantity_herbivor = entity_quantity_herbivor
        self.food_quantity_present = food_quantity
        self.entity_quantity_alive = entity_quantity_herbivor
        self.show_render = False

        self.startRound(entity_quantity_herbivor,food_quantity)

    def startRound(self, entity_quantity_herbivor, food_quantity, restart = True):
        if restart:
            self.global_food = [ [[], [], [], [], []]  , [[], [], [], [], []],   [[], [], [], [], []] , [[], [], [], [], []] ]
            self.entity_list_herbivor = []
            self.food_list = []
            self.food_quantity = food_quantity
            self.entity_quantity = entity_quantity_herbivor
            self.food_quantity_present = food_quantity
            self.entity_quantity_alive = entity_quantity_herbivor


        for i in range(entity_quantity_herbivor):
            position_x = configuration.x / 2 + cos(radians((360 / entity_quantity_herbivor) * i)) * (self.arena_radius - 2)
            position_y = configuration.y / 2 - sin(radians((360 / entity_quantity_herbivor) * i)) * (self.arena_radius - 2)

            self.entity_list_herbivor.append(Entity.EntityHerbivor(configuration.screen, position_x,position_y, 180 + (360 / entity_quantity_herbivor) * i, 1, 10))

        for c in range(food_quantity):
            self.food_list.append(Food.Food(configuration.screen, self.arena_radius, [configuration.screen.get_size()[0] / 2, configuration.screen.get_size()[1] / 2], "orange"))

        for food_for in self.food_list:
            food_x = food_for.getPosition()[0]
            food_y = food_for.getPosition()[1]
            center_distance = sqrt((food_x - (configuration.x / 2)) ** 2 + (food_y - (configuration.y / 2)) ** 2)
            food_circle = floor( center_distance / 60)


            if food_x > configuration.x / 2:
                if food_y < configuration.y / 2:
                    self.global_food[0][food_circle].append(food_for)
                if food_y > configuration.y / 2:
                    self.global_food[3][food_circle].append(food_for)

            if food_x < configuration.x / 2:
                if food_y < configuration.y / 2:
                    self.global_food[1][food_circle].append(food_for)
                if food_y > configuration.y / 2:
                    self.global_food[2][food_circle].append(food_for)
        
        

        self.drawArena()
        self.drawFoods()
        self.drawEntities()

        pygame.display.flip()

    def drawArena(self):
        pygame.draw.circle(configuration.screen, "white", [configuration.x / 2, configuration.y / 2], self.arena_radius)

    def drawFoods(self):
        for food in self.food_list:
            if not food.devoured:
                food.draw()
            
    def drawEntities(self):
        for entity in self.entity_list_herbivor:
            entity.draw()

    def drawHemispheres(self):
        pygame.draw.line(configuration.screen, "red", [0, configuration.y / 2], [configuration.x, configuration.y / 2])
        pygame.draw.line(configuration.screen, "red", [configuration.x / 2, 0], [configuration.x / 2, configuration.y])

    def drawCircles(self):
        for i in range(5, 0, -1):
            color = 255 - (255 / 6) * i
            radius = (self.arena_radius / 5) * i
            pygame.draw.circle(configuration.screen, [color, color, color], [configuration.x / 2, configuration.y / 2], radius)

    def tick(self, collision = True):
        for entity in self.entity_list_herbivor:
            entity.draw()

            temp = self.getArea(entity)
            quadrant = temp[0]
            area = temp[1]
                
            possible_foods = self.global_food[quadrant][area]
            
            if entity.alive:
                if entity.distanceBetween(configuration.x / 2, configuration.y / 2) < self.arena_radius - 1:
                    entity.move(possible_foods)
                    if collision:
                        self.collision(entity, quadrant, area)                
                else:
                    entity.alive = False
                    self.entity_quantity_alive -= 1

    def collision(self, entity, quadrant, area):
        ent_x = entity.getPosition()[0]
        ent_y = entity.getPosition()[1]
        
        for index, food_for in enumerate(self.global_food[quadrant][area]):
            type = Food.Food.getType
            if entity.food_type == type: #checks if herbivor eats a plant
                if not food_for.devoured:
                    food_x = food_for.position_x
                    food_y = food_for.position_y
                    radius_sum = configuration.entity_radius + configuration.food_radius

                    if entity.distanceBetween(food_x, food_y) <= radius_sum:
                        food_for.devoured = True
                        self.food_quantity_present -= 1
                        entity.food_eaten += 1 # when food is eaten, it adds to invetory
                        del self.global_food[quadrant][area][index]
                    if self.show_render:
                        pygame.draw.line(configuration.screen, "blue", [ent_x, ent_y], [food_x, food_y])

    def drawStatistics(self, position):        
        font = pygame.font.SysFont("Verdana", 20)
        text_entities = font.render(f'entidades vivas: {str(self.entity_quantity_alive)}',True, "white")
        text_food = font.render(f'comidas presentes: {str(self.food_quantity_present)}',True, "white")

        configuration.screen.blit(text_entities, position)
        configuration.screen.blit(text_food, [position[0], position[1] + 25])

    def drawRender(self):
        self.show_render = not self.show_render
    
    # at end of simluation define who reproduces, survive or die    
    def addEntity(self):
        for entityEat in self.entity_list_herbivor:
            if entityEat.food_eaten >= 2: # reproduce
                entityEat.food_eaten = 0 # resets invetory to 0
                self.entity_quantity += 1
            elif entityEat.food_eaten == 1: # survives
                entityEat.food_eaten = 0
            else:                           # dies
                self.entity_quantity -= 1
    
    def getArea(self, entity):
        center_distance = sqrt((entity.position_x - (configuration.x / 2)) ** 2 + (entity.position_y - (configuration.y / 2)) ** 2)
        entity.circle = floor( center_distance / 60)
        quadrant = 0
        area = entity.circle

        if entity.position_x > configuration.x / 2:
            if entity.position_y < configuration.y / 2:
                quadrant = 0
            if entity.position_y > configuration.y / 2:
                quadrant = 3

        if entity.position_x < configuration.x / 2:
            if entity.position_y < configuration.y / 2:
                quadrant = 1
            if entity.position_y > configuration.y / 2:
                quadrant = 2
        
        return [quadrant, area]
                
