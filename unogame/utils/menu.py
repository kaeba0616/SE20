import pygame
from pygame.locals import *
import sys

class Menu:
    
    def __init__(self, keys, font, screen):
        self.items = ["Single Player Game", "Settings", "Exit"]
        self.font = font
        self.screen = screen
        self.selected = 0
        self.title_font = pygame.font.SysFont(None, 72)
        self.title_text = self.title_font.render("Uno Game", True, (255, 255, 255))
        self.keys = keys
        self.key_font = pygame.font.SysFont(None, 20)
        self.visible = [False, 255]
        
        # Clear the screen
        self.screen.fill((0, 0, 0))


    def draw(self):
        if self.visible[0]: self.screen.fill((0, 0, 0))
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()

        # Draw the title
        self.screen.blit(
            self.title_text,
            (
            screenW // 2 - self.title_text.get_width() // 2,
             #100
            screenH // 6
            )
        )

        # Draw the menu items
        for i, item in enumerate(self.items):
            text = self.font.render(
                item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
            )
            self.screen.blit(
                text,
                (
                screenW // 2 - text.get_width() // 2,
                screenH // 2 + i * 50
                )
            )
        
        #Show Keys Event
        if self.visible[0]: 
            for i, (name, key) in enumerate(self.keys):
                text = self.key_font.render(
                        f"{name}: {key}",
                        True,
                        (255, 255, 255)
                    )
                text.set_alpha(self.visible[1])
                self.screen.blit(text, (
                    screenW // 16 * 8,
                    screenH // 12 + i * 30
                    ))
            
            if self.visible[1] < 10:
                self.visible[0] = False
                self.visible[1] = 0
            else: self.visible[1] -= 2

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
                        self.visible = [True, 255]


                elif event.type == MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    for i, item in enumerate(self.items):
                        text = self.font.render(
                            item,
                            True,
                            (255, 255, 255)
                        )
                        rect = text.get_rect()
                        rect.topleft = (
                            screenW // 2 - text.get_width() // 2,
                            screenH // 2 + i * 50
                        )
                        if rect.collidepoint(pos):
                            self.selected = i

                elif event.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for i, item in enumerate(self.items):
                        text = self.font.render(item, True, (255, 255, 255))
                        rect = text.get_rect()
                        rect.topleft = (
                            screenW // 2 - text.get_width() // 2,
                            screenH // 2 + i * 50,
                        )
                        if rect.collidepoint(pos):
                            return i

            # Draw the menu
            self.draw()

            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)