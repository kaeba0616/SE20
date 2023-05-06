import pygame
from pygame.locals import *
import sys

class achieveMenu:
    def __init__(self, keys, font, screen, config, soundFX):
        self.items = ["Single Win", "Stage A Clear", "Stage B Clear", "Stage C Clear", "Stage D Clear",
                      "All Story Clear", "In 10 Truns Win", "Only NumberCard Win", "Only SkillCard Win", "Other Player UNO Win",
                      "Grab Over 15 Cards", "Lucky Three"]          # 12개
        self.font = font
        self.descriptionFont = pygame.font.SysFont(None, 20)
        self.screen = screen
        self.keys = keys
        self.key_font = pygame.font.SysFont(None, 76)
        self.visible = [False, 255]
        self.config = config
        self.soundFX = soundFX
        self.currentXY = [2, 0]
        self.num = 0
        self.current = 0
        self.achieve_clear = [bool(int(self.config['Achievement']['singleclear'])), bool(int(self.config['Achievement']['stageaclear'])),
                            bool(int(self.config['Achievement']['stagebclear'])), bool(int(self.config['Achievement']['stagecclear'])),
                            bool(int(self.config['Achievement']['stagedclear'])), bool(int(self.config['Achievement']['stageallclear'])),
                            bool(int(self.config['Achievement']['in10turnwin'])), bool(int(self.config['Achievement']['onlynumbercardwin'])),
                            bool(int(self.config['Achievement']['onlyskillcardwin'])), bool(int(self.config['Achievement']['otherplayerunowin'])),
                            bool(int(self.config['Achievement']['grabover15card'])), bool(int(self.config['Achievement']['luckythree'])),
                            ]
        self.achieve_date = [self.config['date']['singleclear'], self.config['date']['stageaclear'],
                             self.config['date']['stagebclear'], self.config['date']['stagecclear'],
                             self.config['date']['stagedclear'], self.config['date']['stageallclear'],
                             self.config['date']['in10turnwin'], self.config['date']['onlynumbercardwin'],
                             self.config['date']['onlyskillcardwin'], self.config['date']['otherplayerunowin'],
                             self.config['date']['grabover15card'], self.config['date']['luckythree'],
        ]
        self.note = []
        self.note.append('''Single
Win''')
        self.note.append('''Stage A
Clear''')
        self.note.append('''Stage B
Clear''')
        self.note.append('''Stage C
Clear''')
        self.note.append('''Stage D
Clear''')
        self.note.append('''All Story
Clear''')
        self.note.append('''In 10 turns
Win''')
        self.note.append('''Only
Number Card
Win''')
        self.note.append('''Only
Skill Card
Win''')
        self.note.append('''Other Player
UNO Win''')
        self.note.append('''Grab Over
15 Cards''')
        self.note.append('''Lucky
Three''')
        
        self.description = ['You must win the Single Player.', 'You must win Stage A.', 'You must win Stage B.',
                            'You must win Stage C.', 'You must win Stage D.', 'You must win All Stages.',
                            'You must win in 10 turns.', 'You must win using only the Number Card.', 'You must win using only the Skill Card.',
                            'You must win after another player declares UNO.', 'You must grab more than 15 cards.', 'You must give three consecutive attack cards.'
                            ]
        # Clear the screen
        self.screen.fill((0, 0, 0))

    def draw(self):
        self.screen.fill((0, 0, 0))
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()

        if self.num == 0:
            x_pos_list = [(screenW // 7) * i for i in range(1, 7)]                          # 동그라미를 가로로 1/7, 2/7, ... 에 위치하게 함
            y_pos_list = [(screenH // 3) * i - (screenH // 7) for i in range(1, 3)]         # 동그라미를 세로로 1/3, 2/3에 위치하게 함

            if int(self.config['window']['default']) == 1:
                new_font = pygame.font.SysFont(None, 15)
                set_y = 15
            elif int(self.config['window']['default']) == 2:
                new_font = pygame.font.SysFont(None, 20)
                set_y = 20
            elif int(self.config['window']['default']) == 3:
                new_font = pygame.font.SysFont(None, 60)
                set_y = 60

            for i, name in enumerate(self.items):
                # 업적 안깬거는 회색, 깬거는 흰색
                pygame.draw.circle(self.screen, (255, 255, 255) if self.achieve_clear[i] == True else (100, 100, 100),
                                (x_pos_list[i % 6],
                                    y_pos_list[i // 6]), 20)

                if i == (self.currentXY[1] * 6 + self.currentXY[0]):
                    pygame.draw.circle(self.screen, (255, 0, 0), (x_pos_list[i % 6], y_pos_list[i // 6]), 20)

                
                # 맵 선택시 나오는 설명
                lines = self.note[i].splitlines()
                for j, l in enumerate(lines):
                    self.screen.blit(new_font.render(l, True, (255, 255, 255)),
                        (
                        x_pos_list[i % 6] - new_font.render(l, True, (255, 255, 255)).get_width() // 2,
                        y_pos_list[i // 6] + screenH // 20 + set_y * j
                        )
                    )
            font = self.font.render("Go back", True, (255, 255, 255) if self.currentXY[1] != 2 else (255, 0, 0))         # self.current가 0이면 흰, 1이면 빨
            self.screen.blit(font, (screenW // 2 - font.get_width() // 2, screenH * 3.5 // 4))

        else:
            if int(self.config['window']['default']) == 1:
                new_font = pygame.font.SysFont(None, 30)
                set_y = 30
            elif int(self.config['window']['default']) == 2:
                new_font = pygame.font.SysFont(None, 48)
                set_y = 48
            elif int(self.config['window']['default']) == 3:
                new_font = pygame.font.SysFont(None, 60)
                set_y = 60

            text = new_font.render(self.description[self.num - 1], True, (255, 255, 255))
            self.screen.blit(text, (screenW // 2 - text.get_width() // 2,
            screenH * 0.3 - text.get_height() // 2)
            )

            outText = pygame.font.SysFont(None, set_y // 2).render('Click with your mouse or press any key to go back.', True, (255, 255, 255))
            self.screen.blit(outText, (screenW // 2 - outText.get_width() // 2,
                                       screenH * 0.8 - outText.get_height() // 2))

            if self.achieve_clear[self.num - 1]:
                text = new_font.render('Achievement Unlocked', True, (0, 0, 255))
                self.screen.blit(text, (screenW // 2 - text.get_width() // 2,
                screenH * 0.3 - text.get_height() // 2 + set_y * 2)
                )

                date = new_font.render(self.achieve_date[self.num - 1], True, (255, 255, 255))
                self.screen.blit(date, (screenW // 2 - text.get_width() // 2,
                screenH * 0.3 - text.get_height() // 2 + set_y * 2 + set_y)
                )
            
            else:
                text = new_font.render('Achievement Locked', True, (255, 0, 0))
                self.screen.blit(text, (screenW // 2 - text.get_width() // 2,
                screenH * 0.3 - text.get_height() // 2 + set_y * 2)
                )
            
        

    def run(self):
        clock = pygame.time.Clock()
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()

        x_pos_list = [(screenW // 7) * i for i in range(1, 7)]                          # 동그라미를 가로로 1/5, 2/5, ... 에 위치하게 함
        y_pos_list = [(screenH // 3) * i - (screenH // 7) for i in range(1, 3)]         # 동그라미를 세로로 1/4, 2/4, 3/4에 위치하게 함

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and self.num == 0:
                    if event.key == self.keys["UP"]:
                        self.currentXY[1] = (self.currentXY[1] - 1) % 3
                    elif event.key == self.keys["DOWN"]:
                        self.currentXY[1] = (self.currentXY[1] + 1) % 3
                    elif event.key == self.keys["LEFT"]:
                        self.currentXY[0] = (self.currentXY[0] - 1) % 6
                    elif event.key == self.keys["RIGHT"]:
                        self.currentXY[0] = (self.currentXY[0] + 1) % 6
                    elif event.key == self.keys["RETURN"]:
                        if self.currentXY[1] == 2:
                            return self.currentXY[1]
                        else:
                            self.num = (self.currentXY[1] * 6 + self.currentXY[0]) + 1
                    elif event.key == self.keys["ESCAPE"]:
                        pygame.quit()
                        sys.exit()
                
                elif event.type == KEYDOWN and self.num != 0:
                    self.num = 0

                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    text = self.font.render("Go back", True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.topleft = (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() * 3.5 // 4)
                    if event.type == MOUSEBUTTONUP and self.num != 0:
                        self.num = 0
                    for i, item in enumerate(self.items):
                        circle_rect = pygame.Rect(x_pos_list[i % 6] - 20, y_pos_list[i // 6] - 20, 40, 40)
                        if circle_rect.collidepoint(pos):
                            if event.type == MOUSEMOTION:
                                self.currentXY[0] = i % 6
                                self.currentXY[1] = i // 6
                            elif event.type == MOUSEBUTTONUP:
                                print(f"{self.items[i]} click!")
                                self.num = (self.currentXY[1] * 6 + self.currentXY[0]) + 1
                        if text_rect.collidepoint(pos):
                            if event.type == MOUSEMOTION:
                                self.currentXY[1] = 2
                            if event.type == MOUSEBUTTONUP:
                                print("Go Back click!")
                                if self.currentXY[1] == 2:
                                    self.screen.fill((0, 0, 0))
                                    return 0
            # Draw the menu
            self.draw()
            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)
