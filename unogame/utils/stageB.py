import pygame
from models.card import Card
from models.Human import Human
from models.AI import AI
from models.button import Button, Component
from single_play import Game

import itertools
import random
import sys

from pause import PauseClass
import time

# 3명의 컴퓨터 플레이어와 대전 / 첫 카드를 제외하고 모든 카드를 같은 수만큼 플레이어들에게 분배.


class stage_B(Game):
    def __init__(self, screen, player_number, keys, config, soundFX):
        super().__init__(screen, player_number, keys, config, soundFX)

        print("STAGE B")
        # self.deck = []      # 가운데 바닥에 있는 카드 뭉터기들

    def generate_deck(self):
        # 색깔별로 숫자 카드를 담음
        for color, number in itertools.product(Card.colors, Card.numbers):
            self.deck.append(Card(color, number, None, False, self.config))
            if number != 0:
                self.deck.append(Card(color, number, None, False, self.config))

        # 색깔별로 기술 카드를 담음
        for color, skill in itertools.product(Card.colors, Card.skills):
            for _ in range(2):
                self.deck.append(Card(color, None, skill, False, self.config))

        # all, all4 카드 추가
        for _ in range(4):
            self.deck.append(Card(None, None, "all4", True, self.config))
            self.deck.append(Card(None, None, "all", True, self.config))

        random.shuffle(self.deck)
        pop_card = self.deck.pop()

        self.remain.append(pop_card)  # 낸 카드 리스트에 pop_card 추가(바닥에 있는 카드)
        self.turn_index = 0
        self.now_card = pop_card  # pop_card(바닥에 있는 카드)가 현재 카드임
        self.now_card_surf = pop_card.image  # 현재 카드 객체화
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 100, self.screen_height / 3)
        )

        self.turn_list = [Human(i, [], i) if i == 0 else AI(i, [], i) for i in range(4)]

        for player in self.turn_list:
            print(player)

        self.now_turn_list = [
            (
                Game.font.render(f"Player{i + 1}'s turn", False, (64, 64, 64)),
                Game.font.render(f"Player{i + 1}'s turn", False, (64, 64, 64)).get_rect(
                    center=(self.screen_width / 8, self.screen_height / 2)
                ),
            )
            for i in range(self.player_number)
        ]

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

        for i, component in enumerate(self.info_list):
            component.player = self.turn_list[i]
            if i == len(self.turn_list) - 1:
                break
        self.me = self.turn_list[0]

    def player_card_setting(self, player):
        for i in range(31):
            self.draw_card(player.hand)

    def draw_card(self, input_deck):
        if len(self.deck) == 0:
            return
        pop_card = self.deck.pop()
        input_deck.append(pop_card)

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
            # 타이머를 설정하고 타이머가 끝나면 X가 삭제
            pygame.time.set_timer(self.block_timer, 3000)
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
            pass
        elif pop_card.skill == "plus4" or pop_card.skill == "all4":
            pass

        self.is_skill_active = True
        pygame.time.set_timer(self.skill_active_timer, 3000)
