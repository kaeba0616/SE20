import itertools
import random

import pygame
import sys
from operator import attrgetter


class Card(pygame.sprite.Sprite):
    def __init__(self, color, number, skill, wild):
        super().__init__()
        self.color = color
        self.number = number
        self.skill = skill  # block, plus2, reverse, change / change, plus4
        self.is_moving = False
        self.is_wild = wild
        self.file_path = ""
        if number is not None:
            file_path = f"resources/images/card/normalMode/{number}/{self.color}_{number}.png"
        elif color is not None and number is None and skill is not None:
            file_path = f"resources/images/card/normalMode/{skill}/{self.color}_{skill}.png"
        elif color is None:
            if skill == "all":
                file_path = f"resources/images/card/normalMode/change/all_change.png"
            elif skill == "all4":
                file_path = f"resources/images/card/normalMode/plus4/all_plus4.png"
        else:
            print("path error")

        image_surface = pygame.image.load(file_path).convert_alpha()
        # image_surface = pygame.transform.rotozoom(image_surface, 0, 0.5)
        image_surface = pygame.transform.scale(image_surface, (70, 100))
        self.image = image_surface
        self.rect = image_surface.get_rect(center=(0, 0))
        # print(f"width : {self.rect.width} / height : {self.rect.height}")
        self.initial_y = self.rect.y

        self.card_state = False  # 앞뒷면을 나타내는 변수, True = 앞면 / False = 뒷면




def draw_two():  # deck : list / first, second : card

    return deck


def block_turn():
    global turn_list, turn_index
    turn_index = (turn_index + 2) % len(turn_list)


def reverse_turn():
    global turn_list, turn_index
    temp_player = turn_list[turn_index]
    turn_list.reverse()
    turn_index = turn_list[temp_player].index()


def change_color():
    global screen, deck, remain, is_color_change, game_active, now_card_surf, change_color_list
    if is_color_change:
        is_color_change = False
        return 0
    is_color_change = True
    change_color_list = [[red_surf, red_rect, "red"], [green_surf, green_rect, 'green'], [blue_surf, blue_rect, 'blue'],
                         [yellow_surf, yellow_rect, 'yellow']]

    return 0


def wild_draw_four():
    return 0


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


def hand_update(input_deck):
    for i, card in enumerate(input_deck.sprites()):
        card.rect.x = i * (card_width + spacing) + 400 - len(input_deck) * (
                card_width + spacing) // 2
        card.rect.y = card.initial_y


def generate_deck():
    global deck, remain, now_card_surf, now_card_rect
    count = 0
    for color, number in itertools.product(colors, numbers):
        deck.add(Card(color, number, None, False))
        count += 1
        if number != 0:
            deck.add(Card(color, number, None, False))
            count += 1

    # 색깔별로 기술 카드를 담음
    for color, skill in itertools.product(colors, skills):
        for _ in range(2):
            deck.add(Card(color, None, skill, False))
            count += 1

    # all, all4 카드 추가
    for _ in range(4):
        deck.add(Card(None, None, "all4", True))
        count += 1

        deck.add(Card(None, None, "all", True))
        count += 1
    print(f"count : {count}")
    temp_list = deck.sprites()
    random.shuffle(temp_list)
    pop_card = temp_list.pop()
    print(f"{pop_card.color} / {pop_card.number} / {pop_card.skill}")
    deck.remove(pop_card)
    remain.add(pop_card)
    now_card_surf = pop_card.image
    now_card_rect = now_card_surf.get_rect(center=(400 + (now_card_surf.get_width() // 2), 300))


def draw_from_center(input_deck):
    global deck, turn_index
    pop_card = deck.sprites().pop()
    deck.remove(pop_card)
    input_deck.add(pop_card, layer=0)

    if turn_index == 0:
        pop_card.rect.y = 450  # 200 - rect_height // 2
        pop_card.initial_y = 450
    elif turn_index == 1:
        pop_card.rect.y = 50  # 200 - rect_height // 2
        pop_card.initial_y = 50
    else:
        turn_index = 0

    hand_update(input_deck)

    turn_index += 1

    # layer를 다시 수정해주는 작업
    for i, card in enumerate(input_deck.sprites()):
        # input_deck.change_layer(card, len(input_deck.sprites()) - i - 1)
        input_deck.change_layer(card, i)


def player_card_setting(input_deck):
    global deck
    print(len(deck.sprites()))
    if not len(input_deck):  # 초기에 7장 뽑기
        for i in range(7):

            temp_list = deck.sprites()
            random.shuffle(temp_list)
            pop_card = temp_list.pop()
            deck.remove(pop_card)
            input_deck.add(pop_card, layer=i)
            if turn_index == 0:
                pop_card.rect.y = 450  # 200 - rect_height // 2
                pop_card.initial_y = 450
            elif turn_index == 1:
                pop_card.rect.y = 50  # 200 - rect_height // 2
                pop_card.initial_y = 50

    hand_update(input_deck)

    # 레이어 재정렬 - add()의 layer가 차례대로 쌓이기 때문에 역순으로 다시 재정렬 해줘야함
    for i, card in enumerate(input_deck.sprites()):
        # input_deck.change_layer(card, len(input_deck.sprites()) - i - 1)
        input_deck.change_layer(card, i)


def check_turn():
    global turn_index, turn_list, PLAYER_NUMBER
    turn_index += 1
    print(len(turn_list))
    if turn_index == 2:
        print("clear turn_index")
        turn_index = 0
    print(f"after check_turn(): {turn_index}")


def check_condition(input_card):
    # input 카드가 현재 맨 위에 있는 카드에 낼 수 있는 카드인지 확인하는 함수
    global remain
    now = remain.sprites()[-1]
    print(f"input.color : {input_card.color} / now.color : {now.color}")
    print(f"input.skill : {input_card.skill} / now.skill : {now.skill}")
    print(f"input.number : {input_card.number} / now.number : {now.number}")
    if input_card.is_wild or now.is_wild:
        return True

    if input_card.color == now.color: # yellow none 9 / blue none 5
        return True
    elif input_card.number == now.number:
        if input_card.color is not None and input_card.skill is not None:
            if input_card.skill == now.skill:
                return True
            return False
        return True
    elif input_card.skill == now.skill: # yellow none 9 / blue none 5
        if input_card.color is not None and input_card.number is not None:
            return False
        return True
    else:
        return False


def skill_active(skill):
    global turn_list, turn_index
    next_player = turn_index + 1
    if next_player == len(turn_list):
        next_player = 0

    if skill == "reverse":
        reverse_turn()
    elif skill == "block":
        block_turn()
    elif skill == "change":
        change_color()
    elif skill == "plus2":
        for _ in range(2):
            draw_from_center(turn_list[next_player])
    elif skill == "plus4":
        for _ in range(4):
            draw_from_center(turn_list[next_player])



def start_single_play():
    global turn_list, turn_index, deck, now_card_surf, now_card_rect, is_color_change, game_active
    run = True


    while run:
        screen.fill((50,200,50))

        # event loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    change_color()
                    print("hi")

            # 게임 전 카드 덱과 손 패를 세팅하는 부분 > 따로빼서 함수로 refactor하기
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_active:
                    game_active = True
                    generate_deck()
                    for player_deck in turn_list:
                        player_card_setting(player_deck)
                        turn_index += 1
                    turn_index = 0

            else:
                pass
            # 카드에 마우스커서를 올렸을 때 애니메이션 > 리팩토링
            if event.type == pygame.MOUSEMOTION and game_active:
                for card in turn_list[turn_index].sprites():
                    if card.rect.collidepoint(event.pos):
                        # print(turn_list[turn_index].get_sprites_at(event.pos)[0].rect.left)
                        # print("collide")
                        if card.initial_y == card.rect.y and not card.is_moving:
                            card.rect.y -= 10
                            card.is_moving = True

                    elif not card.rect.collidepoint(event.pos):
                        if card.rect.bottom < event.pos[1] <= card.rect.bottom + 10 and card.rect.left < event.pos[
                            0] <= card.rect.left + card.rect.width:
                            pass
                        else:
                            if card.rect.y != card.initial_y and card.is_moving:
                                card.rect.y += 10
                                card.is_moving = False

            # 멀티 플레이 시 turn_index를 가져와야함
            if event.type == pygame.MOUSEBUTTONDOWN and game_active and turn_index == 0:
                clicked_card = None
                for card in turn_list[turn_index].sprites():
                    if card.rect.collidepoint(event.pos):
                        clicked_card = card
                        break
                if clicked_card is not None:
                    print(turn_list[turn_index].get_layer_of_sprite(card))
                print("button down")

            # is_color_change에 따라 색깔을 바꿔주는 옵션
            if is_color_change and event.type== pygame.MOUSEBUTTONDOWN:
                for color_list in change_color_list:
                    if color_list[1].collidepoint(event.pos):
                        print("color chagne active")
                        now_card_surf = pygame.image.load(
                            f"resources/images/card/normalMode/change/{color_list[2]}_change.png").convert_alpha()
                        now_card_surf = pygame.transform.scale(now_card_surf, (70, 100))
                        is_color_change = False

            # turn_index를 이용해 게임 flow control
            # 플레이어 턴에 플레이어가 할 수 있는 행동
            # 1. 낼 수 있는 카드를 낸다
            if event.type == pygame.MOUSEBUTTONDOWN and game_active:
                for card in turn_list[turn_index].sprites():
                    if card.rect.collidepoint(event.pos):
                        if check_condition(card):
                            # 카드 내기
                            print("카드 냈음")
                            pop_card = card
                            turn_list[turn_index].remove(card)
                            remain.add(pop_card)
                            now_card_surf = pop_card.image
                            hand_update(turn_list[turn_index])
                            check_turn()
            # 1-1. 낸 카드의 능력이 있다면 해당 카드의 능력을 수행해야 한다
                            if card.skill is not None:
                                skill_active(card.skill)
            # 2. 가운데에서 카드를 가져온다 > 낼 수 있는 카드가 있다면 낸다
            # 3. 컴퓨터의 알고리즘 수행
            # 4. 카드가 1장만 남았을 경우 UNO 버튼을 눌러야 한다.
            # 5. 누군가의 덱이 모두 사라지면 그 사람의 승리 > 승리 화면 전환 > 메인 화면 전환

        # event loop 종료 *****************************

        if game_active:
            screen.blit(deck_surf, deck_rect)
            screen.blit(now_card_surf, now_card_rect)

            # 누구의 턴인지 보여주는 부분
            if turn_index == 0:
                screen.blit(now_turn_surf, now_turn_rect)
            else:
                screen.blit(now_turn_surf2, now_turn_rect)

            # 손패를 그려주는 부분
            for player_deck in turn_list:
                # sorted_sprites = sorted(player_deck.sprites(), key=lambda s: player_deck.get_layer_of_sprite(s),
                #                         reverse=True)
                # for sprite in sorted_sprites:
                #     screen.blit(sprite.image, sprite.rect)
                player_deck.draw(screen)

            if is_color_change:
                screen.blit(alpha_surface, (0, 0))
                for color_list in change_color_list:
                    screen.blit(color_list[0], color_list[1])

        else:
            screen.fill("green")
            # 게임이 종료되었을 때 덱 초기화
            for player_deck in turn_list:
                player_deck.empty()
            deck.empty()
            remain.empty()

        pygame.display.update()

        # Limit the frame rate
        clock.tick(60)


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
game_active = False
# 싱글 플레이에 필요한 변수 선언
turn_list = []  # 차례의 순서를 나타내는 list
turn_index = 0  # 누구의 차례인지 알려주는 변수
PLAYER_NUMBER = 2
for _ in range(PLAYER_NUMBER):
    turn_list.append(pygame.sprite.LayeredUpdates())

first = None
# 시작 시 카드 세팅
deck = pygame.sprite.Group()
remain = pygame.sprite.Group()

colors = ['red', 'blue', 'green', 'yellow']
numbers = list(range(0, 10))
skills = ['reverse', 'block', 'plus2', 'change', 'plus4']

font = pygame.font.Font("../assets/font/Pixeltype.ttf", 36)
text_surf = font.render("click here to play", False, (64, 64, 64))
text_rect = text_surf.get_rect(center=(400, 300))

deck_surf = pygame.image.load("resources/images/output.png").convert_alpha()
deck_surf = pygame.transform.rotozoom(deck_surf, 0, 0.5)
deck_rect = deck_surf.get_rect(center=(400 - (deck_surf.get_width() // 2), 300))

# 현재 어떤카드가 뒤집혀져있는지 나타내는 변수 / 추후 수정해야 함
# 1. 낸 카드로 이미지가 바뀌게
# 2.
now_card_surf = pygame.image.load("resources/images/output.png").convert_alpha()
# now_card_surf = pygame.transform.rotozoom(now_card_surf, 0, 0.5)
now_card_rect = now_card_surf.get_rect(center=(400 + (now_card_surf.get_width() // 2), 300))

now_turn_surf = font.render(f"Player{turn_index + 1}'s turn", False, (64, 64, 64))
now_turn_surf2 = font.render(f"Player{turn_index + 2}'s turn", False, (64, 64, 64))
now_turn_rect = now_turn_surf.get_rect(center=(100, 300))
now_color = "none"  # 현재 내야하는 색깔

CENTER_X_POS = 625
CENTER_Y_POS = 325
red_surf = pygame.Surface((50,50))
red_surf.fill((255,0,0))
red_rect = red_surf.get_rect(center=(CENTER_X_POS - 25,CENTER_Y_POS - 25))
green_surf = pygame.Surface((50, 50))
green_surf.fill((0,255,0))
green_rect = green_surf.get_rect(center=(CENTER_X_POS + 25, CENTER_Y_POS - 25))
blue_surf = pygame.Surface((50, 50))
blue_surf.fill((0,0,255))
blue_rect = blue_surf.get_rect(center=(CENTER_X_POS - 25, CENTER_Y_POS + 25))
yellow_surf = pygame.Surface((50, 50))
yellow_surf.fill((255,255,0))
yellow_rect = yellow_surf.get_rect(center=(CENTER_X_POS + 25, CENTER_Y_POS + 25))
change_color_list = []

is_color_change = False

alpha_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
alpha_surface.fill((0, 0, 0, 128))
# 카드 생성과 분배
# 카드 덱을 만들고, 플레이어들에게 무작위로 카드를 분배

# 0~9 숫자 카드를 색깔별로 담는 반복문 / product() : color와 nubmber로 조합할 수 있는 모든 경우의 수를 표현
# 현재 게임을 나갈때마다 덱을 다시 generate하는 것이 필요 **********************************


# 현재 카드 표시
# 플레이어가 놓은 카드 중 가장 최근에 놓은 카드를 표시
spacing = 0
card_width = 70
card_height = 100

# 카드 놓기
# 플레이어는 자신의 카드 중 현재 카드와 색상 또는 숫자가 일치하는 카드를 놓을 수 있음


# 특수 카드 처리
# 특수 카드인 Skip, Reverse, Draw Two, Wild, Wild Draw Four 등에 대한 처리를 구현합니다.


# 게임 종료 조건 검사
# 게임이 종료되는 조건인 플레이어의 카드가 모두 소진되거나, 한 명 이상의 플레이어가 이길 때를 검사합니다.
