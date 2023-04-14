import pygame
from .player import Player


class Button:
    def __init__(self, x, y, width, height, color, text, text_color, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font("./resources/fonts/Pixeltype.ttf", font_size)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.alpha = 255
        self.surface.fill((color[0], color[1], color[2], self.alpha))

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.rect.centerx - text_surface.get_width() // 2
        text_y = self.rect.centery - text_surface.get_height() // 2 + 2
        screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Component:
    def __init__(
        self, x, y, width, height, color, player_name, text_color, font_size, player
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = player_name
        self.text_color = text_color
        self.font = pygame.font.Font("./resources/fonts/Pixeltype.ttf", font_size)
        self.player = player

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.rect.x + 5
        text_y = self.rect.y + 5
        if self.player is not None:
            for i in range(len(self.player.hand)):
                surf = pygame.image.load(
                    "resources/images/card/normalMode/backcard.png"
                ).convert_alpha()
                surf = pygame.transform.scale(surf, (15, 20))
                rect = surf.get_rect(
                    midleft=(self.rect.x + 5 + 10 * i, self.rect.y + 50)
                )
                screen.blit(surf, rect)
            text_surface = self.font.render(
                self.text + f"'s remain : {len(self.player.hand)}",
                False,
                self.text_color,
            )
        screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
