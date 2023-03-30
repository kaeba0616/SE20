import itertools
import random

import pygame
import sys
from operator import attrgetter
from models.card import Card
from models.player import Player


def draw_card(input_deck):
    global deck, turn_index, turn_list
    temp_list = deck.sprites()
    random.shuffle(temp_list)
    pop_card = temp_list.pop()
    deck.remove(pop_card)

    if turn_index == 0:
        pop_card.rect.y = 450  # 200 - rect_height // 2
        pop_card.initial_y = 450
    elif turn_index == 1:
        pop_card.rect.y = 50  # 200 - rect_height // 2
        pop_card.initial_y = 50
    input_deck.add(pop_card)



def block_turn():
    global turn_list, turn_index
    print(f"before block : {turn_index}")
    turn_index = (turn_index + 2) % len(turn_list)
    print(f"after block : {turn_index}")
    hand_update(turn_list[turn_index])
def reverse_turn():
    global turn_list, turn_index, now_turn_list
    print(f"before reverse : {turn_index}")
    temp_player = turn_list[turn_index]
    turn_list.reverse()
    turn_index = turn_list.index(temp_player)
    now_turn_list.reverse()
    print(f"after reverse : {turn_index}")

def change_color():
    global is_color_change
    if is_color_change:
        is_color_change = False
        return 0
    is_color_change = True


def draw_two(input_deck, next_player):  # deck : list / first, second : card
    global deck, turn_index, turn_list
    for _ in range(2):
        temp_list = deck.sprites()
        random.shuffle(temp_list)
        pop_card = temp_list.pop()
        deck.remove(pop_card)

        if next_player == 0:
            pop_card.rect.y = 450  # 200 - rect_height // 2
            pop_card.initial_y = 450
        elif next_player == 1:
            pop_card.rect.y = 50  # 200 - rect_height // 2
            pop_card.initial_y = 50

        input_deck.add(pop_card)

    hand_update(input_deck)


def draw_four(input_deck, next_player):
    global deck, turn_index, turn_list
    for _ in range(4):
        temp_list = deck.sprites()
        random.shuffle(temp_list)
        pop_card = temp_list.pop()
        deck.remove(pop_card)

        if next_player == 0:
            pop_card.rect.y = 450  # 200 - rect_height // 2
            pop_card.initial_y = 450
        elif next_player == 1:
            pop_card.rect.y = 50  # 200 - rect_height // 2
            pop_card.initial_y = 50

        input_deck.add(pop_card)

    hand_update(input_deck)

def hand_update(input_deck):
    for i, card in enumerate(input_deck.sprites()):
        card.rect.x = i * (card_width + spacing) + 400 - len(input_deck) * (
                card_width + spacing) // 2
        card.rect.y = card.initial_y


def generate_deck():
    global deck, remain, now_card_surf, now_card_rect, now_card, turn_index
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
    temp_list = deck.sprites()
    random.shuffle(temp_list)
    pop_card = temp_list.pop()
    deck.remove(pop_card)
    remain.add(pop_card)
    turn_index = 0
    now_card = pop_card
    now_card_surf = pop_card.image
    now_card_rect = now_card_surf.get_rect(center=(400 + (now_card_surf.get_width() // 2), 300))


# turn_index를 더 깔끔하게 다루기
def draw_from_center(input_deck):
    global deck, turn_index, is_get
    draw_card(input_deck)
    hand_update(input_deck)
    is_get = True

    # # layer를 다시 수정해주는 작업
    # for i, card in enumerate(input_deck.sprites()):
    #     # input_deck.change_layer(card, len(input_deck.sprites()) - i - 1)
    #     input_deck.change_layer(card, i)


def player_card_setting(input_deck):
    global deck
    print(len(deck.sprites()))
    if not len(input_deck):  # 초기에 7장 뽑기
        for i in range(7):
            draw_card(input_deck)
    hand_update(input_deck)

    # 레이어 재정렬 - add()의 layer가 차례대로 쌓이기 때문에 역순으로 다시 재정렬 해줘야함
    for i, card in enumerate(input_deck.sprites()):
        # input_deck.change_layer(card, len(input_deck.sprites()) - i - 1)
        input_deck.change_layer(card, i)




def check_condition(input_card):
    # input 카드가 현재 맨 위에 있는 카드에 낼 수 있는 카드인지 확인하는 함수
    global remain
    now = now_card
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


def skill_active(skill):
    global turn_list, turn_index
    next_player = turn_index + 1
    if next_player == len(turn_list):
        next_player = 0

    if skill == "reverse":
        reverse_turn()
    elif skill == "block":
        block_turn()
    elif skill == "change" or skill == "all":
        change_color()
    elif skill == "plus2":
        draw_two(turn_list[next_player], next_player)
    elif skill == "plus4" or skill == "all4":
        draw_four(turn_list[next_player], next_player)

def pass_turn():
    global turn_index, turn_list, is_get
    print("turn is passed")
    turn_index += 1
    if turn_index == len(turn_list):
        turn_index = 0
    is_get = False
    for i in range(0,2):
        hand_update(turn_list[i])





class Game:
    font = pygame.font.Font("../assets/font/Pixeltype.ttf", 36)

    spacing = 5
    card_width = 70
    card_height = 100

    CENTER_X_POS = 625
    CENTER_Y_POS = 325
    change_color_list = []

    for color, pos in zip([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
                          [(CENTER_X_POS - 25, CENTER_Y_POS - 25), (CENTER_X_POS + 25, CENTER_Y_POS - 25),
                           (CENTER_X_POS - 25, CENTER_Y_POS + 25), (CENTER_X_POS + 25, CENTER_Y_POS + 25)]):
        surf = pygame.Surface((50, 50))
        surf.fill(color)
        rect = surf.get_rect(center=pos)
        change_color_list.append([surf, rect, color])

    def __init__(self, screen, player_number):
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.player_number = player_number

        self.game_active = False
        self.is_win = False
        self.is_get = False
        self.run = True
        self.is_color_change = False

        self.turn_list = []  # 차례의 순서를 나타내는 list
        self.turn_index = 0  # 누구의 차례인지 알려주는 변수
        for i in range(player_number):
            player = Player(i, list, i)
            turn_list.append(player)
        self.deck = list  # 가운데에서 뽑힐 카드
        self.remain = list  # 낸 카드들

        self.deck_surf = pygame.image.load("resources/images/card/normalMode/backcart.png").convert_alpha()
        self.deck_rect = self.deck_surf.get_rect(center=(self.screen_width / 2 - (self.deck_surf.get_width() // 2), self.screen_height / 2))

        self.now_card = Card('red', None, 0, False)
        self.now_card_surf = pygame.image.load("resources/images/card/normalMode/backcart.png").convert_alpha()
        self.now_card_rect = self.now_card_surf.get_rect(center=(self.screen_width / 2 + (self.now_card_surf.get_width() // 2), self.screen_height / 2))

        self.now_turn_list = list
        for i in range(player_number):
            now_turn_surf = Game.font.render(f"Player{i+1}'s turn", False, (64, 64, 64))
            now_turn_rect = now_turn_surf.get_rect(center=(self.screen_width / 8, self.screen_height / 2))
            self.now_turn_list.append([now_turn_surf, now_turn_rect])

        self.skip_surf = Game.font.render("PASS", False, (64, 64, 64))
        self.skip_rect = self.skip_surf.get_rect(center=(self.now_card_rect.x + self.now_card_rect.width / 2 + 10, self.now_card_rect.y + self.now_card_rect.height / 2))

        self.uno_surf = Game.font.render("UNO!", False, (64, 64, 64))
        self.uno_Rect = self.uno_surf.get_rect(center=(self.deck_rect.x + self.deck_rect.width / 2 - 10, self.deck_rect.y + self.deck_rect.height / 2))

        self.win_list = list
        for i in range(player_number):
            win_surf = Game.font.render(f"Player{i+1} win!", False, (64, 64, 64))
            win_rect = win_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
            self.win_list.append([win_surf, win_rect])

        self.retry_surf = Game.font.render("click to retry", False, (64, 64, 64))
        self.retry_rect = self.retry_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 50))

    def start_single_play(self):
        global turn_list, turn_index, deck, now_card_surf, now_card_rect, is_color_change, game_active, is_get, now_card, is_win
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
                        change_color()
                        print("hi")
                    if event.key == pygame.K_q:
                        turn_list[turn_index].empty()

                # 게임 전 카드 덱과 손 패를 세팅하는 부분 > 따로빼서 함수로 refactor하기
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not game_active:
                        game_active = True
                        is_win = False
                        generate_deck()
                        for player_deck in turn_list:
                            player_card_setting(player_deck)
                            turn_index += 1
                        turn_index = 0

                else:
                    pass
                # 카드에 마우스커서를 올렸을 때 애니메이션 > 리팩토링
                if event.type == pygame.MOUSEMOTION and game_active and not is_color_change:
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
                if event.type == pygame.MOUSEBUTTONDOWN and game_active:
                    clicked_card = None
                    for card in turn_list[turn_index].sprites():
                        if card.rect.collidepoint(event.pos):
                            clicked_card = card
                            break
                    if clicked_card is not None:
                        print(turn_list[turn_index].get_layer_of_sprite(card))
                        print("button down")

                # if now_card.rect.collidepoint(event.pos):
                #     print(f"now.color : {now_card.color}")
                #     print(f"now.skill : {now_card.skill}")
                #     print(f"now.number : {now_card.number}")
                # is_color_change에 따라 색깔을 바꿔주는 옵션
                if is_color_change and event.type == pygame.MOUSEBUTTONDOWN:
                    for color_list in Game.change_color_list:
                        if color_list[1].collidepoint(event.pos):
                            alpha_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                            alpha_surface.fill((0, 0, 0, 128))
                            now_card_surf = pygame.image.load(
                                f"resources/images/card/normalMode/change/{color_list[2]}_change.png").convert_alpha()
                            now_card_surf = pygame.transform.scale(now_card_surf, (70, 100))
                            now_card.color = color_list[2]
                            is_color_change = False
                            pass_turn()

                # turn_index를 이용해 게임 flow control
                # 플레이어 턴에 플레이어가 할 수 있는 행동
                if event.type == pygame.MOUSEBUTTONDOWN and game_active and not is_color_change:

                    # 1. 낼 수 있는 카드를 낸다
                    for card in turn_list[turn_index].sprites():
                        if card.rect.collidepoint(event.pos):
                            if check_condition(card):
                                # 카드 내기
                                print("카드 냈음")
                                pop_card = card
                                turn_list[turn_index].remove(card)
                                remain.add(pop_card)
                                now_card = pop_card
                                now_card_surf = pop_card.image
                                # 1-1. 낸 카드의 능력이 있다면 해당 카드의 능력을 수행해야 한다
                                if card.skill is not None:
                                    skill_active(card.skill)
                                if card.skill not in ['change', 'block', 'all']:
                                    print(card.skill)
                                    print(f"pass_turn call in check condition")
                                    pass_turn()
                                    break
                    # 2. 가운데에서 카드를 가져온다 > 낼 수 있는 카드가 있다면 낸다
                    if Game.deck_rect.collidepoint(event.pos) and not is_get:
                        draw_from_center(turn_list[turn_index])
                    # 3. 낼 수 있는 카드가 없거나, 가운데에서 이미 카드를 가져온 상태면 PASS를 눌러 턴을 넘김
                    if is_get and Game.skip_rect.collidepoint(event.pos):
                        pass_turn()
                    # 4. 컴퓨터의 알고리즘 수행
                    # 5. 카드가 1장만 남았을 경우 UNO 버튼을 눌러야 한다.
                    # 6. 누군가의 덱이 모두 사라지면 그 사람의 승리 > 승리 화면 전환 > 메인 화면 전환
                    for player in turn_list:
                        if len(player.sprites()) == 0:
                            game_active = False
                            is_win = True
            # event loop 종료 *****************************

            if game_active:
                for i in range(0, turn_index):
                    hand_update(turn_list[i])
                screen.blit(deck_surf, deck_rect)
                screen.blit(now_card_surf, now_card_rect)
                screen.blit(uno_surf, uno_Rect)
                # 누구의 턴인지 보여주는 부분
                # if not is_color_change:
                if turn_index == 0:
                    screen.blit(now_turn_list[turn_index], now_turn_rect)
                else:
                    screen.blit(now_turn_list[turn_index], now_turn_rect)

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
                if is_get:
                    pygame.draw.rect(screen, (200, 200, 200), skip_rect, 0)
                    screen.blit(skip_surf, skip_rect)

                else:
                    pygame.draw.rect(screen, (64, 64, 64), skip_rect, 0)
                    screen.blit(skip_surf, skip_rect)
            else:
                screen.fill("green")
                # 게임이 종료되었을 때 덱 초기화
                for player_deck in turn_list:
                    player_deck.empty()
                deck.empty()
                remain.empty()

                if is_win:
                    if turn_index == 0:
                        screen.blit(win_surf2, win_rect)
                    else:
                        screen.blit(win_surf, win_rect)
                    screen.blit(retry_surf, retry_rect)
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)

