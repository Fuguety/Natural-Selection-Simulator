import Helpers.PyGameHelper as PyGameHelper
import Helpers.Persistency as Persitancy
import Entities.Simulation as Simulation
import Entities.fps as fps
import Configuration as configuration
import pygame
import time
from datetime import datetime



simulation = Simulation.Simulation(10, 10 , 300)

running = True

frame_second = fps.fps([20,20])

fps_limit = 60

show_render_division = True

start_time = time.time()

timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M") # Gets current dat and time to create the file for the simulation
file_path = Persitancy.CreateJson(timestamp) # Creates Json for current simulation

simulation_time = 0
time_limit = 60


while running:
    #PyGameHelper.pause(configuration.screen)
    
    current_time = time.time()
    elapsed_time = current_time - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PyGameHelper.pause(configuration.screen)         

            if event.key == pygame.K_ESCAPE:
                running = False             # ends simulation

            if event.key == pygame.K_RIGHT:
                fps_limit = fps_limit * 1.5 # makes simulation faster

            if event.key == pygame.K_LEFT:
                fps_limit = fps_limit / 1.5 # makes simulation slower

            if event.key == pygame.K_UP:
                simulation.drawRender() # turns on line

            if event.key == pygame.K_DOWN:
                show_render_division = not show_render_division # turns on dev view

            if event.key == pygame.K_r:
                '''print("***************")
                print("START ROUND")
                print("***************")'''
                simulation.startRound(0, 1,300) # restart simulation
    
    configuration.screen.fill("WHITE")

    simulation.drawFoods()

    simulation.tick()

    if show_render_division: simulation.drawHemispheres()

    simulation.drawStatistics([20,45])

    frame_second.draw()

    pygame.display.flip()

    configuration.clock.tick(fps_limit) # Fps limiter

    # every X amount of time, the food grows again
    if elapsed_time >= time_limit:
        simulation_time += time_limit
        Persitancy.Persistency(simulation.entity_quantity_herbivor_alive, simulation.entity_quantity_carnivor_alive, simulation.food_quantity_present, simulation_time, file_path)
        simulation.growFood()
        start_time = time.time()

    
    if simulation.entity_quantity == 0:
        print("Population died, no one is left")
        running = False
    
    # when simulation ends, starts a new one with more or less entities
    elif (simulation.entity_quantity_alive == 0) or (simulation.food_quantity_present == 0):
        simulation.addEntity()
        entity_quantity_herbivor = simulation.entity_quantity_herbivor_alive
        entity_quantity_carnivor = simulation.entity_quantity_carnivor_alive
        food_quantity = simulation.food_quantity

        simulation.startRound(entity_quantity_herbivor, entity_quantity_carnivor, food_quantity) 
        
pygame.quit()

# Implementar persistencia no codigo (a cada "tempo", executa a funçao da persistencia)
# Persistency.Persistency(self.entity_quantity_herbivor, self.entity_quantity_carnivor, self.food_quantity, 5)
#
# to do:
# tudo dentro de um round
# reproduzir ao longo do tempo (filho herda atributos do pai, podendo mutar)
# comida crescer ao longo do tempo
# entidade mudar de direçao quando bater na parede
# implementar persistencia
'''


if tempo%60 == 0:
    comida.spawn()

if tempo%60 == 0:
    if EntityCarnivor.food_eaten > 1:
        entity_quantity_carnivor += 1
    
    if random_number > 9:
        EntityCarnivor.EntityCarnivor(position_x, 10, 270, 2, 0.5)

'''