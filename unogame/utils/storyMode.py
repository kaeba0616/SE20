import pygame, configparser
import sys
from pygame.locals import *
from single_play import Game
from utils import menu, settings, sound, stageA, stageC, stageD, stageB
import pygame, configparser
import sys
from pygame.locals import *
from single_play import Game



class StoryModes:

    def __init__(self, screen, font, config, key, soundFX):
        self.screen = screen                                                        # 게임의 스크린
        self.font = font                                                            # 폰트
        self.soundFX = soundFX

        self.stages = ["Stage1", "Stage2", "Stage3", "Stage4"]                      # stage 이름
        self.back = ["Go back"]                                                     # Go back 버튼 이름
        self.current_stage = 0                                                      # 현재 커서의 가로 위치
        self.current_UpDown = 0                                                     # 현재 커서의 세로 위치
        self.text_color = (255, 255, 255)                                           # 텍스트 색깔
        self.note = []
        # self.note = ["Stage 1 description", "Stage 2 description", "Stage 3 description", "Stage 4 description"]    # 적 설명
        self.items = ['Play', 'Back']                                               # 스테이지 선택 시 play or back
        self.WIDTH = self.screen.get_width()
        self.HEIGHT = self.screen.get_height()
        self.config = config
        self.stage_clear = [bool(int(self.config['clear']['stage1'])), bool(int(self.config['clear']['stage2'])),
                            bool(int(self.config['clear']['stage3'])), bool(int(self.config['clear']['stage4'])),
                            True]                                                   # stage 클리어 변수 설정
        self.key = key
        self.window_size = int(self.config['window']['default'])

        self.note.append("""In this stage, on the first distribution,
the opponent player will receive
the skill card with a 50% higher
probability. Use a combo that allows
the opponent player to play two to
three or more cards at once by properly
combining skill cards such as reverse
progression and jump.""")
        self.note.append("""In this stage, you play against
3 opponent players and distribute
all cards to the players in equal numbers
except for the first card.""")
        self.note.append("""In this stage, you will play
against 2 opponent players, and
the color of the card you can play
every 5 turns will be randomly changed.""")
        self.note.append("""In this stage, you play
against the opposition player, and
the opposition starts with three cards
on the first distribution.""")
        
        
        
        self.screen.fill((0, 0, 0))

    def draw(self):
        self.screen.fill((0, 0, 0))
        # 스토리 모드 지도 구현
        x_pos_list = [(self.screen.get_width() // 5) * i for i in range(1, 5)]             # 동그라미를 1/5, 2/5, ... 에 위치하게 함
        y_pos = self.screen.get_height() // 2 - (self.screen.get_height() // 7)
        for i, stage in enumerate(self.stages):
            # 스테이지 안깬거는 회색, 깬거는 흰색
            pygame.draw.circle(self.screen, (255, 255, 255) if self.stage_clear[i] == True else (100, 100, 100), (x_pos_list[i], y_pos), 30)
            stage_name = self.font.render(self.stages[i], True, (255, 255, 255))
            # self.font.render("Go back", True, (255, 255, 255) if self.stage_clear[i] == True else (100, 100, 100))

            # 현재 위치면 빨간색으로
            if self.current_stage == i and self.current_UpDown == 0:
                pygame.draw.circle(self.screen, (255, 0, 0), (x_pos_list[i], y_pos), 30)

            elif self.current_stage == i and self.current_UpDown == 1:
                 pygame.draw.circle(self.screen, (255, 255, 255), (x_pos_list[i], y_pos), 30)
            self.screen.blit(
                stage_name,
                (
                (self.screen.get_width() // 5) * (i+1) - stage_name.get_width() // 2,
                y_pos + self.screen.get_height() // 10
                )
            )
        font = self.font.render("Go back", True, (255, 255, 255) if self.current_UpDown == 0 else (255, 0, 0))
        self.screen.blit(font, (self.screen.get_width() // 2 - font.get_width() // 2, self.screen.get_height() * 3 // 4))

    def description(self, num, selected):
        self.screen.fill((0, 0, 0))

        # 맵 선택시 나오는 play or back
        for i, item in enumerate(self.items):
            text = self.font.render(
                item, True, (255, 255, 255) if i != selected else (255, 0, 0)
            )
            if i == 0:
                self.screen.blit(
                    text, 
                    (self.screen.get_width() * 0.4 - text.get_width() // 2,
                    self.screen.get_height() * 0.75 - text.get_height() // 2)
                )
            else:
                self.screen.blit(
                    text, (
                    self.screen.get_width() * 0.6 - text.get_width() // 2,
                    self.screen.get_height() * 0.75 - text.get_height() // 2
                    )
                )

        if int(self.config['window']['default']) == 1:
            new_font = pygame.font.SysFont(None, 30)
            set_y = 30
        elif int(self.config['window']['default']) == 2:
            new_font = pygame.font.SysFont(None, 48)
            set_y = 48
        elif int(self.config['window']['default']) == 3:
            new_font = pygame.font.SysFont(None, 60)
            set_y = 60


        # 맵 선택시 나오는 설명
        lines = self.note[num].splitlines()
        for i, l in enumerate(lines):
            self.screen.blit(new_font.render(l, True, (255, 255, 255)),
                             (
            self.screen.get_width() // 2 - new_font.render(l, True, (255, 255, 255)).get_width() // 2,
            self.screen.get_height() * 0.2 - new_font.render(l, True, (255, 255, 255)).get_height() // 2 + set_y * i
                )
            )


    def description_draw(self, num):
        clock = pygame.time.Clock()
        running = True
        selected = 0
        text1 = self.font.render("Play", True, (255, 255, 255))
        text2 = self.font.render("Back", True, (255, 255, 255))

        text1_rect = text1.get_rect()
        text2_rect = text2.get_rect()
        text1_rect.topleft = (self.screen.get_width() * 0.4 - text1.get_width() // 2,
                    self.screen.get_height() * 0.75 - text1.get_height() // 2)
        text2_rect.topleft = (self.screen.get_width() * 0.6 - text2.get_width() // 2,
                    self.screen.get_height() * 0.75 - text2.get_height() // 2)
        while running:
            self.description(num, selected)
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.key["LEFT"] or event.key == self.key["RIGHT"]:
                        selected += 1
                    selected = selected % 2
                    if event.key == self.key["RETURN"] and selected == 0:
                        print("Play click!")
                        
                        print(num)
                        if num == 0:            # 스테이지 A 선택 + Play
                            stage = stageA.stage_A(self.screen, 2, self.key, self.config, self.soundFX)
                            win = stage.start_single_play()
                            if win != 0:
                                return
                        elif num == 1:          # 스테이지 B 선택 + Play
                            stage = stageB.stage_B(self.screen, 4, self.key, self.config, self.soundFX)
                            win = stage.start_single_play()
                            if win != 0:
                                return

                        elif num == 2:          # 스테이지 C 선택 + Play
                            stage = stageC.stage_C(self.screen, 3, self.key, self.config, self.soundFX)
                            win = stage.start_single_play()
                            if win != 0:
                                return
                        elif num == 3:          # 스테이지 D 선택 + Play
                            stage = stageD.stage_D(self.screen, 2, self.key, self.config, self.soundFX)
                            win = stage.start_single_play()
                            if win != 0:
                                return

                        # 승리 시, 다음 스테이지를 열게함
                        self.config['clear'][f'stage{num + 2}'] = str(1)
                        with open('setting_data.ini', 'w') as f:
                            self.config.write(f)
                        self.stage_clear = [bool(int(self.config['clear']['stage1'])), bool(int(self.config['clear']['stage2'])), bool(int(self.config['clear']['stage3'])), bool(int(self.config['clear']['stage4'])), True]
                        return
                    

                    elif event.key == self.key["RETURN"] and selected == 1:
                        print("Back click!")
                        return
                    

                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    if text1_rect.collidepoint(pos):
                        if event.type == MOUSEMOTION:
                            selected = 0
                        if event.type == MOUSEBUTTONUP:
                            if num == 0:            # 스테이지 A 선택 + Play
                                stage = stageA.stage_A(self.screen, 2, self.key, self.config, self.soundFX)
                                win = stage.start_single_play()
                                if win != 0:
                                    return
                            elif num == 1:          # 스테이지 B 선택 + Play
                                stage = stageB.stage_B(self.screen, 4, self.key, self.config, self.soundFX)
                                win = stage.start_single_play()
                                if win != 0:
                                    return

                            elif num == 2:          # 스테이지 C 선택 + Play
                                stage = stageC.stage_C(self.screen, 3, self.key, self.config, self.soundFX)
                                win = stage.start_single_play()
                                if win != 0:
                                    return
                            elif num == 3:          # 스테이지 D 선택 + Play
                                stage = stageD.stage_D(self.screen, 2, self.key, self.config, self.soundFX)
                                win = stage.start_single_play()
                                if win != 0:
                                    return
                            
                            self.config['clear'][f'stage{num + 2}'] = str(1)
                            with open('setting_data.ini', 'w') as f:
                                self.config.write(f)
                            self.stage_clear = [bool(int(self.config['clear']['stage1'])), bool(int(self.config['clear']['stage2'])), bool(int(self.config['clear']['stage3'])), bool(int(self.config['clear']['stage4'])), True]
                            return
                            '''
                            Todo
                            대전하기 만들기
                            '''
                    elif text2_rect.collidepoint(pos):
                        if event.type == MOUSEMOTION:
                            selected = 1
                        if event.type == MOUSEBUTTONUP:
                            print(f"Back click!")
                            return
                            '''
                            Todo
                            대전하기 만들기
                            '''

            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60) 



    def run(self):
        # 메인 루프
        clock = pygame.time.Clock()
        running = True
        while running:
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.key["LEFT"]:
                        next = (self.current_stage - 1) % len(self.stages)
                        while self.stage_clear[next] == False:
                            next = (next - 1) % len(self.stages)
                        self.current_stage = next
                                
                    elif event.key == self.key["RIGHT"]:
                        next = (self.current_stage + 1) % len(self.stages)
                        while self.stage_clear[next] == False:
                            next = (next + 1) % len(self.stages)
                        self.current_stage = next
                    
                    elif event.key == self.key["UP"] or event.key == self.key["DOWN"]:
                        if self.current_UpDown == 0:
                            self.current_UpDown = 1
                        else:
                            self.current_UpDown = 0

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == self.key["RETURN"]:
                        
                        if self.current_UpDown == 1:
                            print(f"Go Back click!")
                            self.screen.fill((0, 0, 0))
                            return 0
                        else:
                            print(f"{self.stages[self.current_stage]} click!")
                            self.description_draw(self.current_stage)


                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    text = self.font.render("Go back", True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.topleft = (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() * 3 // 4)
                    for i, stage in enumerate(self.stages):
                        circle_rect = pygame.Rect((self.screen.get_width() // 5) * (i+1) - 30, self.screen.get_height() // 2 - (self.screen.get_height() // 7) - 30, 60, 60)
                        if circle_rect.collidepoint(pos) and self.stage_clear[i]:
                            if event.type == MOUSEMOTION:
                                self.current_UpDown = 0
                                self.current_stage = i
                            elif event.type == MOUSEBUTTONUP:
                                print(f"{self.stages[self.current_stage]} click!")
                                self.description_draw(self.current_stage)
                        elif text_rect.collidepoint(pos):
                            if event.type == MOUSEMOTION:
                                self.current_UpDown = 1
                            elif event.type == MOUSEBUTTONUP:
                                print("Go Back click!")
                                if self.current_UpDown == 1:
                                    self.screen.fill((0, 0, 0))
                                    return 0
            
            
            # 화면 채우기
            self.draw()

            '''
            Todo
            1. 스테이지 구현
            '''
            
            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)