import itertools
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

# 시작 시 카드 세팅
center_card_list = []  # 카드를 담을 리스트
colors = ['Red', 'Blue', 'Green', 'Yellow']
numbers = list(range(0, 10))
skills = ['Reverse', 'Skip', 'Draw Two']
wilds = ['Wild', 'Wild Draw Four']

# 카드 생성과 분배
# 카드 덱을 만들고, 플레이어들에게 무작위로 카드를 분배합니다.

# 0~9 숫자 카드를 색깔별로 담는 반복문 / product() : color와 nubmber로 조합할 수 있는 모든 경우의 수를 표현
for color, number in itertools.product(colors, numbers):
    center_card_list.append(card(color, number, "None"))
    if number != 0:
        center_card_list.append(card(color, number, "None"))

# 색깔별로 기술 카드를 담음
for color, skill in itertools.product(colors, skills):
    for _ in range(2):
        center_card_list.append(card(color, None, skill))

# Wild, Wild Draw Four 카드를 담음
for wild in wilds:
    for _ in range(4):
        center_card_list.append(card(None, None, wild))

now_color = "none"  # 현재 내야하는 색깔
game_active = True

font = pygame.font.Font("../assets/font/Pixeltype.ttf", 36)
test_txt = font.render(center_card_list[3].skill, False, (0, 0, 0))
test_rect = test_txt.get_rect(center=(400, 300))


# 현재 카드 표시
# 플레이어가 놓은 카드 중 가장 최근에 놓은 카드를 표시합니다.


# 카드 놓기
# 플레이어는 자신의 카드 중 현재 카드와 색상 또는 숫자가 일치하는 카드를 놓을 수 있습니다.


# 특수 카드 처리
# 특수 카드인 Skip, Reverse, Draw Two, Wild, Wild Draw Four 등에 대한 처리를 구현합니다.


# 게임 종료 조건 검사
# 게임이 종료되는 조건인 플레이어의 카드가 모두 소진되거나, 한 명 이상의 플레이어가 이길 때를 검사합니다.