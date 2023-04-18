from single_play import Game


class stage_D(Game):
    def __init__(self, screen, player_number, keys, config, soundFX):
        super().__init__(screen, player_number, keys, config, soundFX)

        print("STAGE D")

    def player_card_setting(self, player):
        print("STAGE D")
        startCards = 7
        if player.type == "AI":
            startCards = 3

        for i in range(startCards):
            self.draw_card(player.hand)
