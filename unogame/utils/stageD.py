from single_play import Game

class StageD(Game):
    def __init__(self, screen, player_number, keys, config, soundFX):
        super().__init__(screen, player_number, keys, config, soundFX)

    def player_card_setting(self, player):
        startCards = 7
        if player.type =="AI":
            startCards = 3

        for i in range(startCards):
            self.draw_card(player.hand)