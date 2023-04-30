import pygame
from pygame.locals import *
import sys
import socket, requests, re
from multi_play import Game

class multiPlayMenu:
    def __init__(self, keys, font, screen, config, soundFX):
        self.items = ["Create a Game", "Enter the Game", "Go Back"]
        self.items2 = ["Enter", "Go Back"]
        self.font = font
        self.screen = screen
        self.selected = 0
        self.keys = keys
        self.key_font = pygame.font.SysFont(None, 76)
        self.visible = [False, 255]
        req = requests.get("http://ipconfig.kr")
        self.hostIP = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]
        self.config = config
        self.soundFX = soundFX
        self.option = 0                     # option = 0이면 선택창, option = 1이면 client menu
        self.text = ''
        self.cursorAct = False
        self.currentCursor = pygame.mouse.get_cursor()
        

        # Clear the screen
        self.screen.fill((0, 0, 0))

    def draw(self):
        self.screen.fill((0, 0, 0))
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()
        if self.option == 0:
            CurrentIPAddress = "Current IP Address: "
            hostText = self.font.render(CurrentIPAddress + self.hostIP, True, (255, 255, 255))
            self.screen.blit(hostText, (screenW // 2 - hostText.get_width() // 2, screenH * 0.02))

            # Draw the menu items
            for i, item in enumerate(self.items):
                text = self.key_font.render(
                    item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
                )
                self.screen.blit(
                    text, (screenW // 2 - text.get_width() // 2, screenH // 3.5 + i * screenH // 6)
                )
        elif self.option == 1:
            input_box = pygame.Rect(0, 0, self.screen.get_width() // 1.5, self.screen.get_height() // 10)
            input_box.center = (self.screen.get_width() // 2, self.screen.get_height() // 3)
            optionFont = pygame.font.SysFont(None, screenW // 10)
            pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)
            text_surface = optionFont.render(self.text, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

            # Draw the menu items
            for i, item in enumerate(self.items2):
                text = self.key_font.render(
                    item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
                )
                self.screen.blit(
                    text, (screenW // 3 * (i + 1) - text.get_width() // 2, screenH * 0.75)
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
                elif event.type == KEYDOWN and self.option == 0:
                    if event.key == self.keys["UP"]:
                        self.selected = (self.selected - 1) % len(self.items)
                    elif event.key == self.keys["DOWN"]:
                        self.selected = (self.selected + 1) % len(self.items)
                    elif event.key == self.keys["RETURN"]:
                        if self.selected == 0:
                            self.option = 0
                            game = Game(self.screen, 1, self.keys, self.config, self.soundFX)
                            game.start_multi_play()
                        elif self.selected == 1:
                            self.option = 1
                        elif self.selected == 2:
                            self.option = 0
                            return self.selected
                    elif event.key == self.keys["ESCAPE"]:
                        pygame.quit()
                        sys.exit()


                elif event.type == KEYDOWN and self.option == 1:
                    if event.key == self.keys["LEFT"]:
                        self.selected = (self.selected - 1) % len(self.items2)
                    elif event.key == self.keys["RIGHT"]:
                        self.selected = (self.selected + 1) % len(self.items2)
                    elif event.key == self.keys["RETURN"]:
                        if self.selected == 0:
                            print(self.text)                                    # Todo: self.text(입력한 주소)의 방으로 연결시켜야함
                            self.text = ''                                      # Todo: 비밀번호가 있으면 입력
                        elif self.selected == 1:
                            self.option = 0
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == self.keys["ESCAPE"]:
                        pygame.quit()
                        sys.exit()
                    else:
                        if event.unicode.isnumeric() or event.unicode == '.':
                            self.text += event.unicode


                elif (event.type == MOUSEMOTION or MOUSEBUTTONUP) and self.option == 0:
                    pos = pygame.mouse.get_pos()
                    for i, item in enumerate(self.items):
                        text = self.font.render(item, True, (255, 255, 255))
                        rect = text.get_rect()
                        rect.topleft = (
                            screenW // 2 - text.get_width() // 2, screenH // 3.5 + i * screenH // 6
                        )
                        if rect.collidepoint(pos):
                            if event.type == MOUSEMOTION:
                                self.selected = i
                            elif event.type == MOUSEBUTTONUP:
                                if i == 0:
                                    self.option = 0
                                    game = Game(self.screen, 1, self.keys, self.config, self.soundFX)
                                    game.start_multi_play()
                                elif i == 1:
                                    self.option = 1
                                elif i == 2:
                                    self.option = 0
                                    return i
                                
                elif (event.type == MOUSEMOTION or MOUSEBUTTONUP) and self.option == 1:
                    input_box = pygame.Rect(0, 0, self.screen.get_width() // 1.5, self.screen.get_height() // 10)
                    input_box.center = (self.screen.get_width() // 2, self.screen.get_height() // 3)
                    pos = pygame.mouse.get_pos()
                    if input_box.collidepoint(pos):
                        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                    else:
                        pygame.mouse.set_cursor(*self.currentCursor)

                    for i, item in enumerate(self.items2):
                        text = self.font.render(item, True, (255, 255, 255))
                        rect = text.get_rect()
                        rect.topleft = (
                            screenW // 3 * (i + 1) - text.get_width() // 2, screenH * 0.75
                        )
                        if rect.collidepoint(pos):
                            if event.type == MOUSEMOTION:
                                self.selected = i
                            elif event.type == MOUSEBUTTONUP:
                                if i == 0:
                                    print(self.text)                            # Todo: self.text(입력한 주소)의 방으로 연결시켜야함
                                    self.text = ''
                                elif i == 1:
                                    self.option = 0

            # Draw the menu
            self.draw()

            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)
