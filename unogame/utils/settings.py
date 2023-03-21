import pygame, time
import sys
from pygame.locals import *

class Setting:
    
    def __init__(self, keys, font, screen, visible):
        self.items = [
                      ["Window Size", "Key Configuration", "Color Blindness Mode", "Reset Settings"],
                      ["size 1", "size 2", "Fullscreen"],
                      keys,
                      ["Deuteranopia(Red-Green)", "Tritanopia(Blue-Yellow)", "None"],
                      ]
        self.font = font
        self.screen = screen
        self.selected = 0
        self.title_font = pygame.font.SysFont(None, 72)
        self.titles = ["Settings", "Window Size", "Key Configuration", "Color Blindness Mode"]
        self.keys = keys
        self.key_font = pygame.font.SysFont(None, 20)
        self.option = 0 
        self.visible = visible
        
        # Clear the screen
        self.screen.fill((0, 0, 0))


    def draw(self):
        if self.visible: self.screen.fill((0, 0, 0))
        self.title_text = self.title_font.render(self.titles[self.option], True, (255, 255, 255))

        # Draw the title
        self.screen.blit(
            self.title_text,
            (self.screen.get_width() // 10, self.screen.get_height() // 12),
        )

        # Draw the menu items
        for i, item in enumerate(self.items[self.option]):
            gap = 80
            if self.option == 2:
                text = self.font.render(
                f"{item[0]}: {item[1]}",
                True,
                (255, 255, 255) if i != self.selected else (255, 0, 0)
                )
                gap = 50
            else:   
                text = self.font.render(
                    item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
                    )
                
            self.screen.blit(
                text,
                (self.screen.get_width() // 5, self.screen.get_height() // 4 + i * gap)
            )
        
        text = self.font.render("Save", True,
                                (255, 255, 255) if len(self.items[self.option]) != self.selected else (255, 255, 0)
                                )
        self.screen.blit(
            text,
            (self.screen.get_width() // 5, self.screen.get_height() * 10 // 12)
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
                        self.selected = (self.selected - 1) % (len(self.items[self.option])+1)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % (len(self.items[self.option])+1)
                    elif event.key == K_RETURN:
                        if self.option == 0 and self.selected == 3 :
                            self.reset()
                        elif self.option == 0 and self.selected == 4 :
                            self.screen.fill((0, 0, 0))
                            return 0
                        elif self.option == 0:
                            self.option = self.selected+1
                            self.screen.fill((0, 0, 0))
                        elif self.selected == len(self.items[self.option]):
                            self.screen.fill((0, 0, 0))
                            self.option = 0
                        elif self.option == 1:
                            self.screenSize(self.selected+1)
                        

                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    else:
                        self.visible = not self.visible
                        if self.visible:
                            for i, (name, key) in enumerate(self.keys):
                                text = self.key_font.render(
                                    f"{name}: {key}",
                                    True,
                                    (255, 255, 255),
                                )
                                self.screen.blit(
                                    text,
                                    (self.screen.get_width() // 10 * 8,
                                     self.screen.get_height() // 12 + i * 30)
                                    )
                        self.visible = not self.visible


                elif event.type == MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    for i, item in enumerate(self.items[self.option]):
                        gap = 80
                        if self.option == 2: 
                            text = self.font.render(
                                f"{item[0]}: {item[1]}",
                                True,
                                (255, 255, 255) if i != self.selected else (255, 0, 0)
                            )
                            gap = 50
                        else:
                            text = self.font.render(
                            item,
                            True,
                            (255, 255, 255) if i != self.selected else (255, 0, 0),
                            )
                        
                        rect = text.get_rect()
                        rect.topleft = (
                            self.screen.get_width() // 5,
                            self.screen.get_height() // 4 + i * gap
                        )
                        if rect.collidepoint(pos):
                            self.selected = i

                    save = self.font.render("Save", True, (255, 255, 255))
                    rectSave = save.get_rect()
                    rectSave.topleft = (
                        self.screen.get_width() // 5,
                        self.screen.get_height() * 10 // 12
                    )
                    if rectSave.collidepoint(pos):
                        self.selected = len(self.items[self.option])

                elif event.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    gap = 80
                    for i, item in enumerate(self.items[self.option]):
                        if self.option == 2: 
                            text = self.font.render(
                                f"{item[0]}: {item[1]}",
                                True,
                                (255, 255, 255)
                            )
                            gap = 50
                        elif type(item) == type(str):
                            print(type)
                            #text = self.font.render(item,True,(255, 255, 255)) 

                        rect = text.get_rect()
                        rectSave = save.get_rect()
                        rect.topleft = (
                            self.screen.get_width() // 5,
                            self.screen.get_height() // 4 + i * gap
                        )
                        rectSave.topleft = (
                            self.screen.get_width() // 5,
                            self.screen.get_height() * 10 // 12
                        )

                        if rect.collidepoint(pos):
                            if self.option == 0 and self.selected == 3:
                                self.reset()
                            elif self.option == 0:
                                self.option = i+1
                                self.screen.fill((0, 0, 0))
                            elif self.option == 1:
                                self.screenSize(self.selected+1)

                        if rectSave.collidepoint(pos):
                            if self.option == 0 and self.selected == 4:
                                self.screen.fill((0, 0, 0))
                                return 0
                            else:
                                self.screen.fill((0, 0, 0))
                                self.option = 0

            # Draw the menu
            self.draw()

            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)
    
    def screenSize(self, option):
        if option == 1:
            self.screen = pygame.display.set_mode((800, 600))
        elif option == 2:
            self.screen = pygame.display.set_mode((1000, 750))
        elif option ==3:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def reset(self):
        print('reset!')
        pass