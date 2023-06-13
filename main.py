import Helpers.PyGameHelper as PyGameHelper
import Helpers.Persistency as Persitency
import Entities.Simulation as Simulation
import Entities.fps as fps
import Configuration as configuration
import pygame
import numpy as np
from datetime import datetime

show_simulation = bool(int(input("Deseja Mostrar a simulaçao? [1 | 0] ")))

if not show_simulation:
    
    if int(input("deseja fazer uma simulação repetida? [1 | 0] ")):
        continue_simulation = True
        qnt_simulation_min = int(input("Quantos rounds é o minimo para ser salvo? [int] "))

        simulation_count = 1
        round_count = 0
        round_cap = -2
        simulation_cap = 2
        tryes = 0
        ration_total = 0

    else:    
        temp_imp = input("Quanto rounds deseja simular? enter = 20  ")
        simulation_limite_temp = input("Quantas vezes deseja rodar a simulaçao? enter = 5 ")

        round_cap = int(temp_imp) if temp_imp != "" else 20
        simulation_cap = int(simulation_limite_temp) if simulation_limite_temp != "" else 5
        round_count = 0
        simulation_count = 1
        continue_simulation = False


else:
    round_cap = 4
    simulation_cap = 4
    round_count = 0
    simulation_count = 0
    continue_simulation = False

if continue_simulation:
    qnt_Herb = np.random.randint(10,101)
    qnt_Carniv = np.random.randint(5,51)
    qnt_Food = int(np.random.randint(2,30) * qnt_Herb / 2)

else:
    qnt_Herb = 20
    qnt_Carniv = 5
    qnt_Food = 200

simulation = Simulation.Simulation(qnt_Herb, qnt_Carniv , qnt_Food, show_simulation)



running = True

show_render_division = False

if show_simulation:
    frame_second = fps.fps([20,20])

fps_limit = 60
z = 0

timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M") # Gets current dat and time to create the file for the simulation

if continue_simulation:
    file_path = Persitency.CreateJson(f' Succes {simulation_count}') # Creates Json for current simulation

else:
    file_path = Persitency.CreateJson(f'{timestamp}.0') # Creates Json for current simulation

simulation_time = 0
time_limit = 60

background_render = pygame.image.load("image.jpeg")


while running:
    #PyGameHelper.pause(configuration.screen) 
    
    if show_simulation:
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
                    simulation.startRound(0, 1,300) # restart simulation
        
                if event.key == pygame.K_c:
                    simulation.createHerb([configuration.x / 2, configuration.y / 2]) 
        
        configuration.screen.fill("BLACK")
        configuration.screen.blit(background_render, (0, 0))


    #time.sleep(5)
    #simulation.reproduceHerbivorOrDie() # inicia a primeira chamada linha
    

    simulation.tick()

    if show_render_division: simulation.drawHemispheres()

    if show_simulation: 
        simulation.drawStatistics([20,45])

        frame_second.draw()

        pygame.display.flip()

    
    
    # every X amount of time, the food grows again
    if z == 600 or z == 1200:
        if not show_simulation: 
            round_count += 1 
        
        simulation_time += 10
        ratio = (simulation.entity_quantity_herbivor / simulation.entity_quantity_carnivor) if simulation.entity_quantity_carnivor != 0 else simulation.entity_quantity_herbivor 
        Persitency.Persistency(ratio ,simulation.entity_quantity_herbivor, simulation.entity_quantity_carnivor, simulation.food_quantity_present, simulation_time, file_path)
        simulation.growFood()
        simulation.reproduceHerbivorOrDie()
        
        if continue_simulation: ration_total += ratio

        # Somente se nao mostrar a simulaçao
        if round_count == round_cap or simulation.entity_quantity_herbivor == 0 or simulation.entity_quantity_carnivor == 0:

            ##########   Se  for para fazer continuo   ###########
            if continue_simulation:
                if round_count >= qnt_simulation_min:
                    
                    Persitency.Persistency.add_initial_information(ration_total / round_count,qnt_Herb, qnt_Carniv, qnt_Food, file_path)

                    simulation_count += 1
                    file_path = Persitency.CreateJson(f' Succes {simulation_count}') # Creates Json for next simulation
                    round_count = 0
                    simulation_time = 0
                    ration_total = 0

                    #   Restarting the simulation
                    qnt_Herb = np.random.randint(10,101)
                    qnt_Carniv = np.random.randint(5,51)
                    qnt_Food = np.random.randint(2,30) * qnt_Herb
                    simulation.startRound(qnt_Herb, qnt_Carniv, qnt_Food, True)

                elif tryes < 3:
                    tryes += 1
                    file_path = Persitency.CreateJson(f' Succes {simulation_count}') # Creates Json for next simulation overwritting current
                    round_count = 0
                    simulation_time = 0
                    ration_total = 0 

                    simulation.startRound(qnt_Herb, qnt_Carniv, qnt_Food, True)

                else:
                    file_path = Persitency.CreateJson(f' Succes {simulation_count}') # Creates Json for next simulation overwritting current

                    simulation_time = 0
                    round_count = 0
                    tryes = 0
                    ration_total = 0

                    qnt_Herb = np.random.randint(10,101)
                    qnt_Carniv = np.random.randint(5,51)
                    qnt_Food = np.random.randint(2,30) * qnt_Herb
                    simulation.startRound(qnt_Herb, qnt_Carniv, qnt_Food, True)



            ##########  Se nao for para fazer continuo ###########
            else:
                if simulation_count == simulation_cap:
                    break
                
                else:
                    round_count = 0
                    simulation_time = 0

                    simulation_count+= 1
                    simulation.startRound(qnt_Herb, qnt_Carniv, qnt_Food, True)
                    timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M") # Gets current dat and time to create the file for the simulation
                    file_path = Persitency.CreateJson(f'{timestamp}.{simulation_count}') # Creates Json for current simulation
                    
                    z = -1



    if z == 1200:
        simulation.reproduceCarnivore()
        z = 0
    
    # if z == 500:
    #     simulation.temp()
    #     print("********************************************")
    #     PyGameHelper.pause(configuration.screen)         
    #     z = 0

    z += 1

    if show_simulation: configuration.clock.tick(fps_limit) # Fps limiter

pygame.quit()