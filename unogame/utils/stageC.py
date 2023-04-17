from single_play import Game
import pygame, random

class stageC(Game):
    def __init__(self, screen, player_number, keys, config, soundFX):
        super().__init__(screen, player_number, keys, config, soundFX)
        self.turnCounter = 0
    
    def pass_turn(self):
        self.turnCounter += 1
        if self.turnCounter == 5:
            self.turnCounter = 0
            self.colRandomize()
        return super().pass_turn()
    
    def colRandomize(self):
        colors = ["red", "blue", "green", "yellow"]
        changeToCol = colors[random.randrange(0,4)]

        self.now_card.color = changeToCol
        self.now_card_surf = pygame.image.load(
            f"./resources/images/card/normalMode/change/{self.now_card.color}_change.png"
        ).convert_alpha()
        self.now_card_surf = pygame.transform.scale(self.now_card_surf, (50, 70))
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 100, self.screen_height / 3)
        )
