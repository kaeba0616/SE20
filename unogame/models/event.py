import pygame
import itertools
import random
import sys

import pygame

from pause import PauseClass
import time

class Event:

    pygame.init()

    def __init__(self, game):
        self.game = game

    def event_loop(self, event, game):


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                font = pygame.font.SysFont(None, 48)

                pause = PauseClass(
                    game.screen, font, game.config, game.keys, game.soundFX
                )
                value = pause.run()  # Todo: 일시정지 후 게임 내부 크기 조절 기능 필요..
                for card in game.card_list:
                    card.change_path(game.config)
                game.me.update_hand(game.screen)
                game.now_card_surf = game.now_card.image
                if value == "out":
                    return value
        # 치트키
        #                    if event.key == pygame.K_q and game.game_active:
        #                        game.turn_list[game.turn_index].hand.clear()
        #
        #                    if event.key == pygame.K_w and game.game_active:
        #                        game.turn_list[2].hand.clear()

        if game.is_win and not game.game_active:
            if not game.event_active:
                pygame.time.delay(1000)
                # print("event_active")
                game.resume_event_handling()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return (
                    game.who.number
                )

        # Timer 재설정 하는 event loop

        if event.type == game.move_timer and game.game_active:
            game.moving = False
            game.move_rect.center = game.deck_rect.center
            game.moving_start_time = 0
            game.velocity = 0

        if event.type == game.AI_timer and game.game_active:
            game.is_computer_turn = True
            game.AI_timer_on = False
            pygame.time.set_timer(game.AI_timer, 0)

        if event.type == game.turn_timer and game.game_active:
            if game.current_time == 0:
                game.current_time = 10
                if not game.is_get:
                    game.draw_from_center(game.turn_list[game.turn_index].hand)
                if game.is_color_change:
                    game.is_color_change = False
                    var = random.randint(0, 3)
                    if game.config["color"]["default"] == str(2):
                        game.now_card_surf = pygame.image.load(
                            f"resources/images/card/normalMode/change/{game.change_color_list[var][3]}_change.png"
                        ).convert_alpha()
                    elif game.config["color"]["default"] == str(1):
                        game.now_card_surf = pygame.image.load(
                            f"resources/images/card/YB/change/{game.change_color_list[var][3]}_change.png"
                        ).convert_alpha()
                    elif game.config["color"]["default"] == str(0):
                        game.now_card_surf = pygame.image.load(
                            f"resources/images/card/RG/change/{game.change_color_list[var][3]}_change.png"
                        ).convert_alpha()

                    game.now_card_surf = pygame.transform.scale(
                        game.now_card_surf, (50, 70)
                    )
                    game.now_card.color = game.change_color_list[var][3]
                    game.is_color_change = False
                game.pass_turn()
            game.current_time -= 1

        if (
                event.type == game.skill_active_timer
                and game.game_active
                and not game.is_win
        ):
            game.is_skill_active = False
        if (
                event.type == game.block_timer
                and game.game_active
                and not game.is_win
        ):
            for component in game.info_list:
                component.is_block = False
        elif (
                event.type == pygame.MOUSEBUTTONUP
                and game.start_button.rect.collidepoint(event.pos)
                and not game.edit_name
        ):
            if not game.game_active:
                game.game_active = True
                game.is_win = False
                game.generate_deck()
                for player in game.turn_list:
                    game.player_card_setting(player)
                    game.turn_index += 1
                game.turn_index = 0
        else:
            pass

        if event.type == pygame.MOUSEBUTTONDOWN and not game.game_active:
            for i in range(2, len(game.info_list)):
                if (
                        game.info_list[i].is_clicked(event.pos)
                        and game.info_list[i].text != "EMPTY"
                ):
                    if game.player_number > 2:
                        game.player_number -= 1
                elif (
                        game.info_list[i].is_clicked(event.pos)
                        and game.info_list[i].text == "EMPTY"
                ):
                    if game.player_number <= 5:
                        game.player_number += 1
            if game.info_list[0].is_clicked(event.pos):
                game.edit_name = True

        if event.type == pygame.KEYDOWN and game.edit_name:
            if game.edit_text == "__________":
                game.edit_text = ""

            if event.key == pygame.K_BACKSPACE:
                game.edit_text = game.edit_text[:-1]
            elif event.key == pygame.K_RETURN:
                game.info_list[0].text = game.edit_text
                if game.edit_text == "__________" or game.edit_text == "":
                    game.info_list[0].text = "PLAYER 1(ME)"
                game.edit_name = False
            else:
                if len(game.edit_text) < 8:
                    game.edit_text += pygame.key.name(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN and game.edit_name:
            if game.ok_button.is_clicked(event.pos):
                game.info_list[0].text = game.edit_text
                if game.edit_text == "__________" or game.edit_text == "":
                    game.info_list[0].text = "PLAYER 1(ME)"
                game.edit_name = False

        # 매 턴 UNO를 할 수 있는지 없는지 체크하는 부분
        for player in game.turn_list:
            if len(player.hand) == 1 and player.uno == "unactive":
                pygame.time.set_timer(game.uno_timer, 2000, 1)
                player.uno = "active"
                game.is_uno = True
                break
        if event.type == game.uno_timer and game.game_active:
            for player in game.turn_list:
                if player.uno == "active" and player == game.me:
                    game.draw_card(player.hand)
                    player.uno = "unactive"
                elif player.uno == "active" and player != game.me:
                    player.uno = "success"
            game.is_uno = False

        # 카드에 마우스커서를 올렸을 때 애니메이션 > 리팩토링

        if (
                event.type == pygame.MOUSEMOTION
                and game.game_active
                and not game.is_color_change
        ):
            for card in game.me.hand:
                if card.rect.collidepoint(event.pos):
                    game.now_select = card
            for rect in [
                game.deck_rect,
                game.uno_button.rect,
            ]:
                if rect.collidepoint(event.pos):
                    if rect == game.deck_rect and len(game.deck) == 0:
                        pass
                    else:
                        game.now_select = rect
        elif (
                event.type == pygame.MOUSEMOTION
                and game.game_active
                and not game.is_color_change
        ):
            if game.uno_button.rect.collidepoint(event.pos):
                game.now_select = game.uno_button
        # 키보드 입력을 정의
        if (
                event.type == pygame.KEYDOWN
                and game.game_active
                and not game.is_color_change
                and game.me.type == "Human"
        ):
            if event.key == game.keys["RIGHT"]:
                if game.now_select is None:
                    game.now_select = game.me.hand[0]
                elif game.now_select == game.deck_rect:
                    game.now_select = game.uno_button
                elif game.now_select == game.uno_button and len(game.deck) != 0:
                    game.now_select = game.deck_rect

                elif (
                        len(game.me.hand) == game.me.hand.index(game.now_select) + 1
                ):
                    game.now_select = game.me.hand[0]
                else:
                    game.now_select = game.me.hand[
                        game.me.hand.index(game.now_select) + 1
                        ]

            elif event.key == game.keys["LEFT"]:
                if game.now_select is None:
                    game.now_select = game.me.hand[0]
                elif game.now_select == game.deck_rect and len(game.deck) != 0:
                    game.now_select = game.uno_button

                elif game.now_select == game.uno_button:
                    game.now_select = game.deck_rect

                elif game.me.hand.index(game.now_select) == 0:
                    game.now_select = game.me.hand[len(game.me.hand) - 1]
                else:
                    game.now_select = game.me.hand[
                        game.me.hand.index(game.now_select) - 1
                        ]

            elif event.key == game.keys["UP"]:
                if game.now_select is None:
                    game.now_select = game.me.hand[0]
                elif game.now_select in game.me.hand:
                    if len(game.deck):
                        game.now_select = game.deck_rect
                    else:
                        game.now_select = game.uno_button
                elif game.now_select in [
                    game.deck_rect,
                    game.uno_button,
                ]:
                    game.now_select = game.me.hand[0]
            elif event.key == game.keys["DOWN"]:
                if game.now_select is None:
                    game.now_select = game.me.hand[0]
                elif game.now_select in game.me.hand:
                    if len(game.deck):
                        game.now_select = game.deck_rect
                    else:
                        game.now_select = game.uno_button
                elif game.now_select in [
                    game.deck_rect,
                    game.uno_button,
                ]:
                    game.now_select = game.me.hand[0]
        elif (
                event.type == pygame.KEYDOWN
                and game.game_active
                and not game.is_color_change
                and game.me.turn != game.turn_index
        ):
            if event.key:
                game.now_select = game.uno_button
        # game.is_color_change에 따라 색깔을 바꿔주는 옵션
        if game.is_color_change and event.type == pygame.MOUSEBUTTONDOWN:
            for color_list in game.change_color_list:
                if color_list[1].collidepoint(event.pos):
                    # lsj: 색약모드 change card
                    if game.config["color"]["default"] == str(2):
                        game.now_card_surf = pygame.image.load(
                            f"resources/images/card/normalMode/change/{color_list[3]}_change.png"
                        ).convert_alpha()
                    elif game.config["color"]["default"] == str(1):
                        game.now_card_surf = pygame.image.load(
                            f"resources/images/card/YB/change/{color_list[3]}_change.png"
                        ).convert_alpha()
                    elif game.config["color"]["default"] == str(0):
                        game.now_card_surf = pygame.image.load(
                            f"resources/images/card/RG/change/{color_list[3]}_change.png"
                        ).convert_alpha()

                    game.now_card_surf = pygame.transform.scale(
                        game.now_card_surf, (50, 70)
                    )
                    game.now_card.color = color_list[3]
                    game.is_color_change = False
                    game.pass_turn()

        # 클릭 및 엔터 이벤트
        if game.game_active and not game.is_color_change:
            pos = (0, 0)
            key = None

            if game.turn_list[game.turn_index].type == "Human":
                if (
                        event.type == pygame.MOUSEBUTTONDOWN
                        or event.type == pygame.KEYDOWN
                ):
                    if event.type == pygame.KEYDOWN:
                        key = event.key
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos

                    # 0 덱이 있는지 확인 점수 계산

                    # 1. 낼 수 있는 카드를 낸다

                    if (key == game.keys["RETURN"]) or (
                            game.check_collide(pos) and key is None
                    ):
                        if game.now_select in game.me.hand:
                            if game.check_condition(game.now_select):
                                pop_card = game.now_select
                                game.turn_list[game.turn_index].hand.remove(
                                    pop_card
                                )
                                game.now_select = None
                                # game.remain.append(pop_card)
                                if pop_card.skill is not None:
                                    game.skill_active(pop_card)
                                if pop_card.skill not in [
                                    "change",
                                    "block",
                                    "all",
                                ]:
                                    game.pass_turn()

                                game.now_card = pop_card
                                game.now_card_surf = pop_card.image

                        # 2. 가운데에서 카드를 가져온다
                        if (
                                (key == game.keys["RETURN"] and pos is None)
                                or (game.check_collide(pos) and key is None)
                                and game.now_select == game.deck_rect
                                and not game.is_get
                        ):
                            game.draw_from_center(
                                game.turn_list[game.turn_index].hand
                            )
                            game.now_select = None
                            game.pass_turn()
                            game.next_screen(game.screen)
            # 4. 컴퓨터의 알고리즘 수행

            ## lms
            if game.turn_list[game.turn_index].type == "AI":
                if game.is_computer_turn:
                    game.computer_turn()
                    game.is_computer_turn = False
                    # game.next_screen(screen)
                elif not game.AI_timer_on and not game.is_computer_turn:
                    pygame.time.set_timer(game.AI_timer, 2000)
                    game.AI_timer_on = True
            if game.start_count:
                game.next_screen(game.screen)
                game.start_count -= 1

            ## lms

            # 5. 카드가 1장만 남았을 경우 UNO 버튼을 눌러야 한다.
            if (
                    (key == game.keys["RETURN"] and pos is None)
                    or (game.check_collide(pos) and key is None)
                    and game.now_select == game.uno_button
                    and game.is_uno
            ):
                game.press_uno()
            # 6. 누군가의 덱이 모두 사라지면 그 사람의 승리 > 승리 화면 전환 > 메인 화면 전환
            for player in game.turn_list:
                if len(player.hand) == 0:
                    game.game_active = False
                    game.is_win = True

                    game.who = player

                    game.win_button.text = f"Player {player.number + 1} win !!"
                    game.pause_event_handling()

            # # 7. 뽑을 수 있는 카드가 없고, 모든 플레이어가 현재 낼 수 있는 카드가 없으면 카드가 가장 적은 사람이 승리
            game.deck_none()
