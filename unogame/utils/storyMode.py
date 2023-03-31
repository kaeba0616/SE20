import pygame, configparser
import sys
from pygame.locals import *



class StoryMode:

    def __init__(self, screen, font, config):
        self.screen = screen
        self.font = font
        self.stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Go back"]
        self.current_stage = 0
        self.text_color = (255, 255, 255)
        self.note = ["Stage 1 description", "Stage 2 description", "Stage 3 description", "Stage 4 description"]
        self.items = ['Play', 'Back']
        self.WIDTH = self.screen.get_width()
        self.HEIGHT = self.screen.get_height()
        self.config = config
        self.stage_clear = [bool(int(self.config['clear']['stage1'])), bool(int(self.config['clear']['stage2'])), bool(int(self.config['clear']['stage3'])), bool(int(self.config['clear']['stage4'])), True]
        
    
        
        self.screen.fill((0, 0, 0))

    def draw(self):
        self.screen.fill((0, 0, 0))

        for i, stage in enumerate(self.stages):
            text = self.font.render(stage, True, (255, 255, 255) if self.stage_clear[i] == True else (100, 100, 100))
            if self.current_stage == i:
                text = self.font.render(stage, True, (255, 0, 0))
            self.screen.blit(
                text,
                (
                self.screen.get_width() // 2 - text.get_width() // 2,
                100 + i * 100
                )
            )

    def description(self, num, selected):
        self.screen.fill((0, 0, 0))

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

        text = self.font.render(self.note[num], True, (255, 255, 255))
        self.screen.blit(
            text,
            (
            self.screen.get_width() // 2 - text.get_width() // 2,
            self.screen.get_height() * 0.35 - text.get_height() // 2
            )
        )


    def description_draw(self, num):
        clock = pygame.time.Clock()
        running = True
        selected = 0
        while running:
            self.description(num, selected)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        selected += 1
                    selected = selected % 2
                    if event.key == pygame.K_RETURN and selected == 0:
                        print("Play click!")
                        print("임의로 레벨 clear 시킴")
                        self.config['clear'][f'stage{num + 2}'] = str(1)
                        with open('./unogame/setting_data.ini', 'w') as f:
                            self.config.write(f)
                        self.stage_clear = [bool(int(self.config['clear']['stage1'])), bool(int(self.config['clear']['stage2'])), bool(int(self.config['clear']['stage3'])), bool(int(self.config['clear']['stage4'])), True]
                        return
                        '''
                        Todo
                        대전하기 만들기
                        '''
                    elif event.key == pygame.K_RETURN and selected == 1:
                        print("Back click!")
                        return
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
                    if event.key == pygame.K_UP:
                        next = (self.current_stage - 1) % len(self.stages)
                        while self.stage_clear[next] == False:
                            next = (next - 1) % len(self.stages)
                        self.current_stage = next
                                
                    elif event.key == pygame.K_DOWN:
                        next = (self.current_stage + 1) % len(self.stages)
                        while self.stage_clear[next] == False:
                            next = (next + 1) % len(self.stages)
                        self.current_stage = next
                    elif event.key == pygame.K_ESCAPE: # and self.stage_clear[self.current_stage]:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN and self.stage_clear[self.current_stage]:
                        print(f"{self.stages[self.current_stage]} click!")
                        if self.current_stage == 4:
                            self.screen.fill((0, 0, 0))
                            return 0
                        else:
                            self.description_draw(self.current_stage)
                        '''
                            수정 필요
                            stage 1, stage 2 등의 설명이 나오는 description_draw
                            밑에는 아님..
                            ex) start_single_play(self.current_stage) 식으로
                            current_stage의 스테이지를 플레이할 수 있도록
                        '''


                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for i, stage in enumerate(self.stages):
                        text = self.font.render(stage, True, (255, 255, 255))
                        rect = text.get_rect()
                        rect.topleft = (
                            self.screen.get_width() // 2 - text.get_width() // 2,
                            100 + i * 100
                        )
                        if rect.collidepoint(pos) and self.stage_clear[i]:
                            if event.type == MOUSEMOTION:
                                self.current_stage = i
                            elif event.type == MOUSEBUTTONUP:
                                print(f"{self.stages[self.current_stage]} click!")
                                if self.current_stage == 4:
                                    self.screen.fill((0, 0, 0))
                                    return 0
                                else:
                                    self.description_draw(self.current_stage)
                            '''
                                수정 필요
                                stage 1, stage 2 등의 설명이 나오는 화면
                                밑에는 아님..   
                                ex) start_single_play(self.current_stage) 식으로
                                current_stage의 스테이지를 플레이할 수 있도록
                            '''
            
            
            # 화면 채우기
            self.draw()

            '''
            Todo
            1. 스테이지 클릭 시, 스테이지 설명 화면 + 대결 버튼 + 뒤로가기 버튼
            2. 스테이지 클리어 시, 스테이지 TF 업데이트
            '''
            
            # # 스테이지 텍스트 렌더링
            # for i in range(len(self.stages)):
            #     color = (255, 255, 255) if self.stage_clear[i] else (100, 100, 100)
            #     text = self.font.render(self.stages[i], True, color)
            #     text_rect = text.get_rect(center=(self.screen.get_width()/2, 100+i*100))
            #     self.screen.blit(text, text_rect)
            
            
            # 선택된 스테이지 설명 렌더링
            # description = self.font.render(self.stages[self.current_stage], True, (255, 255, 255))
            # description_rect = description.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()-100))
            # self.screen.blit(description, description_rect)
            
            # 클리어한 스테이지 업데이트
            # if self.current_stage > 0:
            #     self.stage_clear[self.current_stage-1] = True
            
            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)