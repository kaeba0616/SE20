class Player:
    # number : 플레이어 넘버 / type : 어떤 플레이어 종류인지 / hand : 플레이어의 패 / turn : 플레이어 객체의 턴
    def __init__(self, number, hand, turn):
        self.number = number
        self.hand = hand
        self.turn = turn

    def update_hand(self, screen):

        if len(self.hand) <= 10:
            for i, card in enumerate(self.hand):
                card.rect.x = 20 + (card.width + 5) * i
                card.rect.y = screen.get_height() - 120
                card.initial_y = card.rect.y
        elif 10 < len(self.hand) <= 20:
            for i, card in enumerate(self.hand):
                if i <= 9:
                    card.rect.x = 20 + (card.width + 5) * i
                    card.rect.y = screen.get_height() - 200
                    card.initial_y = card.rect.y
                elif 10 <= i < 20:
                    card.rect.x = 20 + (card.width + 5) * (i - 10)
                    card.rect.y = screen.get_height() - 120
                    card.initial_y = card.rect.y

        elif 20 < len(self.hand) <= 30:
            for i, card in enumerate(self.hand):
                card.rect = card.small_image_surface.get_rect(center=(0, 0))
                if i <= 9:
                    card.rect.x = 20 + (card.width // 2 + 5) * i
                    card.rect.y = screen.get_height() - 200
                    card.initial_y = card.rect.y

                elif 10 <= i < 20:
                    card.rect.x = 20 + (card.width // 2 + 5) * (i - 10)
                    card.rect.y = screen.get_height() - 160
                    card.initial_y = card.rect.y

                elif 20 <= i < 30:
                    card.rect.x = 20 + (card.width // 2 + 5) * (i - 20)
                    card.rect.y = screen.get_height() - 120
                    card.initial_y = card.rect.y
                else:
                    pass

    def draw_hand(self, screen):
        self.update_hand(screen)
        for card in self.hand:
            if len(self.hand) > 20:
                screen.blit(card.small_image_surface, card.rect)
            else:
                screen.blit(card.large_image_surface, card.rect)
