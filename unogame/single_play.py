import itertools
import random
import sys

import pygame

from models.button import Button, Component
from models.card import Card
from models.Human import Human
from models.AI import AI

from models.button import Button, Component
from pause import PauseClass
import time

from models.event import *

from utils.achievement import achievement


class Game:
    pygame.font.init()
    font = pygame.font.Font("./resources/fonts/Pixeltype.ttf", 36)
    clock = pygame.time.Clock()

    def __init__(self, screen, player_number, keys, config, soundFX):
        # lms
        self.achieve = achievement(screen, config)
        # lms

        self.start_count = 1

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.player_number = player_number

        self.soundFX = soundFX
        self.screen = screen

        self.who = None
        self.keys = keys
        self.config = config
        self.event_active = True

        self.game_active = False  # start를 누른 이후 게임 진행 중이면 True
        self.is_win = False
        self.is_get = False  # 자기 턴에 카드 뽑음
        self.run = True
        self.is_color_change = False
        self.edit_name = False
        self.edit_text = "__________"

        # color change하는 중 배경
        self.alpha_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        self.alpha_surface.fill(
            (0, 0, 0, 128)
        )  # (0,0,0,128) -> (0,0,0)으로 (불필요한 값. 작동 안될 수 있음)
        self.alpha_surface.set_alpha(128)

        self.turn_list = []  # 차례의 순서를 나타내는 list
        self.turn_index = 0  # 누구의 차례인지 알려주는 변수

        self.me = None
        self.deck = []  # 가운데에서 뽑힐 카드
        self.remain = []  # 낸 카드들

        self.deck_surf = pygame.image.load(
            "resources/images/card/normalMode/backcart.png"
        ).convert_alpha()
        self.deck_rect = self.deck_surf.get_rect(
            center=(self.screen_width / 3, self.screen_height / 3)
        )

        # self.now_card = Card("red", None, 0, False, self.config)
        self.now_card = None
        self.now_card_surf = pygame.image.load(
            "resources/images/card/normalMode/backcart.png"
        ).convert_alpha()
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 30, self.screen_height / 3)
        )

        self.win_list = []

        self.uno_button = Button(
            self.screen_width / 3 + 240,
            self.screen_height / 3,
            50,
            30,
            (255, 255, 255),
            "UNO",
            (64, 64, 64),
            30,
            255,
        )
        self.retry_surf = Game.font.render(
            "click to return to main", False, (64, 64, 64)
        )
        self.retry_rect = self.retry_surf.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2 + 50)
        )

        self.start_button = Button(
            self.screen_width // 2 - 100,
            self.screen_height // 2 - 30,
            100,
            60,
            (255, 255, 255),
            "START",
            (64, 64, 64),
            40,
            255,
        )

        # 로비를 생성하는데 필요한 변수
        self.lobby_background = pygame.Rect(
            self.screen_width - 150, 0, 150, self.screen_height
        )

        self.now_button = Button(
            self.screen_width // 2 + 60,
            self.screen_height // 5 - 50,
            40,
            40,
            (255, 255, 255),
            "now",
            (0, 0, 0),
            15,
            255,
        )

        self.ok_button = Button(
            self.screen_width // 2,
            self.screen_height // 2 + 100,
            40,
            30,
            (255, 255, 255),
            "ok",
            (64, 64, 64),
            40,
            255,
        )
        self.now_turn_button = Button(
            self.screen_width // 8,
            self.screen_height // 2 - 30,
            40,
            30,
            (255, 255, 255),
            "",
            (64, 64, 64),
            35,
            0,
        )

        self.skill_active_button = Button(
            self.screen_width // 8 + 50,
            self.screen_height // 8,
            40,
            30,
            (255, 255, 255),
            "reverse skill active yellow > green",
            (64, 64, 64),
            35,
            0,
        )
        self.info_list = []
        self.info_list.append(
            Component(
                self.lobby_background.x,
                self.lobby_background.y,
                150,
                90,
                (255, 255, 255),
                f"PLAYER 1(ME)",
                (64, 64, 64),
                20,
                None,
            )
        )
        for i in range(1, 6):
            self.info_list.append(
                Component(
                    self.lobby_background.x,
                    self.lobby_background.y + 100 * i,
                    150,
                    90,
                    (64, 64, 64),
                    f"EMPTY",
                    (220, 220, 220),
                    20,
                    None,
                )
            )

        self.move_surf = pygame.image.load(
            "resources/images/card/normalMode/backcard.png"
        ).convert_alpha()
        self.move_surf = pygame.transform.scale(self.move_surf, (50, 70))
        self.move_rect = self.move_surf.get_rect(center=self.deck_rect.center)
        self.moving = False
        self.moving_start_time = 0
        self.velocity = 0

        self.card_list = []

        self.change_color_list = []
        self.CENTER_X_POS = self.screen_width // 10
        self.CENTER_Y_POS = self.screen_height // 5
        for color, pos, color_string in zip(
            [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
            [
                (self.CENTER_X_POS - 25, self.CENTER_Y_POS - 25),
                (self.CENTER_X_POS + 25, self.CENTER_Y_POS - 25),
                (self.CENTER_X_POS - 25, self.CENTER_Y_POS + 25),
                (self.CENTER_X_POS + 25, self.CENTER_Y_POS + 25),
            ],
            ["red", "green", "blue", "yellow"],
        ):
            surf = pygame.Surface((50, 50))
            surf.fill(color_string)
            rect = surf.get_rect(center=pos)
            self.change_color_list.append([surf, rect, color, color_string])

        # 지금 선택한 카드를 나타내는 변수
        self.now_select = None

        # Timer 변수 세팅
        self.turn_timer = pygame.USEREVENT + 1
        self.current_time = 10
        pygame.time.set_timer(self.turn_timer, 1000)

        self.time_button = Button(
            self.screen_width // 8 + 40,
            self.screen_height // 2 + 15,
            80,
            30,
            (255, 255, 255),
            f"TIME : {self.current_time}",
            (64, 64, 64),
            30,
            255,
        )

        self.win_button = Button(
            self.screen_width / 2 - 50,
            self.screen_height / 2 - 20,
            100,
            40,
            (255, 255, 255),
            "Player 1 win !!",
            (64, 64, 64),
            30,
            0,
        )

        self.uno_timer = pygame.USEREVENT + 2
        self.is_uno = False

        self.skill_active_timer = pygame.USEREVENT + 3
        self.is_skill_active = False

        self.block_timer = pygame.USEREVENT + 4

        self.AI_timer = pygame.USEREVENT + 5
        self.is_computer_turn = False
        self.AI_timer_on = False

        self.move_timer = pygame.USEREVENT + 6

        self.event = Event(self)

    def start_single_play(self):
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        while self.run:
            self.screen.fill((50, 200, 50))
            self.make_screen()
            # event loop

            if self.game_active:
                self.time_button.text = f"TIME : {self.current_time}"
                self.time_button.draw(self.screen)
    
            for event in pygame.event.get():
                #print(event)
                if self.event.event_loop(event, self) == "out":
                    return
                if(not self.event_active):
                    pygame.event.clear()
                    break
            # event loop 종료

            self.next_screen(self.screen)
            pygame.display.update()

            # Limit the frame rate
            Game.clock.tick(60)

    def make_screen(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.deck_rect.centerx = self.screen_width / 3
        self.deck_rect.centery = self.screen_height / 3

        self.uno_button.rect.x = self.deck_rect.centerx + 150
        self.uno_button.rect.y = self.deck_rect.centery + 30

        self.retry_rect.centerx = self.screen_width / 2
        self.retry_rect.centery = self.screen_height / 2 + 50

        self.start_button.rect.x = self.screen_width // 2 - 100
        self.start_button.rect.y = self.screen_height // 2 - 30

        self.lobby_background.x = self.screen_width - 150
        self.lobby_background.y = 0
        self.lobby_background.height = self.screen_height

        self.now_button.rect.x = self.deck_rect.centerx + 150
        self.now_button.rect.y = self.deck_rect.centery - 50

        self.skill_active_button.rect.x = self.screen_width // 8 + 50
        self.skill_active_button.rect.y = 30
        self.ok_button.rect.x = self.screen_width // 2
        self.ok_button.rect.y = self.screen_height // 2 + 100

        self.win_button.rect.center = (
            self.screen_width / 2 - 50,
            self.screen_height / 2 - 20,
        )
        self.now_turn_button.center = (
            self.screen_width // 8,
            self.screen_height // 2 - 30,
        )
        self.time_button.center = (
            self.screen_width // 8 + 40,
            self.screen_height // 2 + 15,
        )

        self.now_card_rect.centerx = self.deck_rect.centerx + 80
        self.now_card_rect.centery = self.deck_rect.centery

        self.alpha_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        self.alpha_surface.fill(
            (0, 0, 0, 128)
        )  # (0,0,0,128) -> (0,0,0)으로 (불필요한 값. 작동 안될 수 있음)
        self.alpha_surface.set_alpha(128)

        self.change_color_list = []
        self.CENTER_X_POS = self.screen_width // 10
        self.CENTER_Y_POS = self.screen_height // 5
        for color, pos, color_string in zip(
            [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
            [
                (self.CENTER_X_POS - 32, self.CENTER_Y_POS - 32),
                (self.CENTER_X_POS + 32, self.CENTER_Y_POS - 32),
                (self.CENTER_X_POS - 32, self.CENTER_Y_POS + 32),
                (self.CENTER_X_POS + 32, self.CENTER_Y_POS + 32),
            ],
            ["red", "green", "blue", "yellow"],
        ):
            surf = Game.font.render(color_string, False, (64, 64, 64))
            rect = surf.get_rect(center=pos)
            self.change_color_list.append([surf, rect, color, color_string])

        for i, component in enumerate(self.info_list):
            component.rect.x = self.lobby_background.x
            component.rect.y = self.lobby_background.y + 100 * i

    def next_screen(self, screen):
        #print("next screen")
        #texttt = self.font.render("self.message", True, (255, 255, 255))
        #self.screen.blit(texttt, (50, 50))
        if self.game_active:
            ##
            if len(self.deck):
                screen.blit(self.deck_surf, self.deck_rect)
            screen.blit(self.now_card_surf, self.now_card_rect)

            # 누구의 턴인지 보여주는 부분
            if self.turn_list[self.turn_index] == self.me:
                self.now_turn_button.text = f"my turn"
            else:
                self.now_turn_button.text = (
                    f"PLAYER {self.turn_list[self.turn_index].number + 1}'s turn"
                )
            self.now_turn_button.draw(screen)

            # 손패를 그려주는 부분
            self.me.draw_hand(screen)

            if self.is_color_change:
                screen.blit(self.alpha_surface, (0, 0))
                for color_list in self.change_color_list:
                    screen.blit(color_list[0], color_list[1])
                    temp_rect = pygame.Rect(
                        color_list[1].x - 1,
                        color_list[1].y - 1,
                        color_list[1].width + 2,
                        color_list[1].height + 2,
                    )
                    pygame.draw.rect(screen, (0, 0, 0), temp_rect, 3)

            self.uno_button.draw(screen)
            if (
                self.now_select and self.me.turn == self.turn_index
            ) or self.now_select == self.uno_button:
                pygame.draw.rect(screen, (0, 0, 0), self.now_select, 3)

            pygame.draw.rect(screen, (47, 101, 177), self.lobby_background)
            for i in range(0, self.player_number):
                self.info_list[i].draw(screen, self.player_number, i)

            if self.now_card.color is not None:
                pixel = self.now_card_surf.get_at(
                    (
                        self.now_card_surf.get_width() // 2,
                        self.now_card_surf.get_height() - 1,
                    )
                )

                self.now_button.surface.fill(pixel)
            else:
                self.now_button.surface.fill((80, 80, 80))

            self.now_button.draw(screen)

            if self.is_skill_active:
                self.skill_active_button.draw(screen)

            if self.current_time == 8 and not self.moving:
                pygame.time.set_timer(self.move_timer, 3000)
                self.moving = True
                self.moving_start_time = pygame.time.get_ticks()

            if self.moving:
                c_time = pygame.time.get_ticks()
                self.card_move(
                    self.deck_rect.center, self.me.hand[-1].rect.center, c_time, 3000
                )
                self.screen.blit(self.move_surf, self.move_rect)

        else:
            screen.fill("green")
            # 게임이 종료되었을 때 덱 초기화
            for player in self.turn_list:
                player.hand.clear()
            self.deck.clear()
            self.remain.clear()

            if self.is_win:
                #print("win")
                #time.sleep(1)
                self.achieve.update(screen)
                self.win_button.draw(screen)
                screen.blit(self.retry_surf, self.retry_rect)
            else:
                self.start_button.draw(screen)
                pygame.draw.rect(screen, (47, 101, 177), self.lobby_background)
                for i in range(0, len(self.info_list)):
                    self.info_list[i].draw(screen, self.player_number, i)

            if self.edit_name:
                screen.blit(self.alpha_surface, (0, 0))
                rect = pygame.Rect(
                    self.screen_width // 2 - 150, self.screen_height // 2 - 50, 300, 180
                )
                pygame.draw.rect(screen, (255, 255, 255), rect)
                name_surf = Game.font.render(
                    "Enter Name(maximum 8)", False, (64, 64, 64)
                )
                name_rect = name_surf.get_rect(
                    center=(self.screen_width // 2, self.screen_height // 2 - 20)
                )
                input_surf = Game.font.render(self.edit_text, False, (64, 64, 64))
                input_rect = input_surf.get_rect(
                    center=(self.screen_width // 2, self.screen_height // 2 + 50)
                )
                self.ok_button.rect.center = (
                    self.screen_width // 2,
                    self.screen_height // 2 + 100,
                )
                screen.blit(name_surf, name_rect)
                screen.blit(input_surf, input_rect)
                self.ok_button.draw(screen)

            pygame.display.update()

    def computer_turn(self):
        self.com_card = []

        for card in self.turn_list[self.turn_index].hand:
            if self.check_condition(card):
                self.com_card.append(card)
        if len(self.com_card) == 0:
            self.draw_from_center(self.turn_list[self.turn_index].hand)
            self.pass_turn()
        else:
            self.now_card = self.com_card[0]
            self.now_card_surf = self.now_card.image
            self.turn_list[self.turn_index].hand.remove(self.now_card)
            self.remain.append(self.now_card)
            if self.now_card.skill is not None:
                # edit by sth
                # self.skill_active(self.now_card.skill)
                self.skill_active(self.com_card[0])
            if self.now_card.skill not in [
                # "change",
                "block",
                # "all",
            ]:
                self.pass_turn()

    def deck_none(self):
        if len(self.deck) == 0:
            print("덱이 없어서 계산을 합니다")
            win_condition = True
            ## test
            for hand in self.turn_list[self.turn_index].hand:
                if self.check_condition(hand):
                    win_condition = False
                    break

            if win_condition:
                less_point = self.calculation_point(self.me.hand)
                for player in self.turn_list:
                    if less_point >= self.calculation_point(player.hand):
                        less_point = self.calculation_point(player.hand)

                        # self.win_button.text = f"Player {player.number + 1} win !!"
                    self.who = player
                # lms
                if self.who.type == "Human":
                    self.win_button.text = f"You win !!"
                else:
                    self.win_button.text = f"Player {self.who.number + 1} win !!"
                # lms

                self.game_active = False
                self.is_win = True

                self.pause_event_handling()

    def block_turn(self):
        self.turn_index = (self.turn_index + 1) % len(self.turn_list)
        self.current_time = 10
        self.pass_turn()

    def reverse_turn(self):
        temp_player = self.turn_list[self.turn_index]

        self.turn_list.reverse()
        for player in self.turn_list:
            player.turn = self.turn_list.index(player)

        self.turn_index = self.turn_list.index(temp_player)

        ## lms
        for player in self.turn_list:
            if player.type == "Human":
                self.me = player

    def change_color(self):
        if self.is_color_change:
            self.is_color_change = False
            return 0
        self.is_color_change = True

    def draw_card(self, input_deck):
        if len(input_deck) == 0 and input_deck == self.deck:
            return
        if len(self.deck) != 0:
            pop_card = self.deck.pop()
            input_deck.append(pop_card)

    def plus(self, input_deck, count):  # deck : list / first, second : card
        for _ in range(count):
            if len(self.deck) != 0:
                pop_card = self.deck.pop()
                input_deck.append(pop_card)

    def generate_deck(self):
        for color, number in itertools.product(Card.colors, Card.numbers):
            temp_card = Card(color, number, None, False, self.config)
            self.deck.append(temp_card)
            self.card_list.append(temp_card)

            if number != 0:
                temp_card = Card(color, number, None, False, self.config)
                self.deck.append(temp_card)
                self.card_list.append(temp_card)
        # 색깔별로 기술 카드를 담음
        for color, skill in itertools.product(Card.colors, Card.skills):
            for _ in range(2):
                temp_card = Card(color, None, skill, False, self.config)
                self.deck.append(temp_card)
                self.card_list.append(temp_card)

        # all, all4 카드 추가
        for _ in range(4):
            temp_card = Card(None, None, "all4", True, self.config)
            self.deck.append(temp_card)
            self.card_list.append(temp_card)

            temp_card = Card(None, None, "all4", True, self.config)
            self.deck.append(temp_card)
            self.card_list.append(temp_card)

        random.shuffle(self.deck)
        pop_card = self.deck.pop()

        self.remain.append(pop_card)  # 낸 카드 리스트에 pop_card 추가(바닥에 있는 카드)
        self.turn_index = 0
        self.now_card = pop_card  # pop_card(바닥에 있는 카드)가 현재 카드임
        self.now_card_surf = pop_card.image  # 현재 카드 객체화
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 100, self.screen_height / 3)
        )

        self.turn_list = [
            Human(i, [], i) if i == 0 else AI(i, [], i)
            for i in range(self.player_number)
        ]

        for i, component in enumerate(self.info_list):
            component.player = self.turn_list[i]
            if i == len(self.turn_list) - 1:
                break

            for player in self.turn_list:
                if player.type == "Human":
                    self.me = player

    def draw_from_center(self, input_deck):
        # print("draw_from_center")
        self.draw_card(input_deck)
        self.is_get = True
        self.turn_list[self.turn_index].uno = "unactive"

    def player_card_setting(self, player):
        for i in range(7):
            self.draw_card(player.hand)

    def check_condition(self, input_card):
        now = self.now_card

        if input_card.is_wild or now.is_wild:
            return True

        if input_card.color == now.color:  # yellow none 9 / blue none 5
            return True
        elif input_card.number == now.number:
            if input_card.color is not None and input_card.skill is not None:
                if input_card.skill == now.skill:
                    return True
                return False
            return True
        elif input_card.skill == now.skill:  # yellow none 9 / blue none 5
            if input_card.color is not None and input_card.number is not None:
                return False
            return True
        else:
            return False

    def skill_active(self, pop_card):
        next_player = self.turn_index + 1
        if next_player == len(self.turn_list):
            next_player = 0

        if pop_card.skill == "reverse":
            self.skill_active_button.text = "reverse active : turn reversed"
            self.reverse_turn()
        elif pop_card.skill == "block":
            self.skill_active_button.text = f"block active"
            self.info_list[next_player].is_block = True
            pygame.time.set_timer(self.block_timer, 1000)
            self.block_turn()
        elif pop_card.skill == "change" or pop_card.skill == "all":
            self.skill_active_button.text = (
                f"color is changed {self.now_card.color} > {pop_card.color}"
            )
            if self.turn_list[self.turn_index].type == "Human":
                self.change_color()
            elif self.turn_list[self.turn_index].type == "AI":
                self.change_color_ai()
            else:
                pass

        elif pop_card.skill == "plus2":
            self.skill_active_button.text = "plus2 attack active"
            self.plus(self.turn_list[next_player].hand, 2)
        elif pop_card.skill == "plus4" or pop_card.skill == "all4":
            self.skill_active_button.text = "plus4 attack active"
            self.plus(self.turn_list[next_player].hand, 4)
        self.is_skill_active = True

    def change_color_ai(self):
        color_list = {"red": 0, "blue": 0, "green": 0, "yellow": 0}

        if self.turn_list[self.turn_index].hand is not None:
            for hand in self.turn_list[self.turn_index].hand:
                color = hand.color
                if color == None:
                    continue
                if color != None:
                    color_list[color] += 1

        self.now_card.color = max(color_list, key=color_list.get)

        # lsj: 색약모드 change card
        if self.config["color"]["default"] == str(2):
            self.now_card_surf = pygame.image.load(
                f"resources/images/card/normalMode/change/{self.now_card.color}_change.png"
            ).convert_alpha()
        elif self.config["color"]["default"] == str(1):
            self.now_card_surf = pygame.image.load(
                f"resources/images/card/YB/change/{self.now_card.color}_change.png"
            ).convert_alpha()
        elif self.config["color"]["default"] == str(0):
            self.now_card_surf = pygame.image.load(
                f"resources/images/card/RG/change/{self.now_card.color}_change.png"
            ).convert_alpha()

        self.now_card_surf = pygame.transform.scale(self.now_card_surf, (50, 70))
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 100, self.screen_height / 3)
        )

    def pass_turn(self):
        self.turn_index += 1
        if self.turn_index == len(self.turn_list):
            self.turn_index = 0
        self.is_get = False
        self.current_time = 10
        if (
            len(self.turn_list[self.turn_index].hand) == 1
            and self.turn_list[self.turn_index].uno == "active"
        ):
            self.draw_card(self.turn_list[self.turn_index].hand)
            self.turn_list[self.turn_index].uno = "unactive"

        # 일반카드를 냈을 때도 텍스트가 뜨는 코드 > 바꿔야함
        pygame.time.set_timer(self.skill_active_timer, 3000)

    def check_collide(self, pos):
        # print("check_collide")
        for card in self.me.hand:
            if card.rect.collidepoint(pos):
                return True
        if self.deck_rect.collidepoint(pos):
            return True
        elif self.uno_button.rect.collidepoint(pos):
            return True
        else:
            return False

    def press_uno(self):
        print("uno pressed")
        if self.me.uno == "active" and self.is_uno:
            self.me.uno = "success"
            print("uno success")
        else: print("uno failed")

    def calculation_point(self, input_hand):
        point = 0
        for card in input_hand:
            if card.is_wild:
                point += 5
            elif card.skill:
                point += 3
            else:
                point += 1
        return point

    def test_set_all_card_to_red0(self):
        self.deck.clear()
        for _ in range(0, 128):
            self.deck.append(Card("red", None, 0, False, self.config))
        self.now_card = Card("blue", None, 1, False, self.config)
        self.now_card_surf = self.now_card.image

    def pause_event_handling(self):
        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.event_active = False

    # 마우스 이벤트를 처리할 때, 이벤트 처리를 다시 시작하는 함수
    def resume_event_handling(self):
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
        pygame.event.set_allowed(pygame.MOUSEMOTION)
        self.event_active = True

    def edit_name_function(self, screen):
        self.edit_name = True
        while self.edit_name:
            screen.blit(self.alpha_surface, (0, 0))

    def card_move(self, start, end, current_time, duration):
        elapsed_time = current_time - self.moving_start_time
        #print(elapsed_time)
        progress = min(1, elapsed_time / duration)
        eased_progress = (progress - 1) ** 3 + 1

        self.move_rect.centerx = start[0] + (end[0] - start[0]) * eased_progress
        self.move_rect.centery = start[1] + (end[1] - start[1]) * eased_progress
        # print(self.move_rect.center)

    def checkAchieve(self):
        self.achieve.singleWin()
