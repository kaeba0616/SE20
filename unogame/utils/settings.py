import pygame, configparser
import sys
from pygame.locals import *


class Setting:
    def __init__(self, keys, font, screen, config):
        self.items = [
            [
                "Window Size",
                "Key Configuration",
                "Color Blindness Mode",
                "Reset Settings",
            ],
            ["800 x 600", "size 2", "Fullscreen"],
            list(keys.items()),
            # lms
            # ["Deuteranopia(Red-Green)", "Tritanopia(Blue-Yellow)", "None"],
            ["On", "Off"],
        ]
        self.font = font
        self.screen = screen
        self.selected = 0
        self.title_font = pygame.font.SysFont(None, 72)
        self.titles = [
            "Settings",
            "Window Size",
            "Key Configuration",
            "Color Blindness Mode",
        ]
        self.keys = keys
        self.key_font = pygame.font.SysFont(None, 20)
        self.option = 0
        self.visible = [False, 255]

        # load data
        self.config = config

        # Clear the screen
        self.screen.fill((0, 0, 0))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.title_text = self.title_font.render(
            self.titles[self.option], True, (255, 255, 255)
        )
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()

        # Draw the title
        self.screen.blit(
            self.title_text,
            (screenW // 10, screenH // 12),
        )

        # Draw the menu items
        gap = 80
        for i, item in enumerate(self.items[self.option]):
            if self.option == 2:
                text = self.font.render(
                    f"{item[0]}: {pygame.key.name(item[1]).capitalize()}",
                    True,
                    (255, 255, 255) if i != self.selected else (255, 0, 0),
                )
                gap = 50
            else:
                text = self.font.render(
                    item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
                )

            self.screen.blit(text, (screenW // 5, screenH // 4 + i * gap))

        # Draw "Save"
        text = self.font.render(
            "Save",
            True,
            (255, 255, 255)
            if len(self.items[self.option]) != self.selected
            else (255, 255, 0),
        )
        self.screen.blit(text, (screenW // 5, screenH * 10 // 12))

        # Show Keys Event
        if self.visible[0] and self.option != 2:
            for i, (name, key) in enumerate(self.keys.items()):
                text = self.key_font.render(
                    f"{name}: {pygame.key.name(key).capitalize()}",
                    True,
                    (255, 255, 255),
                )
                text.set_alpha(self.visible[1])
                self.screen.blit(text, (screenW // 10 * 8, screenH // 12 + i * 30))

            if self.visible[1] < 10:
                self.visible[0] = False
                self.visible[1] = 0
            else:
                self.visible[1] -= 2

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
                        self.selected = (self.selected - 1) % (
                            len(self.items[self.option]) + 1
                        )
                    elif event.key == self.keys["DOWN"]:
                        self.selected = (self.selected + 1) % (
                            len(self.items[self.option]) + 1
                        )
                    elif event.key == self.keys["RETURN"]:
                        if (
                            self.option == 0 and self.selected == 3
                        ):  # setting 화면의 reset 버튼
                            self.reset()
                            screenW = self.screen.get_width()  # 화면 크기 다시 계산
                            screenH = self.screen.get_height()
                        elif self.option == 0 and self.selected == len(self.items[self.option]) : # setting 화면의 save 버튼
                            with open('setting_data.ini', 'w') as f:
                                    self.config.write(f)
                            return 0
                        elif self.option == 0:  # setting 화면에 save 제외 버튼 누를 경우
                            self.option = self.selected + 1
                            self.screen.fill((0, 0, 0))
                        elif self.selected == len(
                            self.items[self.option]
                        ):  # 다른 화면의 save 버튼
                            print(self.selected)
                            print(self.option)
                            print(self.items[self.option])
                            self.screen.fill((0, 0, 0))
                            self.option = 0
                        elif self.option == 1:  # 화면 바꾸기 세팅
                            self.screenSize(self.selected + 1)
                            screenW = self.screen.get_width()  # 화면 크기 다시 계산
                            screenH = self.screen.get_height()
                        elif self.option == 2:  # 키 설정 세팅
                            print(self.selected)
                            self.configKeys(
                                self.selected
                            )  # selected는 left 0 right 1 up 2 ...
                            self.screen.fill((0, 0, 0))
                    elif event.key == self.keys["ESCAPE"]:
                        pygame.quit()
                        sys.exit()
                    else:
                        self.visible = [True, 255]

                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    gap = 80
                    for i, item in enumerate(self.items[self.option]):
                        if self.option == 2 and type(item[1]) == int:
                            text = self.font.render(
                                f"{item[0]}: {pygame.key.name(item[1]).capitalize()}",
                                True,
                                (255, 255, 255),
                            )
                            gap = 50
                        elif type(item) == str:
                            text = self.font.render(item, True, (255, 255, 255))

                        rect = text.get_rect()
                        rect.topleft = (screenW // 5, screenH // 4 + i * gap)
                        if rect.collidepoint(pos):
                            if event.type == MOUSEMOTION:
                                self.selected = i
                            elif event.type == MOUSEBUTTONUP:
                                if (
                                    self.option == 0 and self.selected == 3
                                ):  # setting 화면의 reset 버튼
                                    self.reset()
                                    screenW = self.screen.get_width()  # 화면 크기 다시 계산
                                    screenH = self.screen.get_height()
                                elif self.option == 0:  # setting 화면의 다른 버튼
                                    self.option = i + 1
                                    self.screen.fill((0, 0, 0))
                                elif self.option == 1:  # 화면 바꾸기 세팅
                                    self.screenSize(self.selected + 1)
                                    screenW = self.screen.get_width()  # 화면 크기 다시 계산
                                    screenH = self.screen.get_height()
                                elif self.option == 2:  # 키 설정 변경
                                    self.configKeys(self.selected)
                                    self.screen.fill((0, 0, 0))

                    save = self.font.render("Save", True, (255, 255, 255))
                    rectSave = save.get_rect()
                    rectSave.topleft = (
                        screenW // 5,
                        screenH * 10 // 12
                    )
                    if rectSave.collidepoint(pos): # Save 버튼
                        if event.type == MOUSEMOTION: self.selected = len(self.items[self.option])
                        elif event.type == MOUSEBUTTONUP: 
                            if self.option == 0 and self.selected == len(self.items[self.option]): # 메인 화면의 Save 버튼을 눌렀을 때
                                with open('setting_data.ini', 'w') as f: # ini 파일에 저장

                                    self.config.write(f)
                                self.screen.fill((0, 0, 0))
                                return 0
                            else:  # 다른 setting 화면의 Save 버튼을 눌렀을 때
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
        elif option == 3:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.config["window"]["default"] = str(option)

    def configKeys(self, option):
        selKey = self.items[2][option]  # Tuple of selected key

        text = self.font.render(
            f"{selKey[0]}: {pygame.key.name(selKey[1]).capitalize()}",
            True,
            (255, 255, 0),
        )
        self.screen.blit(
            text,
            (self.screen.get_width() // 5, self.screen.get_height() // 4 + option * 50),
        )
        pygame.display.update()

        getKey = True
        while getKey:  # 무조건 key down 해서 설정키 바꾸게 함
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    for i, (name, key) in enumerate(self.keys.items()):  # 키 중복 방지
                        if key == event.key and i != option:
                            return
                    self.keys[selKey[0]] = event.key
                    self.items[2][option] = (selKey[0], event.key)
                    self.config["key"][selKey[0].lower()] = str(event.key)

                    getKey = False

    def reset(self):
        # Screen size reset
        self.screen = pygame.display.set_mode((800, 600))
        self.config["window"]["default"] = "1"

        # Game key reset
        for i, (name, key) in enumerate(self.keys.items()):
            self.keys[name] = pygame.key.key_code(name.lower())
            self.config["key"][name.lower()] = str(pygame.key.key_code(name.lower()))
        self.items[2] = list(self.keys.items())

        # Color mode reset

        #Volume reset
        sound.resetMusicVol()
        self.sounds.resetSoundVol()
        self.config['sound']['music'] = "6"
        self.config['sound']['sound'] = "2"

