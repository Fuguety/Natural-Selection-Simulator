import pygame

pygame.init()
x = 1280
y = 720
screen = pygame.display.set_mode((x, y))
clock = pygame.time.Clock()
food_radius = 5
entity_radius = 10
quantity_circles = 5