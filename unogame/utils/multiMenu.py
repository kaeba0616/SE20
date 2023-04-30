import pygame
from pygame.locals import *
import sys
import socket

class multiPlayMenu:
    def __init__(self, keys, font, screen):
        self.items = ["Create a Game", "Enter the Game", "Go Back"]
        self.font = font
        self.screen = screen
        self.selected = 0
        self.keys = keys
        self.key_font = pygame.font.SysFont(None, 76)
        self.visible = [False, 255]
        self.hostIP = socket.gethostbyname(socket.gethostname())

        # Clear the screen
        self.screen.fill((0, 0, 0))

    def draw(self):
        self.screen.fill((0, 0, 0))
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()
        CurrentIPAddress = "Current IP Address: "
        hostText = self.font.render(CurrentIPAddress + self.hostIP, True, (255, 255, 255))
        self.screen.blit(hostText, (screenW // 2 - hostText.get_width() // 2, screenH * 0.02))

        # Draw the menu items
        for i, item in enumerate(self.items):
            text = self.key_font.render(
                item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
            )
            self.screen.blit(
                text, (screenW // 2 - text.get_width() // 2, screenH // 4 + i * screenH // 4)
            )
        

    def run(self):
        clock = pygame.time.Clock()
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == self.keys["UP"]:
                        self.selected = (self.selected - 1) % len(self.items)
                    elif event.key == self.keys["DOWN"]:
                        self.selected = (self.selected + 1) % len(self.items)
                    elif event.key == self.keys["RETURN"]:
                        if self.selected == 0:
                            pass
                        elif self.selected == 1:
                            pass
                        elif self.selected == 2:
                            return self.selected
                    elif event.key == self.keys["ESCAPE"]:
                        pygame.quit()
                        sys.exit()
                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for i, item in enumerate(self.items):
                        text = self.font.render(item, True, (255, 255, 255))
                        rect = text.get_rect()
                        rect.topleft = (
                            screenW // 2 - text.get_width() // 2, screenH // 4 + i * screenH // 4
                        )
                        if rect.collidepoint(pos):
                            if event.type == MOUSEMOTION:
                                self.selected = i
                            elif event.type == MOUSEBUTTONUP:
                                if i == 0:
                                    pass
                                elif i == 1:
                                    pass
                                elif i == 2:
                                    return i

            # Draw the menu
            self.draw()

            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)
