import pygame

class Card:

    colors = ['red', 'blue', 'green', 'yellow']
    numbers = list(range(0, 10))
    skills = ['reverse', 'block', 'plus2', 'change', 'plus4']
    def __init__(self, color, number, skill, wild):
        self.color = color
        self.number = number
        self.skill = skill  # block, plus2, reverse, change / change, plus4
        self.is_moving = False
        self.is_wild = wild
        self.file_path = ""
        self.width = 50
        self.height = 70
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
        self.large_image_surface = pygame.transform.scale(image_surface, (self.width, self.height))
        self.small_image_surface = pygame.transform.scale(image_surface, (self.width / 2, self.height / 2))

        self.image = self.large_image_surface
        self.rect = self.image.get_rect(center=(0, 0))
        # print(f"width : {self.rect.width} / height : {self.rect.height}")
        self.initial_y = self.rect.y

        self.card_state = False  # 앞뒷면을 나타내는 변수, True = 앞면 / False = 뒷면


    # def draw_now_select(self, screen):
