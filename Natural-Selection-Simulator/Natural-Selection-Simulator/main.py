import Helpers.PyGameHelper as PyGameHelper
import Entities.Simulation as Simulation
import Entities.fps as fps
import Configuration as configuration
import pygame

simulation = Simulation.Simulation(10, 99, 300)

running = True

frame_second = fps.fps([20,20])

fps_limit = 60

show_render_division = True

while running:
    #PyGameHelper.pause(configuration.screen)

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
                simulation.startRound(10,30) # restart simulation
    
    configuration.screen.fill("black")

    simulation.drawArena()    
    
    if show_render_division: simulation.drawCircles()

    simulation.drawFoods()

    simulation.tick()

    if show_render_division: simulation.drawHemispheres()

    simulation.drawStatistics([20,45])

    frame_second.draw()

    pygame.display.flip()

    configuration.clock.tick(fps_limit) # Limitador de fps
    
    
    if simulation.entity_quantity == 0:
        print("Population died, no one is left")
        running = False
    
    # when simulation ends, starts a new one with more or less entities
    elif (simulation.entity_quantity_alive == 0) or (simulation.food_quantity_present == 0):
        simulation.addEntity()
        entity_quantity = simulation.entity_quantity
        food_quantity = simulation.food_quantity
        simulation.startRound(entity_quantity, food_quantity) 
        
pygame.quit()