import random

import pygame
import sys
from random import randint


class card:
    def __init__(self, color, number, skill):
        super().__init__()
        self.color = color
        self.number = number
        self.skill = skill
        card_state = False  # 앞뒷면을 나타내는 변수, True = 앞면 / False = 뒷면

        # 추후 카드 이미지 추가 시 이미지 불러오는 작업 추가

    def draw_two(self, deck, first, second):  # deck : list / first, second : card
        deck.append(first).append(second)
        return deck

    def skip(self):
        # 싱글플레이의 경우 turn % 2 으로 짝수, 홀수로 나누어 턴 계산
        global turn_index
        turn_index = (turn_index + 2) % len(turn_list)

    def reverse_turn(self):
        global turn_list, turn_index
        temp_player = turn_list[turn_index]
        turn_list.reverse()
        turn_index = turn_list[temp_player].index()

    def wild(self, selected_color):
        global now_color
        now_color = selected_color

    def wild_draw_four(self, deck, first, second, third, fourth):
        deck.append(first).append(second).append(third).append(fourth)
        return deck


def setting(num_players):
    global turn_index

    # 인원 수 만큼 차례 추가
    for i in range(0, num_players):
        turn_list.append(i)
    # 시작 할 사람 결정
    turn_index = random.randint(0, 4)
    return turn_list


def draw_card(deck):
    global center_card_list
    deck.append(center_card_list.pop())


def start_single_play(screen):
    clock = pygame.time.Clock()
    while True:
        screen.fill('Green')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if game_active:
            screen.blit(test_txt, test_rect)
            pass
        else:
            pass
        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(60)


pygame.init()
# 싱글 플레이에 필요한 변수 선언
turn_list = []  # 차례의 순서를 나타내는 list
turn_index = 0  # 누구의 차례인지 알려주는 변수
player_card_list = []  # Player 카드 목록
computer_card_list = []  # Computer 카드 목록
center_card_list = []
now_color = "none"  # 현재 내야하는 색깔
game_active = True

font = pygame.font.Font("../assets/font/Pixeltype.ttf", 36)
test_txt = font.render("Hello World", False, (0,0,0))
test_rect= test_txt.get_rect(center = (400,300))
