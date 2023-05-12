import configparser
import pygame

#config  = configparser.ConfigParser()
#config.read("../setting_data.ini")
class achievement:
    def __init__(self, screen, config):
        self.screen = screen
        self.message = "Default"
        self.messages = [
            "Achievement Unlocked: Single Win",
            "Achievement Unlocked: Stage A Clear",
            "Achievement Unlocked: Stage D Clear",
            "Achievement Unlocked: Stage C Clear",
            "Achievement Unlocked: Stage D Clear",
            "Achievement Unlocked: Stage All Clear",
            "Achievement Unlocked: In 10 Turn Win",
            "Achievement Unlocked: Only Number Card Win",
            "Achievement Unlocked: Only Skill Card Win",
            "Achievement Unlocked: Other Player UNO Win",
            "Achievement Unlocked: Grab Over 15 Card",
            "Achievement Unlocked: Lucky Seven"
        ]
        self.visible = False
        self.timer_started = False
        self.timer_start_time = 0
        self.x = 5
        self.y = 5

        #config = configparser.ConfigParser()
        #config.read("../setting_data.ini")
        self.config = config
        self.configKeys = list(self.config["Achievement"].keys())
        self.font = pygame.font.SysFont(None, 48)

    def showMessage(self):
        self.visible = True
        self.timer_started = True
        self.timer_start_time = pygame.time.get_ticks()

    def hideMessage(self):
        self.visible = False

    def update(self, screen):
        if self.visible:
            # Draw the achievement message
            text = self.font.render(self.message, True, (255, 255, 255))
            screen.blit(text, (self.x, self.y))
            # Move the message upward
            if self.y > -50 and self.tickCalcular(self.timer_start_time) > 1000:
                self.y -= 1
            # Check if the timer has expired
            if self.timer_started and self.tickCalcular(self.timer_start_time) > 3000:
                self.hideMessage()
                self.timer_started = False
                self.y = 20

    def tickCalcular(self, ticks):
        return pygame.time.get_ticks() - ticks

    def completeAchieve(self, index):
        self.message = self.messages[index]
        self.config["Achievement"][self.configKeys[index]] = "1"
        with open('setting_data.ini', 'w') as f:
            self.config.write(f)
        self.showMessage()


    def singleWin(self):
        self.message = "Achievement Unlocked: Single Win"
        self.config["Achievement"]["singleWin"] = "1"
        with open('setting_data.ini', 'w') as f:
            self.config.write(f)
        self.showMessage()

    def stageAClear(self):
        self.message = "Achievement Unlocked: Stage A Clear"
        self.config["Achievement"]["stageAClear"] = "1"
        self.showMessage()

    def stageBClear(self):
        self.message = "Achievement Unlocked: Stage B Clear"
        self.config["Achievement"]["stageBClear"] = "1"
        self.showMessage()

    def stageCClear(self):
        self.message = "Achievement Unlocked: Stage C Clear"
        self.config["Achievement"]["stageCClear"] = "1"
        self.showMessage()

    def stageDClear(self):
        self.message = "Achievement Unlocked: Stage D Clear"
        self.config["Achievement"]["stageDClear"] = "1"
        self.showMessage()

    def storyAllClear(self):
        self.message = "Achievement Unlocked: Story All Clear"
        self.config["Achievement"]["storyAllClear"] = "1"
        self.showMessage()

    def In10TurnWin(self):
        self.message = "Achievement Unlocked: In 10 Turn Win"
        self.config["Achievement"]["In10TurnWin"] = "1"
        self.showMessage()

    def OnlyNumberCardWin(self):
        self.message = "Achievement Unlocked: Only Number Card Win"
        self.config["Achievement"]["OnlyNumberCardWin"] = "1"
        self.showMessage()

    def OnlySkillCardWin(self):
        self.message = "Achievement Unlocked: Only Skill Card Win"
        self.config["Achievement"]["OnlySkillCardWin"] = "1"
        self.showMessage()

    def OtherPlayerUNOWin(self):
        self.message = "Achievement Unlocked: Other Player UNO Win"
        self.config["Achievement"]["OtherPlayerUNOWin"] = "1"
        self.showMessage()

    def GrabOver15Card(self):
        self.message = "Achievement Unlocked: Grab Over 15 Card"
        self.config["Achievement"]["GrabOver15Card"] = "1"
        self.showMessage()

    def LuckySeven(self):
        self.message = "Achievement Unlocked: Lucky Seven"
        self.config["Achievement"]["LuckySeven"] = "1"
        self.showMessage()
