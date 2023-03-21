import pygame, time
import sys
from pygame.locals import *
from utils import *



# Define the key_list
key_list = [
    ("LEFT", "Left"),
    ("RIGHT", "Right"),
    ("UP", "Up"),
    ("DOWN", "Down"),
    ("RETURN", "Enter"),
    ("ESCAPE", "Esc"),
]


visible = False
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 48)

# Create the menu, setting
menu = menu.Menu(key_list, font, screen)


while True:
    selected = menu.run()
    # Handle the selected menu item
    if selected == 0:
      # Start single player game
     pass  # Replace with your game code
    elif selected == 1:  
        # Open settings menu
        pass
    elif selected == 2:
        # Exit the program
        pygame.quit()
        sys.exit()