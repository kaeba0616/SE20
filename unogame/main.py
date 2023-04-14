import pygame, configparser
import sys
from pygame.locals import *
from utils import *

# from single_play import start_single_play
from single_play import Game


config = configparser.ConfigParser()
config.read("setting_data.ini")


# Define the key_list
key_list = {
    "LEFT": int(config["key"]["left"]),
    "RIGHT": int(config["key"]["right"]),
    "UP": int(config["key"]["up"]),
    "DOWN": int(config["key"]["down"]),
    "RETURN": int(config["key"]["return"]),
    "ESCAPE": int(config["key"]["escape"]),
}


# Initialize pygame
pygame.init()

if config["window"]["default"] == "1":
    screen = pygame.display.set_mode((800, 600))
elif config["window"]["default"] == "2":
    screen = pygame.display.set_mode((1000, 750))
elif config["window"]["default"] == "3":
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


font = pygame.font.SysFont(None, 48)

# Create the menu
menu = menu.Menu(key_list, font, screen)
setting = settings.Setting(key_list, font, screen, config)
storyMode = storyMode.StoryMode(screen, font, config, key_list)

# Main loop
while True:
    selected = menu.run()
    # Handle the selected menu item
    if selected == 0:
        # Start single player game
        print("Start Game")  # Replace with your game code
        # start_single_play()
        game = Game(screen, 2)
        selected = game.start_single_play()
    elif selected == 1:
        screen.fill((0, 0, 0))
        selected = storyMode.run()

    elif selected == 2:
        # Open settings menu
        screen.fill((0, 0, 0))
        selected = setting.run()
    elif selected == 3:
        # Exit the program
        pygame.quit()
        sys.exit()
