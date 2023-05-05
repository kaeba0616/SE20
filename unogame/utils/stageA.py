import itertools, random
from single_play import Game
from models.card import Card
from models.button import Button
from models.Human import Human
from models.AI import AI


class stage_A(Game):
    def __init__(self, screen, player_number, keys, config, soundFX):
        super().__init__(screen, player_number, keys, config, soundFX)

        print("STAGE A")
        # refactoring needed(after single_play refactoring - function seperation)
        # best: delete all variables below
        self.tempNumDeck = []
        self.tempSkillDeck = []
        self.firstDraw = True
        self.config = config

    def generate_deck(self):
        # 숫자 카드를 모두 덱에 담기
        for color, number in itertools.product(Card.colors, Card.numbers):
            self.deck.append(Card(color, number, None, False, self.config))
            if number != 0:
                self.tempNumDeck.append(Card(color, number, None, False, self.config))

        # 색깔별로 기술 카드를 담음
        self.tempSkillDeck = []
        for color, skill in itertools.product(Card.colors, Card.skills):
            for _ in range(2):
                self.tempSkillDeck.append(Card(color, None, skill, False, self.config))

        # all, all4 카드 추가
        for _ in range(4):
            self.tempSkillDeck.append(Card(None, None, "all4", True, self.config))
            self.tempSkillDeck.append(Card(None, None, "all", True, self.config))

        # 초기 설정(조건에 맞춘 카드 배분)용 임시 덱
        random.shuffle(self.tempNumDeck)
        random.shuffle(self.tempSkillDeck)

        # 0.5로 카드나 숫자 먼저 뽑아서 꺼내기
        if random.randrange(0, 2) == 0:
            self.now_card = self.tempNumDeck.pop()
        else:
            self.now_card = self.tempSkillDeck.pop()

        self.now_card_surf = self.now_card.image
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 100, self.screen_height / 3)
        )

        self.turn_list = [
            Human(i, [], i) if i == 0 else AI(i, [], i)
            for i in range(self.player_number)
        ]

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

        for player in self.turn_list:
            if player.type == "Human":
                self.me = player

    def temp_draw_card(self, input_deck, isNum):
        print("temp draw card")
        if isNum:
            input_deck.append(self.tempNumDeck.pop())
        else:
            input_deck.append(self.tempSkillDeck.pop())

    def player_card_setting(self, player):
        print("STAGE A에서 STAGE D가 출력이 되네?")
        prob = 50
        if player.type == "AI":
            prob = 60

        for i in range(7):
            if random.randrange(0, 100) < prob:
                self.temp_draw_card(player.hand, False)
            else:
                self.temp_draw_card(player.hand, True)

        # refactoring needed
        # player.type == "AI" => distribution ended, empty temp decks

        if player.type == "AI":
            while self.tempNumDeck:
                self.deck.append(self.tempNumDeck.pop())
            while self.tempSkillDeck:
                self.deck.append(self.tempSkillDeck.pop())
            random.shuffle(self.deck)

        # re-shuffle remain cards

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

            if self.now_card.skill == "change":
                self.computer_turn()

            if self.now_card.skill not in [
                # "change",
                "block",
                # "all",
            ]:
                self.pass_turn()

    def checkAchieve(self):
        self.achieve.stageAClear()
