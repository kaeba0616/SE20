import pygame, configparser
import sys
from pygame.locals import *
from utils import *

config = configparser.ConfigParser()
config.read('./unogame/setting_data.ini')

# Define the key_list
key_list = {
    "LEFT": int(config['key']['left']),
    "RIGHT": int(config['key']['right']),
    "UP": int(config['key']['up']),
    "DOWN": int(config['key']['down']),
    "RETURN": int(config['key']['return']),
    "ESCAPE": int(config['key']['escape'])    
}



# Initialize pygame
pygame.init()

if config['window']['default'] == '1':
    screen = pygame.display.set_mode((800, 600))
elif config['window']['default'] == '2':
    screen = pygame.display.set_mode((1000, 750))
elif config['window']['default'] == '3':
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


font = pygame.font.SysFont(None, 48)

# Create the menu
menu = menu.Menu(key_list, font, screen)
setting = settings.Setting(key_list, font, screen,config)

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