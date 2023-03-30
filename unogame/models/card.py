import pygame

class Card:
    def __init__(self, color, number, skill, wild):
        self.color = color
        self.number = number
        self.skill = skill  # block, plus2, reverse, change / change, plus4
        self.is_moving = False
        self.is_wild = wild
        self.file_path = ""
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
        image_surface = pygame.transform.scale(image_surface, (70, 100))
        self.image = image_surface
        self.rect = image_surface.get_rect(center=(0, 0))
        # print(f"width : {self.rect.width} / height : {self.rect.height}")
        self.initial_y = self.rect.y

        self.card_state = False  # 앞뒷면을 나타내는 변수, True = 앞면 / False = 뒷면

    colors = ['red', 'blue', 'green', 'yellow']
    numbers = list(range(0, 10))
    skills = ['reverse', 'block', 'plus2', 'change', 'plus4']