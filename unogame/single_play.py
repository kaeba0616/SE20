import itertools
import random

import pygame
import sys

import io

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


class Card(pygame.sprite.Sprite):
    def __init__(self, color, number, skill):
        super().__init__()
        self.color = color
        self.number = number
        self.skill = skill  # block, plus2, reverse, change / change, plus4
        file_path = ""
        if number is not None:
            file_path = f"resources/images/card/normalMode/{number}/{self.color}_{number}.svg"
        elif color is not None and number is None and skill is not None:
            file_path = f"resources/images/card/normalMode/{skill}/{self.color}_{skill}.svg"
        elif color is None:
            if skill == "all":
                file_path = f"resources/images/card/normalMode/change/all.svg"
            elif skill == "all4":
                file_path = f"resources/images/card/normalMode/plus4/all4.svg"
        else:
            print("path error")

        image_surface = pygame.image.load('resources/images/jump.png')
        image_surface = pygame.transform.rotozoom(image_surface, 0, 0.5)
        self.image = image_surface.convert_alpha()
        self.rect = self.image.get_rect()

        self.card_state = False  # 앞뒷면을 나타내는 변수, True = 앞면 / False = 뒷면

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
    run = True
    game_active = False
    while run:
        screen.fill('Green')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("hi")
                    run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    game_active = True
                    # buttondown이 계속 인식되어 카드가 바로 가져가짐
            else:
                pass


            if event.type == pygame.MOUSEBUTTONDOWN:
                if deck_rect.collidepoint(event.pos):
                    print("collide")
                    if not len(player_deck):
                        print("empty")

                        for _ in range(7):
                            pop_card = deck.sprites().pop()
                            deck.remove(pop_card)
                            player_deck.add(pop_card)
                            pop_card.rect.y = 450  # 200 - rect_height // 2

                        for i, card in enumerate(player_deck.sprites()):
                            card.rect.x = i * (card_width + spacing) + 400 - len(player_deck) * (card_width + spacing) // 2
                    else: # if not len(player_deck)
                        pop_card = deck.sprites().pop()
                        deck.remove(pop_card)
                        player_deck.add(pop_card)
                        pop_card.rect.y = 450  # 200 - rect_height // 2

                        for i, card in enumerate(player_deck.sprites()):
                            card.rect.x = i * (card_width + spacing) + 400 - len(player_deck) * (card_width + spacing) // 2

            else:
                pass

        if game_active:
            screen.blit(deck_surf, deck_rect)
            screen.blit(now_card_surf, now_card_rect)
            player_deck.draw(screen)

        else:
            screen.blit(text_surf, text_rect)
            pass
        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(60)


pygame.init()
screen = pygame.display.set_mode((800, 600))
# 싱글 플레이에 필요한 변수 선언
turn_list = []  # 차례의 순서를 나타내는 list
turn_index = 0  # 누구의 차례인지 알려주는 변수
player_deck = pygame.sprite.Group()  # Player 카드 목록
computer_deck = pygame.sprite.Group()  # Computer 카드 목록

# 시작 시 카드 세팅
deck = pygame.sprite.Group()
colors = ['red', 'blue', 'green', 'yellow']
numbers = list(range(0, 10))
skills = ['reverse', 'block', 'plus2', 'change', 'plus4']

font = pygame.font.Font("../assets/font/Pixeltype.ttf", 36)
text_surf = font.render("click here to play", False, (64, 64, 64))
text_rect = text_surf.get_rect(center=(400, 300))

deck_surf = pygame.image.load("resources/images/output.png").convert_alpha()
deck_surf = pygame.transform.rotozoom(deck_surf, 0, 0.5)
deck_rect = deck_surf.get_rect(center=(400-(deck_surf.get_width() // 2), 300))
# 현재 어떤카드가 뒤집혀져있는지 나타내는 변수 / 추후 수정해야 함
# 1. 낸 카드로 이미지가 바뀌게
# 2.
now_card_surf = pygame.image.load("resources/images/output.png").convert_alpha()
now_card_surf.fill("pink")
now_card_surf = pygame.transform.rotozoom(now_card_surf, 0, 0.5)
now_card_rect = now_card_surf.get_rect(center=(400 + (now_card_surf.get_width() // 2), 300))

_color = "none"  # 현재 내야하는 색깔

# 카드 생성과 분배
# 카드 덱을 만들고, 플레이어들에게 무작위로 카드를 분배

# 0~9 숫자 카드를 색깔별로 담는 반복문 / product() : color와 nubmber로 조합할 수 있는 모든 경우의 수를 표현
for color, number in itertools.product(colors, numbers):
    deck.add(Card(color, number, None))
    if number != 0:
        deck.add(Card(color, number, None))

# 색깔별로 기술 카드를 담음
for color, skill in itertools.product(colors, skills):
    for _ in range(2):
        deck.add(Card(color, None, skill))

# all, all4 카드 추가
for _ in range(4):
    deck.add(Card(None, None, "all4"))
    deck.add(Card(None, None, "all"))

# 현재 카드 표시
# 플레이어가 놓은 카드 중 가장 최근에 놓은 카드를 표시
spacing = -20
card_width = 82
card_height = 128

# 카드 놓기
# 플레이어는 자신의 카드 중 현재 카드와 색상 또는 숫자가 일치하는 카드를 놓을 수 있음


# 특수 카드 처리
# 특수 카드인 Skip, Reverse, Draw Two, Wild, Wild Draw Four 등에 대한 처리를 구현합니다.


# 게임 종료 조건 검사
# 게임이 종료되는 조건인 플레이어의 카드가 모두 소진되거나, 한 명 이상의 플레이어가 이길 때를 검사합니다.
