import itertools
import random
import sys

import pygame

from models.button import Button, Component
from models.card import Card
from models.player import Player

from models.button import Button, Component
from pause import Pause


class Game:
    pygame.font.init()
    font = pygame.font.Font("./resources/fonts/Pixeltype.ttf", 36)
    spacing = 2
    card_width = 50
    card_height = 70

    CENTER_X_POS = 625
    CENTER_Y_POS = 325
    change_color_list = []

    def __init__(self, screen, player_number, keys, config):
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.player_number = player_number
        

        self.keys = keys
        self.config = config


        self.game_active = False
        self.is_win = False
        self.is_get = False
        self.run = True
        self.is_color_change = False

        self.alpha_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.alpha_surface.fill((0, 0, 0, 128))
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

        self.now_card = Card("red", None, 0, False)
        self.now_card_surf = pygame.image.load(
            "resources/images/card/normalMode/backcart.png"
        ).convert_alpha()
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 30, self.screen_height / 3)
        )

        self.now_turn_list = []
        self.win_list = []

        self.skip_button = Button(
            self.screen_width / 3 + 150,
            self.screen_height / 3,
            50,
            30,
            (255, 255, 255),
            "SKIP",
            (64, 64, 64),
            30,
            255
        )

        self.uno_button = Button(
            self.screen_width / 3 + 240,
            self.screen_height / 3,
            50,
            30,
            (255, 255, 255),
            "UNO",
            (64, 64, 64),
            30,
            255
        )
        self.retry_surf = Game.font.render("click to retry", False, (64, 64, 64))
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
            255
        )

        # 지금 선택한 카드를 나타내는 변수
        self.now_select = None

        # 로비를 생성하는데 필요한 변수
        self.lobby_background = pygame.Rect(
            self.screen_width - 150, 0, 150, self.screen_height
        )
        self.add_button = Button(
            self.lobby_background.x + 10,
            self.lobby_background.height - 50,
            40,
            20,
            (255, 255, 255),
            "add",
            (64, 64, 64),
            15,
            255
        )
        self.del_button = Button(
            self.lobby_background.x + 60,
            self.lobby_background.height - 50,
            40,
            20,
            (255, 255, 255),
            "delete",
            (64, 64, 64),
            15,
            255
        )
        self.info_list = []
        for i in range(0, 5):
            self.info_list.append(
                Component(
                    self.lobby_background.x,
                    self.lobby_background.y + 100 * i,
                    150,
                    90,
                    (255, 255, 255),
                    f"PLAYER {i + 2}",
                    (64, 64, 64),
                    20,
                    None,
                )
            )
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
                ["red", "green", "blue", "yellow"]
        ):
            surf = pygame.Surface((50, 50))
            surf.fill(color_string)
            rect = surf.get_rect(center=pos)
            self.change_color_list.append([surf, rect, color, color_string])

        # Timer 변수 세팅
        self.turn_timer = pygame.USEREVENT + 1
        self.current_time = 10000
        pygame.time.set_timer(self.turn_timer, 1000)
        self.time_button = Button(self.screen_width // 8 + 40, self.screen_height // 2 + 15, 80,30,(255,255,255),f"TIME : {self.current_time}", (64,64,64,), 30, 255)

        self.uno_timer = pygame.USEREVENT + 2
        self.is_uno = True
    def start_single_play(self):
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        clock = pygame.time.Clock()

        while self.run:
            screen.fill((50, 200, 50))

            # event loop

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        font = pygame.font.SysFont(None, 48)
                        pause = Pause(screen, font, self.config, self.keys)
                        pause.run()                                                 # Todo: 일시정지 후 게임 내부 크기 조절 기능 필요..

                    if event.key == pygame.K_q:
                        self.turn_list[self.turn_index].hand.clear()

                #Timer 재설정 하는 event loop
                if event.type == self.turn_timer and self.game_active:
                    if self.current_time == 0:
                        self.current_time = 10
                        if not self.is_get:
                            self.draw_from_center(self.turn_list[self.turn_index].hand)
                        self.pass_turn()
                        break
                    self.current_time -= 1

                # 게임 전 카드 덱과 손 패를 세팅하는 부분 > 따로빼서 함수로 refactor하기
                elif (
                        event.type == pygame.MOUSEBUTTONUP
                        and self.start_button.rect.collidepoint(event.pos)
                ):
                    if not self.game_active:
                        self.game_active = True
                        self.is_win = False
                        self.generate_deck()
                        for player in self.turn_list:
                            self.player_card_setting(player.hand)
                            self.turn_index += 1
                        self.turn_index = 0
                        for _ in range(0, 5):
                            self.me.hand.pop()
                        for _ in range(0, 6):
                            self.turn_list[self.turn_index + 1].hand.pop()
                        for _ in range(0, 6):
                            self.turn_list[self.turn_index + 2].hand.pop()
                        # self.me.update_hand(screen)
                else:
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_active:
                    if self.add_button.is_clicked(event.pos):
                        if self.player_number <= 5:
                            self.player_number += 1
                        print(f"add / player_number : {self.player_number}")
                    if self.del_button.is_clicked(event.pos):
                        if self.player_number > 2:
                            self.player_number -= 1
                        print(f"delete / player_number : {self.player_number}")
                
                # 매 턴 UNO를 할 수 있는지 없는지 체크하는 부분
                for player in self.turn_list:
                    if len(player.hand) == 1 and not player.uno and self.is_uno:
                        print("uno timer start")

                        pygame.time.set_timer(self.uno_timer, 5000, 1)
                        player.uno = True
                        break
                if event.type == self.uno_timer and self.game_active:
                    self.is_uno = False
                    for player in self.turn_list:
                        print("turn off player.uno")
                        player.uno = False

                # 카드에 마우스커서를 올렸을 때 애니메이션 > 리팩토링
                if event.type == pygame.MOUSEMOTION and self.game_active and not self.is_color_change and self.me.turn == self.turn_index:
                    for card in self.me.hand:
                        if card.rect.collidepoint(event.pos):
                            self.now_select = card
                    for rect in [self.deck_rect, self.skip_button.rect, self.uno_button.rect]:
                        if rect.collidepoint(event.pos):
                            self.now_select = rect
                # 키보드 입력을 정의
                if (
                        event.type == pygame.KEYDOWN
                        and self.game_active
                        and not self.is_color_change
                        and self.me.turn == self.turn_index
                ):
                    if event.key == self.keys["RIGHT"]:
                        print("key pressed")
                        if self.now_select is None:
                            self.now_select = self.me.hand[0]
                        elif self.now_select == self.deck_rect:
                            print("test")
                            self.now_select = self.skip_button
                        elif self.now_select == self.skip_button:
                            self.now_select = self.uno_button
                        elif self.now_select == self.uno_button:
                            self.now_select = self.deck_rect

                        elif (
                                len(self.me.hand) == self.me.hand.index(self.now_select) + 1
                        ):
                            self.now_select = self.me.hand[0]
                        else:
                            self.now_select = self.me.hand[
                                self.me.hand.index(self.now_select) + 1
                                ]

                    elif event.key == self.keys["LEFT"]:
                        if self.now_select is None:
                            self.now_select = self.me.hand[0]
                        elif self.now_select == self.skip_button:
                            self.now_select = self.deck_rect

                        elif self.now_select == self.deck_rect:
                            self.now_select = self.uno_button

                        elif self.now_select == self.uno_button:
                            self.now_select = self.skip_button

                        elif (
                                self.me.hand.index(self.now_select) == 0
                        ):
                            self.now_select = self.me.hand[len(self.me.hand) - 1]
                        else:
                            self.now_select = self.me.hand[
                                self.me.hand.index(self.now_select) - 1
                                ]

                    elif event.key == self.keys["UP"]:
                        if self.now_select is None:
                            self.now_select = self.me.hand[0]
                        elif self.now_select in self.me.hand:
                            self.now_select = self.deck_rect
                        elif self.now_select in [self.deck_rect, self.skip_button, self.uno_button]:
                            self.now_select = self.me.hand[0]
                    elif event.key == self.keys["DOWN"]:
                        if self.now_select is None:
                            self.now_select = self.me.hand[0]
                        elif self.now_select in self.me.hand:
                            self.now_select = self.deck_rect
                        elif self.now_select in [self.deck_rect, self.skip_button, self.uno_button]:
                            self.now_select = self.me.hand[0]


                # self.is_color_change에 따라 색깔을 바꿔주는 옵션
                if self.is_color_change and event.type == pygame.MOUSEBUTTONDOWN:

                    for color_list in self.change_color_list:
                        if color_list[1].collidepoint(event.pos):
                            self.now_card_surf = pygame.image.load(
                                f"resources/images/card/normalMode/change/{color_list[3]}_change.png"
                            ).convert_alpha()
                            self.now_card_surf = pygame.transform.scale(
                                self.now_card_surf, (50, 70)
                            )
                            self.now_card.color = color_list[3]
                            self.is_color_change = False
                            self.pass_turn()
                
                # 클릭 및 엔터 이벤트
                if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN) and self.game_active and not self.is_color_change:
                    pos = pygame.mouse.get_pos()
                    key = None
                    if event.type == pygame.KEYDOWN:
                        key = event.key
                    # 1. 낼 수 있는 카드를 낸다
                    if key == self.keys["RETURN"] or self.check_collide(pos):
                        if self.now_select in self.me.hand and self.me.turn == self.turn_index:
                            if self.check_condition(self.now_select):
                                pop_card = self.now_select
                                self.turn_list[self.turn_index].hand.remove(pop_card)
                                self.now_select = None
                                self.remain.append(pop_card)
                                self.now_card = pop_card
                                self.now_card_surf = pop_card.image
                                if pop_card.skill is not None:
                                    self.skill_active(pop_card.skill)
                                if pop_card.skill not in ["change", "block", "all"]:
                                    self.pass_turn()

                    # 2. 가운데에서 카드를 가져온다 > 낼 수 있는 카드가 있다면 낸다
                    if (key == self.keys["RETURN"] or self.check_collide(pos)) and self.now_select == self.deck_rect and not self.is_get:
                        self.draw_from_center(self.turn_list[self.turn_index].hand)
                    # 3. 낼 수 있는 카드가 없거나, 가운데에서 이미 카드를 가져온 상태면 PASS를 눌러 턴을 넘김
                    if (key == self.keys["RETURN"] or self.check_collide(pos)) and self.now_select == self.skip_button and self.is_get:
                        self.pass_turn()
                    # 4. 컴퓨터의 알고리즘 수행
                    # 5. 카드가 1장만 남았을 경우 UNO 버튼을 눌러야 한다.
                    if (key == self.keys["RETURN"] or self.check_collide(pos)) and self.now_select == self.uno_button and self.is_uno:
                        print("if enter")
                        self.press_uno()

                    # 6. 누군가의 덱이 모두 사라지면 그 사람의 승리 > 승리 화면 전환 > 메인 화면 전환
                    for player in self.turn_list:
                        if len(player.hand) == 0:
                            self.game_active = False
                            self.is_win = True
                    # 7. 뽑을 수 있는 카드가 없고, 모든 플레이어가 현재 낼 수 있는 카드가 없으면 카드가 가장 적은 사람이 승리
                    if len(self.deck) == 0:
                        win_condition = True
                        for player in self.turn_list:
                            for card in player.hand:
                                if card:
                                    win_condition = False

                        winner = self.me
                        if win_condition:
                            less_point = self.calculation_point(self.me.hand)
                            for player in self.turn_list:
                                if less_point >= self.calculation_point(player.hand):
                                    less_point = self.calculation_point(player.hand)
                                    winner = player
                                    self.win_button.text = f"Player {winner.number} win !!"


            # event loop 종료 *****************************

            if self.game_active:
                if len(self.deck):
                    screen.blit(self.deck_surf, self.deck_rect)
                screen.blit(self.now_card_surf, self.now_card_rect)

                # 누구의 턴인지 보여주는 부분
                screen.blit(
                    self.now_turn_list[self.turn_index][0],
                    self.now_turn_list[self.turn_index][1],
                )

                # 손패를 그려주는 부분
                self.me.draw_hand(screen)

                if self.is_color_change:
                    screen.blit(self.alpha_surface, (0, 0))
                    for color_list in self.change_color_list:
                        screen.blit(color_list[0], color_list[1])

                self.uno_button.draw(screen)
                if self.is_get:
                    self.skip_button.surface.fill((255, 255, 255))
                    self.skip_button.draw(screen)
                else:
                    self.skip_button.surface.fill((120, 120, 120))
                    self.skip_button.draw(screen)
                if self.now_select and self.me.turn == self.turn_index:
                    pygame.draw.rect(screen, (0, 0, 0), self.now_select, 5)
                pygame.draw.rect(screen, (20, 20, 20), self.lobby_background)
                for i in range(0, self.player_number - 1):
                    self.info_list[i].draw(screen)

                self.time_button.text = f"TIME : {self.current_time}"
                self.time_button.draw(screen)

            else:
                screen.fill("green")
                # 게임이 종료되었을 때 덱 초기화
                for player in self.turn_list:
                    player.hand.clear()
                self.deck.clear()
                self.remain.clear()

                pygame.draw.rect(screen, (20, 20, 20), self.lobby_background)
                self.add_button.draw(screen)
                self.del_button.draw(screen)
                for i in range(0, self.player_number - 1):
                    self.info_list[i].draw(screen)
                self.start_button.draw(screen)

                for i in range(0, self.player_number - 1):
                    self.info_list[i].draw(screen)

                if self.is_win:
                    screen.blit(
                        self.win_list[self.turn_index][0],
                        self.win_list[self.turn_index][1],
                    )
                    screen.blit(self.retry_surf, self.retry_rect)
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)

    def block_turn(self):
        print(f"before block : {self.turn_index}")
        self.turn_index = (self.turn_index + 2) % len(self.turn_list)
        print(f"after block : {self.turn_index}")

    def reverse_turn(self):
        print(f"before reverse : {self.turn_index}")
        temp_player = self.turn_list[self.turn_index]
        self.turn_list.reverse()
        for player in self.turn_list:
            player.turn = self.turn_list.index(player)
        self.turn_index = self.turn_list.index(temp_player)
        self.now_turn_list.reverse()
        print(f"after reverse : {self.turn_index}")

    def change_color(self):
        if self.is_color_change:
            self.is_color_change = False
            return 0
        self.is_color_change = True

    def draw_card(self, input_deck):
        pop_card = self.deck.pop()
        input_deck.append(pop_card)

    def plus(
            self, input_deck, next_player, count
    ):  # deck : list / first, second : card
        for _ in range(count):
            pop_card = self.deck.pop()
            input_deck.append(pop_card)

    # def hand_update(self, input_deck):
    #     for i, card in enumerate(input_deck):
    #         card.rect.x = i * (Game.card_width + Game.spacing) + self.screen_width // 6 - len(input_deck) * (
    #                 Game.card_width + Game.spacing) // 2
    #         card.rect.y = card.initial_y

    def generate_deck(self):
        for color, number in itertools.product(Card.colors, Card.numbers):
            self.deck.append(Card(color, number, None, False))
            if number != 0:
                self.deck.append(Card(color, number, None, False))

        # 색깔별로 기술 카드를 담음
        for color, skill in itertools.product(Card.colors, Card.skills):
            for _ in range(2):
                self.deck.append(Card(color, None, skill, False))

        # all, all4 카드 추가
        for _ in range(4):
            self.deck.append(Card(None, None, "all4", True))
            self.deck.append(Card(None, None, "all", True))

        random.shuffle(self.deck)
        pop_card = self.deck.pop()
        self.remain.append(pop_card)
        self.turn_index = 0
        self.now_card = pop_card
        self.now_card_surf = pop_card.image
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 100, self.screen_height / 3)
        )

        self.turn_list = [Player(i, [], i) for i in range(self.player_number)]
        self.now_turn_list = [
            (
                Game.font.render(f"Player{i + 1}'s turn", False, (64, 64, 64)),
                Game.font.render(f"Player{i + 1}'s turn", False, (64, 64, 64)).get_rect(
                    center=(self.screen_width / 8, self.screen_height / 2)
                ),
            )
            for i in range(self.player_number)
        ]
        self.win_list = [
            (
                Game.font.render(f"Player{i + 1} win!", False, (64, 64, 64)),
                Game.font.render(f"Player{i + 1} win!", False, (64, 64, 64)).get_rect(
                    center=(self.screen_width / 2, self.screen_height / 2)
                ),
            )
            for i in range(self.player_number)
        ]
        self.win_button = Button(self.screen_width / 2 - 50, self.screen_height / 2 - 20, 100, 40, (255,255,255),"Player 1 win !!", (64,64,64), 30, 0)

        for i, component in enumerate(self.info_list):
            component.player = self.turn_list[i + 1]
            if i == len(self.turn_list) - 2:
                break
        self.me = self.turn_list[0]

    # self.turn_index를 더 깔끔하게 다루기
    def draw_from_center(self, input_deck):
        self.draw_card(input_deck)
        self.is_get = True

        # # layer를 다시 수정해주는 작업
        # for i, card in enumerate(input_deck.sprites()):
        #     # input_deck.change_layer(card, len(input_deck.sprites()) - i - 1)
        #     input_deck.change_layer(card, i)

    def player_card_setting(self, input_deck):
        if not len(input_deck):  # 초기에 7장 뽑기
            for i in range(7):
                self.draw_card(input_deck)

    def check_condition(self, input_card):
        # input 카드가 현재 맨 위에 있는 카드에 낼 수 있는 카드인지 확인하는 함수
        now = self.now_card
        print(f"input.color : {input_card.color} / now.color : {now.color}")
        print(f"input.skill : {input_card.skill} / now.skill : {now.skill}")
        print(f"input.number : {input_card.number} / now.number : {now.number}")
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

    def skill_active(self, skill):
        next_player = self.turn_index + 1
        if next_player == len(self.turn_list):
            next_player = 0

        if skill == "reverse":
            self.reverse_turn()
        elif skill == "block":
            self.block_turn()
        elif skill == "change" or skill == "all":
            self.change_color()
        elif skill == "plus2":
            self.plus(self.turn_list[next_player].hand, next_player, 2)
        elif skill == "plus4" or skill == "all4":
            self.plus(self.turn_list[next_player].hand, next_player, 4)

    def pass_turn(self):
        print("turn is passed")
        self.turn_index += 1
        if self.turn_index == len(self.turn_list):
            self.turn_index = 0
        self.is_get = False
        self.current_time = 10
        self.is_uno = True
    def check_collide(self, pos):
        for card in self.me.hand:
            if card.rect.collidepoint(pos):
                return True
        if self.deck_rect.collidepoint(pos):
            return True
        elif self.skip_button.rect.collidepoint(pos):
            return True
        elif self.uno_button.rect.collidepoint(pos):
            return True
        else:
            return False

    def press_uno(self):
        print("calling")
        mistake = True
        for player in self.turn_list:
            if len(player.hand) == 1:
                print(len(player.hand))
                mistake = False
                break

        if mistake:
            self.draw_card(self.turn_list[self.turn_index])
        else:
            for player in self.turn_list:
                if len(player.hand) == 1 and player.turn != self.turn_index and player.uno:
                    self.draw_card(player.hand)
                    player.uno = False
        self.is_uno = False
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
