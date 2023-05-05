import configparser
import pygame

config  = configparser.ConfigParser()
config.read("../setting_data.ini")
class achievement:
    def __init__(self, screen):
        self.screen = screen
        self.message = ""
        self.visible = False
        self.timer_started = False
        self.timer_start_time = 0
        self.x = self.screen.get_width()
        self.y = -50

        config = configparser.ConfigParser()
        config.read("../setting_data.ini")
        self.font = pygame.font.SysFont(None, 48)

    def showMessage(self):
        self.visible = True
        self.timer_started = True
        self.timer_start_time = pygame.time.get_ticks()

    def hideMessage(self):
        self.visible = False

    def update(self):
        if self.visible:
            # Draw the achievement message

            text = self.font.render(self.message, True, (255, 255, 255))
            self.screen.blit(text, (self.x, 0))

            # Move the message downwards
            if self.y < 20:
                self.y += 2

            # Check if the timer has expired
            if self.timer_started and self.tickCalcular(self.timer_start_time) > 3000:
                self.hide_message()
                self.timer_started = False
                self.y = -50

    def tickCalcular(self, ticks):
        return pygame.time.get_ticks() - ticks

    def singleWin(self):
        self.message = "Achievement Unlocked: Single Win"
        config["Achievement"]["singleWin"] = "1"
        self.showMessage()

    def stageAClear(self):
        self.message = "Achievement Unlocked: Stage A Clear"
        config["Achievement"]["stageAClear"] = "1"
        self.showMessage()

    def stageBClear(self):
        self.message = "Achievement Unlocked: Stage B Clear"
        config["Achievement"]["stageBClear"] = "1"
        self.showMessage()

    def stageCClear(self):
        self.message = "Achievement Unlocked: Stage C Clear"
        config["Achievement"]["stageCClear"] = "1"
        self.showMessage()

    def stageDClear(self):
        self.message = "Achievement Unlocked: Stage D Clear"
        config["Achievement"]["stageDClear"] = "1"
        self.showMessage()

    def storyAllClear(self):
        self.message = "Achievement Unlocked: Story All Clear"
        config["Achievement"]["storyAllClear"] = "1"
        self.showMessage()

    def In10TurnWin(self):
        self.message = "Achievement Unlocked: In 10 Turn Win"
        config["Achievement"]["In10TurnWin"] = "1"
        self.showMessage()

    def OnlyNumberCardWin(self):
        self.message = "Achievement Unlocked: Only Number Card Win"
        config["Achievement"]["OnlyNumberCardWin"] = "1"
        self.showMessage()

    def OnlySkillCardWin(self):
        self.message = "Achievement Unlocked: Only Skill Card Win"
        config["Achievement"]["OnlySkillCardWin"] = "1"
        self.showMessage()

    def OtherPlayerUNOWin(self):
        self.message = "Achievement Unlocked: Other Player UNO Win"
        config["Achievement"]["OtherPlayerUNOWin"] = "1"
        self.showMessage()

    def GrabOver15Card(self):
        self.message = "Achievement Unlocked: Grab Over 15 Card"
        config["Achievement"]["GrabOver15Card"] = "1"
        self.showMessage()

    def LuckySeven(self):
        self.message = "Achievement Unlocked: Lucky Seven"
        config["Achievement"]["LuckySeven"] = "1"
        self.showMessage()
