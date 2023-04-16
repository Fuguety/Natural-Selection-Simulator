import entidade
import pygameHelpers
import food

import pygame
from math import sin,cos,tan,radians, pi, sqrt


# pygame setup
pygame.init()
x = 1280
y = 720
screen = pygame.display.set_mode((x, y))
clock = pygame.time.Clock()
running = True


# Criando Variaveis de entidades
listEnt = []

qntEnties = 10
for i in range(qntEnties):
    posX = x / 2 + cos(radians((360 / qntEnties) * i)) * 299
    posY = y / 2 - sin(radians((360 / qntEnties) * i)) * 299

    listEnt.append(entidade.entidade(screen,posX,posY, 180 + (360 / qntEnties) * i))


# Criando variaveis de comida
listFood = []

qntFood = 60
for c in range(qntFood):
    listFood.append(food.Food(screen, 300, [x/2, y/2]))


# Ciclo do jogo
while running:
    # Checa a stack de eventos
    # pygame.QUIT é o evento de clicar no X


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Configurando pause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygameHelpers.pause(screen)         

    # apaga o ultimo frame enxendo a tela de preto
    screen.fill("black")

    # Draws arena
    pygame.draw.circle(screen,"white", [x / 2, y / 2], 300)
    

    # Draws food
    for com in listFood:
        com.draw()

    # Draws enties
    for num, ent in enumerate(listEnt):
        ent.draw()
        if ent.calculaDistancia(x / 2, y / 2) < 300:
            ent.randomMove()
            
    # Checks food coordinates    
    for currentFood in listFood:
        currentFood = food.Food.getPosition(currentFood)
        
        for currentEntity in listEnt:   # if entity touches food, the collision happens
            entity = entidade.entidade.getCurrentPosition(currentEntity)
            
            distance = sqrt((entity[0] - currentFood[0])**2 + (entity[1] - currentFood[1])**2)   # sqrt((x1 - x2)^2 + (y1 - y2)^2)
            sumRadius = entity[2] + currentFood[2]
            
            if distance <= sumRadius:
                print("collion happened")
            

    
    
    # Trocando o buffer para aparecer oque foi desenhado
    pygame.display.flip()

    clock.tick(60)  # Limite de FPS

pygame.quit()