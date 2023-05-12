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
        self.soundFX = soundFX
        self.current_stage = 0                                                      # 현재 커서의 가로 위치
        self.config = config
        self.stages = ['stageA', 'stageB', 'stageC', 'stageD']
        self.stage_clear = [bool(int(self.config['clear']['stage1'])), bool(int(self.config['clear']['stage2'])),
                            bool(int(self.config['clear']['stage3'])), bool(int(self.config['clear']['stage4']))]
        self.stage_open = [bool(int(self.config['open']['stage1'])), bool(int(self.config['open']['stage2'])),
                            bool(int(self.config['open']['stage3'])), bool(int(self.config['open']['stage4']))]
        self.key = key
        self.window = int(self.config['window']['default'])
        self.visible = 'main'

        # 이미지
        self.background = [pygame.image.load('./resources/images/storymode/stageA.png'), pygame.image.load('./resources/images/storymode/stageB.png'),
                           pygame.image.load('./resources/images/storymode/stageC.png'), pygame.image.load('./resources/images/storymode/stageD.png')]
        self.memo = [pygame.image.load('./resources/images/storymode/memoA.png'), pygame.image.load('./resources/images/storymode/memoB.png'),
                    pygame.image.load('./resources/images/storymode/memoC.png'), pygame.image.load('./resources/images/storymode/memoD.png')]
        self.check = pygame.image.load('./resources/images/storymode/check.png')
        self.game_start = pygame.image.load('./resources/images/storymode/gamestart.png')


        self.ratio = 1
        
        self.latestClear = 0                                # 제일 마지막으로 깬 단계
        self.x0, self.x1, self.x2, self.x3 = 125, 292, 570, 846
        self.y0, self.y1, self.y2, self.y3 = 188, 350, 198, 260
        self.radius = 40
        self.x_pos_list = [self.x0 * self.ratio, self.x1 * self.ratio, self.x2 * self.ratio, self.x3 * self.ratio]
        self.y_pos_list = [self.y0 * self.ratio, self.y1 * self.ratio, self.y2 * self.ratio, self.y3 * self.ratio]

        self.x4, self.y4 = 28, 666
        self.x5, self.y5 = 107, 473

        self.memo_x, self.memo_y = 652, 501
        self.start_x, self.start_y = 215, 530
        for i in range(4):
            if self.stage_clear[i] == False:
                self.latestClear = i
                break


        self.screen.blit(self.background[self.latestClear], (0, 0))

    def draw(self):

        # 배경화면
        for i in range(4):
            if self.stage_clear[i] == False:
                self.latestClear = i
                break
            elif self.stage_clear[3] == True:
                self.latestClear = 3
                
        self.screen.blit(self.background[self.latestClear], (0, 0))

        # 체크 표시
        for i in range(4):
            if self.stage_clear[i] == True:
                
                self.screen.blit(self.check, (self.x_pos_list[i] - self.check.get_width() // 2, self.y_pos_list[i] - self.check.get_height() // 2.3))

        # 게임 시작, 메모 표시
        if self.visible != 'main':   # self.current_stage
            
            self.screen.blit(self.memo[self.visible], (self.memo_x - self.memo[self.visible].get_width() // 2, self.memo_y - self.memo[self.visible].get_height() // 2))
            
            self.screen.blit(self.game_start, (self.start_x - self.game_start.get_width() // 2, self.start_y - self.game_start.get_height() // 2))



    def run(self):
        # 메인 루프
        clock = pygame.time.Clock()
        running = True
        while running:
            # self.ratio = self.screen.get_height() / self.background[self.latestClear].get_height()

            # self.x0, self.x1, self.x2, self.x3, self.x4, self.radius, self.x5, self.memo_x, self.start_x = [x * self.ratio for x in [self.x0, self.x1, self.x2, self.x3, self.x4, self.radius, self.x5, self.memo_x, self.start_x]]

            self.x_pos_list = [self.x0, self.x1, self.x2, self.x3]
            # self.y0, self.y1, self.y2, self.y3, self.y4, self.y5, self.memo_y, self.start_y = [x * self.ratio for x in [self.y0, self.y1, self.y2, self.y3, self.y4, self.y5, self.memo_y, self.start_y]]

            self.y_pos_list = [self.y0, self.y1, self.y2, self.y3]
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    back_rect = pygame.Rect(self.x4, self.y4, 100, 50)
                    if back_rect.collidepoint(pos):
                        if event.type == MOUSEBUTTONUP:
                            print("Go Back click!")
                            self.visible = 'main'
                            return 0
                    for i in range(4):
                        circle_rect = pygame.Rect(self.x_pos_list[i] - self.radius, self.y_pos_list[i] - self.radius, self.radius * 2, self.radius * 2)
                        if circle_rect.collidepoint(pos) and self.stage_open[i]:
                            if event.type == MOUSEMOTION:
                                self.current_stage = i
                            elif event.type == MOUSEBUTTONUP:
                                print(f"{self.stages[self.current_stage]} click!")
                                self.visible = self.current_stage
                    
                    if self.visible != 'main':
                        start_rect = pygame.Rect(self.x5, self.y5, 216, 114)
                        if start_rect.collidepoint(pos):
                            if event.type == MOUSEBUTTONUP:
                                print(f"{self.stages[self.current_stage]} start!")
                                if self.current_stage == 0:             # 스테이지 A 선택 + Play
                                    print("임의로 게임 clear")
                                    # stage = stageA.stage_A(self.screen, 2, self.key, self.config, self.soundFX)
                                    # win = stage.start_single_play()
                                    # if win != 0:
                                    #     return
                                    
                                elif self.current_stage == 1:          # 스테이지 B 선택 + Play
                                    print("임의로 게임 clear")
                                    # stage = stageB.stage_B(self.screen, 4, self.key, self.config, self.soundFX)
                                    # win = stage.start_single_play()
                                    # if win != 0:
                                    #     return

                                elif self.current_stage == 2:          # 스테이지 C 선택 + Play
                                    print("임의로 게임 clear")
                                    # stage = stageC.stage_C(self.screen, 3, self.key, self.config, self.soundFX)
                                    # win = stage.start_single_play()
                                    # if win != 0:
                                    #     return

                                elif self.current_stage == 3:          # 스테이지 D 선택 + Play
                                    print("임의로 게임 clear")
                                    # stage = stageD.stage_D(self.screen, 2, self.key, self.config, self.soundFX)
                                    # win = stage.start_single_play()
                                    # if win != 0:
                                    #     return
                                
                                self.config['clear'][f'stage{self.current_stage + 1}'] = '1'
                                self.config['open'][f'stage{self.current_stage + 2}'] = '1'
                                with open('setting_data.ini', 'w') as f:
                                    self.config.write(f)
                                self.stage_clear = [bool(int(self.config['clear']['stage1'])), bool(int(self.config['clear']['stage2'])), bool(int(self.config['clear']['stage3'])), bool(int(self.config['clear']['stage4']))]
                                self.stage_open = [bool(int(self.config['open']['stage1'])), bool(int(self.config['open']['stage2'])), bool(int(self.config['open']['stage3'])), bool(int(self.config['open']['stage4']))]
                                
                                self.visible = 'main'
                                return


                        
            
            
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