import pygame, time
import sys
from pygame.locals import *
import utils.settings


class Menu:
    
    def __init__(self, items, keys, font, screen, visible):
        self.items = items
        self.font = font
        self.screen = screen
        self.selected = 0
        self.title_font = pygame.font.SysFont(None, 72)
        self.title_text = self.title_font.render("Uno Game", True, (255, 255, 255))
        self.keys = keys
        self.key_font = pygame.font.SysFont(None, 20)
        self.visible = visible
        
        # Clear the screen
        self.screen.fill((0, 0, 0))


    def draw(self):

        # Draw the title
        self.screen.blit(
            self.title_text,
            (self.screen.get_width() // 2 - self.title_text.get_width() // 2, 100),
        )

        # Draw the menu items
        for i, item in enumerate(self.items):
            text = self.font.render(
                item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
            )
            self.screen.blit(
                text,
                (self.screen.get_width() // 2 - text.get_width() // 2, 300 + i * 50),
            )

    def run(self):
        clock = pygame.time.Clock()
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.items)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.items)
                    elif event.key == K_RETURN:
                        return self.selected
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    else:
                        # print(event)
                        self.visible = not self.visible
                        if self.visible:
                            for i, (name, key) in enumerate(self.keys):
                                text = self.key_font.render(
                                    f"{name}: {key}",
                                    True,
                                    (255, 255, 255),
                                )
                                self.screen.blit(text, (50, 50 + i * 30))
                        self.visible = not self.visible


                elif event.type == MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    for i, item in enumerate(self.items):
                        text = self.font.render(
                            item,
                            True,
                            (255, 255, 255) if i != self.selected else (255, 0, 0),
                        )
                        rect = text.get_rect()
                        rect.topleft = (
                            self.screen.get_width() // 2 - text.get_width() // 2,
                            300 + i * 50,
                        )
                        if rect.collidepoint(pos):
                            self.selected = i

                elif event.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for i, item in enumerate(self.items):
                        text = self.font.render(item, True, (255, 255, 255))
                        rect = text.get_rect()
                        rect.topleft = (
                            self.screen.get_width() // 2 - text.get_width() // 2,
                            300 + i * 50,
                        )
                        if rect.collidepoint(pos):
                            # print(self.items[i])
                            return i

            # Draw the menu
            self.draw()

            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)


# Define the menu items
menu_items = ["Single Player Game", "Settings", "Exit"]

# Define the key_list
key_list = [
    ("LEFT", "Left"),
    ("RIGHT", "Right"),
    ("UP", "Up"),
    ("DOWN", "Down"),
    ("RETURN", "Enter"),
    ("ESCAPE", "Esc"),
]

# Define the opacity percentage and visibiliy flag
opacity = 120  # 0-255 && have to add to code for setting opacity
visible = False
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 48)

# Create the menu
menu = Menu(menu_items, key_list, font, screen, visible)


# Run the menu
selected = menu.run()

setting = utils.settings.Setting(key_list, font, screen, visible)

# Handle the selected menu item
if selected == 0:
    # Start single player game
    pass  # Replace with your game code
elif selected == 1:
    selected = setting.run()
    # Open settings menu
elif selected == 2:
    # Exit the program
    pygame.quit()
    sys.exit()