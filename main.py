import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

self.run = True
while self.run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.run = False

pygame.quit()