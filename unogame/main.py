import pygame, time
import sys
from pygame.locals import *
from utils import *


# Define the key_list
key_list = {
    "LEFT": pygame.K_UP,
    "RIGHT": pygame.K_RIGHT,
    "UP": pygame.K_UP,
    "DOWN": pygame.K_DOWN,
    "RETURN": pygame.K_RETURN,
    "ESCAPE": pygame.K_ESCAPE    
}


# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 48)

# Create the menu
menu = menu.Menu(key_list, font, screen)
setting = settings.Setting(key_list, font, screen)

# Main loop
while True:
    selected = menu.run()
    # Handle the selected menu item
    if selected == 0:
        # Start single player game
        print("Start Game")  # Replace with your game code
    elif selected == 1:  
        # Open settings menu
        screen.fill((0,0,0))
        selected = setting.run()
    elif selected == 2:
        # Exit the program
        pygame.quit()
        sys.exit()